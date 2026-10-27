import React, {useState} from 'react';
import {createRoot} from 'react-dom/client';
import SpotlightCard from './SpotlightCard/SpotlightCard.jsx';
import TiltedCard from './TiltedCard/TiltedCard.jsx';

const q = new URLSearchParams(location.search);
const source=q.get('surface')||'spotlight';
const zh=q.get('lang')==='zh';
const content=[
  {id:'01',title:zh?'为复杂问题保留清晰的阅读路径':'Keeping a clear reading path through complex work',kind:zh?'工作笔记':'Working note',body:zh?'把问题、证据与下一步放在同一条可追溯的路径上。查看原始材料，再决定哪些结论值得保留。':'Bring the question, supporting material and next step into one traceable reading path. Inspect the source before carrying its conclusion forward.'},
  {id:'02',title:zh?'当多文件附件改变输入区的空间关系':'When multiple attachments change the shape of an input',kind:zh?'设计观察':'Design observation',body:zh?'从单行输入扩展到真实内容之后，检查换行、操作位置与连续使用时的视觉稳定性。':'After moving from a single line to real content, inspect wrapping, action placement and visual stability during continued use.'},
  {id:'03',title:zh?'回到证据，再继续工作':'Return to the source, then continue',kind:zh?'阅读记录':'Reading record',body:zh?'让来源和结论之间的往返保持方向感。保留当前选择，而不是每次重新开始。':'Keep orientation while moving between a source and a conclusion. Preserve the current selection instead of starting over.'}
];
function App(){
 const [theme,setTheme]=useState(q.get('theme')||'dark');
 const [filter,setFilter]=useState('');
 const [selected,setSelected]=useState(null);
 const [pending,setPending]=useState(null);
 const rows=content.filter(x=>(x.title+' '+x.body).toLowerCase().includes(filter.toLowerCase()));
 async function open(x){setPending(x.id);await new Promise(r=>setTimeout(r,280));setSelected(x);setPending(null);}
 const inner=x=><div className="note-content"><span className="note-kind">{x.id} / {x.kind}</span><h2>{x.title}</h2><p>{x.body}</p><div className="note-bottom"><span>{zh?'示例材料 · 本地记录':'Sample material · Local record'}</span><button className="open-note" disabled={pending===x.id} onClick={()=>open(x)}>{pending===x.id?(zh?'正在打开':'Opening'):(zh?'打开笔记':'Open note')} <span aria-hidden="true">↗</span></button></div></div>;
 return <div data-theme={theme} className="app"><header><a href="#main" className="brand">ATLAS <span>/ {zh?'研究资料':'RESEARCH LIBRARY'}</span></a><button onClick={()=>setTheme(theme==='dark'?'light':'dark')} aria-label="Toggle theme">{theme==='dark'?'Light':'Dark'}</button></header><main id="main"><section className="intro"><p className="eyebrow">{zh?'你的工作，保持连贯':'YOUR WORK, KEPT CONNECTED'}</p><h1>{zh?'把发现变成\n可以继续的工作。':'Make discoveries\nyou can return to.'}</h1><p className="intro-copy">{zh?'在笔记与原始材料之间自由往返。这里使用明确标记的示例内容，检验实际组件在阅读任务中的表现。':'Move between working notes and their source material. Clearly marked sample content tests an adopted surface in an actual reading task.'}</p></section><section aria-label="Library"><div className="section-head"><div><h2>{zh?'当前笔记':'Working notes'}</h2><p>{zh?'保留问题、依据与下一步。':'Keep the question, its basis, and the next step.'}</p></div><label>{zh?'查找笔记':'Find a note'}<input aria-label="Find a note" value={filter} onChange={e=>setFilter(e.target.value)} placeholder={zh?'输入标题或内容':'Search title or content'}/></label></div><div className="notes">{rows.map(x=>source==='tilt'?<TiltedCard key={x.id} className="note-tilt" containerWidth="100%" containerHeight="340px" imageWidth="100%" imageHeight="340px" showTooltip={false} intro={false} gyroscope={false} scaleOnHover={1.015} rotateAmplitude={7} glare={0.2} shadow={0.2}>{inner(x)}</TiltedCard>:source==='plain'?<article className="plain-note" key={x.id}>{inner(x)}</article>:<SpotlightCard key={theme+x.id} theme={theme} className="note-spotlight" spotlightColor={theme==='dark'?'#e8be8c':'#735836'} intensity={0.14} borderGlow={0.45} smoothing={0.25} flare={false} grain={0} ambient={false}>{inner(x)}</SpotlightCard>)}</div>{!rows.length&&<p role="status">{zh?'没有匹配的示例笔记。':'No sample notes match.'}</p>}</section>{selected&&<section className="reader" aria-label="Selected note"><button onClick={()=>setSelected(null)}>{zh?'关闭阅读':'Close reading'}</button><span className="eyebrow">{zh?'当前阅读':'CURRENT READING'}</span><h2>{selected.title}</h2><p>{selected.body}</p><p>{zh?'这是组件适配研究中的示例记录，不代表真实研究结论。':'This is a sample record in a component-adoption study, not a real research finding.'}</p></section>}<footer><span>ATLAS / {zh?'维护者局部试装':'MAINTAINER LOCAL TRIAL'}</span><span>{source} · React Bits source e12c221</span><a href="LICENSE.md">Source license</a></footer></main></div>
}
createRoot(document.getElementById('root')).render(<App/>);
