# Folio — a complete personal research experience

Use the supplied ui-spec skill to turn this starter into a polished, usable personal research conversation product. Design the complete everyday journey at a visual and interaction quality comparable to mature research assistants such as Perplexity and ChatGPT, with an independent Folio identity. The open-source Vane (formerly Perplexica) reference is provided as one stable, inspectable example; you may research other public primary sources and implementation resources as useful. This is a runnable frontend product with an authoritative local service fixture, not a production search service. Keep that service boundary truthful in the interface.

Finish the populated experience as carefully as the empty state: initiating a research question, attaching material, reading a long cited answer, inspecting a source, continuing a thread, and returning to past work. Provide light and dark appearances and responsive behavior at 390, 900 and 1440 pixels. Support keyboard actions, visible focus, modal Escape/focus return and reduced-motion preferences. Make choices autonomously; this task delegates art direction and routine implementation decisions.

Business requirements (all remain in scope):

1. On first load show the seeded conversation “A cooler route through the city” and its existing answer; expose both seeded history threads and a new-research action.
2. New research clears the current conversation; sending a nonempty question by button or Enter creates a user message and uses requestAnswer to obtain the answer. Shift+Enter adds a line break; an empty question cannot send.
3. Attach multiple local files, visibly identify them and remove an attachment before sending. Pass their names to the service fixture. Files stay local in this prototype.
4. Each source reference opens the matching source title, publisher and readable full text. Close/Escape returns focus to its trigger.
5. Select either previous thread and continue it without overwriting other histories. Threads persist after reload.
6. Slow responses show honest pending feedback and a Stop action. A stopped or superseded response must not appear in another thread, and text typed while awaiting a response must survive.
7. A fixture failure offers a working retry of the same question without duplicating the user message. The supplied service fails once then succeeds.
8. Long answers remain readable with continued access to the composer, source inspection and history navigation. Avoid horizontal page overflow at all three required widths.
9. Theme switching works throughout the source dialog, composer, history and populated conversation. Both themes retain readable content and focus feedback.
10. Keyboard-only new conversation, send, source reading and close are usable. Under reduced-motion preference, remove nonessential movement while retaining state feedback.

Do not modify src/domain.js. Its business data, latency and failure semantics are shared product contracts. You may replace all UI source, and add appropriately licensed resources and dependencies. Preserve or faithfully reattach the automation hooks in CONTRACT.md; they do not prescribe appearance. Keep the application runnable with npm run build and npm run dev. Use public source access only; no paid account, credential, publishing or human handoff is needed. Record substantive source identities and actual checks in project notes so the work can be maintained. Deliver the finished code, build output, and concise implementation handover.
