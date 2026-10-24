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

## Design the understanding before the arrangement

For the current task, identify what the person knows on arrival, what they must understand next, what evidence supports that understanding and which action becomes reasonable afterward. Use this to order and group content. A reachable purchase button establishes access; clear differences, obligations and credible evidence establish an informed choice.

Give each meaningful region a communication job: orient, explain, compare, substantiate, decide, act or recover. Several jobs may share a region. Choose copy, examples, comparisons, imagery, diagrams or direct manipulation by how well they answer the user's question. A README often needs fit, a working installation command, a usage example and a way to inspect evidence before its full architecture. A workspace may expose the next action alongside the evidence needed to take it.

Write with representative real content early. Headings state meaning; labels name objects consistently; actions describe their consequences; feedback explains actual state and recovery. Distinguish facts, hypotheses, illustrative values and promises. Respect user-authored content and factual copy when improving expression. Treat length, terminology, units and localization as part of the design material.

## Choose a representation before a component

Match the user's cognitive operation to a useful form. These are candidate relationships, not automatic prescriptions:

| Needed understanding or operation | Candidate representation | Check before choosing |
|---|---|---|
| Compare the same properties across objects | Aligned table, comparison rows or coordinated small multiples | Comparable units, consistent order, missing values and narrow-screen reading |
| Find one item in a repeated collection | List/grid with meaningful filters and selection | Distinguishing attributes, scan density and retained query context |
| Understand a dependency or state transition | Diagram, timeline or explicit state presentation | Correct direction, guards, cycles and a readable alternative |
| Inspect the basis for a claim | Claim/evidence pairing, traceable citation or coordinated panes | Provenance, visible association, permissions and navigation back |
| See how a parameter changes a result | Direct manipulation with timely feedback | Safe bounds, actual authority, latency and reversible changes |
| Learn a sequence | Ordered steps, worked example or progressive disclosure | Prerequisites, exceptions, recovery and whether order actually matters |

Choose the simplest representation that preserves the important relationship. Then select the component or production technique. A graph's visual attraction is useful only when its topology helps the task. Distinguish categories, quantities, sequence and uncertainty in data graphics; show units, scale, baseline and missingness honestly. Simulated charts are labeled as fixtures.

## Form a concept that carries across surfaces

Derive direction from the product's distinctive mechanism, subject, audience scene and available material. Name the organizing idea in plain words and connect it to concrete choices. “Evidence beside conclusions” can shape reading panes, citation treatment, comparison views and selection feedback. “Premium” alone leaves those decisions open.

Separate inherited identity, the surface's composition and a local refinement. A coherent incumbent can be authoritative in code even without a design document. Preserve user-pinned decisions. For an open direction, explore materially different organizations when doing so can change the decision; choose a grounded recommendation and demonstrate it. Candidate counts follow useful uncertainty rather than a fixed ceremony.

Evaluate a concept by product fit, clarity, distinctiveness, expansion to related surfaces, implementation feasibility and user control. Distinctiveness can be precise density and excellent status handling, not only expressive artwork. Use analogies to reveal relationships while preserving recognizable controls and accessibility. A concept earns its place through several mutually supporting decisions, not a decorative motif.

## Read references as mechanisms

Select references for a named quality: a comparison's scanability, a publication's type hierarchy, a transition's orientation, or a visual identity's discipline. Use whole → relationships → details observation. Describe what is visible first, then the mechanism you infer. Record uncertain claims as hypotheses; observe live behavior when motion or interaction matters.

Identify what carries the reference's quality, what relies on its content/assets/platform, and what transfers to this task. A photographic composition depends on suitable imagery; its grid alone may carry little of its effect. Learn the grammar while producing original composition and respecting assets' rights. Product popularity and an author's preferred palette supply context rather than universal rules.

## Make decisions explainable and adjustable

For a consequential choice, retain a compact causal trace in the existing design record: the intended outcome, the relationship chosen, the means used, the important tradeoff and what rendering or task evidence would confirm it. This can be one paragraph. Routine adjustments stay in implementation.

Expose the meaningful controls in source: semantic type/color roles, composition bounds, component states, content fields, image focal positions and timing relationships. Preserve their purpose so a later iteration or real integration can change content without losing the design. Treat a successful case as conditional evidence for a method, not as a universal template.

## Let available excellence inform the solution

Use external discovery both to realize a chosen idea and to reveal a stronger expression while the relevant choice is open. Translate the task into a perceptual outcome, interaction and material constraints, then inspect useful incumbent/native capabilities and ecosystem work. A concrete demonstration can expose a possibility that an abstract brief did not name.

Assess the mechanism behind that possibility and its conditions. Preserve binding product direction; compare whether the candidate improves clarity, task behavior, quality or total cost. Choose the appropriate reuse layer before committing implementation effort. An existing suitable choice can continue; a meaningful new requirement merits a fit check. The [resource sourcing reference](component-sourcing.md) supplies the method, the catalog supplies leads, and actual project evidence establishes the result.
