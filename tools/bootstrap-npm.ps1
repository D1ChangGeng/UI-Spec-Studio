# Official first-publication bootstrap and safe re-verification of an existing release.
# Authentication is always handled locally by npm; no access tokens are logged.
[CmdletBinding()]
param(
    [ValidatePattern('^\d+\.\d+\.\d+$')]
    [string]$Version = '1.20.3',
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$PackageName = 'ui-spec-studio'
$Repository = 'D1ChangGeng/UI-Spec-Studio'
$Registry = 'https://registry.npmjs.org/'
$UrlBase = "https://github.com/$Repository/releases/download/v$Version"
$Folder = Join-Path ([System.IO.Path]::GetTempPath()) ('ui-spec-npm-bootstrap-' + [guid]::NewGuid().ToString('N'))
$Tarball = Join-Path $Folder 'ui-spec-installer.tgz'
$Sums = Join-Path $Folder 'SHA256SUMS.txt'
$Published = $false
$Verified = $false

function Assert-LastExit([string]$Action) {
    if ($LASTEXITCODE -ne 0) { throw "$Action failed (exit $LASTEXITCODE)" }
}

function Get-RegistryVersion() {
    # The version-specific, unauthenticated metadata endpoint bypasses npm CLI's
    # stale negative local cache immediately following a successful first publish.
    $Uri = $Registry + $PackageName + '/' + $Version
    try {
        return Invoke-RestMethod -Method Get -Uri $Uri -Headers @{
            'Cache-Control' = 'no-cache'
        } -ErrorAction Stop
    } catch {
        $Status = if ($null -ne $_.Exception.Response) {
            [int]$_.Exception.Response.StatusCode
        } else { -1 }
        if ($Status -eq 404) { return $null }
        throw
    }
}

function Confirm-ExactIntegrity($Metadata, [string]$ExpectedIntegrity) {
    if ($null -eq $Metadata) { throw 'No public package metadata to verify.' }
    $Name = [string]$Metadata.name
    $ActualVersion = [string]$Metadata.version
    $Integrity = [string]$Metadata.dist.integrity
    $Repo = if ($Metadata.repository -is [string]) {
        [string]$Metadata.repository
    } else {
        [string]$Metadata.repository.url
    }
    $Repo = $Repo -replace '^git\+', '' -replace '\.git$', ''
    $ExpectedRepo = "https://github.com/$Repository"
    if ($Name -ne $PackageName -or $ActualVersion -ne $Version -or $Repo -ne $ExpectedRepo) {
        throw "Public registry identity mismatch: $Name@$ActualVersion, repo=$Repo. No further publishing."
    }
    if ($Integrity -ne $ExpectedIntegrity) {
        throw 'Public npm archive SHA-512 differs from the verified GitHub Release. No further publishing.'
    }
    Write-Host "PUBLIC_REGISTRY_INTEGRITY_VERIFIED $Name@$ActualVersion"
}

try {
    New-Item -ItemType Directory -Path $Folder -Force | Out-Null
    Write-Host "UI Spec Studio | npm first-publication / verification: v$Version"
    Write-Host 'This process never clones the source repository.'
    Write-Host '1/5  Download the exact, published GitHub Release installer and checksums'
    Invoke-WebRequest -Uri "$UrlBase/ui-spec-installer.tgz" -OutFile $Tarball -UseBasicParsing
    Invoke-WebRequest -Uri "$UrlBase/SHA256SUMS.txt" -OutFile $Sums -UseBasicParsing

    Write-Host '2/5  Check the original GitHub release SHA-256 and npm archive SHA-512'
    $ChecksumRows = @(Get-Content -LiteralPath $Sums | Where-Object {
        $_ -match '^[0-9a-fA-F]{64}\s+\*?ui-spec-installer\.tgz\s*$'
    })
    if ($ChecksumRows.Count -ne 1) { throw 'Expected exactly one installer SHA-256 entry in the release.' }
    $Expected = ($ChecksumRows[0].Trim() -split '\s+')[0].ToLowerInvariant()
    $Observed = (Get-FileHash -LiteralPath $Tarball -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($Expected -ne $Observed) {
        throw "Checksum mismatch; refusing npm publication. expected=$Expected observed=$Observed"
    }
    $Sha512 = [System.Security.Cryptography.SHA512]::Create()
    try {
        $ExpectedIntegrity = 'sha512-' + [Convert]::ToBase64String(
            $Sha512.ComputeHash([System.IO.File]::ReadAllBytes($Tarball))
        )
    } finally { $Sha512.Dispose() }

    Write-Host '3/5  Inspect package identity and runtime files without running install scripts'
    $ReportText = & npm pack --dry-run --json --ignore-scripts $Tarball
    Assert-LastExit 'npm pack --dry-run'
    $Report = @($ReportText | ConvertFrom-Json)[0]
    if ($Report.name -ne $PackageName -or $Report.version -ne $Version) {
        throw "Unexpected package identity: $($Report.name)@$($Report.version)"
    }
    $Paths = @($Report.files | ForEach-Object { $_.path })
    foreach ($Required in @('bin/ui-spec.mjs', 'payload/skill/SKILL.md', 'harnesses.json', 'LICENSE')) {
        if ($Paths -notcontains $Required) { throw "Missing installer runtime file: $Required" }
    }
    Write-Host "Verified: $PackageName@$Version; $($Paths.Count) files; SHA-256 $Observed"

    Write-Host '4/5  Check npm registry and verify an existing publication before any write'
    $Registered = $false
    try {
        $Response = Invoke-WebRequest -Uri ($Registry + $PackageName) -UseBasicParsing
        if ([int]$Response.StatusCode -eq 200) { $Registered = $true }
    } catch {
        $Status = if ($null -ne $_.Exception.Response) {
            [int]$_.Exception.Response.StatusCode
        } else { -1 }
        if ($Status -ne 404) { throw }
    }
    if ($Registered) {
        $Existing = Get-RegistryVersion
        if ($null -eq $Existing) {
            throw 'The npm package name exists, but the exact version is not published. Refusing an automatic second publish.'
        }
        Confirm-ExactIntegrity $Existing $ExpectedIntegrity
        $Verified = $true
        Write-Host "ALREADY_PUBLISHED_VERIFIED: $PackageName@$Version"
    } else {
        Write-Host "$PackageName is not yet registered; only its npm account owner can publish it."
    }

    if ($DryRun) {
        Write-Host 'DRY RUN PASS — no registry write, no login, no local Skill changes.'
        return
    }
    if ($Verified) {
        Write-Host 'No second npm publish is needed. Proceed to configure Trusted publishing.'
        return
    }

    Write-Host '5/5  npm owner login/2FA and explicit publication approval'
    & npm whoami --registry $Registry | Out-Null
    if ($LASTEXITCODE -ne 0) {
        & npm login --registry $Registry
        Assert-LastExit 'npm login'
    }
    $Account = (& npm whoami --registry $Registry)
    Assert-LastExit 'npm whoami'
    Write-Host "Authenticated npm account: $Account"
    Write-Host "Package: $PackageName@$Version"
    Write-Host "Source: $UrlBase"
    $Answer = Read-Host 'Type PUBLISH to publish this exact verified archive (anything else cancels)'
    if ($Answer -cne 'PUBLISH') { throw 'Cancelled; no npm registry write performed.' }

    & npm publish $Tarball --access public --registry $Registry
    Assert-LastExit 'npm publish'
    $Published = $true
    Write-Host "PUBLISH_ACCEPTED: $PackageName@$Version. Checking public registry replication."

    # New npm packages can return a transient E404 immediately after a
    # successful publish. Recheck the public version-specific metadata rather
    # than interpreting the first 404 as a failed publish.
    $Metadata = $null
    for ($Attempt = 1; $Attempt -le 9; $Attempt++) {
        $Metadata = Get-RegistryVersion
        if ($null -ne $Metadata) { break }
        if ($Attempt -lt 9) {
            Write-Host "Registry is still processing the new version (check $Attempt/9)."
            Start-Sleep -Seconds ([Math]::Min(2 * $Attempt, 10))
        }
    }
    if ($null -eq $Metadata) {
        Write-Warning 'PUBLISH_ACCEPTED; PUBLIC_READBACK_PENDING. Do not publish again.'
        Write-Host "Read-back command: npm view $PackageName@$Version version dist.integrity --prefer-online"
        Write-Host "Rerun this same bootstrap script to verify the existing publication safely."
        return
    }
    Confirm-ExactIntegrity $Metadata $ExpectedIntegrity
    $Verified = $true
    Write-Host "PUBLISHED_AND_VERIFIED: $PackageName@$Version"
    Write-Host 'Next: npmjs.com > ui-spec-studio > Settings > Trusted publishing (GitHub Actions).'
    Write-Host 'GitHub owner D1ChangGeng | repository UI-Spec-Studio | workflow npm-publish.yml | Allow direct npm publish.'
    Write-Host 'Official command: npx --yes ui-spec-studio@latest'
} finally {
    if ($DryRun -or $Verified -or $Published) {
        Remove-Item -LiteralPath $Folder -Recurse -Force -ErrorAction SilentlyContinue
    } else {
        Write-Host "Verification files preserved for diagnosis: $Folder"
    }
}
