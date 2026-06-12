# Word 内容自动排版到 PSD 最终规则说明

## 1. 项目目标

本规则用于指导开发 Photoshop JSX 自动排版脚本：先把 Word 教材内容解析成结构化数据，再根据 PSD 模板中的页面壳、标题、框线、表格、文字样式，把内容自动排入 PSD，并生成可继续编辑的 PSD 页面。

本项目不是把 Word 内容整段复制到 PSD，而是将 Word 拆分为以下教材结构，再按 PSD 模块化排版：

```text
Lesson 标题
Part 1: Reading & Dialogue
Part 2: Vocabulary & Idioms
Part 3: Grammar points
Part 4: Exercise
```

最终目标是支持 37 个 Lesson 批量排版。每个 Lesson 的页数不固定，由 Word 内容长度决定。

---

## 2. 总体工作流程

推荐流程：

```text
Word DOCX
  ↓
Python / VBA / 人工预处理
  ↓
结构化 JSON
  ↓
Photoshop JSX
  ↓
复制 PSD 页面壳模板
  ↓
按 Part 内容流动态排版
  ↓
保存 PSD
  ↓
导出 JPG / PNG 预览
```

### 2.1 不建议 JSX 直接读取 Word

Photoshop JSX 适合操作 PSD 图层，不适合解析 `.docx`。因此建议先用 Python、VBA 或其他工具把 Word 转成 JSON，再由 JSX 读取 JSON 排版。

### 2.2 推荐文件结构

```text
/project
  /input
    lesson.docx
  /templates
    lesson_first_shell.psd
    lesson_continue_shell.psd
  /style_reference
    ref_part1_reading_dialogue.psd
    ref_vocab_grammar.psd
    ref_grammar_continue.psd
    ref_exercise_start.psd
    ref_exercise_continue.psd
  /data
    lesson.json
  /jsx
    layout_lesson.jsx
    rename_layers.jsx
  /output
    Lesson_1-2_page_01.psd
    Lesson_1-2_page_02.psd
    Lesson_1-2_page_03.psd
    preview_page_01.jpg
    preview_page_02.jpg
    preview_page_03.jpg
```

---

## 3. 核心排版逻辑

### 3.1 页面壳与内容模块分离

规则必须拆成两部分：

```text
A. 页面壳模板
B. Part 1–Part 4 内容模块
```

页面壳模板负责：

```text
PSD 顶部标题
底部页码
绿色背景纹理
顶部横条
顶部断条装饰
白色圆角内容底板
左右页脚装饰
```

Part 内容模块负责：

```text
Part 1 Reading & Dialogue
Part 2 Vocabulary & Idioms
Part 3 Grammar points
Part 4 Exercise
```

JSX 开发时不要把页面壳和 Part 内容写死到固定页码中。正确做法是：先选择页面壳，再根据内容流动态放置 Part 模块。

### 3.2 页面壳只分两种

| 页面壳类型 | 来源 PSD | 图层来源 | 用途 |
|---|---|---|---|
| Lesson 首页页壳 | `PSD 3-4 1` | `@SHELL_FIRST_TOP_HEADER_GROUP + @SHELL_FIRST_CONTENT_PANEL_GROUP + @LESSON_COVER_TITLE_GROUP + @PAGE_NO_LEFT_TEXT / @PAGE_NO_RIGHT_TEXT` | 每个 Lesson 的第一页 |
| Lesson 后续页页壳 | `PSD 3-4 2` | `@SHELL_TOP_HEADER_GROUP + @SHELL_CONTENT_PANEL_LEFT / @SHELL_CONTENT_PANEL_RIGHT + @PAGE_NO_LEFT_TEXT / @PAGE_NO_RIGHT_TEXT` | 每个 Lesson 的第二页及之后所有页面 |

每个 Lesson 的页面结构为：

```text
1 个 Lesson 首页页壳
+
若干个 Lesson 后续页页壳
```

示例：

```text
Lesson 1-2
  page 01：使用 Lesson 首页页壳
  page 02：使用 Lesson 后续页页壳
  page 03：使用 Lesson 后续页页壳
  page 04：使用 Lesson 后续页页壳
  ...直到 Part 1–Part 4 全部排完
```

### 3.3 1–5 页 PSD 的定位

上传的 1–5 页 PSD 不应理解为所有 Lesson 都固定生成 5 页，而应理解为样式参考页：

```text
3-4 1：Lesson 首页页壳 + Part 1 起始样式参考
3-4 2：Lesson 后续页页壳 + Vocabulary / Grammar 样式参考
3-4 3：Grammar 续排样式参考
3-4 4：Grammar 结束 + Exercise 起始样式参考
3-4 5：Exercise 续排 / 最后一页样式参考
```

实际排版时，JSX 根据内容长度动态决定：

```text
Part 1 是否只在首页结束
Part 2 是否跨页
Part 3 是否跨页
Part 4 是否跨页
最终输出多少页
```

### 3.4 Part 内容模块采用动态流式布局

`PART 1` 标题及标题框的起始位置基本固定。其余 Part 内容的位置需要根据上一部分结束位置动态计算。

规则：

- `PART 1` 标题框位置基本固定，作为每个 Lesson 内容流起点。
- `PART 2`、`PART 3`、`PART 4` 的标题框、说明框、标题条、文本框、表格行、答题线等元素，不应写死在某一页某一坐标。
- 这些元素的形状、颜色、字体、字号、行距、底色样式必须参考 PSD 模板。
- 这些元素的实际 y 坐标必须根据上一部分内容结束位置动态计算。
- 当前页剩余高度不足以放下下一个完整模块时，应切换到后续页页壳继续排版。
- Part 标题条与至少第一行正文必须同页出现；如果当前页只够放标题条，不够放正文，则标题条也移动到下一页。

推荐内容流：

```text
创建页面壳
↓
放 Lesson 页眉
↓
从固定位置放 PART 1
↓
排 Reading / Dialogue
↓
根据当前 y 位置放 PART 2
↓
排 Vocabulary
↓
根据当前 y 位置放 PART 3
↓
排 Grammar
↓
根据当前 y 位置放 PART 4
↓
排 Exercise
↓
内容溢出时复制后续页页壳继续
```

---

## 4. 最高优先级样式规则

### 4.1 文字、音标、标点符号样式锁定

将 Word 内容放到 PSD 时，文字、音标、标点符号的字体、字号、颜色必须严格按照 PSD 模板中对应部分执行。不能由开发者或 JSX 脚本凭感觉调整。

规则：

- 所有标题、正文、音标、对话人物标记、词汇表文字、语法说明、练习题、标点符号，都必须使用 PSD 模板中对应区域的字体、字号、颜色。
- 不可因为内容过长而擅自缩小字号、改变字体、改变颜色、改变字重。
- 内容过长时，优先使用以下方式处理：
  1. 调整对应外框高度；
  2. 调整顶部横条长度或断条位置；
  3. 按规则换行；
  4. 切换到后续页页壳继续排版。
- 除非 PSD 模板中本来存在对应样式变化，否则不得新增新的字体样式。
- 标点符号必须跟随所在文字层的样式，不得单独改变字号、颜色或字体。

JSX 应建立“样式映射表”，所有文本层都从 PSD 模板文本层复制样式，不直接手写字体参数。

### 4.1.1 禁止硬编码或估算文字样式

后续所有 Photoshop JSX 排版脚本必须把 PSD 模板作为唯一文字样式来源。禁止在脚本中直接写死或凭经验估算字体、字号、颜色、行距、段落样式。

禁止做法包括但不限于：

```text
Times New Roman
42px
red
#C01818
手动指定某个字体作为正文或音标默认字体
手动指定某个字号作为正文或音标默认字号
手动指定某个颜色作为正文或音标默认颜色
```

正确做法：

- 启动排版前，必须用 Photoshop 打开 PSD 模板，读取或复制对应样式源图层。
- Reading 正文、Reading 音标、Dialogue 正文、Dialogue 音标、Vocabulary 单词、Vocabulary 音标、Vocabulary 释义、Grammar 正文、Exercise 正文等，都必须分别绑定到 PSD 中对应的样式源图层。
- 新建文本层时，应从对应 PSD 样式源图层 duplicate，再替换文本内容；或先读取 PSD 样式源，再批量应用到目标文本层。
- 如果 PSD 模板中找不到某类文字的样式源，脚本必须停止并在日志中报告缺失样式源，不允许临时改用估算字体、估算字号或估算颜色。
- Word 中的字体、字号、颜色、底色不作为最终排版样式依据；除非用户在当前项目中明确指定某类 Word 标注需要转换为 PSD 标注。
- 音标必须完整保留 Unicode 字符链路：docx 解析、JSON 保存、JSX 读取、Photoshop 写入都必须使用 Unicode/UTF-8，不得转为 ANSI、GBK 或其他会导致 IPA 乱码的编码。

验收标准：

- 生成 PSD 中不得出现因字体或编码错误导致的音标方框、乱码、丢字符。
- Reading 英文正文必须使用 PSD 模板正文样式，不能被音标红色样式或其他临时样式污染。
- 音标与正文必须分层或分样式处理，不能将两者套用同一个手写样式。

### 4.2 全局黑色色值

PSD 中所有黑色统一为：

```text
C: 0
M: 0
Y: 0
K: 100
```

JSX 中如果需要临时使用 RGB，可用：

```text
R: 0
G: 0
B: 0
```

最终印刷 PSD 中应保持 `C0 M0 Y0 K100`，不要使用四色黑。

---

## 5. PSD 全局参数

### 5.1 画布参数

| 项目 | 参数 |
|---|---:|
| 画布宽度 | 5031 px |
| 画布高度 | 3579 px |
| 分辨率 | 300 dpi |
| 左内容白底区域 | x≈137, y≈277, w≈2380, h≈3111 |
| 右内容白底区域 | x≈2515, y≈278, w≈2381, h≈3109 |
| 左正文安全区 | x≈200–2150 |
| 右正文安全区 | x≈2768–4840 |
| 顶部页眉 y | 179–245 |
| 底部页码 y | 3441–3504 |

JSX 开头必须设置像素单位：

```javascript
app.preferences.rulerUnits = Units.PIXELS;
```

### 5.2 固定元素

以下元素不建议由 JSX 重绘，直接保留 PSD 模板图层：

```text
绿色背景纹理
顶部横条
顶部断条装饰
白色圆角内容底板
左右页脚装饰条
橙色 Part 标签底形
黄色标题条
绿色小节标题条
词汇表浅绿色底条
答题线参考样式层
```

JSX 主要执行：

```text
1. 替换文字
2. 复制样式层
3. 移动 / 调整动态外框
4. 显示 / 隐藏已有图层组
5. 根据内容溢出复制后续页页壳
```

---

## 6. 图层命名规范

本节中的图层名已经同步到你当前 **用 JSX 重命名后的 PSD**。后续开发时，MD 中凡是提到的模板图层名，都应以这些新名称为准。

总原则：

- 模板内已有图层：直接按现有新名称查找、复制、移动、改字。
- 运行时新增或克隆的图层：沿用同一前缀规则命名，便于 JSX 后续查找。
- 不再以旧的中文图层名或我之前草拟的抽象名为准。
- 不再要求额外建立 `@STYLE_ROOT`；直接以现有模板图层作为样式源。

### 6.1 Lesson 首页页壳（PSD 3-4 1）关键图层

```text
@SHELL_FIRST_BG_TEXTURE_FULL
@SHELL_FIRST_TOP_HEADER_GROUP
@SHELL_TOP_LESSON_NO_TEXT
@SHELL_TOP_LESSON_TITLE_TEXT
@SHELL_FIRST_TOP_BAR_MAIN_SHAPE_01
@SHELL_FIRST_TOP_BAR_BREAK_SHAPE_01
@SHELL_FIRST_TOP_BAR_MAIN_SHAPE_02
@SHELL_FIRST_CONTENT_PANEL_GROUP
@SHELL_CONTENT_PANEL_LEFT
@SHELL_CONTENT_PANEL_RIGHT
@SHELL_PANEL_CORNER_DECOR_LEFT
@SHELL_PANEL_CORNER_DECOR_RIGHT
@LESSON_COVER_TITLE_GROUP
@LESSON_NO_COVER_TEXT
@LESSON_TITLE_COVER_TEXT
@SHELL_FIRST_COVER_BAR_MAIN_SHAPE
@SHELL_FIRST_COVER_BAR_BREAK_SHAPE
@PAGE_NO_LEFT_BG_SHAPE
@PAGE_NO_LEFT_TEXT
@PAGE_NO_RIGHT_BG_SHAPE
@PAGE_NO_RIGHT_TEXT
```

说明：

- Lesson 首页页壳的页眉以 `@SHELL_FIRST_TOP_HEADER_GROUP` 为主。
- Lesson 首页封面标题区以 `@LESSON_COVER_TITLE_GROUP` 为主。
- 如需根据标题长度调整顶部横条，优先调整：
  - `@SHELL_FIRST_COVER_BAR_MAIN_SHAPE`
  - `@SHELL_FIRST_COVER_BAR_BREAK_SHAPE`
- 页面内容白底区域主要依赖：
  - `@SHELL_FIRST_CONTENT_PANEL_GROUP`
  - `@SHELL_CONTENT_PANEL_LEFT`
  - `@SHELL_CONTENT_PANEL_RIGHT`

### 6.2 Lesson 后续页页壳（PSD 3-4 2 / 3 / 4 / 5）关键图层

```text
@SHELL_BG_TEXTURE_FULL
@SHELL_TOP_HEADER_GROUP
@SHELL_TOP_LESSON_NO_TEXT
@SHELL_TOP_LESSON_TITLE_TEXT
@SHELL_BOOK_TITLE_BG_SHAPE
@SHELL_BOOK_TITLE_TEXT
@SHELL_TOP_BAR_MAIN_SHAPE
@SHELL_TOP_BAR_BREAK_SHAPE
@SHELL_CONTENT_PANEL_LEFT
@SHELL_CONTENT_PANEL_RIGHT
@SHELL_CONTENT_PANEL_DECOR_SHAPE_LEFT
@SHELL_CONTENT_PANEL_DECOR_SHAPE_RIGHT
@SHELL_PANEL_CORNER_DECOR_LEFT
@SHELL_PANEL_CORNER_DECOR_RIGHT
@PAGE_NO_LEFT_BG_SHAPE
@PAGE_NO_LEFT_TEXT
@PAGE_NO_RIGHT_BG_SHAPE
@PAGE_NO_RIGHT_TEXT
```

说明：

- `PSD 3-4 2`、`PSD 3-4 3`、`PSD 3-4 4`、`PSD 3-4 5` 的后续页页壳命名体系一致。
- 后续页的顶部横条和断条，使用：
  - `@SHELL_TOP_BAR_MAIN_SHAPE`
  - `@SHELL_TOP_BAR_BREAK_SHAPE`
- 后续页书名条使用：
  - `@SHELL_BOOK_TITLE_BG_SHAPE`
  - `@SHELL_BOOK_TITLE_TEXT`

### 6.3 Part 1：Reading & Dialogue 图层

```text
@PART1_TITLE_GROUP
@PART1_TITLE_TEXT
@PART1_TITLE_BG_SHAPE_A
@PART1_TITLE_BG_SHAPE_B
@PART1_CONTENT_GROUP
@PART1_READING_DIALOGUE_GROUP
@PART1_READING_LEFT_TEXT_STYLE_SOURCE
@PART1_READING_RIGHT_TEXT_STYLE_SOURCE
@PART1_READING_BORDER_SHAPE_A
@PART1_READING_BORDER_SHAPE_B
@PART1_DIALOGUE_INTRO_TEXT
@PART1_DIALOGUE_ROLE_MAP_TEXT
@PART1_DIALOGUE_YELLOW_BG_SHAPE
@PART1_DIALOGUE_BORDER_LEFT_SHAPE
@PART1_DIALOGUE_BORDER_TOP_SHAPE
@PART1_DIALOGUE_BORDER_BOTTOM_SHAPE
@PART1_DIALOGUE_LINE_BG_SHAPE
@PART1_DIALOGUE_SAMPLE_LINE_TEXT
```

说明：

- Part 1 标题使用 `@PART1_TITLE_GROUP` / `@PART1_TITLE_TEXT`。
- Reading 正文样式源使用：
  - `@PART1_READING_LEFT_TEXT_STYLE_SOURCE`
  - `@PART1_READING_RIGHT_TEXT_STYLE_SOURCE`
- Reading 外框相关图层使用：
  - `@PART1_READING_BORDER_SHAPE_A`
  - `@PART1_READING_BORDER_SHAPE_B`
- 其中建议把 **下边线动态调整对象** 统一视为 `@PART1_READING_BORDER_SHAPE_B`。
- Dialogue 说明文字和角色映射使用：
  - `@PART1_DIALOGUE_INTRO_TEXT`
  - `@PART1_DIALOGUE_ROLE_MAP_TEXT`
- Dialogue 动态底框与边线使用：
  - `@PART1_DIALOGUE_YELLOW_BG_SHAPE`
  - `@PART1_DIALOGUE_BORDER_LEFT_SHAPE`
  - `@PART1_DIALOGUE_BORDER_BOTTOM_SHAPE`
- `@PART1_DIALOGUE_SAMPLE_LINE_TEXT` 可作为运行时新增对话行的样式源。

### 6.4 Part 2：Vocabulary & Idioms 图层

Part 2 标题与内容容器：

```text
@PART2_TITLE_GROUP
@PART2_TITLE_TEXT
@PART2_TITLE_BG_SHAPE_A
@PART2_TITLE_BG_SHAPE_B
@PART2_CONTENT_GROUP
@PART2_VOCAB_ROW_01_GROUP
@PART2_VOCAB_ROW_02_GROUP
@PART2_VOCAB_ROW_01_NO_TEXT
@PART2_VOCAB_ROW_01_WORD_TEXT
@PART2_VOCAB_ROW_01_PHONETIC_TEXT
@PART2_VOCAB_ROW_01_MEANING_TEXT
@PART2_VOCAB_ROW_02_NO_TEXT
@PART2_VOCAB_ROW_02_WORD_TEXT
@PART2_VOCAB_ROW_02_PHONETIC_TEXT
@PART2_VOCAB_ROW_02_MEANING_TEXT
```

后续页词条参考组：

```text
@PART2_VOCAB_CONT_GROUP
@PART2_VOCAB_ROW_09_GROUP
@PART2_VOCAB_ROW_10_GROUP
...
@PART2_VOCAB_ROW_21_GROUP
```

说明：

- `@PART2_VOCAB_ROW_01_GROUP`、`@PART2_VOCAB_ROW_02_GROUP` 可作为奇偶行样式源。
- 每个词条内部统一采用：
  - `..._NO_TEXT`
  - `..._WORD_TEXT`
  - `..._PHONETIC_TEXT`
  - `..._MEANING_TEXT`
- 如运行时克隆新词条，建议延续同一命名逻辑，例如：
  - `@PART2_VOCAB_ROW_22_GROUP`
  - `@PART2_VOCAB_ROW_22_NO_TEXT`
  - `@PART2_VOCAB_ROW_22_WORD_TEXT`
  - `@PART2_VOCAB_ROW_22_PHONETIC_TEXT`
  - `@PART2_VOCAB_ROW_22_MEANING_TEXT`

### 6.5 Part 3：Grammar points 图层

Part 3 起始页关键图层（主要来自 PSD 3-4 2）：

```text
@PART3_TITLE_GROUP
@PART3_TITLE_TEXT
@PART3_TITLE_BG_SHAPE_A
@PART3_TITLE_BG_SHAPE_B
@PART3_CONTENT_GROUP
@PART3_LEAD_GROUP
@PART3_LEAD_ORANGE_ITALIC_TEXT
@PART3_SECTION_GROUP
@PART3_BODY_TEXT_BLOCK_02
@PART3_BODY_TEXT_BLOCK_03
@PART3_SUBTITLE_01_GROUP
@PART3_SUBTITLE_01_NO_TEXT
@PART3_SUBTITLE_01_TEXT
@PART3_SUBTITLE_02_GROUP
@PART3_SUBTITLE_02_NO_TEXT
@PART3_SUBTITLE_02_TEXT
```

Part 3 续排页参考图层（主要来自 PSD 3-4 3 / 4）：

```text
@PART3_CONT_GROUP
@PART3_CONT_TEXT_BLOCK_LEFT_01
@PART3_CONT_TEXT_BLOCK_LEFT_02
@PART3_CONT_TEXT_BLOCK_LEFT_03
@PART3_CONT_TEXT_BLOCK_RIGHT_01
@PART3_CONT_TEXT_BLOCK_RIGHT_02
@PART3_SUBTITLE_03_GROUP
@PART3_SUBTITLE_03_NO_TEXT
@PART3_SUBTITLE_03_TEXT
@PART3_SUBTITLE_04_GROUP
@PART3_SUBTITLE_04_NO_TEXT
@PART3_SUBTITLE_04_TEXT
@PART3_SUBTITLE_05_GROUP
@PART3_SUBTITLE_05_NO_TEXT
@PART3_SUBTITLE_05_TEXT
```

说明：

- Word 中橙色首句，对应 PSD 使用 `@PART3_LEAD_ORANGE_ITALIC_TEXT` 样式。
- 语法小点的编号条与标题，直接参考：
  - `@PART3_SUBTITLE_01_GROUP`
  - `@PART3_SUBTITLE_02_GROUP`
  - `@PART3_SUBTITLE_03_GROUP`
  - `@PART3_SUBTITLE_04_GROUP`
  - `@PART3_SUBTITLE_05_GROUP`
- 若运行时新增第 6 个及之后的小点，可延续命名：
  - `@PART3_SUBTITLE_06_GROUP`
  - `@PART3_SUBTITLE_06_NO_TEXT`
  - `@PART3_SUBTITLE_06_TEXT`

### 6.6 Part 4：Exercise 图层

Part 4 起始页关键图层（主要来自 PSD 3-4 4）：

```text
@PART4_TITLE_GROUP
@PART4_TITLE_TEXT
@PART4_TITLE_BG_SHAPE_A
@PART4_TITLE_BG_SHAPE_B
@PART4_CONTENT_GROUP
@PART4_EXERCISE_GROUP
@PART4_EXERCISE_Q1_NO_TEXT
@PART4_EXERCISE_Q1_BODY_TEXT
@PART4_EXERCISE_Q2_NO_TEXT
@PART4_EXERCISE_Q2_BODY_TEXT
```

Part 4 续排页参考图层（主要来自 PSD 3-4 5）：

```text
@PART4_TITLE_GROUP_REF
@PART4_CONTENT_GROUP_REF
@PART4_EXERCISE_CONT_GROUP_REF
@PART4_EXERCISE_CONT_BODY_TEXT
```

说明：

- Part 4 起始页标题使用 `@PART4_TITLE_GROUP` / `@PART4_TITLE_TEXT`。
- 续排页参考使用：
  - `@PART4_TITLE_GROUP_REF`
  - `@PART4_CONTENT_GROUP_REF`
  - `@PART4_EXERCISE_CONT_GROUP_REF`
- 运行时新增的答题块可沿用命名：
  - `@PART4_EXERCISE_Q03_NO_TEXT`
  - `@PART4_EXERCISE_Q03_BODY_TEXT`
  - `@PART4_EXERCISE_Q03_ANSWER_LINE`

### 6.7 页码图层

首页和后续页都统一使用以下页码命名：

```text
@PAGE_NO_LEFT_BG_SHAPE
@PAGE_NO_LEFT_DECOR_SHAPE
@PAGE_NO_LEFT_TEXT
@PAGE_NO_RIGHT_BG_SHAPE
@PAGE_NO_RIGHT_DECOR_SHAPE
@PAGE_NO_RIGHT_TEXT
```

页码数字替换时，优先直接改 `@PAGE_NO_LEFT_TEXT` 或 `@PAGE_NO_RIGHT_TEXT`。

### 6.8 运行时新增图层命名建议

对于 JSX 在排版过程中新增或克隆出的图层，建议沿用以下命名逻辑：

```text
@PART1_DIALOGUE_ROLE_LINE_001_TEXT
@PART1_DIALOGUE_BODY_LINE_001_TEXT
@PART1_DIALOGUE_PHONETIC_LINE_001_TEXT

@PART2_VOCAB_ROW_22_GROUP
@PART2_VOCAB_ROW_22_NO_TEXT
@PART2_VOCAB_ROW_22_WORD_TEXT
@PART2_VOCAB_ROW_22_PHONETIC_TEXT
@PART2_VOCAB_ROW_22_MEANING_TEXT

@PART3_SUBTITLE_06_GROUP
@PART3_SUBTITLE_06_NO_TEXT
@PART3_SUBTITLE_06_TEXT

@PART4_EXERCISE_Q03_NO_TEXT
@PART4_EXERCISE_Q03_BODY_TEXT
@PART4_EXERCISE_Q03_ANSWER_LINE
```

原则：

- 模板已有图层名，不改前缀。
- 运行时新增图层，沿用模板前缀 + 序号。
- 所有序号建议固定两位或三位，避免排序混乱。

---

## 7. Word 预处理数据结构

建议把每个 Lesson 解析成以下 JSON：

```json
{
  "lessonNo": "Lesson 1-2",
  "lessonTitle": "Rome Wasn’t Built in a Day",
  "part1": {
    "title": "Reading&Dialogue",
    "reading": [],
    "dialogueIntro": "Mack is talking to his friend Don.",
    "dialogueRoleNote": "(M = Mack; D = Don)",
    "dialogue": []
  },
  "part2": {
    "title": "Vocabulary&Idioms",
    "items": []
  },
  "part3": {
    "title": "Grammar points",
    "paragraphs": [],
    "sections": []
  },
  "part4": {
    "title": "Exercise",
    "sections": []
  }
}
```

---

## 8. Lesson 标题规则

Word 开头两行：

```text
Lesson 1-2
Rome Wasn’t Built in a Day
```

对应 PSD 顶部：

```text
Lesson 1-2    ROME WASN’T BUILT IN A DAY
```

规则：

- `LessonNo` 保留 Word 原格式，例如 `Lesson 1-2`。
- `lessonTitle` 按 PSD 样式处理，可统一转成大写。
- 标题字体、字号、颜色必须复制 PSD 模板标题层。
- 如果标题过长，不改变右侧英文标题字号。
- 标题过长时，根据标题长度调整顶部绿色横条长度。
- 顶部横条左侧起点位置不变，只向右延长。
- 横条延长后，同步调整右侧断条位置。
- 不允许为了标题变长而压缩字体或改变颜色。

伪代码：

```javascript
setText("@SHELL_TOP_LESSON_NO_TEXT", data.lessonNo);
setText("@SHELL_TOP_LESSON_TITLE_TEXT", data.lessonTitle.toUpperCase());

var titleWidth = measureLayerWidth("@SHELL_TOP_LESSON_TITLE_TEXT");
resizeHeaderBar("@SHELL_TOP_BAR_MAIN_SHAPE", titleWidth);
moveHeaderBreak("@SHELL_TOP_BAR_BREAK_SHAPE", newBreakX);
```

---

## 9. Part 1：Reading & Dialogue

### 9.1 Part 1 标题

PSD 样式为：

```text
PART 1    Reading&Dialogue
```

规则：

- 橙色 `PART 1` 标签保留。
- 黄色标题条保留。
- 只替换文字，不重绘底形。
- `Reading&Dialogue` 优先保留 Word 原文。
- 字体、字号、颜色严格复制 PSD 对应标题层。

### 9.2 Reading 主课文规则

Word 中 Reading 典型结构：

```text
               /ɪntɚˈnæʃənl/ /ˈlæŋɡwɪdʒ/
English is an international language. Therefore, it is necessary for
                        /rɪˈwɔrdɪŋ/
us to learn it. It can be rewarding or just a waste of time.
```

排入 PSD 时：

- `/.../` 音标行不能当作普通黑色正文。
- `/.../` 音标统一转换为 `[...]`。
- 音标使用 PSD 中对应的红色小字样式。
- 音标放在对应英文词或短语上方。
- 第一版无法精确定位时，可先保留为一整行红色音标层，放在对应英文句子上一行。
- 英文正文使用 PSD 中 Reading 正文样式。
- 主课文段落格式按“音标行 + 英文课文行 + 空行”循环。
- 如果两行课文之间没有音标，则正常排正文，并在段落结束后空一行。
- 英文正文首行缩进，缩进宽度参考 PSD 原正文。
- 不建议把音标和英文正文放在同一个文本层里。

推荐 JSON：

```json
{
  "type": "readingLine",
  "phonetic": "[ɪntɚˈnæʃənl] [ˈlæŋɡwɪdʒ]",
  "text": "English is an international language. Therefore, it is necessary for"
}
```

### 9.3 Reading 绿线边框动态调整

Reading 主课文外侧绿线边框必须根据主课文长度调整。

规则：

- 主要调整绿色边框的下线位置。
- 上线、左线、右线不动。
- 不改变线颜色、粗细、直角与圆角样式。
- 边框底线与正文最后一行之间保留 PSD 模板中的原始内边距。

伪代码：

```javascript
var readingBottom = getReadingContentBottom("@PART1_CONTENT_GROUP");
var paddingBottom = getTemplatePadding("readingFrameBottom");
moveFrameBottom("@PART1_READING_BORDER_SHAPE_B", readingBottom + paddingBottom);
```

### 9.4 Dialogue 说明框

Word 中：

```text
Mack is talking to his friend Don.
```

PSD 中应放入对应说明框，并补充角色说明：

```text
Mack is talking to his friend Don.
(M = Mack; D = Don)
```

规则：

- `Mack is talking to his friend Don.` 放到 Dialogue 对应说明框内。
- `(M = Mack; D = Don)` 也放到对应框内。
- `M = Mack` 使用红色。
- `D = Don` 使用蓝色。
- 如果以后出现 `A = ...`，使用 PSD 模板中第三角色颜色。
- 角色说明不参与普通正文流，不挤进 Reading 正文。

### 9.5 Dialogue 对话正文

Word 中：

```text
M: Hi, Don! How are you doing in your English class.
D: Not so well, I’m afraid.
M: What’s the problem?
```

规则：

- `M:`、`D:`、`A:` 等人物开头必须保留颜色区分。
- `M:` 使用红色。
- `D:` 使用蓝色。
- `A:` 使用 PSD 模板中第三角色颜色。
- 对话正文内容使用黑色。
- 人物代号与正文建议拆成两个文本层或两个相邻文本框，便于 JSX 控色。
- 对话前的音标行同样按照 Reading 音标规则处理：`/.../` 转为 `[...]`，红色小字，放在对应句子上一行或对应词上方。

推荐拆层：

```text
@PART1_DIALOGUE_ROLE_LINE_001_TEXT    M:
@PART1_DIALOGUE_BODY_LINE_001_TEXT    Hi, Don! How are you doing in your English class.
@PART1_DIALOGUE_ROLE_LINE_002_TEXT    D:
@PART1_DIALOGUE_BODY_LINE_002_TEXT    Not so well, I’m afraid.
```

### 9.6 Dialogue 绿线 + 黄色底框动态调整

Dialogue 区域必须根据对话内容长度自动调整。

规则：

- 黄色底框上边界、左边界、右边界保持模板位置。
- 主要调整黄色底框下边界。
- 左侧绿色竖线必须与黄色底框高度同步调整。
- 不改变黄色底框颜色、透明度、圆角、描边样式。
- 不改变左侧绿色线颜色、粗细、端点样式。
- 当前页不足以容纳 Dialogue 框时，整体换到下一页，不要拆开说明框和前几句对话。

伪代码：

```javascript
var dialogueBottom = getDialogueContentBottom("@PART1_CONTENT_GROUP");
var paddingBottom = getTemplatePadding("dialogueBoxBottom");
resizeYellowBox("@PART1_DIALOGUE_YELLOW_BG_SHAPE", dialogueBottom + paddingBottom);
resizeVerticalLine("@PART1_DIALOGUE_BORDER_LEFT_SHAPE", dialogueBottom + paddingBottom);
moveHorizontalBorder("@PART1_DIALOGUE_BORDER_BOTTOM_SHAPE", dialogueBottom + paddingBottom);
```

---

## 10. Part 2：Vocabulary & Idioms

### 10.1 词条解析

Word 中词汇行：

```text
1. international  KK: [ˌɪntɚˈnæʃənl]  IPA: [ˌɪntərˈnæʃənəl]  adj. 国际性的；国际间的
```

解析为：

```json
{
  "index": "1.",
  "word": "international",
  "kk": "KK: [ˌɪntɚˈnæʃənl]",
  "ipa": "IPA: [ˌɪntərˈnæʃənəl]",
  "meaning": "adj. 国际性的；国际间的"
}
```

### 10.2 四列排版

每个词条按四列排版：

```text
序号 | 单词 / 短语 | KK / IPA | 词性释义
```

规则：

- 序号列固定宽度，序号位置不随其他列换行移动。
- 单词 / 短语列固定宽度。
- KK / IPA 列固定宽度，可分两行显示：第一行 KK，第二行 IPA。
- 词性释义列固定宽度。
- 每行词条在垂直方向居中。
- 奇数行使用浅绿色底。
- 偶数行使用白底或无底色。
- 短语词条如 `depend on`、`be afraid to + 动词原形` 不要拆开。
- 某个词条过长时，允许该词条内部换行。
- 词条换行时，序号列位置不变，其他列内容在本词条高度内换行。
- 不使用空格模拟四列表格。

### 10.3 长词条处理优先级

```text
1. 释义列自动换行
2. KK / IPA 列拆成两行
3. 单词 / 短语列保持完整，不拆词
4. 增加该词条行高
5. 当前页放不下整条词条时，整条移动到下一页
```

禁止做法：

```text
不要把短语拆成两条词汇
不要为了塞进一行而压缩字号
不要让序号列跟随释义换行往下偏移
不要用空格模拟四列表格
不要把一个词条拆到两页
```

---

## 11. Part 3：Grammar points

### 11.1 Grammar 总规则

规则：

- 语法内容按 Word 段落顺序排入。
- 行距必须复制 PSD 对应文本层的实测行距；MD 中出现的 `24 px` 只能作为早期估算，不得覆盖 PSD 实测样式。
- 中英混排保持原来的示例顺序。
- 以 `①②③④` 开头的例句建议单独成段。
- 以 `→` 开头或包含 `→` 的变形句，必须保留箭头，不要转成项目符号。
- 如果 Word 没有明显小标题，不要强行套用 PSD 里的小绿编号标题。
- 没有对应内容的小绿标题组可以隐藏。
- 如果 Word 有多个语法小点，可自动生成 `1`、`2`、`3`……小绿标题条。
- 自动生成的小绿标题文字必须来自 Word 小标题或明确内容结构，不要凭空添加教材没有的概念。

### 11.2 Part 3 标题下第一句橙色斜体

Part 3 每个标题下第一句，如果 Word 中为橙色文字，排入 PS 后也必须保持橙色斜体。

规则：

- 该句识别为 `grammarLeadSentence`。
- 字体、字号、颜色、斜体样式参考 PSD 模板 `3-4 2` 中对应样式。
- 不要把该句当普通黑色正文处理。
- 如果该句跨行，跨行部分仍保持橙色斜体。
- 后续普通语法说明恢复为黑色正文，行距仍以 PSD 对应文本层实测值为准。

推荐 JSON：

```json
{
  "type": "grammarLeadSentence",
  "text": "本节课主要学习特殊疑问词引导的名词性从句。",
  "styleRef": "@PART3_LEAD_ORANGE_ITALIC_TEXT"
}
```

### 11.3 Grammar 段落类型

普通段落：

```json
{
  "type": "paragraph",
  "text": "对于特殊疑问句，我们只需要把特殊疑问词后面倒装的句子还原成正常的语序就可以当名词性从句用了。"
}
```

变形句：

```json
{
  "type": "transformExample",
  "source": "What is your name?",
  "arrow": "→",
  "target": "what your name is.",
  "note": "be动词回到主语后面"
}
```

编号例句：

```json
{
  "type": "numberedExample",
  "number": "①",
  "text": "What your name is doesn’t matter to me.",
  "note": "名词性从句作主语"
}
```

### 11.4 示例句排版

规则：

- 原句、`变从句`、箭头、变形后句子、中文说明保持同一逻辑行。
- 如果行太长，可以在中文说明前换行。
- 箭头 `→` 必须保留。
- 不要把 `→` 改成 `-`、`>` 或项目符号。
- `①②③④` 开头例句单独成段。
- 中文功能说明可跟在后面；行宽不够时，中文说明换到下一行并缩进。

---

## 12. Part 4：Exercise

### 12.1 Exercise 总标题

PSD 样式：

```text
PART 4    Exercise
```

规则：

- 橙色 `PART 4` 标签保留。
- 黄色标题条保留。
- 只替换文字，不重绘底形。
- Part 4 总标题只出现一次。
- 如果当前页无法开始 Exercise，则隐藏该组，等后续练习页开始时再显示。

### 12.2 练习题结构

Word 中：

```text
1. 从下列句子中找出名词性从句，在从句下方画横线。
1　 What he needs is more time.

2. 翻译
1　 我不知道如何提高我的国际语言水平。（international language）
```

建议解析为：

```json
{
  "sectionNo": "1.",
  "title": "从下列句子中找出名词性从句，在从句下方画横线。",
  "items": [
    { "number": "1", "text": "What he needs is more time.", "answerLines": 0 }
  ]
}
```

```json
{
  "sectionNo": "2.",
  "title": "翻译",
  "items": [
    { "number": "1", "text": "我不知道如何提高我的国际语言水平。（international language）", "answerLines": 1 }
  ]
}
```

### 12.3 Exercise 排版规则

- 大题号 `1.`、`2.` 单独作为橙色数字层。
- 大题标题使用 PSD 对应黑色正文样式。
- 小题列表使用 PSD 对应黑色正文样式。
- 翻译题每题后生成答题线。
- 带答题线的小题必须作为完整题块分页，不允许题目和答题线拆到两页。
- 练习题续排时继续上一页编号，不重新编号。
- 如果上一页已经显示过 `2. 翻译`，下一页只续题，不重复小节标题。

### 12.4 答题线规则

每道翻译题格式：

```text
④ 我明白了什么才是真正值得做的事。（worthy）
____________________________________________________________
```

规则：

- 每道题包括题目行 + 答题线行。
- 答题线长度参考 PSD。
- 不要用多个空格模拟答题线。
- 第一版可用下划线文本。
- 稳定版建议复制 `@PART4_EXERCISE_CONT_BODY_TEXT` 形状线。

---

## 13. 样式参考页说明

### 13.1 `3-4 1`：首页页壳 + Part 1 起始样式

主要参考：

```text
Lesson 标题
Part 1 Reading
Part 1 Dialogue
Part 2 Vocabulary 起始
```

首页排版顺序示例：

```text
1. 替换 LessonNo 与 LessonTitle
2. 根据 LessonTitle 宽度调整顶部绿色横条和断条
3. 填入 PART 1 / Reading&Dialogue
4. 填入 Reading 主课文
5. 根据 Reading 内容调整绿线边框下线
6. 填入 Dialogue 说明框与角色说明
7. 填入 Dialogue 对话正文
8. 根据 Dialogue 内容调整黄色底框和左侧绿线
9. 当前页剩余空间足够时，开始 Part 2 Vocabulary
10. 放不下的内容进入后续页页壳
```

### 13.2 `3-4 2`：后续页页壳 + Vocabulary / Grammar 样式

主要参考：

```text
Vocabulary 继续
Part 3 Grammar points 开始
Part 3 橙色斜体首句样式
```

规则：

- 第 1 页放不下的词条进入后续页。
- 每个词条按四列排版。
- Vocabulary 结束后，根据剩余空间开始 Grammar。
- `PART 3 Grammar points` 只出现一次。

### 13.3 `3-4 3`：Grammar 续排样式

主要参考：

```text
Grammar 普通正文续排
Grammar 小绿标题条
Grammar 小节正文
左右栏续排方式
```

规则：

- 如果 Word 没有小标题，隐藏小绿标题组。
- 如果 Word 有小标题，显示小绿标题组。
- 左侧区域放不下后进入右侧区域。
- 当前页仍放不下时，继续复制后续页页壳。

### 13.4 `3-4 4`：Grammar 结束 + Exercise 开始样式

主要参考：

```text
Grammar 结束
Part 4 Exercise 开始
练习大题号
练习正文
```

规则：

- 只有 Grammar 已经排完，才允许在同页开始 Exercise。
- Grammar 未排完时，不显示 Part 4。
- Exercise 开始后，Part 4 总标题只出现一次。

### 13.5 `3-4 5`：Exercise 续排 / 最后一页样式

主要参考：

```text
Exercise 续排
翻译题续排
答题线样式
左右栏练习续排
```

规则：

- 默认不重复 `PART 4 Exercise` 总标题。
- 左侧放不下后进入右侧。
- 右侧仍放不下时，继续复制后续页页壳作为练习续页。
- 题目和答题线不得拆页。

---

## 14. 自动分页策略

### 14.1 内容流顺序

```text
Lesson 标题
↓
Part 1 Reading
↓
Dialogue
↓
Part 2 Vocabulary
↓
Part 3 Grammar
↓
Part 4 Exercise
```

### 14.2 页面壳使用顺序

```text
第 1 个输出页：复制 Lesson 首页页壳
第 2 个输出页及以后：复制 Lesson 后续页页壳
直到当前 Lesson 内容全部排完
```

伪流程：

```text
createPage(shell = lesson_first_shell)
layout Part 1 起始内容

while 当前 Lesson 还有内容未排完:
    if 当前页剩余高度不足:
        createPage(shell = lesson_continue_shell)
    继续排当前 Part
    当前 Part 排完后，根据 currentY + 模块间距 放下一个 Part 标题
```

### 14.3 拆分原则

普通正文：

```text
优先按段落拆
段落太长时按句子拆
句子仍太长时按字符二分法拆
```

词汇表：

```text
必须按完整词条拆
不允许一个词条跨页
```

练习题：

```text
必须按完整题块拆
题目和答题线不允许跨页
```

Part 标题：

```text
Part 标题条 + 至少第一行内容必须同页出现
如果当前页只够放 Part 标题条，则标题条移动到下一页
```

---

## 15. Word → JSON 预处理规则

### 15.1 音标

把 Word 中的：

```text
/ɪntɚˈnæʃənl/
```

转换为：

```text
[ɪntɚˈnæʃənl]
```

规则：

- 只转换独立音标，不误改普通英文斜杠。
- 一行中多个 `/.../` 都要分别转换。
- 转换后标记为 `phonetic` 类型。

### 15.2 对话

识别：

```text
M:
D:
A:
```

输出：

```json
{
  "speaker": "M",
  "speakerStyle": "@PART1_DIALOGUE_SAMPLE_LINE_TEXT",
  "text": "Hi, Don! How are you doing in your English class."
}
```

### 15.3 词汇

识别：

```text
序号 + 单词/短语 + KK + IPA + 词性释义
```

短语词条没有单独序号时，如果包含 `KK:` / `IPA:`，应作为独立词条处理，但编号规则要按教材实际决定。

例如：

```text
3. rewarding ...
    depend on   KK: ... IPA: ... 视……而定
```

`depend on` 是短语词条，不要并入 `rewarding` 的释义，也不要拆成 `depend` 和 `on`。

### 15.4 Grammar

识别以下内容：

```text
普通中文解释段落
中英混合示例句
包含 → 的变形句
①②③④ 开头的例句
可能的小标题
橙色斜体首句
```

如果没有明显小标题，全部作为普通 Grammar 正文流。

### 15.5 Exercise

识别：

```text
大题号：1.、2.
小题号：1　、2　 或 ①②③
翻译题括号提示词
是否需要答题线
```

翻译题默认需要一条答题线。

---

## 16. JSX 主流程建议

```javascript
app.preferences.rulerUnits = Units.PIXELS;

var data = readJson("/data/lesson.json");

var firstShell = "/templates/lesson_first_shell.psd";
var continueShell = "/templates/lesson_continue_shell.psd";

var pageIndex = 1;
var currentPage = createPage(firstShell, pageIndex);

updateHeader(currentPage, data.lessonNo, data.lessonTitle);

layoutPart1(data.part1);
layoutPart2(data.part2);
layoutPart3(data.part3);
layoutPart4(data.part4);

saveAllPages();
exportAllPreviews();
```

推荐函数：

```javascript
function findLayerByName(container, layerName) {}
function setText(layerName, content) {}
function copyTextStyle(sourceLayerName, targetLayerName) {}
function duplicateStyledTextLayer(sourceLayerName, newLayerName) {}
function duplicateStyledGroup(sourceGroupName, newGroupName) {}
function measureLayerWidth(layerName) {}
function measureTextBottom(layerName) {}
function splitTextToFit(text, area, styleRef) {}
function createNextPageIfNeeded(requiredHeight) {}
function layoutPartTitle(partNo, title) {}
function layoutReading(readingData) {}
function layoutDialogue(dialogueData) {}
function layoutVocabRows(items) {}
function layoutGrammarBlocks(blocks) {}
function layoutExerciseBlocks(blocks) {}
function resizeHeaderBar(layerName, targetWidth) {}
function moveHeaderBreak(layerName, targetX) {}
function moveFrameBottom(layerName, targetY) {}
function resizeYellowBox(layerName, targetBottomY) {}
function resizeVerticalLine(layerName, targetBottomY) {}
function hideUnusedGroups() {}
function saveAsPSD(outputPath) {}
function exportPreviewJPG(outputPath) {}
```

---

## 17. 禁止做法

- 不要让 JSX 直接读取 `.docx`。
- 不要把音标和正文硬塞进同一个黑色文本层。
- 不要把 `/.../` 音标当普通正文。
- 不要使用空格模拟词汇表四列。
- 不要使用空格模拟答题线。
- 不要为了塞内容擅自缩小字号。
- 不要改变 PSD 模板中对应部分的字体、字号、颜色。
- 不要强行显示 Word 中没有的小绿标题。
- 不要把一个词条拆到两页。
- 不要把一个翻译题的题目和答题线拆到两页。
- 不要覆盖原 PSD 模板文件。
- 不要在 Photoshop 外部直接修改 PSD 二进制结构。

---

## 18. 开发执行清单

1. 用 Python 或 VBA 读取 Word，导出 `lesson.json`。
2. 在 Photoshop 中整理两个页面壳模板：
   - `lesson_first_shell.psd`：对应 `PSD 3-4 1`，关键图层使用 `@SHELL_FIRST_TOP_HEADER_GROUP`、`@SHELL_FIRST_CONTENT_PANEL_GROUP`、`@LESSON_COVER_TITLE_GROUP` 与页码层。
   - `lesson_continue_shell.psd`：对应 `PSD 3-4 2`，关键图层使用 `@SHELL_TOP_HEADER_GROUP`、`@SHELL_CONTENT_PANEL_LEFT`、`@SHELL_CONTENT_PANEL_RIGHT` 与页码层。
3. JSX 统一按当前已重命名图层名查找模板层，模板层名以本 MD 第 6 节为准。
4. 直接以现有模板层作为样式源，不再额外建立 `@STYLE_ROOT`。
5. JSX 读取 `lesson.json`。
6. 创建当前 Lesson 的第 1 个输出页，使用首页页壳。
7. 替换 Lesson 标题，根据标题长度调整顶部横条和断条，不缩小标题字号。
8. 从固定起点排入 `PART 1 Reading&Dialogue`。
9. Reading 音标转为红色 `[...]`。
10. 排入 Dialogue 说明框、角色说明和对话正文。
11. 根据 Reading 内容高度调整 Reading 绿线边框下线。
12. 根据 Dialogue 内容高度调整黄色底框和左侧绿线。
13. 根据当前 y 坐标动态放置 `PART 2 Vocabulary&Idioms`。
14. Vocabulary 使用四列表格，奇偶行底色交替，词条不可拆页。
15. 根据当前 y 坐标动态放置 `PART 3 Grammar points`。
16. Grammar 按段落顺序排，行距 24 px。
17. Grammar 标题下第一句橙色文字在 PS 中保持橙色斜体。
18. Word 无小标题时隐藏小绿标题组。
19. 根据当前 y 坐标动态放置 `PART 4 Exercise`。
20. Exercise 翻译题按完整题块生成，题目和答题线不可拆分。
21. 当前页空间不足时，复制后续页页壳继续排。
22. 每个文本框写入后检查是否溢出。
23. 溢出时按段落 / 词条 / 题块拆分。
24. 保存新 PSD，不覆盖模板。
25. 导出 JPG 预览。
26. 第一轮先生成 1 个 Lesson 完整页面，确认样式后再批量生成 37 个 Lesson。

---

## 19. 最终目标结构

最终系统应形成：

```text
2 种页面壳
+
若干可复用内容模块
+
动态分页引擎
+
PSD 样式复制机制
+
Word 结构化解析机制
```

页面壳只负责页面基础视觉；Part 模块负责教材内容；JSX 根据内容高度动态生成页面。这样可以适配 37 个 Lesson 中每课内容长短不同的问题。


---

## 20. 本次合并修正说明（2026-06-11）

本文件为执行版规则，合并依据如下：

- 以 `PSD_layer_rename_SAFE_JSX_scripts_最终MD同步版/Word内容自动排版到PSD_最终规则说明_图层名已同步.md` 为主规则。
- 桌面 `Word到PSD自动排版_Codex直接执行极简版_37Lesson批量版.md` 作为执行摘要，不作为最终图层名依据。
- 所有 Photoshop 自动排版脚本必须以第 6 节中的 `@SHELL_*`、`@PART*_*`、`@PAGE_*`、`@LESSON_*` 新图层名为准。
- 旧图层名或旧伪代码名不得再使用，包括 `@HEADER_LESSON_NO`、`@HEADER_LESSON_TITLE`、`@HEADER_GREEN_BAR`、`@STYLE_ROOT`。
- 所有字体、字号、颜色、行距、段落格式以 PSD 内部实测图层为准；MD 中的数字如果与 PSD 实测冲突，以 PSD 为准。

## 21. PS 内部验证要求

正式排版前必须先运行 Photoshop 内部图层验证：

```text
输入 PSD：
C:\Users\Administrator\Desktop\中级美语\3-4 1.psd
C:\Users\Administrator\Desktop\中级美语\3-4 2.psd
C:\Users\Administrator\Desktop\中级美语\3-4 3.psd
C:\Users\Administrator\Desktop\中级美语\3-4 4.psd
C:\Users\Administrator\Desktop\中级美语\3-4 5.psd

输出报告：
C:\Users\Administrator\Desktop\中级美语\PS内部图层验证报告.json
C:\Users\Administrator\Desktop\中级美语\PS内部图层验证报告.md
```

验收标准：

- 5 个 PSD 都能由 Photoshop 打开。
- manifest 中 367 个模板图层名都能在对应 PSD 内找到。
- 缺失图层数必须为 0。
- 若 Photoshop 内存在重复图层名，应在正式排版脚本中使用父组路径或 manifest 类型辅助定位，避免误取同名层。

## 22. 当前文件核对结果

已通过静态核对：

- manifest 文件数：5
- manifest 图层映射总数：367
- 每个模板 manifest 内部无重复新图层名
- Word 可识别 Lesson 数量：37
- Word 可识别 Part 1 / Part 2 / Part 3 / Part 4 数量：均为 37

最终是否可执行，以 Photoshop 内部验证报告为准。
