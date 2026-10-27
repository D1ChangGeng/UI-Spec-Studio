import React, { useEffect, useRef, useState } from 'react';
import {
  WORKSPACE_NAME, STATUSES, loadState, saveState, loadTheme, saveTheme,
  selectProjects, getScheduleProjects, getWorkspaceSummary, getProjectById,
  updateProjectStatus, addProjectNote,
} from './domain.js';

const statusSlug = (status) => status.toLowerCase().replaceAll(' ', '-');
const money = (value) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(value);
const date = (value) => new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${value}T12:00:00Z`));

export default function App() {
  const [state, setState] = useState(loadState);
  const [theme, setTheme] = useState(loadTheme);
  const [view, setView] = useState('overview');
  const [query, setQuery] = useState('');
  const [status, setStatus] = useState('All');
  const [selectedId, setSelectedId] = useState(null);
  const [note, setNote] = useState('');
  const [message, setMessage] = useState('');
  const dialogRef = useRef(null);
  const openerRef = useRef(null);
  const summary = getWorkspaceSummary(state);
  const filtered = selectProjects(state, { query, status });
  const selected = selectedId ? getProjectById(state, selectedId) : null;

  useEffect(() => {
    if (!saveState(state)) setMessage('Changes could not be saved on this device.');
  }, [state]);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;
    saveTheme(theme);
  }, [theme]);

  useEffect(() => {
    if (selectedId && dialogRef.current && !dialogRef.current.open) {
      dialogRef.current.showModal();
      dialogRef.current.querySelector('[data-testid="detail-title"]')?.focus();
    }
  }, [selectedId]);

  function openProject(event, projectId) {
    openerRef.current = event.currentTarget;
    setSelectedId(projectId);
    setNote('');
    setMessage('');
  }

  function closeProject() {
    dialogRef.current?.close();
    setSelectedId(null);
    setNote('');
    requestAnimationFrame(() => openerRef.current?.focus());
  }

  function changeStatus(nextStatus) {
    setState((current) => updateProjectStatus(current, selectedId, nextStatus));
    setMessage(`Status changed to ${nextStatus}.`);
  }

  function submitNote(event) {
    event.preventDefault();
    if (!note.trim()) return;
    setState((current) => addProjectNote(current, selectedId, note));
    setNote('');
    setMessage('Note saved.');
  }

  function projectContent(project, schedule = false) {
    return (
      <article key={project.id} className="project-item" data-testid={`project-item-${project.id}`}>
        <div>
          <button className="project-link" data-testid={`project-open-${project.id}`} onClick={(event) => openProject(event, project.id)}>
            <span data-testid={`project-title-${project.id}`}>{project.title}</span>
          </button>
          <p>{project.owner} · {project.region}</p>
        </div>
        <dl className="project-meta">
          <div><dt>Status</dt><dd data-testid={`project-status-${project.id}`}>{project.status}</dd></div>
          <div><dt>Budget</dt><dd>{money(project.budget)}</dd></div>
          {schedule && <div><dt>Starts</dt><dd><time data-testid={`schedule-start-${project.id}`} dateTime={project.startDate}>{date(project.startDate)}</time></dd></div>}
          <div><dt>Due</dt><dd><time data-testid={schedule ? `schedule-due-${project.id}` : undefined} dateTime={project.dueDate}>{date(project.dueDate)}</time></dd></div>
        </dl>
      </article>
    );
  }

  return (
    <div className="app" data-testid="app-shell" data-theme={theme}>
      <header className="header">
        <div><strong>{WORKSPACE_NAME}</strong><p>Studio field research</p></div>
        <button data-testid="theme-toggle" aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`} onClick={() => setTheme((current) => current === 'light' ? 'dark' : 'light')}>
          {theme === 'light' ? 'Dark theme' : 'Light theme'}
        </button>
      </header>
      <nav aria-label="Workspace views">
        {['overview', 'projects', 'schedule'].map((name) => (
          <button key={name} data-testid={`nav-${name}`} aria-current={view === name ? 'page' : undefined} onClick={() => setView(name)}>{name[0].toUpperCase() + name.slice(1)}</button>
        ))}
      </nav>
      <main>
        <h1>{view[0].toUpperCase() + view.slice(1)}</h1>
        {view === 'overview' && (
          <section className="summary" aria-label="Workspace summary" data-testid="overview-summary">
            <div><span>Total projects</span><strong data-testid="summary-total-projects">{summary.totalProjects}</strong></div>
            <div><span>Total budget</span><strong data-testid="summary-total-budget">{money(summary.totalBudget)}</strong></div>
            {STATUSES.map((item) => <div key={item}><span>{item}</span><strong data-testid={`summary-${statusSlug(item)}-count`}>{summary.statusCounts[item]}</strong></div>)}
            <div className="chart" aria-label="Projects by status" data-testid="status-chart">
              {STATUSES.map((item) => <div className="chart-row" key={item}><span>{item}</span><div className="bar-track"><div className="bar" style={{ width: `${summary.statusCounts[item] / summary.totalProjects * 100}%` }} /></div><span>{summary.statusCounts[item]}</span></div>)}
            </div>
          </section>
        )}
        <section className="filters" aria-label="Project filters">
          <label>Find project<input type="search" value={query} data-testid="search-input" placeholder="Title, owner, or region" onChange={(event) => setQuery(event.target.value)} /></label>
          <label>Status<select value={status} data-testid="status-filter" onChange={(event) => setStatus(event.target.value)}><option value="All">All statuses</option>{STATUSES.map((item) => <option key={item}>{item}</option>)}</select></label>
          <button data-testid="clear-filters" onClick={() => { setQuery(''); setStatus('All'); }}>Clear filters</button>
        </section>
        <p data-testid="results-count" aria-live="polite">{filtered.length} of {summary.totalProjects} projects</p>
        <section className={view === 'overview' ? 'project-grid' : 'project-list'} data-testid={`${view}-view`} aria-label={`${view} projects`}>
          {(view === 'schedule' ? getScheduleProjects(state, { query, status }) : filtered).map((project) => projectContent(project, view === 'schedule'))}
          {filtered.length === 0 && <p data-testid="empty-state">No projects match these filters.</p>}
        </section>
      </main>
      <dialog ref={dialogRef} data-testid="project-detail" aria-labelledby="detail-title" onCancel={(event) => { event.preventDefault(); closeProject(); }} onClose={() => { setSelectedId(null); requestAnimationFrame(() => openerRef.current?.focus()); }}>
        {selected && <>
          <div className="dialog-heading"><h2 id="detail-title" tabIndex={-1} data-testid="detail-title">{selected.title}</h2><button data-testid="detail-close" aria-label="Close project detail" onClick={closeProject}>Close</button></div>
          <p data-testid="detail-summary">{selected.summary}</p>
          <dl className="detail-meta">
            <div><dt>Project</dt><dd data-testid="detail-id">{selected.id}</dd></div>
            <div><dt>Owner</dt><dd data-testid="detail-owner">{selected.owner}</dd></div>
            <div><dt>Region</dt><dd data-testid="detail-region">{selected.region}</dd></div>
            <div><dt>Budget</dt><dd data-testid="detail-budget">{money(selected.budget)}</dd></div>
            <div><dt>Starts</dt><dd><time data-testid="detail-start" dateTime={selected.startDate}>{date(selected.startDate)}</time></dd></div>
            <div><dt>Due</dt><dd><time data-testid="detail-due" dateTime={selected.dueDate}>{date(selected.dueDate)}</time></dd></div>
            <div><dt>Methods</dt><dd>{selected.methods.join(', ')}</dd></div>
          </dl>
          <label>Project status<select data-testid="detail-status" value={selected.status} onChange={(event) => changeStatus(event.target.value)}>{STATUSES.map((item) => <option key={item}>{item}</option>)}</select></label>
          <h3>Research notes</h3>
          <ul className="notes" data-testid="detail-notes">{selected.notes.map((item) => <li key={item.id} data-testid="project-note"><p>{item.body}</p><small>{item.author} · {date(item.createdAt.slice(0, 10))}</small></li>)}</ul>
          <form onSubmit={submitNote}>
            <label>Add a research note<textarea data-testid="note-input" value={note} maxLength={2000} rows={3} onChange={(event) => setNote(event.target.value)} /></label>
            <button data-testid="note-save" disabled={!note.trim()} type="submit">Save note</button>
          </form>
          <p className="message" data-testid="detail-message" role="status">{message}</p>
        </>}
      </dialog>
    </div>
  );
}
