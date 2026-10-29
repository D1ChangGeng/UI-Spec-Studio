from playwright.sync_api import sync_playwright,expect
from pathlib import Path
import json,traceback
OUT=Path(__file__).parent;checks=[];metrics=[]
EN_TITLE='How neighbourhood shade, shared seating and accessible routes shape the experience of a long summer walk'
EN_BODY='WORKING QUESTION\n\nA shaded path can feel very different from an exposed route of the same length. We want to understand which features people notice, and which of our assumptions still need evidence.\n\nObservation plan\nWalk both routes at the same time of day. Record the places where participants choose to stop. Keep their words separate from our interpretation.\n\n'+('Evidence and limits\nA short walk cannot establish why someone chose a route. Ask about recent journeys, compare observations across days, and record counterexamples. The notes here are fictional planning material.\n\n'*5)+'Next step\nReturn to the map and identify one question worth investigating.'
ZH_TITLE='从树荫、座椅到无障碍路径：比较不同街区在炎热午后如何支持居民的日常步行与短暂停留'
ZH_BODY='研究问题\n\n同样长的一段路，在树荫下与没有遮蔽的街道上，可能给人不同的感受。我们希望记录居民自己的描述，而不是先用研究者的分类替代他们的经验。\n\n观察计划\n选择两条距离相近的路线，在相同时间步行。记录人们在哪些位置放慢速度、短暂停留，以及他们如何解释自己的选择。\n\n'+('证据与限制\n一次观察不能说明因果关系。天气、同行者、出行目的和身体状况，都可能影响路线选择。需要保留反例，并区分实际记录、尚待核查的判断与未来的研究问题。本段内容是虚构的研究示例。\n\n'*6)+'下一步\n回到地图上，标出需要再次观察的地点。'
def check(name,fn):
 try:fn();checks.append({'name':name,'result':'PASS'})
 except Exception as e:checks.append({'name':name,'result':'FAIL','error':str(e),'trace':traceback.format_exc()})
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 c=b.new_context(viewport={'width':1440,'height':900});q=c.new_page();errors=[];q.on('pageerror',lambda e:errors.append(str(e)));q.goto('http://127.0.0.1:8619/');q.evaluate('document.fonts.ready')
 for title,body in [(EN_TITLE,EN_BODY),(ZH_TITLE,ZH_BODY)]:
  q.locator('#new-note').click();q.locator('#note-title').fill(title);q.locator('#note-body').fill(body);q.locator('#save').click();expect(q.locator('#save-status')).to_have_text('Saved locally')
 check('Create and save long Chinese and English research notes',lambda:expect(q.locator('.note-row')).to_have_count(7))
 for size in [(1440,900),(390,844)]:
  q.set_viewport_size({'width':size[0],'height':size[1]})
  for lang,title,body in [('en',EN_TITLE,EN_BODY),('zh',ZH_TITLE,ZH_BODY)]:
   if size[0]<700:q.locator('#back').click()
   q.locator('#search').fill('neighbourhood shade' if lang=='en' else '树荫、座椅');q.locator('.note-row').click();q.locator('#note-title').blur()
   if q.locator('html').get_attribute('lang')!=('en' if lang=='en' else 'zh-CN'):q.locator('#locale-toggle').click()
   for density in ['comfortable','compact']:
    q.locator('#density').select_option(density)
    for theme in ['light','dark']:
     if q.locator('html').get_attribute('data-theme')!=theme:q.locator('#theme-toggle').click()
     q.screenshot(path=str(OUT/f'long-{size[0]}-{lang}-{density}-{theme}.png'))
     geometry=q.evaluate("""() => {const a=document.querySelector('#note-body'),t=document.querySelector('#note-title'),r=document.querySelector('.note-row');return {bodyWidth:a.getBoundingClientRect().width,bodySize:getComputedStyle(a).fontSize,bodyLeading:getComputedStyle(a).lineHeight,titleSize:getComputedStyle(t).fontSize,rowHeight:r.getBoundingClientRect().height,overflow:document.documentElement.scrollWidth>innerWidth}}""")
     metrics.append({'viewport':size,'locale':lang,'density':density,'theme':theme,**geometry})
     checks.append({'name':f'Long note text and reflow {size} {lang} {density} {theme}','result':'PASS' if not geometry['overflow'] and q.locator('#note-title').input_value()==title and q.locator('#note-body').input_value()==body else 'FAIL'})
 def preserve():
  original_title=q.locator('#note-title').input_value();selected=q.locator('.note-row[aria-current]').get_attribute('data-id');draft=ZH_BODY+'\n尚未保存的新观察。';q.locator('#note-body').fill(draft)
  for value in ['comfortable','compact']:
   q.locator('#density').select_option(value);q.locator('#locale-toggle').click();q.locator('#theme-toggle').click();assert q.locator('.note-row[aria-current]').get_attribute('data-id')==selected;expect(q.locator('#note-title')).to_have_value(original_title);expect(q.locator('#note-body')).to_have_value(draft)
  q.reload();expect(q.locator('#density')).to_have_value('compact');expect(q.locator('html')).to_have_attribute('data-density','compact');expect(q.locator('#note-body')).to_have_value(draft);assert q.locator('.note-row[aria-current]').get_attribute('data-id')==selected
 check('Selected note and unsaved draft survive density/theme/language changes; density and draft survive reload',preserve)
 def reopen_delete():
  if q.locator('html').get_attribute('lang')!='en':q.locator('#locale-toggle').click()
  q.locator('.note-row[aria-current]').click();q.locator('#save').click();expect(q.locator('#mobile-save-status')).to_have_text('Saved locally');q.locator('#back').click();q.locator('#search').fill('尚未保存的新观察');expect(q.locator('.note-row')).to_have_count(1);q.locator('.note-row').click();expect(q.locator('#note-body')).to_contain_text('尚未保存的新观察');q.locator('#delete-note').click();expect(q.locator('#delete-description')).to_contain_text(ZH_TITLE);q.screenshot(path=str(OUT/'long-delete-mobile.png'));q.get_by_role('button',name='Keep note',exact=True).click();expect(q.locator('#note-title')).to_have_value(ZH_TITLE);q.locator('#delete-note').click();q.locator('#confirm-delete').click();assert all(n['title']!=ZH_TITLE for n in json.loads(q.evaluate("localStorage.getItem('leafnote-notebook-v2')"))['notes'])
 check('Long-content save, full-text search, reopen, delete cancel and confirmation',reopen_delete)
 def keyboard_pref():
  q.locator('#density').focus();q.keyboard.press('Home');q.keyboard.press('Enter');expect(q.locator('#density')).to_have_value('comfortable');q.reload();expect(q.locator('#density')).to_have_value('comfortable')
 check('Native density select works by keyboard and persists',keyboard_pref)
 checks.append({'name':'No runtime JavaScript errors','result':'PASS' if not errors else 'FAIL','errors':errors})
 (OUT/'density-results.json').write_text(json.dumps({'browser':b.version,'checks':checks,'geometry':metrics},indent=2,ensure_ascii=False));print(json.dumps(checks,indent=2,ensure_ascii=False));c.close();b.close()
