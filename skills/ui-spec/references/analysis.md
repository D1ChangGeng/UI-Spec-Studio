# Analysis: decide what is worth building

## Eight lenses, one useful decision

Use these lenses together to understand the current increment. Give depth to the questions that can change the outcome; a concise decision with sound reasons is sufficient.

| Lens | What to establish | Effect on the work |
|---|---|---|
| People and outcomes | Who arrives, their context, main task and observable success | Choose a meaningful increment and the information it needs |
| Product truth | Established capabilities, content, rules, permissions and commitments | Separate facts, fixtures and decisions requiring authority |
| Information architecture | Page responsibility, naming, hierarchy, entry points and shared shell | Create, reuse, consolidate or adjust the right surface |
| Journeys and states | Actions, guards, destinations, retained context, returns and recovery | Build a continuous task rather than isolated screens |
| Visual direction | Subject, tone, hierarchy, density, composition, typography and assets | Form a coherent identity with purpose-specific expression |
| Components and implementation | Existing components, candidate behavior, framework and data boundaries | Choose reliable parts and a practical implementation |
| Inclusive use and performance | Input methods, assistive use, variants, content growth and device constraints | Make the intended experience usable in its actual conditions |
| Verification and delivery | Required observations, review scope, dependencies and completion evidence | Design a result that can be inspected and continued |

## Lead users with different levels of direction

When the user supplies only a product goal, infer a reasonable task and direction from project facts, study relevant examples and recommend a solution. Show a working result that can be evaluated. Routine choices belong to the agent's work.

When the user supplies preferences, references or selected components, identify the intended qualities and binding constraints. Fill the remaining gaps coherently. A precise implementation request warrants fidelity; a mood reference warrants interpretation of its relevant qualities. Preserve explicit preferences and explain material conflicts with behavior, accessibility or feasibility.

Participation can vary by surface and by round. Carry the user's established decisions forward, while continuing to make the open professional choices. Ask a focused question when a missing fact determines a consequential commitment and cannot be recovered from authorized sources. Continue independent work with clearly scoped assumptions.

## Reason about uncertainty

Product uncertainty calls for task/content analysis. Aesthetic uncertainty often benefits from a small rendered composition. Technical uncertainty benefits from an isolated implementation probe. Money, permissions, retention, publication and other consequential business commitments require an authoritative rule or explicit authorization.

Choose the next action using impact, reversibility, current evidence and cost of obtaining better evidence. A low-risk uncertainty often supports an agent-made assumption and a visible trial. A confident preference still benefits from rendering and interaction checks. Keep room for exploration where a decision is cheap to revise; establish important constraints early where they can invalidate later work.

A design direction should be specific enough to guide choices: audience/task, desired tone, content hierarchy, typographic character, density, imagery and motion. Tie the explanation to the subject. Keep factual claims and testimonials anchored in real supplied material; use identifiable representative fixtures to test layout.

## Define each surface by responsibility

Establish its audience/role, job, main action, relevant content and states, entry, next action, shared shell and data owner. Choose the appropriate presentation: public introduction, reading surface, collection/detail, focused task, workspace or overlay.

Merge surfaces when their user task, authority and lifecycle are the same and the difference can be represented by entry context or state. Keep distinct responsibilities separate even when their layouts look alike. Preserve meaningful URLs, browser back/forward, discoverable navigation and task-local actions.

Describe a task as a directed state graph or a short transition table. Return, retry, cancellation and recovery are ordinary parts of the graph. For a meaningful transition, identify its visible control or legitimate entry, precondition, destination, retained context and result. A preview selector establishes display access; actual controls establish task continuity.

For example, a sign-in interruption can preserve an editing draft and return target, establish a session, then resume the intended save with server validation. The page responsibilities follow that task rather than the number of screens a template provides.

## Choose a bounded increment

A strong round improves an identifiable outcome, runs independently enough to inspect, and is small enough for focused feedback. It may be one page, a connected journey, a shared component family or a systemic correction.

Prioritize task/correctness/accessibility blockers, shared defects, missing valuable journeys, design-affecting integration risks, then supporting states and refinement. Adjust that order for explicit goals and actual impact. Consider reach, dependency order, effort and what the round will teach. Explain the important tradeoff briefly; a mandatory scoring formula adds little to a clear choice.

When told to continue, select the next increment from the accepted scope, incomplete journeys and observed defects. A user can redirect that choice at any point. Keep new exploration proportional to what remains unresolved.

## Preserve the right facts

User intent explains the desired outcome; approved design describes accepted experience; code and runtime describe present capability; tests describe observed behavior. Record tensions between these sources rather than treating one as an answer to every question.

For development builds, evolve current code and data models with reproducible initialization. For operating products, derive compatibility, data and availability work from actual obligations. Use the current framework and meaningful abstractions. Scope architecture changes to what the desired experience truly requires.

Record reusable decisions where the project already keeps them. Keep source links and the smallest rationale needed for another round to make the right choice. This enables continuity while leaving detailed implementation in code and history in Git.
