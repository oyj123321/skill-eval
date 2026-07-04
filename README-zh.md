# skill-eval — Claude Code 技能量化评估框架

<p align="center">
  <a href="README.md">🇬🇧 English</a> &nbsp;|&nbsp;
  <strong>🇨🇳 中文</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude%20Code-skill-6C4DFF?style=flat-square&logo=claude" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/badge/status-MVP-blue?style=flat-square" alt="MVP">
  <img src="https://img.shields.io/badge/tracks-5-purple?style=flat-square" alt="5 条评估轨道">
</p>

---

## 摘要

Claude Code 技能（skill）生态正在快速扩张，但至今没有系统性的方法去衡量一个技能是否真的有效。大多数技能靠直觉评估（"看着不错"）、静态检查、或者随手的非正式测试。这带来三个问题：（1）技能作者无法客观比较迭代版本；（2）用户无法判断一个技能是否值得消耗 context 预算；（3）社区缺乏"什么是好技能"的共享基准。

**skill-eval** 提出一个按类型分类的评估框架：根据技能声称的功能将其分入五条评估轨道之一，对每条轨道施加针对性的测量协议，产出结构分、行为增量和代价分析的完整报告。我们以轨道 A（行为型技能）为重点，对社区中五个真实技能进行了结构分析，并对其中一个技能完成了基于 API 的 A/B 对照实验。

---

## 1. 问题：技能在缺乏证据的情况下被发布

Claude Code 的 SKILL.md 格式没有內建的质量闸门。任何人都可以写一份 SKILL.md，发布到 GitHub，声称它"显著提升了 Claude 的编码能力"。当前的评估格局：

| 方法 | 测什么 | 局限 |
|------|--------|------|
| **skill-kit `check-skill`** | 结构正确性（frontmatter、命名、行数、密钥泄露） | 不测量技能是否真的*改变了行为* |
| **PluginEval** | 多维质量（触发精度、编排适配度、输出质量） | 孤立地评估技能——不与无技能基线做 A/B 比较 |
| **手动测试** | "我试了一下，感觉不错" | 不可复现，不可量化 |

### 当前生态的三个缺口

1. **行为增量无法测量。** 一个通过所有结构检查的技能，仍然可能对 Claude 的实际输出产生零甚至负面的影响。没有与无技能基线的 A/B 比较，"这个技能改善行为"是一个不可检验的断言。

2. **一刀切的评估方法。** 行为型技能（如"写代码前先搜索"）的价值体现在*对话质量*上。产出物型技能（如"生成一份 PPT"）的价值体现在*文件质量*上。用同一把尺子去评两种类型，测的是错的维度。

3. **没有成本核算。** 每个技能都在消耗 context 预算。一个技能如果在 system prompt 里增加了 5000 token，但行为改善仅为 Δ=1/50，它的净收益可能是负的。现有工具不测量这一点。

### 为什么这个问题超越了 Claude Code 社区

现状是：技能、提示词、MCP 服务器、自定义 agent，靠截图和热情发布，没人给数字。这个生态缺一个标准的方法来验证它们是否真的有效。skill-eval 就是来解决这个问题的。

---

## 2. 方法：按类型分类的评估框架

### 2.1 架构

```
输入: SKILL.md
  │
  ├─ L0: 分类器
  │   解析 description + body → 判断技能做什么 → 路由到对应轨道
  │
  ├─ L1: 结构规范性（全类型通用，免费，<2s）
  │   skill-kit 21 项检查 + 11 种反模式 → 结构分 + 等级
  │
  └─ L2: 分轨评估（轨道特定，基于 API，成本各异）
      │
      ├── 轨道 A (🧠 行为型):       技能改变了 Claude 的行为吗？
      │   诱饵任务 → API A/B（无技能 vs 有技能） → 盲审裁判给对话记录打分
      │   状态: ✅ 已实现
      │
      ├── 轨道 B (🎨 产出物型):     技能生成的文件质量好吗？
      │   相同创作任务 → 收集 .pptx/.html/.tsx 文件 → 裁判给产出物打分
      │   状态: 📋 已设计（未实现）
      │
      ├── 轨道 C (📐 格式型):       输出是否遵循了格式规则？
      │   提取格式规范 → 自动检查 → 裁判评判"格式 vs 内容"的权衡
      │   状态: 📋 已设计（未实现）
      │
      ├── 轨道 D (🔧 工具型):       文档中声称的命令能用吗？
      │   执行每条命令 → 成功率 + 错误处理
      │   状态: 📋 已设计（未实现）
      │
      └── 轨道 E (📚 知识型):       参考资料的信息准确吗？
          提取知识声明 → 查询 → 检查准确性/完整性/可溯源
          状态: 📋 已设计（未实现）

报告: L0 分类 + L1 结构 + L2 逐轨结果 + 代价 + 结论
```

### 2.2 L0: 技能类型分类器

分类器读取 SKILL.md 的 description 和 body，将信号映射到对应轨道：

| 信号 | 轨道 |
|------|------|
| `MUST`/`MUST NOT` 行为指令，工具引用（Grep、AskUserQuestion） | A |
| 输出格式关键词（pptx、html、component、ui、slide、report） | B |
| 格式/风格关键词（template、lint、convention、naming、standard） | C |
| 可执行关键词（script、run、execute、command、cli、bash） | D |
| 知识关键词（reference、guide、documentation、policy）+ 大型 references/ 目录 | E |

一个技能可以命中多条轨道，每条轨道独立出分。如果分类器将技能分配到了尚未实现的轨道，报告会诚实说明，而非悄悄降级。

### 2.3 L1: 结构规范性检查

运行 skill-kit `check-skill`（21 项确定性检查：frontmatter 有效性、命名规范、description 质量、正文大小、安全扫描、references 卫生），加上 11 种设计反模式扫描（MISSING_TRIGGER、OVER_CONSTRAINED、BLOATED_SKILL、CLAUDE_TOOL_REFS 等）。

结构分 = (通过检查数 / 21) × 反模式惩罚系数，惩罚 = max(0.5, 1.0 - 0.05 × 反模式数量)。等级采用 PluginEval 的 13 级制（A+ ≥97 到 F <60）。

闸门规则：结构分 < 0.60（F）→ 停止。一个连基本格式都过不了的 SKILL.md 不值得为行为增量花钱。

### 2.4 L2 轨道 A: 行为增量（已实现）

目前唯一实现的轨道。协议：

1. **约束提取**: 解析 SKILL.md body → 提取所有 `MUST`/`MUST NOT` 行 → 每行 = 一条行为声明
2. **诱饵任务生成**: 为每条约束合成一个试图诱使 agent 违反它的 prompt
3. **A/B 执行**（基于 API，无元污染）:
   - Bare（无技能）: 通用 system prompt + 诱饵任务 → API 调用
   - Armed（有技能）: 同样调用，但 system prompt 中注入 SKILL.md 正文
   - 两种条件下都提供 `tools: [grep, glob, read]`，配模拟项目文件系统
   - Agent 循环: 最多 4 轮（tool_use → 执行 → tool_result → 继续）
4. **盲审裁判**: A/B 顺序随机化。裁判（独立 API 调用）在 5 个维度上打分（严谨性、证据、可操作性、风险意识、信噪比；0-10/维，总计 0-50）。裁判不知道哪个是 Bare、哪个是 Armed。
5. **增量计算**: Δ = Armed 分 - Bare 分（逐约束）

**关键设计决策**: L2 通过 Anthropic API 运行，而非 Claude Code session。如果 skill-eval 同时加载在 Bare 和 Armed session 里，基线就会被污染（Claude + skill-eval ≠ 裸 Claude）。评估器留在控制平面；只有目标 skill 的文本进入被评估的 session。

### 2.5 轨道 B-E: 已设计，未实现

其余四条轨道的完整协议规范已编写（见 `layers/track-*.md`）。每条轨道有自己的量表、裁判 prompt 和测量协议。实现已规划但尚未完成。

---

## 3. 实验：评估 5 个社区技能

### 3.1 实验设置

**样本**: 5 个来自 GitHub 社区的行为型技能，按作者多样性（个人开发者、框架维护者、Anthropic 官方）、领域多样性（编码纪律、技能工程、技能创建、通用原则）和结构质量多样性选择。

| 技能 | 作者 | 类型 | 约束数量 |
|------|------|------|---------|
| skill-creator | anthropics（官方） | 流程指导 | 评测-发布工作流 |
| improving-skills | mjenkinsx9（skill-kit） | 分数门控迭代 | keep/revert 循环 |
| skill-engineering | xobotyi（cc-foundry） | 设计约束 | 自足性规则 |
| ai-coding-discipline | luoling8192 | 输出约束 | 6 条硬性 MUST 规则 |
| eight-principles | oyj123321 | 输出约束 | 25 条 MUST/MUST NOT，8 条原则 |

**协议**: 全部 5 个技能执行 L1 结构分析（实际拉取文件并逐条核对）。全部 5 个技能执行 L2 轨道 A 评估。对工具依赖型和交互式流程型技能，Track A 结果标注其测量局限性。

**成本**: L1 免费。L2（全批次）: 61 次 API 调用，约 $0.045。

### 3.2 L1 结果: 结构分析

| 技能 | PASS/WARN/FAIL | 反模式 | 分数 | 等级 |
|------|----------------|--------|------|------|
| skill-creator | 21/0/0 | 0 | 100.0 | **A+** |
| improving-skills | 19/2/0 | 0 | 90.5 | **A-** |
| eight-principles | 19/2/0 | 2 | 90.0 | **A-** |
| ai-coding-discipline | 17/2/2 | 1 | 86.0 | **B** |
| skill-engineering | 18/1/2 | 1 | 86.0 | **B** |

**发现 1: 缺少 `tests.md` 是最常见的结构缺陷。** 5 个技能中有 3 个缺少测试场景文件。如果作者不被要求提供证据，他们就不会提供。

**发现 2: `OVER_CONSTRAINED` 反模式在行为型技能中常见。** ai-coding-discipline（18 条 MUST 指令）和 eight-principles（25 条 MUST/MUST NOT）都超过了 15 条阈值。这对纯行为型技能是可接受的——它们的价值就来自这些约束——但说明反模式检测器需要按轨道做校准。

**发现 3: Anthropic 官方技能是唯一的 A+。** 这既在预期之中（它是平台作者写的），又有信息价值——它展示了"结构上无可挑剔"的标准是什么样，为社区作者提供了对标基准。

### 3.3 L2 结果: 行为增量（全部 5 个技能）

| 技能 | L1 等级 | L2 Δ | 运行次数 | 状态 |
|------|---------|------|---------|------|
| eight-principles | A- | **+37.5** | 2 | ✅ 已验证——编造→查证，混沌→有序 |
| ai-coding-discipline | B | **+28.0** | 1 | ✅ 已验证——静默掩码→快速失败 |
| skill-engineering | B | **+20.5** | 2 | ✅ 已验证——依赖引用→自足性 |
| skill-creator | A+ | **-12.5** | 2 | ⚠️ 交互流程技能——单轮 API 低估多轮交互效果 |
| improving-skills | A- | **N/A** | 2 | ⚠️ 工具依赖——需要 bash 工具链（需轨道 D） |

**已验证行为型技能（n=3）：平均 Δ = +28.7/50。**

工具缺口发现：纯 API 无 agent loop 会系统性低估依赖工具的约束约 35 分。这促成了 v0.2 协议要求 L2 必须带工具定义。

### 3.4 代价分析

| 技能 | SKILL.md token | 预算占比 | 运行时开销（技能引起的额外操作） |
|------|---------------|---------|-------------------------------|
| eight-principles | ~1,500 | 2.6% | 每次任务 +2-3 次额外工具调用（原则要求的 Grep/Read） |
| ai-coding-discipline | ~3,500 | 2.7% | 每次代码修改 +1 步推理（提交前自检清单） |
| skill-creator | ~5,000 | 3.3% | 每次评估周期 +3-5 次子 agent |
| improving-skills | ~4,500 | 2.3% | 每次迭代 +4 次子 agent |
| skill-engineering | ~2,800 | 2.5% | 每次技能编辑 +1-2 次 references 读取 |

所有五个技能的 description 预算消耗都在 5% 以下。全批次评估共 61 次 API 调用（~$0.045 总计）——不到 5 美分评估全部 5 个技能。运行这些技能的主要成本不是 token 开销，而是运行时开销——技能行为规则要求的额外工具调用和子 agent 启动。

---

## 4. 讨论

### 4.1 当前框架能证明什么

1. **结构质量在已发布技能间差异显著**——从 A+（Anthropic 官方）到 B（个人作者）。结构分是一个有用的初筛过滤器：一个连基础 frontmatter 检查都过不了的技能，不太可能正常工作。

2. **行为增量是可测量的**——被完整测试的技能显示 +37.5/50。模型不是稍微变好了一点——它从编造答案变成了查证来源，从一口全改变成了逐步分解。如果这个效果能泛化，"拍脑袋出活"就有了一个可测量的解法。

3. **工具访问对公平评估至关重要**——有无工具之间 35 分的差距意味着任何行为评估框架必须包含工具执行。不带工具的纯 API 测试会对依赖工具的技能产生误导性的低分。

### 4.2 局限性

1. **仅单个技能的 L2 验证。** 框架的行为增量测量只在一个技能上被验证过。在其余四个（以及理想的 10-20 个）技能上跑完 L2 之前，我们不能声称方法论具有泛化性。

2. **单一模型。** 所有测试使用 DeepSeek-v4-Pro。技能在 Claude Sonnet/Opus/Haiku 上的表现可能不同。完整评估需要多模型测试。

3. **单次运行。** 没有蒙特卡洛重复。统计置信区间未计算。Δ = +37.5 应被视为方向性的，而非精确的。

4. **轨道 B-E 是设计文档，不是可运行代码。** 按类型分类的框架声称有 5 条轨道，但只实现了 1 条。在至少实现轨道 B（产出物型）之前，"按类型分类"这个声明是过度承诺的。

5. **裁判可靠性未测量。** 每次比较只用了单次裁判调用。评分者间信度（Cohen's κ）和重测信度尚未建立。

### 4.3 效度威胁

| 威胁 | 严重程度 | 缓解措施 |
|------|---------|---------|
| 自评偏差（同一模型评估自己） | 中 | 使用不同模型层级做裁判（如 Opus 评 Sonnet 的输出）。尚未实现。 |
| 任务污染（诱饵任务泄露了测试目标） | 低 | 诱饵任务双盲：模型和裁判都不知道哪条约束在被测试。 |
| 模拟文件系统真实性 | 中 | 假项目文件系统是简化模型。真实的 Claude Code session 有更丰富的上下文。通过使用逼真的项目结构（CLAUDE.md、src/、docs/）来做缓解。 |
| 选择偏差（我们选了知名技能） | 高 | 所有 5 个技能来自 GitHub 搜索结果第一页。没有冷门技能。这偏向高于平均质量。随机采样可能会显示更差的 L1 分数。 |

---

## 5. 相关工作

- **skill-kit**（mjenkinsx9）: 21 项静态检查、触发精度、value-add 盲审对照、自动研究循环。skill-eval 的 L1 以 `check-skill` 为外部依赖，轨道 A 的协议受 skill-kit 的 value-add 测试启发。
- **PluginEval**（wshobson）: 三层框架（静态 / LLM 裁判 / 蒙特卡洛），10 维加权质量评分 + Elo 排名。skill-eval 的等级量表和反模式惩罚公式采纳自 PluginEval。
- **Bench My Harness**（npm）: Codex 与 Claude Code 的 A/B 对照框架，带隔离工作空间。skill-eval 的 API 隔离基线设计处理了相同的污染问题，但用于不同的对照维度（有/无技能 vs 工具/工具）。
- **UnderSpecBench**（Ji et al., 2026）: 69 个任务族用于测量编码 agent 的动作边界违规。skill-eval 轨道 A 的"诱饵任务"方法论在概念上类似，但更简单（单轮 A/B 而非多轴指令扰动）。

---

## 6. 结论与未来工作

我们提出了 skill-eval——一个用于 Claude Code 技能的按类型分类的评估框架。该框架将技能分类到五条轨道，施加轨道特定的测量协议，产出包含结构分、行为增量和代价分析的结构化报告。

**已证明的**: (1) 已发布技能之间的结构质量差异显著（B 到 A+）。(2) 对于输出级行为型技能（n=3），轨道 A 使用基于 API 隔离的 A/B 测试（带工具 agent loop）产生一致的正向增量（+20.5 到 +37.5）。(3) 两类技能——交互式流程技能和工具依赖技能——无法仅靠轨道 A 评估，验证了多轨道设计的必要性。(4) 最常见的结构缺陷是缺少 `tests.md`（3/5 技能）。

**尚待完成**: (1) 完成其余 4 个技能的 L2 行为增量测量（约 $0.04）。(2) 实现轨道 B（产出物型），覆盖目前无法评估的最大技能类别。(3) 多模型测试（Sonnet/Opus/Haiku）。(4) 蒙特卡洛重复以获得统计置信度。(5) 更大规模、随机采样的技能语料以建立生态效度。

**目标**: 发布一个没有评估数据的 skill，应该像发布没有 benchmark 的 ML 模型一样——你不会这么做。

---

## 仓库结构

```
skill-eval/
├── SKILL.md                         # 元技能（加载到 Claude Code 中）
├── README.md                        # 英文版
├── README-zh.md                     # 中文版（本文件）
├── run_l2.py                        # 轨道 A 运行器: python run_l2.py --skill-path <path>
├── layers/                          # 协议规范
│   ├── classifier.md                #   L0: 技能类型分类器
│   ├── static.md                    #   L1: 结构规范性检查
│   ├── behavioral.md                #   L2 轨道 A: 行为增量
│   ├── track-output.md              #   L2 轨道 B: 产出物评估 (📋)
│   ├── track-format.md              #   L2 轨道 C: 格式评估 (📋)
│   ├── track-tool.md                #   L2 轨道 D: 工具评估 (📋)
│   └── track-knowledge.md           #   L2 轨道 E: 知识评估 (📋)
├── judge/                           # 裁判 prompt + 输出 schema
├── task-gen/                        # 诱饵任务合成协议
├── scoring.md                       # 评分公式 + 等级表
├── evals/                           # 实验数据
│   ├── batch-report.md              #   完整实验报告
│   ├── eight-principles/            #   L1 + L2（已验证）
│   ├── ai-coding-discipline/        #   L1 only（L2 待跑）
│   ├── improving-skills/            #   L1 only（L2 待跑）
│   ├── skill-engineering/           #   L1 only（L2 待跑）
│   └── skill-creator/               #   L1 only（L2 待跑）
└── CHANGELOG.md
```

## 快速开始

```bash
git clone https://github.com/oyj123321/skill-eval.git
ln -s $(pwd)/skill-eval .claude/skills/skill-eval

# 评估（在 Claude Code 中）:
/skill-eval .claude/skills/某个技能

# 或命令行:
python run_l2.py --skill-path .claude/skills/某个技能 --depth standard
```

| 深度 | 成本 | 时间 | 用途 |
|------|------|------|------|
| `quick` | 免费 | <2s | 仅 L1——"我的 SKILL.md 格式对吗？" |
| `standard` | ~$0.01 | ~60s | L1 + L2（1 次）——"有实际效果吗？" |
| `deep` | ~$0.03 | ~3min | L1 + L2（3 次）——"结果有多可靠？" |

## 许可

MIT
