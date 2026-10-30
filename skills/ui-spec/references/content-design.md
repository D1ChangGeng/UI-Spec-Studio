# Content design, UX writing and typographic expression

## Contents

- [Purpose and product understanding](#treat-words-as-product-behavior-and-design-material)
- [Information placement](#give-information-a-home-along-the-journey)
- [Element-level writing](#write-at-the-scale-of-the-element)
- [Voice and tone](#establish-voice-and-adapt-tone)
- [Text and composition](#compose-actual-words-with-the-interface)
- [State language](#write-every-meaningful-state)
- [Localization](#localize-the-message-and-its-composition)
- [Roles and maintenance](#maintain-content-through-roles-and-updates)
- [Decisions and verification](#keep-a-traceable-content-decision-where-it-matters)
- [Design-execution output and product language](#distinguish-design-execution-output-from-product-language)

## Treat words as product behavior and design material

Content design decides what people need to understand, at which moment, in which place and form. UX writing gives interface text the right meaning, voice and action. Typography makes that content readable and gives it visual weight in the composition. Design these together with structure, controls, assets and states from the first meaningful slice.

Use the same professional loop that governs visual work: **user/task and source facts → needed understanding → content roles and distribution → product-language research → wording and tone → composition and behavior → real reading/action checks**. Revisit earlier decisions as rendered content, new reference work or authentic product data changes what is needed. The loop is a judgment method, not a required document sequence.

## Begin with the person's understanding

Establish the product model, audience, experience level, first task, familiar vocabulary and what the person already knows. For each important step, identify:

- **Decision or action:** what the person is trying to determine or complete.
- **Missing understanding:** the fact, distinction, condition or consequence needed to proceed.
- **Content authority:** where the actual product fact, rule, price, permission or service outcome comes from.
- **Best carrier:** heading, comparison, form label, short instruction, source, direct manipulation or another medium.
- **Time and placement:** what should be visible on arrival, at decision, during progress and after the outcome.

Use product documentation, tutorials, research and feedback to investigate meaning, operating conditions and familiar vocabulary. Keep the current user's intent, audience evidence and reference-product claims distinct. Follow important textual findings into actual views and operation at the same task step. Attribute marketing copy, interface labels and authored work to their own surfaces. Transfer useful naming and feedback patterns using this product's voice and facts; promises, pricing and policies retain their source's authority.

Domain and engineering terms clarify how the system works. Choose user-facing names by what users recognize, search for and act on. Define technical language at the point of need when it is essential to the task. Keep one stable name for the same object, action or state across navigation, panels, notifications and documentation. A synonym can signal a meaningful change in scope; use it intentionally.

## Give information a home along the journey

Map the user's next question to the surface responsible for answering it. Page headings orient; navigation labels establish destinations; controls express available actions; help text explains an input or condition; comparison content makes differences visible; feedback reports actual outcomes and recovery. Each region can carry several of these responsibilities when their relationship is clear.

Present the information needed for the current decision, then provide sufficient detail when the user explores or commits. Put facts affecting trust, money, safety, eligibility, access or irreversible actions at the decision point where they matter. An important condition may appear at more than one step when context or risk requires it. Evaluate duplication by purpose and timing. Repeated presentation can use a shared fact source while expressing that fact appropriately for each step.

Choose the best expression for the information. A short label can replace a paragraph when the action is evident; a table can clarify repeated differences; an inline example can clarify an unfamiliar input; a link can lead to extended instructions. The design should make the content's job evident without requiring ornamental explanation. If the meaning changes the information architecture, revisit the page/section relationship.

## Write at the scale of the element

| Element | Writing judgment | Reading/action check |
|---|---|---|
| Page title and section heading | Name the subject, task or meaningful change; lead with the relevant idea | Someone can orient and scan headings independently |
| Navigation, tabs and filters | Use stable user-level object/category names; distinguish destinations | Labels predict the location and preserve cross-page vocabulary |
| Buttons, links and menus | Describe the action or destination, with consequence when important | The label matches what the control actually does; alternatives are distinguishable |
| Input label and hint | Name expected input; give format, scope or rules when needed | Input remains understandable without a placeholder; errors attach to the field |
| Product/service details | Distinguish offering, attributes, limits, price/units and delivery | People can compare accurately and understand commitments before acting |
| Empty and first-use states | Explain the relevant condition and available meaningful next action | The user knows whether content is absent, filtered or not yet created |
| Pending and progress | Say what has started and what is awaiting a result | A pending attempt reads differently from a completed operation |
| Success, warning and failure | State confirmed outcome, material consequence and viable next action | Feedback matches the trusted result and supports recovery |
| Dialog and confirmation | State the decision and its effects; make action labels answer it | A reader can identify the consequences of each choice |
| Help, editorial and published docs | Start with the question/answer or task, then supporting evidence and depth | The reading path supports scanning and following through |

Write natural, specific language at the reading distance of the component. Use short copy where the meaning fits; give a consequential task enough precise explanation. A label, heading and adjacent explanation should each add information rather than paraphrase one another. Text that is meaningful at one step can be better placed in another step when the task evolves.

## Establish voice and adapt tone

**Voice** expresses the product's relatively stable language character, terminology and relationship with its audience. **Tone** adjusts that voice for the current situation, user state and consequence. A marketing introduction may be expressive; an account form should be direct; a financial commitment exact; an error constructive; a success message proportionate to the result.

Choose a voice from the actual brand and users; describe it through observable writing characteristics and a few approved examples. Establish conventions for point of view, formality, technical language, sentence style, punctuation and terminology when these decisions recur. A style reference gives candidates and reasons; the current product owns the final choice.

Write and review for accuracy, natural rhythm and semantic precision. Prefer the user's vocabulary and active, concrete verbs when actions are involved. Sentence fragments can serve headings and control labels; complete sentences clarify relationships and causes. Use punctuation according to language, component and meaning: labels and short headings commonly need no terminal period, while warnings, instructions, explanations and errors may need normal sentence punctuation. Respect intentional brand expression where it serves recognition.

Preserve necessary qualifiers. Money, eligibility, delivery, privacy, permissions and guarantees need authoritative rules or approval. Customer counts, testimonials, cases and service promises use confirmed facts; mark illustrative content clearly. Preview actions and messages describe their actual simulated boundary.

## Compose actual words with the interface

Text occupies space. Consider wording, typography and the container together: length, line breaks, script, punctuation, measure, weight, contrast and surrounding space determine hierarchy and optical balance. Design with representative short, common and long content before fixing the layout. Choose fonts by actual language coverage, metric behavior and text role; distinguish a display/wordmark asset from a reusable reading font.

Assign clear roles to display titles, headings, body, labels, supporting explanations, alerts and comparable data. A heading may need semantic line breaks and artistic rhythm; dense operational content needs scannable alignment; reading text needs sustained measure and line rhythm. Text size, wrapping and visible occupancy must remain useful across supported viewports, zoom and themes. Validate actual font readiness, fallback, numeral treatment, punctuation and mixed scripts in the renderer. Adjust theme-specific optical weight only when observation shows a real imbalance. Check that user text-spacing overrides preserve content and controls; accessibility test values describe supported overrides, not default typography tokens.

When content grows, choose precise editing, variable layout, wrapping, disclosure or another representation by the user's need. Text and design influence each other: a simpler name can improve navigation; a consequential condition can require another section; an image can change text placement. Preserve factual meaning. Observe font arrival, expanding content and changing feedback through time for readable holds, reflow and attention; settled text alone cannot establish the reading continuity of that process.

## Write every meaningful state

Design the initial state and the state transitions together. For an asynchronous action, connect **user intent → immediate acknowledgment → pending explanation → authoritative outcome → next action**. Distinguish request receipt, saved data and completed service work when those are separate boundaries. A timeout can leave the outcome unknown: describe what is known and offer the supported status check or recovery path. Retry wording must match whether repeating the action is safe. For partial completion, identify the affected scope and remaining work. Progress, animation and words refer to the same operation; repeated, cancelled or stale requests follow the latest valid task state. Preserve useful input through recovery.

Errors identify the affected item or operation, explain what can be done when known and support the actual recovery path. Associate input errors with their fields; a page-level summary can aid navigation for complex forms. Present service failures, capacity limits and permission conditions where their task-level effect can be explained. Warnings state consequences before commitments. Empty states reflect whether no record exists, no result matches the filter or access is restricted; those conditions lead to different next steps. Keep live announcements useful and proportionate, and preserve focus unless the task requires moving it.

Keep visible labels and accessible names aligned: the accessible name of a text-labelled control contains its visible label. Name icon-only controls by their action and context. Localize accessible names and state announcements with visible copy, and verify that feedback can be perceived in the current reading position and through the implemented accessibility semantics.

Review user-visible content wherever it appears: menus, tooltips, status regions, overlays, first-use guidance, notifications, accessibility names, placeholders, exports and external communication when within task scope. Asset failures and permission-denied paths also need meaningful language.

## Localize the message and its composition

For each supported locale, produce natural target-language copy while preserving the same product facts, user decision and action outcome. Translate meanings and user vocabulary in context, including errors, conditional strings, accessibility labels and dynamic information. Maintain a lightweight glossary for recurring product terms, action labels and protected names. User-authored content and fixed product identities keep their intended ownership.

Use complete, contextual translation units. Preserve translator context for the object, action, state and variable meanings; allow variables and clauses to be reordered. Reuse a message when its meaning and grammatical role are shared, rather than because individual source-language words happen to match. Use the project's localization format for plurality and interpolation, and escape substitutions safely.

Consider script width, punctuation, case, date/time/unit formatting, numbers and language-specific line breaking. Verify the UI with actual strings, long names, supported writing direction and font fallbacks. Keep locale switching compatible with task state. Currency and business terms follow their real authority; language selection changes their presentation only within that authority.

A locale can use different lengths or sentence structures while preserving information and brand character. Revisit component dimensions, image-text balance, reading order and line wraps as needed. Judge both language versions at their actual viewports and themes rather than assuming a string-level equivalence proves layout equivalence.

## Maintain content through roles and updates

Express shared facts according to each role's task and permissions. A customer may need service availability, delivery impact and an available next action; an operator may need the cause, affected items and a recovery control. Both views describe the same underlying condition. Keep useful technical detail with the role that can act on it.

Identify which content comes from code, business data, shared templates, object-specific overrides or editorial tools. Choose the inheritance and override model the product needs, and make the effective content understandable to its editor. Define the meaning of missing, intentionally empty and untranslated values where they differ. Preview actual inherited content and long or unusual values in the consuming interface. Distinguish draft, saved and published results when those states exist. Keep owners, source revisions, locale updates and affected placements traceable for important changes; stale wording should be revised with the fact it describes.

## Keep a traceable content decision where it matters

Use existing project design/content records for significant decisions. The optional [content record](../assets/templates/content-decisions.md) can describe **surface/state → user question → role and placement → approved copy/locale variants → source authority → behavior/visual check**. Keep one authoritative place for product terminology, content ownership and approved wording; share identifiers across pages instead of duplicating the same decision record.

A record is most useful for substantive navigation or product-language choices, payment/permission/contract content, important state text and localized content that changes layout. Routine copy edits remain close to components and tests. Distinguish proposed, implemented, reviewed and explicitly approved wording; actual business facts remain with their source owners. Treat consent, terms and legally consequential copy as decisions requiring the appropriate owner.

## Verify through comprehension and real behavior

Revisit the research question with actual words: can a reader identify the page, choice, consequence and next action? Follow first use, work, errors and recovery. Check scoped page/component content, accessible associations, string coverage, clipping, reflow, focus, status and locale/viewport variants. Inspect hierarchy, density, rhythm and optical balance at comparable content length and scale. Use the [primary references](content-sources.md) for platform and language conditions.

Test the promises made by copy against actual capabilities: a button named “Save” must reach a real save boundary or be clearly labeled as a demo; a success message follows a confirmed result; permission and price text reflect the authoritative system. Use representative scenarios and source-backed review for consequential text. When direct comprehension research is warranted and available, observe users attempting credible tasks without telling them the intended path. Report automated checks, editorial judgment and actual user observations as distinct evidence.

The strongest content outcome makes the next meaningful decision understandable at the moment it is needed, while retaining coherent brand voice and a clear visual place in the product.

## Put language relationships on the same evidence map

Connect consequential copy to its journey question, owning surface/state, factual authority, locale/type treatment and actual checked conditions using [the shared map](evidence-map.md). A new product term can alter L2 navigation, L3 control roles and L4 wrapping; trace those dependents instead of duplicating decision records. Preserve actual source authority for promises and approvals. A translation entry establishes available text; rendered inspection and actual user comprehension require separate evidence. Routine supported wording edits can inherit the established system and retain a short scoped check.


## Explain the visible result before naming its implementation

When presenting a design choice to the user, describe the perceptible difference and its task value before its internal label. For example, explain that a soft light follows the pointer while the reading surface stays still, or that an input grows without moving its primary action. A library name, shader term or “premium material” adjective alone does not explain what the person will experience.

Keep precise resource/version/configuration language in the supporting design record so engineering remains traceable. Distinguish an observed effect from an intended one and actual reuse from a proposed option. Show representative renders or episodes when the choice is visual. Do not expose internal implementation strategy as reassuring product copy, or imply that a known dependency guarantees quality.

Adapt actual wording and type together with a reused block. Preserve factual meaning when sample text is replaced, inspect glyph coverage, CJK/Latin punctuation and line breaking, and verify action/error/pending language at the actual component states. A borrowed block's elegant demo copy may not survive long real labels. Keep ordinary low-impact wording changes proportional to their known design basis.

## Distinguish design-execution output from product language

In the conversation, present consequential design work as observable findings, judgments and results using the [design-event principle](workflow.md#make-consequential-design-work-observable). Make the design object and its changed relationship the subject. Connect what was observed, why it matters, what decision or action follows, and what result or gap remains as useful to that event. These relationships guide clear prose; they do not require four headings, a fixed format or a retelling of internal reasoning. Distinguish an observation from an inference, a selected route from an executed change, and a proposed effect from one actually viewed.

For example, when supported by the evidence: “The expanded input keeps its action row stable, but reduces the message reading area enough to obscure the newest content. The local trial will retain the action layout while the growth limit and scroll relationship are revised.” Pair a visual finding with the relevant real result. The reader can understand the professional judgment and its execution consequence without reconstructing a search log or being asked to decide each routine adjustment. Use direct collaboration when an actual user decision or explanation is needed.

The product interface serves the end user's task and uses its own voice, terminology and information order. Keep design findings, resource comparisons and implementation rationale in the conversation and project records unless the product's task specifically needs them. Express promised hierarchy, material and movement through the actual interface. Tables, borders and explanatory text remain useful when they clarify real information or action; their presence does not prove or disprove craft. The evidence map's categories need not become the product's layout, and a label claiming a visual quality cannot provide it.

Both audiences draw on the same current facts. Revise a superseded design choice in the current model and explain a consequential change when it occurs; preserve the earlier observation at its historical scope. Reuse existing evidence and concise, task-relevant wording so presentation supports continued design work without creating parallel reporting obligations.
