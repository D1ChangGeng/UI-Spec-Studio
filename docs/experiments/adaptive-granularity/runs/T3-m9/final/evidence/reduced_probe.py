from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 c=b.new_context(viewport={'width':1440,'height':900},color_scheme='dark',reduced_motion='reduce');g=c.new_page();g.goto('http://127.0.0.1:8939');g.evaluate('window.events=[];["click","pointerdown","pointerup"].forEach(n=>document.addEventListener(n,e=>window.events.push([n,e.target.id,e.target.className]),true))');g.locator('#save').click();g.wait_for_timeout(1800);print(json.dumps(g.evaluate('({events,face:document.querySelector("#note-card").dataset.face,storage:localStorage.getItem("ui-spec-temporal-note-v1"),status:document.querySelector("#status").textContent,transform:getComputedStyle(document.querySelector("#note-card")).transform})')));g.screenshot(path='evidence/reduced-probe.png');b.close()
