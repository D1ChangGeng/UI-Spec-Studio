from pathlib import Path
from playwright.sync_api import sync_playwright
import os,json
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
root=Path(__file__).resolve().parent
zh_title='街道树荫如何影响人们停留、交谈与选择步行路线？'
zh_body='研究问题\n\n在同一条街道上，树荫、座椅和临街活动如何共同影响人们的停留？目前的观察只能提出问题，还不能说明因果关系。\n\n观察与线索\n• 分别记录中午、下午与傍晚的使用情况。\n• 比较相似距离内有树荫和没有树荫的位置。\n• 区分行走、等候、休息与交谈，避免把不同活动混为一谈。\n\n需要核查的判断\n舒适的停留点可能和更短的步行路线同样重要。但遮阴之外，座椅朝向、噪声、无障碍通行和沿街用途也可能改变使用方式。下次观察要为这些条件留下记录。\n\n下一步\n选择两个工作日和一个周末，各记录三个时段。用简单的现场草图标注树荫边界，按十分钟间隔统计座椅使用情况。不记录个人身份，也不把观察结果描述成受访者意见。\n\n方法备注\n这是用于界面测试的虚构研究笔记，不包含真实参与者或测量结果。'
(root/'long-content.json').write_text(json.dumps({'zh_title':zh_title,'zh_body':zh_body},ensure_ascii=False,indent=2))
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox']);p=b.new_page(viewport={'width':1440,'height':900});p.goto('http://127.0.0.1:8844/');p.locator('#samples').click();p.locator('.note-row').first.click();p.locator('.editor-toolbar').click(position={'x':180,'y':10});p.screenshot(path=str(root/'before-desktop-en.png'))
 p.locator('#new-note').click();p.locator('#note-title').fill(zh_title);p.locator('#note-body').fill(zh_body);p.locator('#save').click();p.locator('#locale-toggle').click();p.locator('.editor-toolbar').click(position={'x':180,'y':10});p.screenshot(path=str(root/'before-desktop-zh.png'));p.set_viewport_size({'width':390,'height':844});p.screenshot(path=str(root/'before-mobile-zh.png'));b.close()
