import React, { useState } from 'react';
import { NAVIGATION } from './navigation.js';
import { SOURCE_SUMMARIES } from './domain.js';

// ACCEPTED SHELL: preserve this component and its content.
export default function Shell({ onOpenSource }) {
  const [activeNav, setActiveNav] = useState('notebooks');
  const [draft, setDraft] = useState('Look for the moments between destinations: waiting, crossing, and finding somewhere to pause.');

  return (
    <div className="app-shell" data-testid="app-shell">
      <header className="app-header" data-testid="app-header">
        <a className="brand" href="#notebook" aria-label="Margin home"><span className="brand-mark" aria-hidden="true">m</span>margin</a>
        <div className="header-location"><span>Workspace</span><span aria-hidden="true">/</span><strong>Personal</strong></div>
        <div className="header-right"><span className="local-status"><i /> All changes saved</span><span className="avatar" aria-label="Your profile">AL</span></div>
      </header>
      <aside className="sidebar" data-testid="sidebar" aria-label="Workspace navigation">
        <div className="workspace-label">YOUR WORKSPACE</div>
        <nav>
          {NAVIGATION.map((item) => (
            <button key={item.id} type="button" className={`nav-item ${activeNav === item.id ? 'selected' : ''}`} aria-pressed={activeNav === item.id} data-testid={`nav-${item.id}`} onClick={() => setActiveNav(item.id)}>
              <span aria-hidden="true" className="nav-icon">{item.icon}</span><span>{item.label}</span><span className="nav-count">{item.count}</span>
            </button>
          ))}
        </nav>
        <div className="sidebar-rule" />
        <div className="workspace-label">NOTEBOOKS</div>
        <div className="notebook-item current"><span className="notebook-dot olive" />Cooling the city</div>
        <div className="notebook-item"><span className="notebook-dot sand" />Everyday infrastructure</div>
        <div className="notebook-item"><span className="notebook-dot mauve" />Places to return to</div>
        <div className="sidebar-bottom"><span className="private-mark" aria-hidden="true">⌑</span> A little room for your thinking.</div>
      </aside>
      <main id="notebook" className="reading-pane" data-testid="reading-pane">
        <div className="reading-inner">
          <div className="notebook-eyebrow"><span className="notebook-dot olive" /> RESEARCH NOTEBOOK <span className="notebook-privacy">Private</span></div>
          <div className="notebook-heading"><h1>Cooling the city</h1><span className="page-menu" aria-hidden="true">···</span></div>
          <p className="notebook-description">Notes on shade, public space, and the everyday experience of a warmer city.</p>
          <div className="notebook-meta"><span>8 notes</span><span>3 sources</span><span>Updated just now</span></div>
          <section className="source-strip" aria-label="Notebook sources">
            <div className="source-strip-label">SOURCES <span>03</span></div>
            <div className="source-chips">
              {SOURCE_SUMMARIES.map((source, index) => (
                <button type="button" key={source.id} className="source-chip" data-testid={`citation-${source.id}`} onClick={(event) => onOpenSource(source.id, event.currentTarget)} aria-haspopup="dialog">
                  <span className="citation-number">{index + 1}</span><span>{source.shortLabel}</span><span aria-hidden="true" className="source-arrow">↗</span>
                </button>
              ))}
            </div>
          </section>
          <article className="notebook-article">
            <div className="article-label">WORKING NOTE <span>·</span> 6 MIN READ</div>
            <h2>A cooler city is a connected city</h2>
            <p className="article-lede">The question is not only where a city is hot. It is what a person can do, and where they can go, while it is hot.</p>
            <p>A temperature map gives us a useful beginning. It shows patterns across a district and makes differences visible at a glance. But an ordinary day unfolds at a smaller scale: a walk to the bus stop, a wait at a crossing, a grocery bag carried home. A neighborhood average cannot tell the whole story of those trips.</p>
            <p>I keep returning to the spaces between destinations. The shaded courtyard matters, but so does the route that leads to it. A park can sit close to housing and still be difficult to reach if the intervening street offers no protection, nowhere to sit, and a long wait to cross.</p>
            <blockquote>Think in routes, pauses, and hours — not only in patches of green.</blockquote>
            <h3>Start with the trip someone already makes</h3>
            <p>There is a practical difference between creating a special destination and making an existing routine more comfortable. The first asks someone to change their day. The second meets them during a day they already have. A shaded seat beside a shop may provide a small but dependable benefit precisely because it lies on a familiar route.</p>
            <p>This suggests a different starting point for observation. Instead of surveying every street in the same way, follow a handful of common trips. Walk from housing to the school gate in the afternoon. Walk from the transit stop to the clinic. Notice where someone must stand still, where they can choose a different path, and where no reasonable alternative exists.</p>
            <p>The observations should include time. A comfortable morning walk may be a difficult afternoon walk, and a useful indoor place may close before the evening has cooled. The route is the same on a plan, but the experience changes as the sun moves and opening hours end.</p>
            <h3>Shade is useful when it is usable</h3>
            <p>Access has several layers. Physical distance is one of them, alongside entrances, crossings, seating, maintenance, and a sense of permission to be there. A courtyard that looks inviting from above can feel private at street level. A roof can cover a bus shelter while leaving its seats exposed to the late sun.</p>
            <p>These are details a broad inventory can miss. They are also details that can sometimes change quickly. Repairing a fountain or moving a bench will not replace a long-term canopy plan, but it can make a place useful while that plan takes shape. The small intervention and the long investment should inform one another.</p>
            <div className="working-question"><span>QUESTION TO KEEP</span><p>Could we describe a neighborhood by the longest uncomfortable gap in an everyday trip?</p></div>
            <h3>The day continues after sunset</h3>
            <p>Outdoor shade is only part of this notebook. Heat also moves indoors and persists into the night. A home may remain warm long after the street becomes comfortable. The ability to recover then depends on building conditions, the options a household has, and the conditions outside an open window.</p>
            <p>A public response organized around the afternoon maximum can overlook these hours. Libraries, evening public spaces, reliable transit, and clear information may all matter at different times. I want to keep the relationship between home and neighborhood visible instead of treating them as separate subjects.</p>
            <p>That relationship also changes how we read success. A place can be cooler in a measurement and still fit poorly into daily life. Conversely, a modest change along an essential route may be valuable even if it barely moves a citywide average. We need both views to understand what a project has accomplished.</p>
            <h3>A working frame for the next round</h3>
            <p>The next set of notes should connect three kinds of evidence: what is measured, what people describe, and what they actually have the option to do. None is a complete account on its own. Together they can reveal where a proposed improvement addresses the problem and where it depends on an assumption that needs testing.</p>
            <p>For now, the most useful frame is a connected network of ordinary places. A comfortable route should lead to somewhere useful; a useful place should be reachable at the time it is needed. The edges between those conditions are where this notebook will look next.</p>
          </article>
          <section className="draft-section" aria-labelledby="draft-label">
            <div className="draft-heading"><h3 id="draft-label">A thought to come back to</h3><span>Draft note</span></div>
            <textarea data-testid="notebook-draft" value={draft} onChange={(event) => setDraft(event.target.value)} aria-label="Notebook draft note" rows={4} />
            <p>Keep a thought here while you read. This draft stays in place as you explore sources.</p>
          </section>
          <footer className="reading-footer">A work in progress, with room in the margins.</footer>
        </div>
      </main>
    </div>
  );
}
