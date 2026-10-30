# L6 修复副本的独立定向延续复核

## 结论

**原先“翻面早期按 Shift+Tab 会进入不可见背面正文”的问题，在旧 L6 的两个指定尺寸均重新出现，在修复副本 T2-k2 的相同操作中均未出现。** 新副本此时让背面保持 `aria-hidden=true`、`inert=true`，键盘焦点落在仍然可见的主题按钮上，截图可见焦点轮廓。

反方向操作也得到合理结果：从可见背面开始转回正面，背面仍朝向读者时可以用 Shift+Tab 进入正文；背面转离后，焦点移到翻面按钮，未留在不可见正文。越中点反转与减少动态效果检查没有出现新的明显焦点问题。

这一结论只关闭本次复现的具体交互差距。没有重跑保存、存储失败、长文或完整语言/主题套件，也不据此宣称全部产品行为均已重新验收。原始三组比较报告保持原样。

## 对象、操作与证据边界

- 旧版：`observable-product-review/T2/L6/app`，本轮由只读 HTTP 服务 8671 提供。
- 修复副本：`observable-continuation/T2-k2/app`，使用提供的服务 8493。
- 条件：1440×900 与 390×844、设备像素比 1、英文浅色、环境指定的 Chromium headless shell。
- 输入：真实鼠标点击及 Playwright 键盘 Space、Shift+Tab。反方向检查先将翻面按钮设为操作起点，然后使用真实键盘激活；没有用脚本直接改变应用的卡片面或 aria/inert 状态。
- 观测：旋转矩阵、实际 activeElement、两面的 aria/inert、真实视口截图。每段记录器都撤销旧监听器，原始 click 时间没有重复注册问题。

此次未阅读参与者的断言清单或作者说明，也未读取修复代码作语义分析。应用文件与旧比较报告的前后 SHA-256 完全相同，记录在原始测量中；本轮未修改这些文件。

**自然速度观看能力仍不可用。** 截图与动画帧轨迹只能支持所记录时刻的状态，不支持对主观流畅度、惯性或完整动效品质作推断。本文也不包含屏幕阅读器实测。

## 1. 原问题：两个尺寸的同操作对照

从正面开始，点击翻面，等待 45ms 后按 Shift+Tab，然后读取状态并截图。由于真实输入、调度与读取有开销，表中状态实际在 click 后约 57–61ms 取得。

这里 `m11` 接近 +1 表示卡片仍几乎正面朝向读者；截图中也确实仍显示问题与方格插图。

| 版本与尺寸 | 采样 m11 | 背面 aria-hidden / inert | 实际焦点 | 观察 |
|---|---:|---|---|---|
| 旧版，1440×900 | +0.999334 | false / false | preview-note | 进入仍不可见的背面正文 |
| 修复副本，1440×900 | +0.999335 | true / true | theme-toggle | 主题按钮有可见焦点轮廓 |
| 旧版，390×844 | +0.999881 | false / false | preview-note | 同样进入不可见正文 |
| 修复副本，390×844 | +0.999331 | true / true | theme-toggle | 同样保持可见焦点 |

截图为紧邻测量时刻取得的真实渲染，采集本身还会经过若干帧；不能把旧、新两张截图当成严格相同角度的冻结画面。

| 尺寸 | 旧版截图 | 修复副本截图 |
|---|---|---|
| 1440×900 | [旧版早期 Shift+Tab](captures/original-desktop-early-shifttab.png) | [新副本早期 Shift+Tab](captures/fixed-desktop-early-shifttab.png) |
| 390×844 | [旧版早期 Shift+Tab](captures/original-mobile-early-shifttab.png) | [新副本早期 Shift+Tab](captures/fixed-mobile-early-shifttab.png) |

## 2. 正在离开的可见背面：焦点转移

先让背面停稳。以翻面按钮为键盘起点按 Space，启动返回正面的动作；45ms 后按 Shift+Tab，随后持续记录焦点。

修复副本在两个尺寸下，早期矩阵都接近 −1，背面仍可见且可访问；Shift+Tab 进入正文，并出现正文焦点轮廓。继续转动后，焦点移至翻面按钮，同时背面变为 inert / aria-hidden。桌面首次记录到这次移交约在激活后 271ms，手机约 282ms。最终正面停稳、焦点保持在翻面按钮。此次轨迹没有记录到正文已经明显转到背后而焦点仍留在正文的窗口。

旧版在同一反方向操作中会立即关闭仍可见的背面；Shift+Tab 因此回到主题按钮。这进一步支持原问题属于目标状态与当前可见面的时机差异。

关键截图：[新副本桌面，背面仍可见时的正文焦点](captures/fixed-desktop-back-leaving-focus.png)；[背面离开后，焦点移至翻面按钮](captures/fixed-desktop-handoff-settled.png)。手机对应证据见 [背面正文焦点](captures/fixed-mobile-back-leaving-focus.png) 与 [移交后状态](captures/fixed-mobile-handoff-settled.png)。

## 3. 越中点后反转

从正面用 Space 启动翻面，待矩阵 `m11 < −0.3`，即背面已经朝向读者，再按 Space 反转一次。每个尺寸和版本均只执行这一轮针对性反转。

修复副本桌面反转前后立即读取的 m11 均为 −0.309317；手机均为 −0.309874，没有观察到激活瞬间重置到正面的矩阵跳变。随后两者都以 m11=+1 停在正面，正面 `aria-hidden=false`、背面 `aria-hidden=true`，焦点留在翻面按钮，文案与最终面一致。旧版最终也能回到正面，原差距集中在中段的可访问面时机。

这只能说明这些输入下的瞬时朝向与最终状态，不能据此断言速度连续或主观顺滑。[修复副本手机越中点反转截图](captures/fixed-mobile-after-midpoint-reversal.png)展示了实际中段画面。

## 4. 减少动态效果

用新的浏览器上下文在启动时设为 `prefers-reduced-motion: reduce`，重复同样的早期点击与 Shift+Tab 操作。

旧版和修复副本在两个尺寸下均直接显示背面：m11=−1，背面可访问，Shift+Tab 正常进入可见正文，正文焦点轮廓可见。停稳时 `document.getAnimations()` 返回空数组。修复副本没有为了避开普通动效的早期焦点问题而阻止减少动态效果下的正常阅读入口。

截图：[修复副本桌面减少动态效果](captures/fixed-desktop-reduced-motion.png)；[修复副本手机减少动态效果](captures/fixed-mobile-reduced-motion.png)。

## 5. 保留的边缘观测与未确认内容

修复副本的逐帧记录仍有少量接近侧缘的属性窗口：例如普通翻面时 m11≈−0.154 的一个采样，两面都为 inert / aria-hidden；越中点反转时 m11≈+0.052 的一个采样，背面尚未关闭。下一采样即更新，焦点在这些记录中始终位于主题或翻面按钮，没有进入不可见正文。

这些原始样本完整保留。本轮未诊断它们的实现原因，也没有自然速度观察或屏幕阅读器证据支持将其判成新的明显故障。它们同时限制了结论强度：本报告确认指定键盘复现已修复，不能宣称所有时刻的矩阵和 aria 属性严格同帧变化。

服务预检曾遇到旧 8671 服务 connection refused，发生在任何产品操作之前；脚本在自身生命周期内重新提供原产品只读服务后完成全部检查。修复副本 8493 预检正常。没有其他未完成的产品操作或脚本异常。该环境记录另存于 [failed-checks.md](failed-checks.md)。

## 文件与停止范围

- [raw-measurements.json](raw-measurements.json)：全部原始帧、点击时刻、截图前后状态和文件指纹。
- [measurements-summary.json](measurements-summary.json)：指定复现、焦点移交、反转与减少动态效果的摘要。
- [review_continuation.py](review_continuation.py)：独立复现脚本。
- [execution.log](execution.log)：实际执行日志。

本轮结果独立保存在 observable-continuation-review，未回写原比较报告；针对性复核已完成，停止扩测。
