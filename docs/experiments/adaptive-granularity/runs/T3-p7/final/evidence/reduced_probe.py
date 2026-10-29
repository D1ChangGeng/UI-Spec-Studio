from playwright.sync_api import sync_playwright
from pathlib import Path
D=Path(__file__).parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':390,'height':844},reduced_motion='reduce');page.goto('http://127.0.0.1:8737');page.locator('#save').click(timeout=5000);page.wait_for_timeout(750);page.screenshot(path=str(D/'reduced-probe.png'));print('Saved face:',page.locator('#note-card').get_attribute('data-face'));page.locator('#return').click();print('Returned focus:',page.evaluate('document.activeElement.id'));b.close()
