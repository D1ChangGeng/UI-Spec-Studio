# UI Spec Studio

**以优秀的成熟成果为起点，设计真正属于当前产品的界面。**

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/studio-compact-dark.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/studio-compact-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/studio-dark.svg">
  <img src="docs/assets/studio-light.svg" alt="三个相互连接的设计判断：研究成熟成果，选择适合的设计基础，再形成可编辑、可验证的实际作品。" width="1100">
</picture>

[English](README.md) · [使用指南](docs/GUIDE.md) · [Skill 源码](skills/ui-spec/SKILL.md) · [正式版本](https://github.com/D1ChangGeng/UI-Spec-Studio/releases)

适用于**应用界面、README、文档、图表、演示文稿**等屏幕视觉作品的通用 [Agent Skill](https://agentskills.io/specification)。理解用户期待的体验，深入研究真实证据，比较并采用成熟成果，在实际使用中检验品质。

## 在项目中直接开始

```bash
npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec
```

随后向编程 Agent 说明目标即可，设计方向可以由 Agent 主动研究：

```text
使用 ui-spec，理解当前项目、目标用户及其期待的体验。
研究重要问题，比较成熟设计参照与可采用的实现，
完成第一份可审阅的 SPEC，展示实际结果和关键证据。
```

审阅通过后，只需说 **「本轮通过，继续」**，Agent 就会沿已确认的方向推进下一项有价值的工作；使用 **「ui-spec: finish」**，则会将已确认的设计接入真实内容、功能或作品的发布环境。[安装与宿主选项](docs/INSTALL.md) · [多轮使用指南](docs/GUIDE.md)

## 成熟成果承接视觉品质，原创遵守明确边界

**正常实现路径中默认禁止从零自建 UI。** Agent 主动发现外部成熟实现，同时评估项目中已验证的可复用成果，把它们的设计关系带入实际产品。业务接线、配置和必要适配继续正常进行；一个成熟区块或 Token 体系可以承接多个可见元素，无须逐元素重复搜索。

原创只允许用于实际获授权的 **W1 专属身份与艺术资产、W2 成熟资源确实无法承接的特殊产品表达、W3 必要局部专用扩展**。参考截图、搜索失败、元素简单或技术熟悉均不自动提供权限。已明确授予的范围直接使用；未解决的视觉责任保持可见，同时继续独立工作。

资源获取、实际采用和成熟设计品质保留分别验证。原始 Demo、当前项目试装与最终整合 UI 共同说明：哪些品质真实保留，整体是否协调，哪些差距仍需解决。

[实施边界与示例](docs/ORIGINAL-CONSTRUCTION.md) · [v1.19 版本评审](docs/REVIEW-v1.19.0.md) · [真实比较实验](docs/experiments/default-deny/RESULTS.md)

## 让每项设计增量充分兑现品质

**正式 UI SPEC** 是持续演进产品中的一项内聚设计增量，拥有明确的体验目标和可实际审阅的成果。完整产品目标持续保留；单次范围则根据重要品质所需的研究、实现与验证深度确定。

- 常规设置页面已有成熟设计系统承接相关关系时，可以作为一个 SPEC。
- 输入区增长、流式回答与阅读位置控制共同形成连续体验时，可以纳入同一个 SPEC。
- 共享字体体系调整可以跨越多个页面，同时检查文字换行与视觉层级。

Agent 在 `init` 中说明可修订的候选规划，再根据实际证据保持、拆分、合并或重新划定范围。每项增量作用于当前产品；服务于原目标的研究、候选替换和修复继续归属原 SPEC，范围调整后仍保留未解决的品质问题。

你会看到实际成果、重要设计选择、真正采用的资源与已观察的差距。首个增量应建立值得继承的代表性体验；后续工作可以新增、替换、简化，也可以重新判断已有设计。

[多轮使用方式](docs/GUIDE.md) · [v1.17 版本评审](docs/REVIEW-v1.17.0.md) · [实验记录](docs/experiments/adaptive-granularity/RESULTS.md)

## 直接看见设计如何形成

重要设计事件会随实际工作自然呈现：影响方向的研究发现或资源选择、首次有意义的局部成果、重大品质差距，以及正式增量的交付。Agent 展示具体对象与证据，说明已形成的判断，并继续完成已授权的工作。

资源原始演示、项目试装与整合后的产品各自保留真实身份。早期预览让已经形成的品质和仍需修正的关系及时可见；同一份当前设计认识支持对话与后续工作，常规搜索和修改由 Agent 自主推进。

[可观察的设计执行](docs/OBSERVABLE-EXECUTION.md) · [v1.18 版本评审](docs/REVIEW-v1.18.0.md)

## 先理解体验，再选择设计

「像某个产品」可能指熟悉的工作方式、信息组织、视觉气质或交互细节。Agent 先形成可修正的理解，分别研究当前用户的明确意图、相关用户经验与参考产品的真实表现。

研究围绕**任务、页面、状态及其关系**展开。产品资料与用户材料解释含义，真实界面揭示视觉品质，实际操作与连续画面呈现时间体验。参考版本、平台和使用条件由目标体验决定，新的发现可以改变产品模型、搜索方向或资源选择。

[体验研究与证据规划](docs/EXPERIENCE-RESEARCH.md) · [产品对齐方法](docs/PRODUCT-ALIGNMENT.md)

## 视觉素材与界面共同设计

品牌符号、图标、字体与字形、插画、图片、空间化图形和动态资产共同形成产品表达。
Agent 研究成熟素材、判断制作路径、维护可编辑母版与交付变体，并在实际界面中检查视觉、加载与降级状态。
素材也可以反向决定构图与排版。[资产工程方法](docs/VISUAL-ASSETS.md) · [浏览器验收样例](examples/asset-review/README.md)

## 让成熟实现承接产品品质

**品质目标 → 成熟实现 → 局部试装 → 针对性适配 → 完整体验验证。**

**Product UI Experience Alignment**（产品 UI 体验对齐）以符合当前用户、任务、内容和运行条件的设计成熟度为目标。指定产品提供探索入口，开放需求由 Agent 主动建立参照。研究提炼构图、排版、组件细节、状态反馈与连续交互中值得继承的关系，再形成当前产品自己的表达。

**成熟实现是全部可见 UI 的正常基础。** 参照研究与资源选型持续配对，从整页、设计系统、布局、区块、组件、素材或动效中选择适当范围。重要候选先查看原始演示，再用项目的真实内容、字体、主题与状态局部试装，通过后扩大集成。配置、组合、接线和必要适配保留使其值得采用的关系；原创必须属于具有实际授权的封闭例外。

整合后的界面与连续任务再次接受审阅。采用记录说明实际由哪个实现承担目标品质、进行了哪些改动、验证到什么程度，并区分研究来源与最终采用。[产品对齐与主动探索](docs/PRODUCT-ALIGNMENT.md) · [资源复用指南](docs/RESOURCE-REUSE.md)

[37 项带来源记录的资源线索](skills/ui-spec/references/resource-catalog.md) · [设计决策记录](docs/DESIGN-DECISIONS.md)

## 复用视觉工艺，不止基础功能

功能组件库可以提供可靠操作，但不自动决定页面的排版、材质与动态品质。根据当前任务，研究适当范围的成熟页面、功能区块、视觉组件和素材；将**实际观察到的视觉完成度**与其功能覆盖范围分别判断。

用专业知识发现和比较更好的资源，再通过配置、组合与针对性适配保留其设计价值。外部真实 Demo 承担主要正向实例职责；知名库只是开放入口，不是封闭名单或品质保证。专业软件同样可以在真实工作区中形成鲜明的艺术表达。

[职责与复用范围检索、三类限定应用验证](docs/REVIEW-v1.16.1.md)

[成熟视觉工艺复用](docs/VISUAL-CRAFT-REUSE.md) · [Finesse 研究与吸收边界](docs/FINESSE-ADAPTATION.md) · [限定范围的应用证据](docs/REVIEW-v1.16.0.md)

## 让熟悉的任务拥有独立的视觉语言

**Art Direction**（艺术指导）围绕产品气质协调题材、字形、构图、材质与动态表达。专业工具同样可以拥有鲜明艺术性。明确提出的审美目标与任务清晰、状态准确、使用可靠共同构成交付要求。

**Expressive Contrast**（表达性反差）同时研究功能体验、跨领域表达与实际实现资源，通过完成度相称的预览比较实质方向，再将选择转为按角色组织的视觉系统。成熟资源与针对性素材制作，让视觉语言进入填入内容后的输入、导航、结果与连续工作。

**体验成立性**与**表达完成度**分别审阅。源设计保真保护已采用或确认的细节，感知评估判断真实呈现；作者时间轴支持可重复的画面比较，真实产品另需实际操作与运行证据。[艺术指导与表达性设计](docs/ART-DIRECTION.md)

## 让设计决策在不同尺度之间有据可循

**多尺度设计证据地图**连接产品目标、用户旅程、页面、功能区域、感知细节和实际实现。研究范围由用户任务与真实参照共同校验；证据、资源采用、验证条件与用户确认分别保留实际含义。

Agent 根据实际证据判断下一步研究、比较、试装或实现。同一份记录支持**整体总览、局部深查和执行验证**。已有 Markdown 记录即可使用。

结构检查器只描述记录表达了什么，不裁定适用性、研究充分性或任务完成。声明结果、例外与未记录项分别呈现；当前判断链接重要修订和原始证据，避免旧结论混入当前模型。

[职责边界与升级说明](docs/STRUCTURAL-INSPECTION.md) · [方法与示例](docs/DESIGN-EVIDENCE.md) · [三组对比实验方案](docs/experiments/design-evidence/PROTOCOL.md)

## 持续探索，让重要选择有据可依

**证据驱动探索**连接研究问题、搜索、实际观察、候选比较与下一项问题。投入由设计影响、不确定性和潜在改进价值决定。一个决定产品气质的字体、背景或交互可以获得跨大量独立来源的持续研究；已有可靠依据的常规组件可以较快进入验证。

比较具有实质差异的候选，主动寻找可能改变初始选择的方案。沿着新线索播放、滚动、切换状态、研究实现并局部试装。访问不完整时继续寻找合理的替代证据，必要时请求具体取材协助。实际观察、资料描述、专业判断与剩余缺口分别保留依据。

**Human-centered Visual Inspection & Perceptual Design Analysis**（面向人类视觉感知的观察与设计分析）将真实观看转为专业判断。从正常尺度下的整体印象与注意力层级开始，深入构图、功能区域及重要组件或素材细节，再回到完整界面。按问题选择排版、光学平衡、色彩、材质和动效等维度，理解品质如何形成，并据此选择能够承接这些关系的成熟实现。

观察覆盖**单个画面、连续变化与完整使用旅程**。时序视觉观察跟随触发、首次反馈、过渡与稳定结果；先以正常速度理解体验，再通过有价值的细节观察与重放分析原因，最后回到完整过程判断。行为与设计影响决定观察深度。

从覆盖、细节、时间、相关性和可靠性判断证据。可能改变选择的缺口继续研究；已有依据的方向进入试装；关键适配成立后扩大实现。搜索次数和用时描述投入，证据实际回答了什么决定下一步。

[研究方法](docs/EXPERIENCE-RESEARCH.md) · [视觉观察](docs/VISUAL-INSPECTION.md) · [时序样例](examples/temporal-review/README.md)

## 文字内容也是完整的 UI 设计对象

Agent 需要判断**用户应该理解什么、信息由哪里承担、怎样自然表达，以及文字如何在页面中呈现**。内容设计与 UX Writing 将真实产品信息、用户熟悉的术语、操作文案、动态反馈、本地化和字体排版与页面结构、视觉素材一同设计。文字变化可以推动布局调整，实际渲染也可以反过来优化内容。

[内容设计指南](docs/CONTENT-DESIGN.md) · [双语可运行示例](examples/content-review/README.md)

## 面向真实使用与持续运营设计

产品模型、视觉素材、内容、布局、组件状态和动效共同服务于**流畅的操作与可持续维护的内容**。Agent 从连续操作追踪输入、可用结果和权威完成，根据实际收益与有效性选择提前准备、并发和缓存；保持对象变化与滚动的位置连续性，再围绕真实维护任务设计共享内容、单项覆盖和批量恢复。

[完整体验模型](docs/EXPERIENCE-QUALITY.md) · [运行与运营接线](skills/ui-spec/references/integration.md) · [验证方法](skills/ui-spec/references/verification.md)

## 一套方法，适用于不同视觉媒介

通用原则提供专业判断；**具体媒介决定表现形式与最终验收方式**。

| 设计对象 | 用户首先需要完成的事 | SPEC 应当确认的结果 |
|---|---|---|
| **产品界面** | 发起、完成并继续一项任务 | 真实的交互状态、稳定布局、操作路径与业务结果 |
| **README 与文档** | 理解工具、复制命令、找到下一步说明 | 阅读顺序、原生文字与链接、宿主渲染、主题图片和窄屏表现 |
| **图解与数据表达** | 追踪关系、解读数据或比较方案 | 正确的关系语义、可读标注、数据映射与可访问的替代表达 |
| **演示文稿与视觉媒体** | 随空间和时间顺序理解内容 | 清晰的注意力节奏、可编辑素材及实际展示/播放条件下的验证 |

[专业能力模型](docs/PROFESSIONAL-MODEL.md)与[条件明确的设计技法](skills/ui-spec/references/patterns.md)进一步连接排版、构图、色彩、素材、交互与时间表达。

## 这份 README 也通过 UI SPEC 持续演进

仓库首页首先是一种**阅读与发布界面**。新读者需要快速理解 Skill 的作用、判断是否符合自己的任务，然后完成第一次使用。视觉表达服务于这条阅读路径，核心信息依然由 GitHub 原生 Markdown 承载。

本次复用侧重**信息组织和发布媒介的成熟设计关系**。完整的候选比较与采用范围保存在 [README 设计说明](docs/design/README-SPEC.md)：

- **[Vercel Skills CLI](https://github.com/vercel-labs/skills/blob/main/README.md) — 先让读者开始行动。** 借鉴其清晰的产品用途、快速安装与深入文档路径，将首次命令和 Agent 指令前置。
- **[Typst](https://github.com/typst/typst/blob/main/README.md) — 用视觉例子解释方法。** 通过可编辑插图说明「研究 → 选择 → 实现」，同时以原生正文保留完整说明。
- **[GitHub Markdown 规范](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github) — 充分利用宿主能力。** 标题、链接和代码块使用原生结构，插图分别适配明暗主题及宽窄视口。
- **原有 UI Spec Studio 视觉体系 — 延续统一的设计语言。** 保留克制的主题色与编辑式排版，将表达重点调整为成熟成果驱动的设计过程。

这里继承的是成熟的设计方法，插图与 Markdown 内容由本仓库维护。[设计记录](docs/design/README-SPEC.md)同时说明实现位置、渲染核查与证据边界。

另有一份[研究产品设计案例](examples/product-intent/README.md)，展示应用 UI 中的整页设计迁移，并保留[采用来源与继承关系](examples/product-intent/FOUNDATION.md)。

## 从设计推进到真实结果

主线是 `init → iterate → finish`。可选 **shape** 用于收敛重要设计方向，**audit** 可在任何阶段检查质量与覆盖范围。这些是工作意图，使用自然语言即可启动。

每项正式 SPEC 由 Agent 选择体验内聚、便于审阅的范围，完成实现与实际检查；内部研究和修复可以持续多个执行轮次。确认后的设计可以进入真实产品接线，也可以完成文档、图表或演示内容本身的发布。仍然适用的既有决策持续继承，当前增量与受影响的产品关系分别检验，来源证据、渲染观察与用户批准分别记录。

进入实质工作前，Agent 会**完整读取八份通用参考**：[工作流](skills/ui-spec/references/workflow.md)、[分析视角](skills/ui-spec/references/analysis.md)、[视觉原则](skills/ui-spec/references/principles.md)、[资源发现](skills/ui-spec/references/component-sourcing.md)、[交互与变体](skills/ui-spec/references/interaction-and-variants.md)、[验证方法](skills/ui-spec/references/verification.md)、[视觉素材与资产工程](skills/ui-spec/references/visual-assets.md)、[内容设计与 UX Writing](skills/ui-spec/references/content-design.md)。真实业务接线另需[集成参考](skills/ui-spec/references/integration.md)。Skill 负责专业方法与读取契约，宿主负责工具、执行和上下文管理。

## 安装、验证与维护

```bash
# 将 Skill 安装到当前项目的 Codex
npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec -a codex

# 固定正式发布版本
npx skills add https://github.com/D1ChangGeng/UI-Spec-Studio/tree/v1.19.0 --skill ui-spec
```

安装检查也覆盖 Claude Code 和 OpenCode。核心参考以 Markdown 提供；可选记录工具使用 Python 3.10+ 标准库。[离线安装与更新](docs/INSTALL.md)。

工程检查覆盖文件引用、辅助工具、安装路径及可复现打包；发布检查覆盖双语 README、响应式图片和实际页面渲染。具体产品的设计品质与业务接线效果由该项目的实际验证决定。[验证与保证范围](docs/EVALUATION.md) · [CI](https://github.com/D1ChangGeng/UI-Spec-Studio/actions/workflows/validate.yml) · [版本记录](CHANGELOG.md)

<details>
<summary><strong>维护者资料与本地检查</strong></summary>

[跨版本内容保真审查](docs/REVIEW-v1.13.0.md) · [长期维护原则](docs/CONTENT-INTEGRITY.md) · [完整理解模型](docs/MODEL.md) · [写作标准](docs/WRITING.md) · [研究来源](docs/RESEARCH.md) · [README 设计记录](docs/design/README-SPEC.md) · [发布流程](docs/PUBLISHING.md) · [贡献指南](CONTRIBUTING.md) · [安全说明](SECURITY.md)

```bash
python tools/validate_package.py
python tools/readme_art.py --check
python tools/catalog_docs.py --check
python -m unittest discover -s tests -v
python tools/package.py
```

</details>

[MIT 许可证](LICENSE) · [设计与研究来源说明](skills/ui-spec/references/sources.md)
