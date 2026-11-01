# One-time npmjs.org ownership bootstrap. No npm access token is accepted or logged.
# The end-user npx CLI is versionless; this maintainer-only first publish is pinned.
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

function Assert-LastExit([string]$Action) {
    if ($LASTEXITCODE -ne 0) { throw "$Action failed (exit $LASTEXITCODE)" }
}

try {
    New-Item -ItemType Directory -Path $Folder -Force | Out-Null
    Write-Host "UI Spec Studio | npm first-publication bootstrap: v$Version"
    Write-Host 'This process never clones the GitHub repository.'
    Write-Host '1/5  Download the version-pinned, already released installer and checksums'
    Invoke-WebRequest -Uri "$UrlBase/ui-spec-installer.tgz" -OutFile $Tarball -UseBasicParsing
    Invoke-WebRequest -Uri "$UrlBase/SHA256SUMS.txt" -OutFile $Sums -UseBasicParsing

    Write-Host '2/5  Verify downloaded bytes against the published SHA-256 checksum'
    $Matches = @(Get-Content -LiteralPath $Sums | Where-Object {
        $_ -match '^[0-9a-fA-F]{64}\s+\*?ui-spec-installer\.tgz\s*$'
    })
    if ($Matches.Count -ne 1) { throw 'Expected exactly one installer SHA-256 entry in the release.' }
    $Expected = ($Matches[0].Trim() -split '\s+')[0].ToLowerInvariant()
    $Observed = (Get-FileHash -LiteralPath $Tarball -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($Expected -ne $Observed) {
        throw "Checksum mismatch; refusing npm publication. expected=$Expected observed=$Observed"
    }

    Write-Host '3/5  Inspect npm package identity without publishing or installing anything'
    $ReportText = & npm pack --dry-run --json --ignore-scripts $Tarball
    Assert-LastExit 'npm pack --dry-run'
    $Report = @($ReportText | ConvertFrom-Json)[0]
    if ($Report.name -ne $PackageName -or $Report.version -ne $Version) {
        throw "Unexpected package identity $($Report.name)@$($Report.version)"
    }
    $Paths = @($Report.files | ForEach-Object { $_.path })
    foreach ($Required in @('bin/ui-spec.mjs', 'payload/skill/SKILL.md', 'harnesses.json', 'LICENSE')) {
        if ($Paths -notcontains $Required) { throw "Installer missing runtime file: $Required" }
    }
    Write-Host "Verified: $PackageName@$Version; $($Paths.Count) bundled files; checksum $Observed"

    Write-Host '4/5  Check whether the public npm package name is already registered'
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
        Write-Host "$PackageName already exists on npmjs.org."
        if (-not $DryRun) {
            throw 'Refusing a first-registration publish into an existing package; inspect package ownership and integrity before proceeding.'
        }
    } else {
        Write-Host "$PackageName is currently unregistered. Only an authorized account can claim it."
    }

    if ($DryRun) {
        Write-Host 'DRY RUN PASS — no registry write, no login, no changes to your installed Skill.'
        return
    }

    Write-Host '5/5  Sign into your npm account with 2FA; explicit approval is required to publish'
    & npm whoami --registry $Registry 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'npm login required: browser-based account authentication and 2FA'
        & npm login --registry $Registry
        Assert-LastExit 'npm login'
    }
    $Account = (& npm whoami --registry $Registry)
    Assert-LastExit 'npm whoami'
    Write-Host "Authenticated npm account: $Account"
    Write-Host "Package: $PackageName@$Version"
    Write-Host "Repository: https://github.com/$Repository"
    $Answer = Read-Host 'Type PUBLISH to claim the npm name and publish this exact verified release (anything else cancels)'
    if ($Answer -cne 'PUBLISH') { throw 'Cancelled by publisher; no npm registry write performed.' }

    & npm publish $Tarball --access public --registry $Registry
    Assert-LastExit 'npm publish'
    $Published = $true
    Write-Host 'Checking npm readback for the published version and SHA-512 integrity'
    $MetadataText = & npm view "$PackageName@$Version" name version dist.integrity repository --json --prefer-online --registry $Registry
    Assert-LastExit 'npm view'
    $Metadata = $MetadataText | ConvertFrom-Json
    if ($Metadata.name -ne $PackageName -or $Metadata.version -ne $Version) {
        throw 'The npm registry readback does not match the package identity.'
    }
    $Sha512 = [System.Security.Cryptography.SHA512]::Create()
    try {
        $ExpectedIntegrity = 'sha512-' + [Convert]::ToBase64String($Sha512.ComputeHash([System.IO.File]::ReadAllBytes($Tarball)))
    } finally {
        $Sha512.Dispose()
    }
    if ($Metadata.dist.integrity -ne $ExpectedIntegrity) {
        throw "Published registry integrity differs from the checked tarball. Inspect publication before promoting README."
    }
    Write-Host "PUBLISHED AND VERIFIED: $PackageName@$Version"
    Write-Host 'Next: configure npm Trusted publishing for D1ChangGeng/UI-Spec-Studio workflow npm-publish.yml (Allow direct npm publish).'
    Write-Host 'Then verify: npx --yes ui-spec-studio@latest --version'
} finally {
    if ($DryRun -or $Published) {
        Remove-Item -LiteralPath $Folder -Recurse -Force -ErrorAction SilentlyContinue
    } else {
        Write-Host "Verification files preserved for diagnosis: $Folder"
    }
}
