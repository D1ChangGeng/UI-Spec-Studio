# UI Spec Studio

**以优秀的成熟成果为起点，设计真正属于当前产品的界面。**

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/studio-compact-dark.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/studio-compact-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/studio-dark.svg">
  <img src="docs/assets/studio-light.svg" alt="三个相互连接的设计判断：研究成熟成果，选择适合的设计基础，再形成可编辑、可验证的实际作品。" width="1100">
</picture>

[English](README.md) · [使用指南](docs/GUIDE.md) · [Skill 源码](skills/ui-spec/SKILL.md) · [正式版本](https://github.com/D1ChangGeng/UI-Spec-Studio/releases)

适用于**应用界面、README、文档、图表、演示文稿**等屏幕视觉作品的通用 [Agent Skill](https://agentskills.io/specification)。Agent 主动研究成熟设计成果，进行专业选型与适配整合，再验证实际效果。

## 在项目中直接开始

```bash
npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec
```

随后向编程 Agent 说明目标即可，设计方向可以由 Agent 主动研究：

```text
使用 ui-spec，理解当前项目、目标用户和主要使用场景。
主动寻找成熟的设计参考与实现，选择最适合的设计基础，
完成第一份可审阅的 SPEC，并展示实际结果和关键选型依据。
```

审阅通过后，只需说 **「本轮通过，继续」**，Agent 就会推进下一项有价值的工作；使用 **「ui-spec: finish」**，则会将已确认的设计接入真实内容、功能或作品的发布环境。[安装与宿主选项](docs/INSTALL.md) · [多轮使用指南](docs/GUIDE.md)

## 视觉素材与界面共同设计

品牌符号、图标、字体与字形、插画、图片、空间化图形和动态资产共同形成产品表达。
Agent 研究成熟素材、判断制作路径、维护可编辑母版与交付变体，并在实际界面中检查视觉、加载与降级状态。
素材也可以反向决定构图与排版。[资产工程方法](docs/VISUAL-ASSETS.md) · [浏览器验收样例](examples/asset-review/README.md)

## 从有依据的设计起点开始

**理解任务 → 实际搜索与浏览 → 专业比较和选择 → 适配整合 → 观察验证。**

设计理论帮助 Agent 判断一种设计*为什么有效*；成熟 UI 生态提供值得研究、比较和复用的*实际成果*。两类知识共同参与每一轮判断。新的资源发现可以完善最初的设计方向，最终渲染则用来检查方案是否真正适合当前任务。

复用以**最高适当层级**为原则：从整页设计、设计系统与功能区块，到组件体系和局部视觉技法，选择最能解决当前问题的成熟基础。重点是继承其中相互协调的信息层级、空间比例、排版节奏、交互和状态设计，再根据产品定位完成适配。自主设计集中用于产品差异化、整体整合与必要的独特需求。

[资源发现与复用方法](skills/ui-spec/references/component-sourcing.md) · [37 项带来源记录的资源线索](skills/ui-spec/references/resource-catalog.md) · [设计决策记录](docs/DESIGN-DECISIONS.md) · [资源复用指南](docs/RESOURCE-REUSE.md)

## 文字内容也是完整的 UI 设计对象

Agent 需要判断**用户应该理解什么、信息由哪里承担、怎样自然表达，以及文字如何在页面中呈现**。内容设计与 UX Writing 将真实产品信息、用户熟悉的术语、操作文案、动态反馈、本地化和字体排版与页面结构、视觉素材一同设计。文字变化可以推动布局调整，实际渲染也可以反过来优化内容。

[内容设计指南](docs/CONTENT-DESIGN.md) · [双语可运行示例](examples/content-review/README.md)

## 一套方法，适用于不同视觉媒介

通用原则提供专业判断；**具体媒介决定表现形式与最终验收方式**。

| 设计对象 | 用户首先需要完成的事 | SPEC 应当确认的结果 |
|---|---|---|
| **产品界面** | 发起、完成并继续一项任务 | 真实的交互状态、稳定布局、操作路径与业务结果 |
| **README 与文档** | 理解工具、复制命令、找到下一步说明 | 阅读顺序、原生文字与链接、宿主渲染、主题图片和窄屏表现 |
| **图解与数据表达** | 追踪关系、解读数据或比较方案 | 正确的关系语义、可读标注、数据映射与可访问的替代表达 |
| **演示文稿与视觉媒体** | 随空间和时间顺序理解内容 | 清晰的注意力节奏、可编辑素材及实际展示/播放条件下的验证 |

[专业能力模型](docs/PROFESSIONAL-MODEL.md)与[条件明确的设计技法](skills/ui-spec/references/patterns.md)进一步连接排版、构图、色彩、素材、交互与时间表达。

## 这份 README 本身就是一份 UI SPEC

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

每轮由 Agent 选择有价值、便于审阅的范围，完成实现与实际检查。确认后的设计可以进入真实产品接线，也可以完成文档、图表或演示内容本身的发布。既有决策持续继承，来源证据、渲染观察与用户批准分别记录。

进入实质工作前，Agent 会**完整读取八份通用参考**：[工作流](skills/ui-spec/references/workflow.md)、[分析视角](skills/ui-spec/references/analysis.md)、[视觉原则](skills/ui-spec/references/principles.md)、[资源发现](skills/ui-spec/references/component-sourcing.md)、[交互与变体](skills/ui-spec/references/interaction-and-variants.md)、[验证方法](skills/ui-spec/references/verification.md)、[视觉素材与资产工程](skills/ui-spec/references/visual-assets.md)、[内容设计与 UX Writing](skills/ui-spec/references/content-design.md)。真实业务接线另需[集成参考](skills/ui-spec/references/integration.md)。Skill 负责专业方法与读取契约，宿主负责工具、执行和上下文管理。

## 安装、验证与维护

```bash
# 将 Skill 安装到当前项目的 Codex
npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec -a codex

# 固定正式发布版本
npx skills add https://github.com/D1ChangGeng/UI-Spec-Studio/tree/v1.6.0 --skill ui-spec
```

安装检查也覆盖 Claude Code 和 OpenCode。核心参考以 Markdown 提供；可选记录工具使用 Python 3.10+ 标准库。[离线安装与更新](docs/INSTALL.md)。

工程检查覆盖文件引用、辅助工具、安装路径及可复现打包；发布检查覆盖双语 README、响应式图片和实际页面渲染。具体产品的设计品质与业务接线效果由该项目的实际验证决定。[验证与保证范围](docs/EVALUATION.md) · [CI](https://github.com/D1ChangGeng/UI-Spec-Studio/actions/workflows/validate.yml) · [版本记录](CHANGELOG.md)

<details>
<summary><strong>维护者资料与本地检查</strong></summary>

[完整理解模型](docs/MODEL.md) · [写作标准](docs/WRITING.md) · [研究来源](docs/RESEARCH.md) · [README 设计记录](docs/design/README-SPEC.md) · [发布流程](docs/PUBLISHING.md) · [贡献指南](CONTRIBUTING.md) · [安全说明](SECURITY.md)

```bash
python tools/validate_package.py
python tools/readme_art.py --check
python tools/catalog_docs.py --check
python -m unittest discover -s tests -v
python tools/package.py
```

</details>

[MIT 许可证](LICENSE) · [设计与研究来源说明](skills/ui-spec/references/sources.md)
