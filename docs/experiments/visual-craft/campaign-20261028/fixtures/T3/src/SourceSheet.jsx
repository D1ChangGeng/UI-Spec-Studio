import React, { useEffect, useRef, useState } from 'react';
import { fetchSource, readSavedNote, saveSourceNote, SOURCE_SUMMARIES } from './domain.js';

export default function SourceSheet({ sourceId, onSelectSource, onClose, draftsRef }) {
  const [expanded, setExpanded] = useState(false);
  const [source, setSource] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [attempt, setAttempt] = useState(0);
  const [note, setNote] = useState('');
  const [noteStatus, setNoteStatus] = useState('');
  const sheetRef = useRef(null);
  const closeRef = useRef(null);
  const activeRequest = useRef(0);
  const selectedSummary = SOURCE_SUMMARIES.find((item) => item.id === sourceId);

  useEffect(() => {
    closeRef.current?.focus({ preventScroll: true });
    const shell = document.querySelector('[data-testid="app-shell"]');
    if (shell) shell.inert = true;
    return () => { if (shell) shell.inert = false; };
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    const request = ++activeRequest.current;
    setSource(null);
    setLoading(true);
    setError(null);
    setNote(draftsRef.current[sourceId] ?? readSavedNote(sourceId));
    setNoteStatus('');
    fetchSource(sourceId, { signal: controller.signal })
      .then((record) => { if (request === activeRequest.current) setSource(record); })
      .catch((reason) => { if (reason.name !== 'AbortError' && request === activeRequest.current) setError(reason.message); })
      .finally(() => { if (!controller.signal.aborted && request === activeRequest.current) setLoading(false); });
    return () => controller.abort();
  }, [sourceId, attempt, draftsRef]);

  const handleKeyDown = (event) => {
    if (event.key === 'Escape') {
      event.preventDefault();
      onClose();
    }
    if (event.key === 'Tab') {
      const focusable = Array.from(sheetRef.current.querySelectorAll('button, textarea, a[href], [tabindex="0"]')).filter((el) => !el.disabled && el.getClientRects().length);
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
      if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
    }
  };

  const updateNote = (value) => {
    setNote(value);
    draftsRef.current[sourceId] = value;
    setNoteStatus('Unsaved changes');
  };

  const saveNote = () => {
    try {
      saveSourceNote(sourceId, note);
      setNoteStatus('Note saved');
    } catch {
      setNoteStatus('Could not save this note. Try again.');
    }
  };

  return (
    <div className="sheet-backdrop" data-testid="source-backdrop" onPointerDown={(event) => { if (event.target === event.currentTarget) onClose(); }}>
      <section ref={sheetRef} className={`source-sheet ${expanded ? 'is-expanded' : ''}`} role="dialog" aria-modal="true" aria-labelledby="source-title" data-testid="source-sheet" data-mode={expanded ? 'expanded' : 'compact'} data-source-id={sourceId} onKeyDown={handleKeyDown}>
        <div className="sheet-drag-handle" data-testid="source-drag-handle" aria-hidden="true"><span /></div>
        <header className="sheet-header">
          <div><span className="sheet-kicker">SOURCE DETAILS</span><h2 id="source-title" data-testid="source-title">{selectedSummary.title}</h2></div>
          <button ref={closeRef} type="button" className="sheet-close" onClick={onClose} data-testid="source-close" aria-label="Close source details">×</button>
        </header>
        <div className="sheet-tools">
          <div className="sheet-source-picker" aria-label="Choose source">
            {SOURCE_SUMMARIES.map((item, index) => <button type="button" key={item.id} data-testid={`sheet-source-${item.id}`} aria-label={`Read ${item.title}`} aria-pressed={sourceId === item.id} onClick={() => onSelectSource(item.id)}>{index + 1}</button>)}
          </div>
          <button type="button" className="expand-button" data-testid="source-expand" aria-expanded={expanded} onClick={() => setExpanded((value) => !value)}>{expanded ? 'Compact view' : 'Expand reading view'}</button>
        </div>
        <div className="sheet-body" data-testid="source-content">
          {loading && <div className="sheet-message" role="status" data-testid="source-loading">Loading source…</div>}
          {error && <div className="sheet-message" role="alert" data-testid="source-error"><p>{error}</p><button type="button" data-testid="source-retry" onClick={() => setAttempt((value) => value + 1)}>Try again</button></div>}
          {source?.id === sourceId && !loading && !error && <>
            <div data-testid="source-metadata"><p className="source-metadata">{source.authors.join(' & ')} · {source.year} · {source.kind}</p>
            <p className="source-publication">{source.publication} · {source.readingMinutes} min read</p></div>
            <p className="source-summary">{source.summary}</p>
            <blockquote className="source-quote">“{source.keyQuote}”</blockquote>
            <div className="source-sections">
              {source.sections.map((section) => <section key={section.heading}><h3>{section.heading}</h3>{section.paragraphs.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}</section>)}
            </div>
            <section className="source-citation"><h3>Citation</h3><p>{source.citation}</p><p className="fixture-attribution">Fictional source provided for this interface exercise.</p></section>
          </>}
        </div>
        <footer className="sheet-note">
          <label htmlFor="source-note">Your note on this source</label>
          <textarea id="source-note" data-testid="source-note" rows={2} value={note} onChange={(event) => updateNote(event.target.value)} placeholder="What would you like to remember?" />
          <div className="sheet-note-actions"><span role="status" data-testid="source-note-status">{noteStatus}</span><button type="button" data-testid="source-note-save" onClick={saveNote}>Save note</button></div>
        </footer>
      </section>
    </div>
  );
}
