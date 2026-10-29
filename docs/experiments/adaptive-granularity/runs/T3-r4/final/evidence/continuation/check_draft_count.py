from playwright.sync_api import sync_playwright
from pathlib import Path
import json,hashlib
O=Path(__file__).parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox']);q=b.new_page(viewport={'width':1440,'height':900});q.goto('http://127.0.0.1:8314');q.evaluate("()=>localStorage.setItem('fieldnote-collection-v2',JSON.stringify({version:2,notes:[{id:'count-fixture',title:'A saved note',text:'Confirmed text'}]}))");q.reload();q.locator('.note-tile').click();q.locator('#note-text').fill('Unsaved changes');q.locator('#back-collection').click();result={'check':'existing-note edits are counted as a draft','pass':q.locator('#collection-count').inner_text()=='1 saved note · 1 draft','display':q.locator('#collection-count').inner_text(),'app_js_sha256':hashlib.sha256((O.parent.parent/'app/app.js').read_bytes()).hexdigest()};q.screenshot(path=str(O/'draft-count.png'));b.close();(O/'draft-count-report.json').write_text(json.dumps(result,indent=2));print(result)
