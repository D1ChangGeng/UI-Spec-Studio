#!/usr/bin/env python3
"""Complete the task-owned 1.4 candidate before ordinary release validation."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
def edit(name, old, new):
    path=ROOT/name; text=path.read_text(encoding='utf-8')
    if old not in text: raise ValueError(f'Expected revision context missing: {name}: {old[:70]}')
    path.write_text(text.replace(old,new,1),encoding='utf-8',newline='\n')
def add(name, text):
    path=ROOT/name; path.write_text(path.read_text(encoding='utf-8').rstrip()+'\n\n'+text.strip()+'\n',encoding='utf-8',newline='\n')
def write(name, text):
    path=ROOT/name; path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text.strip()+'\n',encoding='utf-8',newline='\n')

if (ROOT/'VERSION').read_text().strip() != '1.4.0':
    raise SystemExit('This revision applies to the staged 1.4.0 candidate.')
edit('.github/workflows/validate.yml', '  push:\n    branches-ignore:\n      - work/ui-spec-1.4-resource-foundations\n', '  push:\n')

edit('skills/ui-spec/SKILL.md', 'Develop a coherent interface through small, reviewable increments, then carry the accepted experience into the real product.', 'Build from suitable mature design work, refine it through small, reviewable increments, then carry the accepted experience into the real product.')
edit('skills/ui-spec/SKILL.md', '## Establish the professional context', '''## Start from mature design work

Use design theory and resource knowledge together. Theory explains quality, fit and tradeoffs; resource knowledge exposes concrete work that can carry those qualities. Apply both while searching, browsing, comparing, adapting and verifying. Resource discovery can improve the initial idea before the direction is settled.

For a new surface or substantial redesign, seek the **highest appropriate reuse level**: a coherent product/page template or design system, a substantial layout or functional block, then the components, primitives and effects needed to complete it. Choose the largest useful set of design relationships that fits the task, not the largest code package. An established accepted page may need only a component-level change.

Inherit valuable decisions about hierarchy, proportions, reading rhythm, interaction and states. Concentrate original design on product differences, missing capabilities, coherent adaptation and integration. Inspect concrete candidates and explain a native or original choice when its fit is stronger. A few sourced details do not establish a page-level foundation; show which important relationships the selected work actually supplies.

## Establish the professional context''')
edit('skills/ui-spec/SKILL.md', 'Connect **task and facts → needed understanding → expression concept → information/visual/interaction grammar → assets and implementation → observed outcome**.', 'Connect **product intent → search and actual browsing → professional comparison → foundation and reuse decisions → adaptation and integration → observed outcome**. Keep needed understanding, expression concept and visual/interaction grammar active as questions throughout this loop.')
edit('skills/ui-spec/SKILL.md', 'For a substantive visual or interaction need, actively inspect existing project capabilities and relevant external work. Find a strong starting point before committing to a custom build.', 'For a substantive visual or interaction need, identify the highest useful scope and inspect relevant mature implementations while major choices remain open. Evaluate internal candidates against the same target. Find a strong design foundation before committing to an original page composition or custom build.')
edit('skills/ui-spec/SKILL.md', 'product evidence, meaningful alternatives, selected resources by surface/element, actual implementation locations and observed results.', 'product evidence, compared foundations, chosen reuse granularity, relationships being inherited, meaningful alternatives, selected resources by surface/element, actual implementation locations and observed results.')

edit('skills/ui-spec/references/analysis.md', '## Recognize the product through its use', '''## Use theory to investigate real design work

Treat theoretical knowledge and UI resource knowledge as complementary working material. Theory makes hierarchy, rhythm, visual weight, interaction and engineering tradeoffs legible. Resource knowledge gives those judgments concrete candidates and realistic implementation choices. Analyze to guide the search; browse to find possibilities; compare to select; implement to test the fit. Findings can refine the original representation or product hypothesis.

For an open surface, ask which mature page, system or substantial block already resolves most of its important relationships. Study that whole before separating out local components. Carry forward a coherent foundation when it fits, and identify the particular changes the product needs. Original design fills meaningful gaps and coordinates the result. For a bounded correction in an accepted system, inherit that foundation and investigate only the affected decision.

## Recognize the product through its use''')
edit('skills/ui-spec/references/analysis.md', 'Choose the simplest representation that preserves the important relationship. Then select the component or production technique.', 'Choose a representation that preserves the important relationship, and test it against concrete mature implementations. A strong candidate can refine that choice. Select the appropriate page, block, component or production technique at the useful reuse level.')
edit('skills/ui-spec/references/component-sourcing.md', 'Treat the UI ecosystem as part of the design workspace.', 'Treat the UI ecosystem as a primary source of design and engineering foundations.')
edit('skills/ui-spec/references/component-sourcing.md', '## Research product conventions and implementation resources in parallel', '''## Choose the highest appropriate reuse level

Match the scope of the design problem to the largest coherent set of mature decisions worth inheriting. For a new page, inspect page/application templates and design systems before assembling isolated parts. For an accepted page with a local gap, investigate the relevant block or component directly. Reuse granularity and adoption method are separate choices: a whole-page composition can be transferred across stacks, while one primitive can be adopted as a package.

| Reuse level | Valuable decisions to inherit | Fit to establish |
|---|---|---|
| Product/page template or design system | Primary loop, shell, information hierarchy, proportions, typography, tokens and state family | Product model, content, rights, supported states and practical adaptation boundary |
| Layout or functional block | A coherent region, internal hierarchy, spacing rhythm and connected interaction | Region responsibility, surrounding composition, responsive behavior and shared state |
| Component family or behavior primitive | Consistent semantics, variants, focus and reliable controls | Required behavior, design-system integration and real state ownership |
| Asset, background, motion or micro-interaction | A specific expressive or feedback mechanism | Role, restraint, attention, accessibility and combined runtime cost |

The highest appropriate level is the most valuable coherent fit, not the maximum amount of imported code. A full template with the wrong task model may impose more redesign than a suitable block. Prefer one compatible visual language for the major regions, then use complementary parts where they add value. A copied design system's completeness, a source's popularity and the current product's quality remain separate evidence.

Read, view and compare the actual candidate at its consequential states and sizes. Preserve the mechanism and relationships that justify selection. When an otherwise useful source crosses frameworks, assess both a matching-stack implementation and a deliberate design/code port. Keep rights, behavior and maintenance responsibilities clear. Use original implementation for the gaps or tradeoffs that the comparison actually establishes.

## Research product conventions and implementation resources in parallel''')
edit('skills/ui-spec/references/component-sourcing.md', 'Start the shortlist before implementation; reconcile it with code and observed output at review.', 'Start the foundation comparison and shortlist before implementation; reconcile them with code and observed output at review. Name the selected granularity, the relationships inherited together, material changes and why that level is appropriate.')
edit('skills/ui-spec/references/component-sourcing.md', 'Find resources by **design need**; choose adoption by **delivery form**:', 'Search by **product pattern and design need**, choose the useful **reuse granularity**, then determine **delivery form and adoption method**:')
edit('skills/ui-spec/references/component-sourcing.md', 'A strong starting point can improve the design itself as well as shorten its realization.', 'A strong foundation carries resolved relationships in layout, hierarchy, type, interaction and implementation. Its value is the useful design decisions inherited, as well as the work saved.')

edit('skills/ui-spec/references/workflow.md', '3. **Form a direction.**', '3. **Explore mature foundations.** Use the proposed product model to locate suitable complete pages, design systems or substantial blocks. Browse concrete candidates and their source; compare the design relationships, states and adaptation burden they supply. Let a strong candidate refine the initial hypothesis. Choose the highest appropriate reuse level before committing to a new composition.\n4. **Form a direction.**')
edit('skills/ui-spec/references/workflow.md', '4. **Check implementation fit.**', '5. **Check implementation fit.**')
edit('skills/ui-spec/references/workflow.md', '5. **Make the important choice inspectable.**', '6. **Make the important choice inspectable.**')
edit('skills/ui-spec/references/workflow.md', '6. **Carry a usable decision forward.**', '7. **Carry a usable decision forward.**')
edit('skills/ui-spec/references/workflow.md', 'Connect content meaning to an expression concept, a representation and concrete visual/interaction grammar.', 'Apply design theory to concrete foundation candidates, then carry the selected hierarchy, proportions, type rhythm and state relationships into the increment. Connect content meaning to an expression concept, a representation and concrete visual/interaction grammar.')
edit('skills/ui-spec/references/workflow.md', 'Use representative short, typical and long content, realistic data density and meaningful state changes.', 'Adapt the selected foundation at its useful granularity and preserve its valuable relationships. Use representative short, typical and long content, realistic data density and meaningful state changes.')

add('skills/ui-spec/references/principles.md', '''## Inherit and adapt resolved relationships

Read a mature foundation as a connected set of decisions: content hierarchy, measure, alignment, spacing rhythm, surface roles, states and attention. Preserve the relationships that make it effective while changing the product-specific content and behavior. Evaluate a typography or spacing change through its effects on the whole composition rather than as an isolated improvement.

Use theory to select, explain, combine and verify those relationships throughout discovery and implementation. A coherent page or block often provides a stronger starting point than separately invented regions. When combining sources, establish one governing visual language and adapt secondary parts to it. Confirm the selected foundation still works with actual content, states and viewing conditions.''')
add('skills/ui-spec/references/interaction-and-variants.md', '''## Inherit behavior at its useful scope

Study the foundation's complete task loop, not only its resting appearance. Preserve useful focus, input, scroll, loading, interruption and recovery decisions as a coordinated system. Directly adopt proven behavior when compatible; test the equivalent contract when porting. Product-specific authority and real service results remain owned by the current application.''')
add('skills/ui-spec/references/verification.md', '''## Inspect inherited design value

Identify the major relationships supplied by the selected page, system or block and compare them with the actual result. Verify the chosen reuse granularity, the important adaptations, and the evidence for using that foundation. Source attribution proves origin; rendered comparisons and real tasks establish retained quality. Treat a static design port, a runtime component integration and an accepted product as different observations.

A useful review explains what mature work contributed to the overall composition and what original work solved. Check the assembled page with representative content and states, including changes that might undermine the foundation's hierarchy, proportions, reading rhythm or interaction continuity.''')
add('skills/ui-spec/references/integration.md', '''## Preserve the foundation through real integration

Carry the accepted page/block relationships and behavior into the current product rather than rebuilding their surface from memory. Keep source configuration and adaptation controls identifiable. Replace fixture boundaries with the real application's owners, preserving hierarchy, content measure, state continuity and editable design decisions. Reassess only the affected foundation choice when actual constraints materially change its fit.''')
add('skills/ui-spec/references/examples.md', '''## A page-level foundation before local component selection

For a conversational research surface, compare a suitable assistant page template with a task-dashboard template using the same primary loop and content. If the assistant page already resolves welcome composition, composer continuity, message measure and action placement, inherit those decisions together. Add the product's source inspection and research states within that language. A static cross-stack probe can port those relationships with its scope stated; a compatible production stack can retain the source components and runtime behavior directly.

For a small control change inside an accepted interface, that accepted page is already the foundation. Research at the affected component level and preserve the rest. The useful granularity follows the actual problem.''')

edit('skills/ui-spec/assets/templates/design-decisions.md', '## Reuse assessment', '''## Foundation comparison and selected granularity

Concrete mature page/system/block candidates, source/demo/revision, actual observed
states and evidence. Explain the selected level, valuable design relationships
inherited together, adaptation boundaries and meaningful alternatives. State what
is direct code reuse, configuration, composition, design transfer or original work.

## Reuse assessment''')
edit('docs/DESIGN-DECISIONS.md', '## Recognize use before fixing the shell', '''## Mature work is the default design starting point

Design theory and UI resource knowledge work together throughout the process:
product understanding → search and actual browsing → comparison → foundation and
reuse decisions → adaptation/integration → real verification. New discoveries can
refine the initial concept. Theory supplies judgment; resources supply concrete
objects for that judgment; implementation and observation test the result.

For a new surface, explore the highest appropriate reuse level: a complete page or
design system, a functional block, then the required components and effects.
Inherit coherent hierarchy, proportions, typography rhythm and interaction
relationships. Original work concentrates on product differences, integration and
gaps. For a local correction, the accepted product can already be the foundation.

## Recognize use before fixing the shell''')
add('docs/WRITING.md', '''## Write from mature design foundations

Express professional knowledge as guidance for investigating and applying concrete
work. Name the useful reuse granularity and explain which connected decisions
are inherited. Distinguish resource scope from adoption method. State how new
observations can change the choice and how adaptation preserves the valuable
relationships. Original work has a product-specific role and verification target.''')
add('docs/MODEL.md', '''## 16. 成熟成果驱动的设计工程判断

设计理论知识负责识别质量、解释机制并判断适用条件；UI 资源知识提供具体候选、
获取路径和实现方式。两者贯穿产品分析、实际搜索与浏览、专业比较、选型、适配整合、
验证和迭代。资源发现可以反过来完善初始判断。

新页面优先寻找最高适当复用层级，继承成熟页面、设计系统或功能区块中的整体关系，
再补足局部组件与特定效果。局部任务继承已确认的整体基础。复用价值来自符合当前任务的
成熟设计决策，而不是资源数量；自主创造集中用于产品差异、整体协调、定制与真实接线。''')
add('docs/PROFESSIONAL-MODEL.md', '''## 两类知识共同作用于实际选型

理论知识支持对具体成熟成果的理解、审美判断与工程取舍；资源知识让判断有可研究、
可比较、可复用的对象。以最高适当复用层级继承整体设计关系，再完成产品化适配，
使专业创造力集中在差异化需求、整体协调和体验优化。发现、比较与验证可以持续修正方案。''')
add('docs/RESOURCE-REUSE.md', '''## Start at the highest useful level

For substantial new work, begin with suitable page/application templates, design
systems and functional blocks. Compare which coherent decisions they already
resolve, then select smaller pieces for the remaining needs. Reuse granularity is
separate from delivery form: a whole-page design can be ported, and one primitive
can be installed. Match the level to the task; preserve an accepted foundation for
local changes. Record the inherited relationships and verify them in the result.''')
add('docs/REVIEW-v1.4.0.md', '''## Mature-foundation refinement

The final revision makes design theory and resource knowledge work together in
search, browsing, comparison, selection, adaptation and verification. New surfaces
seek the highest appropriate reuse level, carrying coherent page/system/block
relationships before selecting isolated details. Resource discoveries can refine
the initial concept. This changes the default decision process rather than
introducing a resource quota.

The research example now uses an identified assistant-ui page composition as its
conversational foundation, with explicit preserved relationships and scoped
adaptations. Its native fixture is a design port, not a claim of integrating the
upstream React runtime. The source revision, license, adoption boundary and actual
browser observations are retained. Product acceptance stays with the user.''')
edit('docs/RESEARCH.md','The skill text, templates and Python tools are original to this repository. Source projects are linked for methodological attribution; their scripts, images, fonts and skill bundles are not redistributed here. There is no endorsement or affiliation claim.','The skill text, record templates and Python tools are original to this repository. Methodological references are credited separately from copied implementation material. The worked example identifies its adapted source relationships and preserves the notices for Radix Colors and assistant-ui. Source access, license scope, project adoption and endorsement remain distinct facts.')
add('docs/RESEARCH.md', '''## Mature page foundation (1.4)

The assistant-ui ChatGPT example and its exact source at commit
`1fbf00dd0388fee912af95401876a6cc3c232b2c` were inspected for whole-page relationships:
welcome positioning, reading measure, shared composer, primary action, message
shape and active reading layout. The sample records design transfer and its real
fixture checks separately from upstream runtime behavior. Official shadcn blocks
provide a contrasting page/block discovery route. Candidate maturity is assessed
through the relevant evidence rather than inferred from popularity.''')
edit('README.md','**A design practice for your agent.**','**A resource-led design engineering practice for your agent.**')
edit('README.zh-CN.md','**给 Agent 一套完整的设计实践。**','**以成熟设计成果为起点的专业设计工程实践。**')
edit('README.md','## Begin with the experience people expect','''## Build on mature design work

Design theory supplies judgment; UI resources supply concrete work to study and
adapt. Start at the highest appropriate reuse level—page or design system,
functional block, component—so valuable hierarchy, proportions, typography and
interaction decisions carry into the product together. Search and actual browsing
inform the concept; comparison, adaptation and real checks keep improving it.

Original work focuses on product differences, integration and the gaps that the
chosen foundation leaves. A local improvement preserves its accepted foundation.

## Begin with the experience people expect''')
edit('README.zh-CN.md','## 先确认用户期待怎样使用产品','''## 从成熟设计成果建立起点

设计理论提供判断能力，UI 资源提供可研究、可比较、可复用的实际对象。
新页面优先寻找最高适当复用层级：完整页面或设计系统、功能区块，再到组件与具体效果。
继承有价值的层级、比例、排版节奏和交互关系，将自主创造集中用于产品差异、适配、整合与体验优化。

产品分析、实际搜索与浏览、专业比较、选型、实现和验证持续联动；新的资源发现也可以完善初始方案。
局部改进则继承已确认的整体基础，在适当范围内继续工作。

## 先确认用户期待怎样使用产品''')
edit('CHANGELOG.md','- Recognize user-level interaction models before settling page structures.','- Use mature page/system/block foundations at the highest appropriate reuse level.\n- Connect design theory and resource knowledge through actual discovery, comparison, adaptation and verification.\n- Recognize user-level interaction models before settling page structures.')
edit('docs/releases/v1.4.0.md','## Product intent and decisions','''## Product intent and decisions

- Make mature design foundations the default starting point for substantial work,
  selecting the highest appropriate reuse level and preserving coherent decisions.
- Apply theory and resource knowledge together through actual search, browsing,
  comparison, adaptation and verification.''')
# This pending file still carried its previous fixed-version assertion.
edit('tests/test_resources.py', "self.assertIn('tree/v1.3.0',text)", "self.assertIn('tree/v'+(ROOT/'VERSION').read_text().strip(),text)")

