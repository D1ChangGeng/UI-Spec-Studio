# T2 观察后的局部源码诊断

检查顺序：先实际打开三者、操作翻面和返回、写下 initial-perception.md；再完成长文、保存压力与中段焦点观察；之后才读取与现象相关的 app.js 和 styles.css。未查看作者 README、参与者说明、Skill 条件或方法映射。

## L6 与 P8 的中段可访问面

在各自 `app/app.js` 的 `setFace(next)` 中，目标面写入 `note-card.dataset.face` 后，`card-front` 和 `card-back` 的 inert/aria-hidden 立即按目标值设置。各自样式中 #note-card 的变换有 720ms 过渡。这样会在正面仍可见时先将背面开放给键盘；与真实点击后 45ms 左右按 Shift+Tab 进入 preview-note 的现象吻合。

P8 有位于 CSS 伪元素的翻面旋转箭头，因此其实际可访问名称不能假定与 innerText 完全相等。第一次精确名称定位超时属于审阅脚本假设错误。

## N3 的中段同步

`app/app.js` 中 `syncVisibleFace()` 创建 `DOMMatrixReadOnly(getComputedStyle(note-card).transform)`，使用矩阵 m11 的符号判断哪面当前朝向用户，更新 inert/aria 隐藏属性；在将被隐藏的面内存在焦点时，移动到翻面按钮。`setFace()` 后续用 requestAnimationFrame 跟随约 760ms。

这解释了普通翻面早期 Shift+Tab 不能进入背面、实际越中点后才开放背面的差异。记录器在越中点反转中仍记录到两次孤立的近中点不同步样本；观测回调与产品回调的先后顺序可能造成一个采样间隔的差值。没有屏幕阅读器或自然速度观察结果支持更强判断。

## P8 的长文提示与返回入口

`updateOverflow()` 比较 preview-note 的 scrollHeight 和 clientHeight，切换 `draftMore` / `draftBoundary` 文案；输入、语言和返回编辑时请求重算。实际长文截图显示“当前草稿 · 可滚动阅读全文”，短文截图仅显示预览说明。

浏览器 DOM 实际顺序中，P8 的 return 在 saved-card 之前；L6、N3 的 return 在 saved-card 之后。手机长文实测进入已存页时返回按钮分别位于视口 y≈211.8、2066.5、1803.3，解释了视觉到达成本差异。

## 保存与返回状态

三者保存函数都先创建点击时的 record，延迟 900ms 后尝试原生 localStorage.setItem；成功后检查当前 textarea 是否仍等于提交记录，从而区分 saved 与 earlier；失败时触发 failed 状态，没有覆盖当前输入。

三者 showCollection 都记录并恢复选区与 textarea 的 scrollTop；存在可见 retry 时返回优先聚焦 retry，否则返回 textarea。P8 还存储页面 scrollY 并使用 preventScroll。源代码解释与真实保存压力、成功/失败返回、长文键盘恢复测量一致。

未根据实现长度、复杂度或这些机制本身评分；产品层结论见 review.md。
