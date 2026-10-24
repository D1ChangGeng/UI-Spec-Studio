write('examples/product-intent/styles.css', r'''
@import url("tokens.css");
/* Conversational page relationships adapted from assistant-ui's pinned ChatGPT
   example. See FOUNDATION.md and THIRD-PARTY.md for scope and MIT notices. */
:root{--ink:#0d0d0d;--quiet:#5d5d5d;--chat-surface:#fff;--chat-border:#e5e5e5;--bubble:#0d0d0d;--bubble-ink:#fff;--chat-width:48rem;--accent:#0d0d0d;--on-accent:#fff;--canvas:#fff}
:root[data-theme=dark]{--ink:#ececec;--quiet:#afafaf;--chat-surface:#212121;--chat-border:transparent;--bubble:#ececec;--bubble-ink:#0d0d0d;--accent:#ececec;--on-accent:#0d0d0d;--canvas:#000}
*{box-sizing:border-box}body{margin:0;height:100dvh;display:flex;flex-direction:column;background:var(--canvas);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans CJK SC","Microsoft YaHei",sans-serif}button,input,textarea,select{font:inherit}button{cursor:pointer;border:1px solid transparent;background:transparent;color:inherit;border-radius:8px;padding:8px 12px;min-height:36px;transition:background-color .12s ease}button:hover{background:var(--slate3)}button:disabled{cursor:default;opacity:.45}a{color:inherit;text-underline-offset:3px}button:focus-visible,a:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--slate11);outline-offset:3px}[hidden]{display:none!important}.sr-only{position:absolute;width:1px;height:1px;clip:rect(0,0,0,0);overflow:hidden}.skip{position:fixed;top:-80px;z-index:40;background:var(--canvas);padding:10px}.skip:focus{top:6px}h1,h2,h3,p{margin:0}p{color:var(--quiet)}h2{font-size:22px;font-weight:550}h3{font-size:16px}.eyebrow{display:block;font-size:12px;color:var(--quiet);margin-bottom:8px}.studybar{display:flex;align-items:center;justify-content:space-between;gap:12px;border-bottom:1px solid var(--slate6);padding:10px 24px;flex:none}.study-name{display:flex;align-items:center;gap:20px;font-size:12px}.study-name strong{letter-spacing:.12em}.study-name>span{color:var(--quiet)}.badge{padding:3px 7px;background:var(--slate3);border-radius:5px;margin-left:8px}.tools{display:flex;gap:6px;flex:none}.tools button{font-size:13px}.direction{display:flex;justify-content:space-between;align-items:center;gap:24px;padding:14px 24px;background:var(--slate2);border-bottom:1px solid var(--slate6);flex:none}.direction p{font-size:13px;color:var(--ink)}fieldset{display:flex;flex:none;border:1px solid var(--slate7);border-radius:9px;padding:4px;margin:0;background:var(--canvas)}fieldset label{position:relative;cursor:pointer}fieldset input{position:absolute;opacity:0}fieldset span{display:block;padding:8px 13px;font-size:13px;border-radius:5px;white-space:nowrap}fieldset input:checked+span{background:var(--ink);color:var(--canvas)}fieldset input:focus-visible+span{outline:3px solid var(--slate11);outline-offset:2px}.app{display:grid;grid-template-columns:216px minmax(0,1fr);flex:1;min-height:0}.sidebar{display:flex;flex-direction:column;gap:24px;padding:24px 14px;background:var(--slate2);border-right:1px solid var(--slate6);min-height:0}.identity{display:flex;align-items:center;gap:12px}.brand-mark{display:grid;place-items:center;width:32px;height:32px;border:1px solid var(--slate8);border-radius:9px}.identity strong{font-size:20px}.identity small,.sidebar-foot small{display:block;color:var(--quiet);font-size:11px}.new{border-color:var(--slate7);background:var(--canvas);text-align:left;font-size:14px}.sidebar nav{overflow:auto;min-height:0}.nav-label{font-size:12px;color:var(--quiet);display:block;margin:0 10px 8px}.topic{display:block;text-align:left;width:100%;font-size:13px;margin-bottom:6px}.topic small{display:block;color:var(--quiet);font-size:11px;margin-top:4px}.topic.active{background:var(--slate4)}.sidebar-foot{margin-top:auto;display:flex;gap:10px;align-items:center;border-top:1px solid var(--slate6);padding-top:16px;font-size:12px}.avatar{display:grid;place-items:center;width:30px;height:30px;background:var(--slate4);border-radius:50%}main{min-width:0;min-height:0;overflow:auto;padding:0 24px 24px}.workspace-head{display:flex;align-items:center;gap:12px;font-size:12px;color:var(--quiet);min-height:54px;flex:none}.data-note{margin-left:auto}.mobile-only{display:none}#evidence{display:none}
/* F1: a page-level welcome/active system, not independently invented regions. */
[data-model=conversation] .app{grid-template-columns:minmax(0,1fr)}[data-model=conversation] .sidebar{display:none}[data-model=conversation] #history{display:inline-block}[data-model=conversation] main{display:flex;flex-direction:column;overflow:hidden;padding:0 16px 10px}#conversation{width:100%;max-width:var(--chat-width);margin:0 auto;display:flex;flex:1;min-height:0;flex-direction:column;justify-content:center;padding:0 16px min(16vh,120px)}.welcome{text-align:center;margin-bottom:24px}.welcome h1{font-size:24px;line-height:28px;font-weight:400;letter-spacing:0}.welcome>.eyebrow,.welcome>p{display:none}#composer{width:100%;border:1px solid var(--chat-border);background:var(--chat-surface);border-radius:28px;padding:8px;flex:none}.composer-row{display:flex;align-items:flex-end;gap:4px}.composer-row textarea{display:block;flex:1;min-width:0;width:100%;min-height:36px;max-height:208px;resize:vertical;line-height:24px;background:transparent;border:0;color:var(--ink);padding:6px 12px;font-size:16px}.composer-row textarea::placeholder{color:var(--quiet)}#send,#stop{display:grid;place-items:center;width:36px;height:36px;min-height:36px;flex:none;border-radius:50%;padding:0;background:var(--ink);color:var(--canvas)}#send span:not(.sr-only){font-size:22px}#stop>span:not(.sr-only){font-size:14px}.composer-footer{display:flex;justify-content:center;margin:6px 8px 0;color:var(--quiet);font-size:11px}.suggestions{width:100%;margin-top:24px;display:flex;flex-wrap:wrap;justify-content:center;gap:8px}.suggestions>.eyebrow{display:none}.suggestions button{border:1px solid var(--slate6);border-radius:18px;font-size:12px;padding:7px 12px}.suggestions button span{margin-left:10px;color:var(--quiet)}.has-result #conversation{justify-content:flex-start;padding:0 0 4px}.has-result #thread{flex:1;min-height:0;overflow:auto;padding:28px 8px 12px}.has-result #composer{margin-top:8px}.message{width:100%;font-size:16px;line-height:24px;margin:0 auto 32px;overflow-wrap:anywhere}.message.user{width:fit-content;max-width:70%;margin-left:auto;margin-right:0;border-radius:22px;background:var(--bubble);color:var(--bubble-ink);padding:10px 16px}.message p{color:var(--ink);margin-bottom:14px}.response-label{display:block;color:var(--quiet);font-size:11px;margin-bottom:12px}.source-button{min-height:32px;font-size:12px;color:var(--quiet);padding:5px 8px;border-radius:8px}.error{border:1px solid var(--slate8);padding:16px;border-radius:12px}.error button{display:block;margin-top:12px;background:var(--slate3)}.pending{font-size:14px;color:var(--quiet);padding:14px 0}#feedback{max-width:var(--chat-width);width:100%;margin:8px auto 0;flex:none;font-size:12px;color:var(--quiet)}.primary{background:var(--ink);color:var(--canvas);white-space:nowrap}.primary:hover{background:var(--ink);opacity:.9}.doc-heading{display:flex;align-items:center;justify-content:space-between;gap:24px;margin:40px 0 24px}.doc-heading h1{font-size:30px;line-height:1.4;font-weight:550;margin-bottom:12px}.doc-heading p{font-size:14px}.table-head,.document{display:grid;grid-template-columns:minmax(0,1fr) 80px 60px;gap:12px;align-items:center;width:100%;text-align:left}.table-head{font-size:12px;color:var(--quiet);padding:12px}.document{padding:18px 12px;border-top:1px solid var(--slate6);border-radius:0;font-size:14px}.document strong{font-weight:500}.status-pill{font-size:11px;background:var(--slate3);padding:3px 8px;border-radius:5px;width:fit-content}#editor label{display:block;color:var(--quiet);font-size:12px;margin:20px 0 8px}#editor input,#editor textarea{width:100%;border:1px solid var(--slate7);border-radius:8px;background:var(--slate2);color:var(--ink);padding:12px}#editor textarea{resize:vertical;line-height:1.7}.editor-footer{display:flex;justify-content:space-between;align-items:center;gap:24px;margin-top:20px}.editor-footer span{font-size:12px;color:var(--quiet)}.testbar{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:9px 20px;border-top:1px solid var(--slate6);font-size:11px;color:var(--quiet);flex:none}.testbar details{max-width:70%}.testbar summary{cursor:pointer}.testbar details[open] summary{margin-bottom:8px}.testbar details span{margin-left:12px}.testbar select{margin-left:8px;font-size:12px}dialog{width:min(920px,calc(100vw - 32px));max-height:85dvh;border:1px solid var(--slate7);border-radius:16px;padding:28px;background:var(--canvas);color:var(--ink);box-shadow:0 24px 80px #0003}dialog::backdrop{background:#10182088}.dialog-head{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;margin-bottom:16px}.dialog-head button{border-color:var(--slate7)}dialog p{font-size:14px;line-height:1.7}.decision-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:24px 0}.decision-grid article{border:1px solid var(--slate7);border-radius:10px;padding:20px}.decision-grid h3{margin-bottom:12px}.decision-grid a{display:inline-block;font-size:12px;margin-top:16px}.decision-table{overflow:auto}table{width:100%;border-collapse:collapse;font-size:12px}th,td{min-width:120px;text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid var(--slate6)}th{background:var(--slate2)}code{font-size:11px}.footnote{font-size:11px!important;margin-top:20px}#history-dialog button[data-history]{display:block;width:100%;text-align:left}*{scrollbar-width:thin;scrollbar-color:var(--slate8) transparent}
@media(max-width:650px){.studybar{padding:10px 14px}.study-name{display:block;font-size:10px}.study-name>span{display:block;margin-top:4px}.tools{gap:2px}.tools button{padding:7px;font-size:12px}.direction{display:block;padding:12px 16px}.direction p{font-size:12px;margin-bottom:12px}fieldset{width:100%}fieldset label{flex:1;text-align:center}fieldset span{padding:8px;font-size:12px}.app{grid-template-columns:minmax(0,1fr)}.sidebar{display:none}.mobile-only{display:inline-block}main{padding:0 16px 16px}.data-note{display:none}#conversation{padding-left:0;padding-right:0;padding-bottom:8vh}.welcome h1{font-size:23px;line-height:30px}#send,#stop{width:44px;height:44px}.message.user{max-width:85%}.suggestions{margin-top:20px;gap:8px}.suggestions button{font-size:11px}.composer-footer{font-size:10px}.doc-heading{display:block;margin-top:24px}.doc-heading button{margin-top:16px}.table-head,.document{grid-template-columns:minmax(0,1fr) 65px 36px;padding-left:0;padding-right:0;gap:8px;font-size:12px}.editor-footer{align-items:flex-start}.editor-footer span{max-width:60%}.testbar{padding:8px 12px;font-size:10px;gap:8px}.testbar>span{max-width:55%;text-align:right}.testbar details[open] span{display:block;margin:8px 0}.decision-grid{grid-template-columns:1fr;gap:12px}dialog{padding:20px}.has-result #thread{padding-top:18px}.has-result .composer-row textarea{max-height:110px}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
''')

page=ROOT/'examples/product-intent/index.html'
html=page.read_text(encoding='utf-8')
html=html.replace('你的下一项研究，<br>从什么问题开始？','从哪里开始这次研究？')
start=html.index('   <form id="composer">'); end=html.index('</form>',start)+len('</form>')
html=html[:start]+'''   <form id="composer"><label for="question" class="sr-only">研究问题</label><div class="composer-row"><textarea id="question" placeholder="描述一个问题，或继续追问…" rows="1" maxlength="3000"></textarea><button type="submit" id="send" disabled aria-label="发送研究问题"><span aria-hidden="true">↑</span></button><button id="stop" type="button" hidden aria-label="停止研究"><span aria-hidden="true">■</span></button></div><div class="composer-footer">演示研究 · 不发送外部请求</div></form>'''+html[end:]
html=html.replace('<tbody>','''<tbody>
<tr data-foundation="assistant-ui-chatgpt"><td>整体页面 / 对话研究</td><td><a href="https://www.assistant-ui.com/examples/chatgpt">assistant-ui · ChatGPT page</a> · 页面级设计迁移</td><td>继承空态构图、768px 阅读宽度、共享输入区、消息比例与状态布局；见 FOUNDATION.md 的来源、变化和范围</td></tr>''',1)
html=html.replace('此方案推荐对话作为主循环。','此方案以成熟对话页面为基础。')
page.write_text(html,encoding='utf-8',newline='\n')
# Preserve newly typed drafts and bind retry to the failed request's own intent.
edit('examples/product-intent/app.js', "retry.onclick = () => { answer.remove(); submit(lastQuestion, true); };", "retry.onclick = () => { answer.remove(); submit(question, true); };")
edit('examples/product-intent/app.js', "$('question').value = ''; $('send').disabled = true;\n      }", "if ($('question').value.trim() === question) $('question').value = '';\n        $('send').disabled = !$('question').value.trim();\n      }")

foundation={
 'id':'assistant-ui-chatgpt', 'scope':'conversation page composition',
 'granularity':'page', 'method':'cross-stack design transfer',
 'source_commit':'1fbf00dd0388fee912af95401876a6cc3c232b2c',
 'source_path':'apps/docs/components/pages/examples/chatgpt.tsx',
 'source_blob':'0f22e7855a954269ecdee0fd9963240c966e1bc1',
 'demo':'https://www.assistant-ui.com/examples/chatgpt',
 'source':'https://github.com/assistant-ui/assistant-ui/blob/1fbf00dd0388fee912af95401876a6cc3c232b2c/apps/docs/components/pages/examples/chatgpt.tsx',
 'reviewed_on':'2026-10-25', 'approval':'pending',
 'preserved':['welcome composition and primary action','48rem reading measure','shared composer across empty and active states','28px composer and 22px user-message radii','right-aligned bounded user messages','independently growing reading area with reachable composer','theme roles and state-prioritized actions'],
 'adapted':['Chinese research content','source-inspection action','native fixture state and one local note','44px phone action targets','85% narrow user bubble','legible placeholder color'],
 'scope_limits':['The React runtime is not installed in this native fixture.','Voice, attachments, hosted history and real research services are outside the fixture.','The document model remains a comparison probe, not the selected production foundation.'],
 'alternatives':[{'item':'shadcn dashboard-01','source':'https://ui.shadcn.com/blocks','decision':'Its dashboard cards/charts address a different primary task; useful for an operational surface.'},{'item':'shadcn sidebar-07','source':'https://ui.shadcn.com/blocks/sidebar','decision':'Useful shell block; it leaves the conversation page decisions open.'}],
 'verification':'report.json from tools/validate_scenario.py; image inspection and actual project acceptance remain scoped'
}
write('examples/product-intent/foundation.json',json.dumps(foundation,ensure_ascii=False,indent=2))
write('examples/product-intent/FOUNDATION.md', '''# Conversational page foundation

The selected starting point is the [assistant-ui ChatGPT page example](https://www.assistant-ui.com/examples/chatgpt),
with [source pinned to 1fbf00dd](https://github.com/assistant-ui/assistant-ui/blob/1fbf00dd0388fee912af95401876a6cc3c232b2c/apps/docs/components/pages/examples/chatgpt.tsx).
The reviewed source blob is `0f22e7855a954269ecdee0fd9963240c966e1bc1`.

## Why this reuse level

The assumed task starts with a question and continues through a thread. The
complete page already coordinates the welcome composition, primary input,
reading measure, user/assistant distinction, action placement and active-state
layout. Inheriting those relationships together resolves more consequential
choices than selecting a color palette and an isolated input.

The official shadcn dashboard-01 was compared as a page-level alternative. Its
metrics/chart/table hierarchy serves an operational overview rather than this
primary loop. Sidebar-07 is a useful shell-level candidate but leaves most of the
conversation composition unresolved. These are task-fit decisions, not universal
quality rankings.

## Inherited relationships and actual locations

| Source relationship | Project realization | Observation |
|---|---|---|
| Empty heading and composer grouped above center | `#conversation`, `.welcome`, `#composer` | Whole empty-state viewport at four sizes |
| Shared 48rem reading/composer measure | `--chat-width`, `#conversation` | Computed width and active-state render |
| 24px/28px regular empty heading | `.welcome h1` | Actual Chinese rendering; narrow adaptation recorded |
| 28px composer; state-prioritized send/cancel | `#composer`, `#send`, `#stop` | Source radius, input/cancel/retry tasks |
| 70% bounded, right-aligned user message with 22px radius | `.message.user` | Active-state geometry; 85% phone adaptation |
| A stable reachable composer during growing results | `.has-result #thread`, `#composer` | Long-content scroll and input retention |
| Coherent light/dark reading and composer roles | Root tokens in `styles.css` | Targeted actual contrast pairs and rendered themes |

The adoption method is **page-level design transfer into a native fixture**.
It inherits the page's coordinated design decisions; it does not install the
upstream React runtime. For a compatible real React product, adopting the actual
components/runtime is a candidate before rewriting their behavior. This fixture's
portability constraint is local, not a default implementation policy.

Research copy, source inspection, local note behavior and accessible phone targets
are explicit product/fixture adaptations. Voice, attachments, hosted history and
real research services are outside this sample. Document-first remains a bounded
comparison probe. The actual product owner still selects the product direction.

The official documentation and exact source were inspected on 2026-10-25. The
native projection is rendered and exercised by the scenario runner. Upstream live
browser observations, when available in the release evidence, retain their actual
URL/date and are separate from the pinned code and the adapted sample.

See [the decision record](README.md), [machine-readable source mapping](foundation.json)
and [preserved notices](THIRD-PARTY.md).
''')
add('examples/product-intent/README.md', '''## Page-level foundation

The conversational direction now starts from a concrete mature page rather than
independently authored major regions. [The foundation record](FOUNDATION.md)
explains the candidates compared, chosen granularity, inherited relationships,
precise source identity and deliberate adaptations. The source map is in
[foundation.json](foundation.json). The document direction remains a comparison
probe; real product intent and acceptance remain open.

This is a whole-page design transfer into the native fixture. Runtime integration
is a separate adoption decision for the consuming product's actual stack. The
browser checks inspect the realized relationships and state paths rather than
using attribution alone as evidence of quality.''')
# Keep the old detailed row map accurate under the selected foundation.
edit('examples/product-intent/README.md', '| D1 / shared navigation |', '| D1 / study navigation (supporting probe) |')
edit('examples/product-intent/README.md', 'Neutral reading surfaces with project-authored blue emphasis; actual paired contrasts are measured', 'Slate study chrome supports the adopted assistant page\'s monochrome reading roles; actual paired contrasts are measured')
edit('examples/product-intent/README.md', 'Typography,', 'Typography,') if False else None
add('examples/product-intent/THIRD-PARTY.md', '''## assistant-ui page composition

The page-level relationships and corresponding style values identified in
FOUNDATION.md are adapted from `assistant-ui/assistant-ui` at commit
`1fbf00dd0388fee912af95401876a6cc3c232b2c`,
`apps/docs/components/pages/examples/chatgpt.tsx`.

MIT License

Copyright (c) 2026 AgentbaseAI Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''')
edit('examples/product-intent/THIRD-PARTY.md','The semantic role mappings and all scenario behavior/layout are project-authored.','The Slate role mappings and fixture behavior are project-authored. The page-level\nlayout adaptation is separately identified below.')

