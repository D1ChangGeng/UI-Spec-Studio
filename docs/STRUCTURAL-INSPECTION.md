# 结构观察、专业判断与持续演进

## 四类职责分别提供什么

**设计证据地图维护当前认识；结构覆盖检查器描述记录事实；Agent 判断意义并执行；独立验证检查真实结果。**

| 机制 | 能提供什么 | 不能由它代替什么 |
|---|---|---|
| Design Evidence Map（设计证据地图） | 体验、对象、依据、选择、采用、条件与历史的关联 | 真实产品本身或已执行工作 |
| Structural Coverage Inspector（结构覆盖检查器） | 可读性、字段、ID、引用、文件元数据、声明关系与类别提示 | 研究充分性、专业正确性、动作裁定、整体完成 |
| Agent Design Judgment & Execution（专业判断与执行） | 根据任务、设计知识、实际证据决定研究、比较、试装、实现或修订 | 未实际执行的观察、测量和授权 |
| Verification & Acceptance（验证与验收） | 特定条件下的视觉观察、连续操作、工程断言与用户决定 | 超出检查对象与条件的普遍结论 |

**The structural inspector reports what is represented, not what is professionally sufficient, correct, ready, or complete.**

结构检查器可以指出一个引用未解析，不能据此判断设计必然缺少某项能力；可以呈现已有的高影响问题和行动声明，不能决定 Agent 是否可实施。它也不以两个候选名称证明比较有价值。

## 以 v1.14.0 为基准的职责修订

v1.14.0 已有只读和证据边界说明，但代码仍将“至少两个不同候选名称”“当前版本下观察到匹配种类的证据”“高影响缺口与 expand/finish 的组合”转成失败条件。Manifest 还将部分豁免并入 satisfied，并按 review/finish 模式增加完整性门槛。

1.15 将这些机械专业裁定移出检查器。原则继续完整保留在已安装的 `evidence-actions.md`、`evidence-map.md` 和 `verification.md` 中，由 Agent 结合具体任务运用。安全路径、JSON 解析、唯一 ID、声明引用、对象关系和只读性继续检查。独立摘要检查通过新的 `check_file_integrity.py` 执行，不再混进设计记录的结构结果。

## 两种缺失不能混为一谈

**声明内缺失**：某条记录引用了不存在的 ID，或明确列出的检查目标尚无对应记录。检查器可以直接描述这个事实。已有工作也可能记录在其他文件，仍需 Agent 核实。

**理论候选缺失**：专业覆盖词汇包含某类别，但当前对象没有相应显式标签。检查器报告 `candidate_unrepresented_categories`，明确适用性未判断。它不分析散文语义，也不把标签缺失等同于真实设计遗漏。

词汇覆盖产品目标、旅程、架构、组件、内容排版、构图、素材、状态反馈、时序、响应式、可访问性、恢复、性能、复用、实现验证和运营内容。它们提供分析入口，不是所有项目都必须填写的字段。一份纯阅读工具记录不需要为了清空提示而编造表单。

**Agent 决定纳入、排除、合并、拆分或继续研究。** 新的真实产品证据仍应挑战初始范围，理论词汇也不宣称穷尽未知设计空间。

## 输出与退出码

| 观察 | 新输出 | 边界 |
|---|---|---|
| 文件是否成功读取 | `record_readability: readable / unreadable` | readable 不意味着结构正确或设计完成 |
| 字段形态与引用问题 | `structural_findings`、`field_observations` | 指向具体位置，不生成设计命令 |
| 已声明的检查 | `declared_check_records` | pass/fail 是记录作者的声明，不是本工具执行结果 |
| 豁免和例外 | `declared_exception_records`，Manifest 另列 waived checks | 不与真实检查成功合并 |
| 显式目标没有记录 | `unlisted_declared_items` | 不宣布项目范围完整或任务必须停止 |
| 理论类别无显式标签 | `candidate_unrepresented_categories` | 适用性由 Agent 判断 |
| 某变化的已声明关联 | `declared_relation_review_candidates` | 不表示缺陷或强制复验；未列出的影响也可能存在 |
| 下一步 | `declared_actions` | 仅回显 Agent 已写内容，不生成或裁定行动 |

结构工具退出码 **0 表示检查操作运行完成，即使有结构问题**；2 表示调用或读取失败。不再用退出码 1 表示研究不足、覆盖不全或阶段未就绪。多个具体观察取代总括 `ok` 或 `satisfied`。

这不是放松真实工程测试。独立摘要工具的 0/1 仍表示指定字节摘要匹配/不匹配，浏览器和工程测试仍可判定它们明确执行的断言。检查对象、条件和结果必须同时保留，不能扩大为整体审美或产品认证。

## 查询模式与兼容性

推荐 Manifest 查询：

```bash
python <skill-dir>/scripts/check_manifest.py --project-root <project> --view overview --json
python <skill-dir>/scripts/check_manifest.py --project-root <project> --view checks --json
python <skill-dir>/scripts/check_manifest.py --project-root <project> --view connections --json
```

旧 `--mode draft / review / finish` 仍可调用，分别映射到以上三个视图，但只是显示别名，没有额外完成门槛。`phase` 字段记录 Agent 当前意图，不是检查器授予的状态。

`ui-spec-evidence/1` 和 Manifest `schema_version: 1` 输入仍支持读取。**报告结构有意变更**：依赖旧 `ok`、`errors`、`coverage.satisfied` 或 `pending_coverage` 的集成必须改读具体观察，不应寻找另一个总括成功布尔值。Python `validate()` 名称作为兼容入口保留，但返回同一中性报告。

Manifest 把显式 requirements 与由已声明页面、视口、变体投影出的 inventory combinations 分开。后者是可审视的组合，不是工具替项目新增的强制需求。已有 planned、failed 或 blocked 记录也能匹配一个地址，但不因此成为通过项。

## v1.17 的可选正式增量声明

`ui-spec-evidence/1` 保持兼容。已有 Markdown、项目记录与旧 JSON 可以继续使用；需要结构化呈现时，可以在同一当前模型中增加以下声明：

| 可选内容 | 记录关系 |
|---|---|
| `product_context` | `overall_goal` 与 `current_ui` 分别描述完整产品目标和当前实现基础 |
| `candidate_specs` | 带 `id` 的候选增量；用于可修订规划，记录存在不代表正式开始 |
| `formal_specs` | 带 `id` 的正式增量；叙述其 `purpose`、`quality_goals` 等实际责任 |
| SPEC 内的对象引用 | `objects`、`research_objects`、`implementation_objects`、`regression_objects` 引用已有设计对象；三种范围可以不同 |
| SPEC 内的决策引用 | `decisions` 连接已有选择、实际证据、采用位置与开放问题 |
| 增量之间的关联 | `related_specs` 连接候选或正式 SPEC，关系声明不自动产生顺序或依赖结论 |

多个 SPEC 可以作用于同一页面或共享系统，一项 SPEC 也可以关联多个 L0–L5 对象与横向关系。对象树与正式工作范围分别表达。新的搜索、试装和修复通常仍是现有 SPEC 的内部工作，不要求逐次建立正式记录。

检查器呈现已给字段、声明记录和引用解析结果，候选与正式记录分列；三个视图使用同一当前信息。字段可读或引用可解析不证明范围合理、研究充分、实际采用或视觉成熟。缺少可选字段不构成填写配额；工具不拆分任务、不选择下一步，也不增加 SPEC 状态迁移或完成门槛。

范围变化由 Agent 根据新证据判断。当前模型保留完整目标和正在承担的责任，重要修订说明变化原因及影响，原有未解决问题继续通过决策与证据追溯。把问题关联到后续 SPEC 不等于已经解决；实际成果需要当前增量品质和关联产品体验两项验证。具体可选表达见[记录说明](../skills/ui-spec/references/evidence-records.md)。

## 当前模型、重要修订、原始证据

当前有效模型首先回答：现在追求什么体验、采用什么资源、哪些条件已有依据、有什么未解决问题。重要修订回答：什么认识变了、为什么、影响什么、现在采用什么判断。原始证据档案保存截图、录屏、源代码身份、运行记录和历史设计，不必常驻当前工作上下文。

可选 JSON 的根 objects/decisions 表示当前模型，`revisions` 存简要变化，`archive` 链接历史或原始材料；普通 Markdown 与 Git 可以承担同样职责。检查器不自动迁移、重写或冻结这些状态，也不把档案载入成另一套当前选择。

例如，输入区单行状态曾被实际观察，新增多附件后出现换行问题：保留单行检查的历史事实，更新当前条件和问题，记录修订原因，按实际影响决定新观察。仅修改无关后台代码，不要求所有页面重测；字体变化则可能影响多个共享区域。

两条主线持续相互修订：**体验理解—研究—判断**确定目标，**资源发现—试装—实现—验证**检验实现。任何新证据都可重开相关决定，过去批准和测试分别保留来源与范围。

## 初始化与资源查询

`prepare.py` 只创建未确认模板，保留已有文件。它不再默认添加桌面视口、英文或浅色主题；找到 DESIGN.md 只说明文件存在，不说明内容已读或用户已批准。项目名称的参数/目录来源被明确标记。

`find_resources.py` 按本地目录和过滤条件返回带日期的来源条目。无匹配是目录查询事实，不是“继续搜索”的工具指令。目录自身的采用说明属于来源材料；实际资源适用性、访问、采用和下一步仍由 Agent 决定。

## 三类验证分别作结论

边界回归检查工具是否只做结构观察；真实 Agent 任务检查结构提示如何被解释、行动是否仍由专业判断产生；真实 UI 评审检查产物的视觉、交互与工程品质。结构测试通过、源代码完整、发布成功和模型能力提升属于不同结论。

v1.15.0 的实际命令、逐项回归、维护者自应用与当时尚未执行的独立实验范围在[历史版本评审](REVIEW-v1.15.0.md)中分别记录。v1.17.0 的修订与验证范围见[当前版本评审](REVIEW-v1.17.0.md)，实际 Agent 对照记录见[本轮实验](experiments/adaptive-granularity/RESULTS.md)。旧实验输入和历史证据不会被改名成新版本实验结果。
