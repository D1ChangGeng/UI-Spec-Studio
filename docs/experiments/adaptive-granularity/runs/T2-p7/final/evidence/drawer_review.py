from playwright.sync_api import sync_playwright
from pathlib import Path
import json,hashlib
out=Path(__file__).parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);page.goto('http://127.0.0.1:8767/app/');page.locator('#question').fill('A draft to keep');page.locator('#mobile-history').click();page.screenshot(path=str(out/'review-mobile-navigation.png'))
 bounds=page.locator('#history-dialog').bounding_box();page.keyboard.press('Escape')
 checks=[{'name':'Navigation drawer fits phone viewport','pass':bounds['x']==0 and bounds['width']<=390 and bounds['height']<=844,'bounds':bounds},{'name':'Drawer Escape returns focus and retains draft','pass':page.locator('#mobile-history').evaluate('(e)=>e===document.activeElement') and page.locator('#question').input_value()=='A draft to keep'}]
 page.locator('#mobile-history').click();page.locator('#history-dialog [data-theme-toggle]').click();page.screenshot(path=str(out/'review-mobile-navigation-dark.png'))
 checks.append({'name':'Theme toggles inside native navigation drawer','pass':page.locator('html').get_attribute('data-theme')=='dark'})
 (out/'drawer-review.json').write_text(json.dumps({'checks':checks,'source_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('app').glob('*') if f.is_file()}},indent=2));print(json.dumps(checks));b.close()
