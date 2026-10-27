/**
 * FROZEN BUSINESS FIXTURE. Do not modify this file during a benchmark run.
 * Presentation code may be replaced. Change project state through the exports.
 */

export const WORKSPACE_NAME = 'ATELIER';
export const STORAGE_KEY = 'atelier-workspace-t2-v1';
export const THEME_STORAGE_KEY = 'atelier-theme-t2-v1';
export const STATUSES = Object.freeze(['Planned', 'In progress', 'Review']);
export const CURRENCY = 'USD';

const projects = [
  { id: 'PRJ-001', title: 'Harbor Night Markets', owner: 'Maya Chen', region: 'East Asia', status: 'In progress', budget: 48000, startDate: '2026-10-05', dueDate: '2026-11-13', summary: 'Study how evening market rituals shape shared space along the harbor. Bring vendor interviews, movement observations, and lighting notes into one account.', methods: ['Interviews', 'Observation'], note: 'Vendor interviews are scheduled for the first two evenings.' },
  { id: 'PRJ-002', title: 'Alpine Public Rooms', owner: 'Jonas Weber', region: 'Europe', status: 'Review', budget: 36500, startDate: '2026-09-14', dueDate: '2026-10-30', summary: 'Map the public interiors that support daily life in a mountain town, with particular attention to informal gathering and winter access.', methods: ['Spatial mapping', 'Interviews'], note: 'The town library and station waiting room are ready for comparison.' },
  { id: 'PRJ-003', title: 'Delta Water Stories', owner: 'Amara Okafor', region: 'West Africa', status: 'Planned', budget: 62000, startDate: '2026-11-02', dueDate: '2026-12-11', summary: 'Document everyday relationships with water through household stories, community walks, and seasonal routes across the delta.', methods: ['Community walks', 'Audio diaries'], note: 'Confirm the community walk route with local partners.' },
  { id: 'PRJ-004', title: 'Transit After Hours', owner: 'Luis Ortega', region: 'North America', status: 'In progress', budget: 54500, startDate: '2026-10-12', dueDate: '2026-11-20', summary: 'Follow late-shift journeys and the places where people wait between connections. Identify opportunities for clearer, more welcoming nighttime transit.', methods: ['Journey mapping', 'Observation'], note: 'The first overnight observation covers three interchange stops.' },
  { id: 'PRJ-005', title: 'Courtyard Commons', owner: 'Noor Haddad', region: 'Middle East', status: 'Review', budget: 41000, startDate: '2026-09-21', dueDate: '2026-11-06', summary: 'Explore how shared courtyards balance privacy, hospitality, and neighborhood activity through interviews and measured spatial records.', methods: ['Interviews', 'Spatial mapping'], note: 'Check the courtyard drawings against the final resident interviews.' },
  { id: 'PRJ-006', title: 'Coastal Repair Cultures', owner: 'Sofia Martins', region: 'South America', status: 'In progress', budget: 58750, startDate: '2026-10-01', dueDate: '2026-11-27', summary: 'Trace repair knowledge across coastal workshops, markets, and homes. Record tools, material flows, and the social networks behind everyday maintenance.', methods: ['Workshop visits', 'Object studies'], note: 'Two boat-repair workshops have agreed to a follow-up visit.' },
  { id: 'PRJ-007', title: 'Northern Light Diaries', owner: 'Erik Solberg', region: 'Northern Europe', status: 'Planned', budget: 32750, startDate: '2026-11-09', dueDate: '2026-12-04', summary: 'Collect short diaries about changing daylight and domestic routines, connecting personal accounts to the design of shared indoor spaces.', methods: ['Photo diaries', 'Interviews'], note: 'Prepare the participant diary packs before the November launch.' },
  { id: 'PRJ-008', title: 'Everyday River Crossings', owner: 'Priya Raman', region: 'South Asia', status: 'In progress', budget: 47250, startDate: '2026-10-19', dueDate: '2026-12-18', summary: 'Observe river crossings as places of work, exchange, and waiting. Pair route records with accounts from regular passengers and operators.', methods: ['Route mapping', 'Interviews'], note: 'Compare the morning ferry route with the late-afternoon crossing.' },
  { id: 'PRJ-009', title: 'Desert Listening Posts', owner: 'Salma Benali', region: 'North Africa', status: 'Planned', budget: 39500, startDate: '2026-11-16', dueDate: '2026-12-18', summary: 'Build a sound-led record of gathering places at the edge of the desert, linking listening sessions with local accounts of change.', methods: ['Sound recording', 'Community walks'], note: 'Agree on recording permissions before the listening sessions.' },
  { id: 'PRJ-010', title: 'Shared Kitchen Atlas', owner: 'Nico Rossi', region: 'Southern Europe', status: 'Review', budget: 51250, startDate: '2026-09-28', dueDate: '2026-11-09', summary: 'Study shared kitchens as social infrastructure through cooking sessions, annotated plans, and interviews with the people who keep them running.', methods: ['Participatory sessions', 'Spatial mapping'], note: 'The final atlas needs the partner kitchen captions.' },
  { id: 'PRJ-011', title: 'Market Street Futures', owner: 'Ada Brooks', region: 'Oceania', status: 'In progress', budget: 46000, startDate: '2026-10-26', dueDate: '2026-12-07', summary: 'Investigate how a changing market street supports small businesses, public life, and seasonal events. Combine storefront records with trader conversations.', methods: ['Street survey', 'Interviews'], note: 'Begin the storefront survey at the eastern end of the street.' },
  { id: 'PRJ-012', title: 'Forest Edge Exchanges', owner: 'Elena Petrova', region: 'Eastern Europe', status: 'Planned', budget: 67500, startDate: '2026-11-23', dueDate: '2026-12-21', summary: 'Follow the exchange of materials and knowledge between a forest-edge settlement and nearby workshops, using visits, object stories, and route mapping.', methods: ['Object studies', 'Route mapping'], note: 'Arrange the initial workshop visits with the regional coordinator.' },
].map(({ note, ...project }) => ({
  ...project,
  notes: [{ id: `seed-${project.id}`, body: note, author: project.owner, createdAt: '2026-10-26T09:00:00.000Z' }],
}));

function deepFreeze(value) {
  Object.values(value).forEach((entry) => {
    if (entry && typeof entry === 'object') deepFreeze(entry);
  });
  return Object.freeze(value);
}

export const INITIAL_PROJECTS = deepFreeze(projects);

export function createInitialState() {
  return { schemaVersion: 1, projects: structuredClone(INITIAL_PROJECTS) };
}

function browserStorage() {
  try { return typeof window === 'undefined' ? null : window.localStorage; }
  catch { return null; }
}

// Restore editable state only. Budgets, identities, dates, and all other fixture
// metadata always come from the frozen seed, even after a reload.
function normalizeState(candidate) {
  const state = createInitialState();
  if (!candidate || candidate.schemaVersion !== 1 || !Array.isArray(candidate.projects)) return state;
  state.projects = state.projects.map((project) => {
    const saved = candidate.projects.find((entry) => entry?.id === project.id);
    if (!saved) return project;
    const seedIds = new Set(project.notes.map((note) => note.id));
    const extraNotes = Array.isArray(saved.notes) ? saved.notes.filter((note) =>
      note && typeof note.id === 'string' && !seedIds.has(note.id) &&
      typeof note.body === 'string' && note.body.trim().length > 0 &&
      typeof note.createdAt === 'string' && !Number.isNaN(Date.parse(note.createdAt))
    ).map((note) => ({ id: note.id, body: note.body.trim().slice(0, 2000), author: 'You', createdAt: note.createdAt })) : [];
    return { ...project, status: STATUSES.includes(saved.status) ? saved.status : project.status, notes: [...project.notes, ...extraNotes] };
  });
  return state;
}

export function loadState(storage = browserStorage()) {
  if (!storage) return createInitialState();
  try { return normalizeState(JSON.parse(storage.getItem(STORAGE_KEY))); }
  catch { return createInitialState(); }
}

export function saveState(state, storage = browserStorage()) {
  if (!storage) return false;
  try { storage.setItem(STORAGE_KEY, JSON.stringify(normalizeState(state))); return true; }
  catch { return false; }
}

export function getProjectById(state, projectId) {
  return state.projects.find((project) => project.id === projectId) ?? null;
}

export function selectProjects(state, { query = '', status = 'All' } = {}) {
  const needle = query.trim().toLocaleLowerCase('en');
  return state.projects.filter((project) =>
    (status === 'All' || project.status === status) &&
    (!needle || [project.title, project.owner, project.region].some((value) => value.toLocaleLowerCase('en').includes(needle)))
  );
}

export function getScheduleProjects(state, filters = {}) {
  return [...selectProjects(state, filters)].sort((left, right) => left.dueDate.localeCompare(right.dueDate) || left.id.localeCompare(right.id));
}

export function getWorkspaceSummary(state) {
  const statusCounts = Object.fromEntries(STATUSES.map((status) => [status, 0]));
  const budgetByStatus = Object.fromEntries(STATUSES.map((status) => [status, 0]));
  let totalBudget = 0;
  state.projects.forEach((project) => {
    statusCounts[project.status] += 1;
    budgetByStatus[project.status] += project.budget;
    totalBudget += project.budget;
  });
  return { totalProjects: state.projects.length, totalBudget, statusCounts, budgetByStatus };
}

export function updateProjectStatus(state, projectId, status) {
  if (!STATUSES.includes(status)) throw new Error(`Unknown project status: ${status}`);
  if (!getProjectById(state, projectId)) throw new Error(`Unknown project: ${projectId}`);
  return { ...state, projects: state.projects.map((project) => project.id === projectId ? { ...project, status } : project) };
}

export function addProjectNote(state, projectId, body) {
  if (!getProjectById(state, projectId)) throw new Error(`Unknown project: ${projectId}`);
  const text = String(body).trim();
  if (!text || text.length > 2000) throw new Error('A note must contain 1–2000 characters.');
  const note = { id: `note-${globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(36).slice(2)}`}`, body: text, author: 'You', createdAt: new Date().toISOString() };
  return { ...state, projects: state.projects.map((project) => project.id === projectId ? { ...project, notes: [...project.notes, note] } : project) };
}

export function loadTheme(storage = browserStorage()) {
  try { return storage?.getItem(THEME_STORAGE_KEY) === 'dark' ? 'dark' : 'light'; }
  catch { return 'light'; }
}

export function saveTheme(theme, storage = browserStorage()) {
  if (!['light', 'dark'].includes(theme) || !storage) return false;
  try { storage.setItem(THEME_STORAGE_KEY, theme); return true; }
  catch { return false; }
}
