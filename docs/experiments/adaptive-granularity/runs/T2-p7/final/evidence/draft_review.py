from playwright.sync_api import sync_playwright
from pathlib import Path
import json,hashlib
out=Path(__file__).parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);page.goto('http://127.0.0.1:8767/app/');page.locator('#question').fill('An unsent idea worth keeping');page.locator('#mobile-history').click();page.screenshot(path=str(out/'review-mobile-navigation-with-draft.png'));page.locator('#history-dialog [data-new]').click();page.locator('#mobile-history').click();page.locator('#mobile-threads .thread-button').click()
 ok=page.locator('#question').input_value()=='An unsent idea worth keeping';print('Unsent draft can be resumed after New research:',ok)
 assert ok
 (out/'draft-review.json').write_text(json.dumps({'checks':[{'name':'Unsent draft is listed and resumes after New research','pass':ok}],'source_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('app').glob('*') if f.is_file()}},indent=2));b.close()
