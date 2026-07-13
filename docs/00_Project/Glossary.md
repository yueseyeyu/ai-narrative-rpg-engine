# Glossary（项目术语标准）

**Version:** v3.0  
**Status:** Active  
**Last Updated:** 2026-07-13

---

## Purpose（文档目的）

本文档是 AI Narrative RPG Engine 项目的**唯一术语标准**（Glossary / 术语宪法）。所有其他文档必须严格引用本文件定义。

## Responsibilities（职责）

- 建立统一语言体系
- 消除术语歧义
- 保证跨文档一致性
- 为后续所有文档提供语义基础

## In Scope

核心概念的正式定义、命名规则、禁止术语

## Out of Scope

具体实现细节、代码示例、Prompt 模板

## Document Governance（文档治理）

**Owner:** Chief Architect  
**Reviewers:** Product Architect, Engine Architect  
**Approval:** Architecture Review Required  
**Update Policy:** Only update after ADR approval if core meaning changes.  
**Stability Level:** Stable（核心术语） / Experimental（新术语）

---

## Naming Principles（命名原则）

- 一个概念只能有一个正式名称（One Concept, One Name）
- 优先使用英文作为正式术语
- 避免同义词混用
- 变量/字段使用 snake_case
- 类/模块使用 PascalCase

---

## Forbidden Terms（禁止术语）

| Forbidden | Use Instead | Reason |
|-----------|-------------|--------|
| Conversation | Scene | 对话不是最小运行单位，Scene 才是 |
| Chat History | Memory | 聊天记录不是记忆，结构化经历才是 |
| Image Prompt | Image Blueprint | 图像生成依赖结构化蓝图，而非裸 Prompt |
| NPC Memory | Character Memory | 所有角色记忆统一为 Character Memory |
| Runtime Context | Runtime State | 统一使用 Runtime State 作为运行时状态的正式名称 |
| Current Context | Runtime State | 同上 |
| Scene Runtime | Runtime State | 同上 |
| Behavior Tendencies | Behavior Tendency | 统一使用单数形式 |
| Behavior Profile | Behavior Tendency | 统一使用 Behavior Tendency |
| State Context | Runtime State | 统一使用 Runtime State |

---

## Core Terminology（核心术语）

### Engine（引擎）

整个 AI Narrative RPG Engine 的统称。包含 Simulation、Narrative Director、Prompt Builder、Renderer、Persistence 等全部模块。Engine ≠ LLM。

### Character（角色）

玩家长期拥有的数字角色资产。具有持续身份、人格、成长能力和长期记忆。可跨世界复用，是项目最重要的长期资产之一。

### Relationship（关系）

角色之间持续演化的多维度长期状态（Trust、Affection、Dependence、Intimacy、Jealousy 等）。是剧情推进的核心驱动力。

### Scene（场景）

系统最小运行单位（Smallest Runtime Unit）。包含时间、地点、角色、状态、Dialogue、Event。所有长期状态在 Scene 结束时统一更新。

### Memory（记忆）

经过筛选的高价值经历集合。是玩家真正的长期资产，而非原始聊天记录。

### Narrative Director（叙事导演）

负责剧情规划、节奏控制、Event 选择、Relationship 演化策略。不负责自然语言生成。

### Mature Profile（成人体验配置）

Content Profile 的一种。面向成年用户，提供基于长期 Relationship 发展的亲密互动体验。核心原则：Story Before Intimacy、Emotion Before Content、Relationship Driven。

---

## Runtime Terminology（运行时术语）

### Runtime State（运行时状态）

Engine 在运行时维护的全部长期状态的统称。包括 Character State、Relationship State、World State、Scene State、Memory State、Timeline State。

Runtime State 是 Engine 中唯一的事实来源（Ground Truth）。所有生成内容都建立在 Runtime State 之上。

**禁止混用：** Runtime Context、Current Context、Scene Runtime、State Context。统一使用 Runtime State。

**引用文档：** Simulation Layer Blueprint、Relationship Engine Blueprint、Memory Architecture Blueprint、Prompt Builder Blueprint、LLM Runtime Blueprint

---

### Relationship State（关系状态）

Relationship Engine 管理的多维度持久化关系数据。是 Runtime State 的核心组成部分。

Relationship State 不是单一分数，而是由 Trust、Respect、Familiarity、Attachment、Affection、Intimacy 等独立维度组成的结构化状态。

Relationship State 驱动叙事规划、对话基调、场景可用性、CG 触发等运行时行为。

**引用文档：** Relationship Engine Blueprint、Narrative Director Blueprint、Simulation Layer Blueprint

---

### Simulation Tick（模拟 Tick）

Simulation Layer 的最小执行单元。每个 Scene 必须且仅执行一次 Simulation Tick。

一个 Simulation Tick 包含：加载状态 → 应用玩家行为 → 角色更新 → 关系评估 → 规则评估 → 事件解析 → 状态转换 → 一致性验证。

一个 Simulation Tick 必须产出且仅产出一个经过验证的 State Transition。

**引用文档：** Simulation Layer Blueprint、Runtime Architecture Blueprint、Scene Engine Blueprint

---

### Behavior Tendency（行为倾向）

Relationship Engine 产出的结构化运行时输出，描述角色当前最可能采取的行为倾向，而不是最终行为。

Behavior Tendency 包含 willingness_to_help、hostility、openness、initiative 等量化指标，以及 tone_modifier 和 suggested_actions 等建议。

Behavior Tendency 指导 Narrative Director 的叙事决策，但不直接生成对话。

**禁止混用：** Behavior Tendencies（复数）、Behavior Profile。统一使用 Behavior Tendency。

**引用文档：** Relationship Engine Blueprint、Narrative Director Blueprint、Prompt Builder Blueprint

---

### Narrative Goal（叙事目标）

Narrative Director 为每个 Scene 设定的单一主要叙事目标。如 Build Trust、Increase Suspense、Deepen Relationship 等。

Narrative Goal 只影响呈现方式，永远不改变 Simulation Result。

每个 Scene 必须有且仅有一个 Primary Narrative Goal。

**引用文档：** Narrative Director Blueprint、Prompt Builder Blueprint

---

### Experience Plan（体验计划）

Narrative Director 产出的结构化叙事规划。包含事件排序、情感编排、角色焦点、对话风格、CG 决策等。

Experience Plan 是确定性输出 — 给定相同的 Runtime State 和 Simulation Result，产出相同的 Experience Plan。

Experience Plan 指导 Prompt Builder 的组装逻辑，但不包含任何具体文本。

**引用文档：** Narrative Director Blueprint、Prompt Builder Blueprint

---

### Prompt Package（Prompt 包）

Prompt Builder 产出的结构化提示词包。由 System Prompt、Character Context、Relationship Context、Scene Context、Memory Context、Narrative Goal、Style Instructions、Constraints、Output Schema、Metadata 等模块化 Block 组成。

Prompt Package 是一次性的 — 每次 Scene 执行时从 Runtime State 重新构建，不缓存不复用。

Prompt Package 不包含任何业务逻辑，仅描述事实。

**引用文档：** Prompt Builder Blueprint、LLM Runtime Blueprint

---

### Memory Activation（记忆激活）

Memory System 的核心机制，决定哪些记忆在运行时推理中被激活。

Memory Activation 不直接检索记忆，而是调整记忆参与运行时推理的概率。

激活触发器包括：当前场景、情感上下文、关系状态、叙事目标、玩家行为、环境线索。

Memory Activation 修改检索优先级，但不改变历史事实，也不创建新记忆。

**引用文档：** Memory Architecture Blueprint、Narrative Director Blueprint

---

## Module Terminology（模块术语）

### Simulation Layer（模拟层）

Engine 中唯一有权演化 Runtime State 的核心模块。负责状态转换、规则评估、事件解析和一致性验证。

### Relationship Engine（关系引擎）

Simulation Layer 内的核心子系统。负责关系状态演化、行为倾向产出和关系约束生成。

### Narrative Director（叙事导演）

故事编排层。将模拟结果转化为连贯的叙事体验。负责叙事规划、情感编排、事件选择。

### Prompt Builder（Prompt 构建器）

翻译层。将结构化 Runtime State 转化为模型就绪的 Prompt Package。不引入业务逻辑。

### LLM Runtime（LLM 运行时）

模型抽象与推理基础设施。隐藏不同提供商实现，暴露统一推理接口。

### Scene Engine（场景引擎）

核心执行容器。协调一次完整的叙事模拟事务（Atomic Narrative Simulation Transaction）。

### Memory System（记忆系统）

长期体验持久化层。将完成的 Scene 转化为结构化、持续演化的记忆。

---

## References

**Depends On:**

- Design Constitution
- Project Vision

**Referenced By:**

- PRD
- All Architecture Overviews
- All Architecture Blueprints
- All Data Schemas
- All Development Documents

---

## Revision History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| v3.0 | 2026-07-13 | - | Architecture Cleanup: 添加 8 个核心运行时术语（Runtime State、Relationship State、Simulation Tick、Behavior Tendency、Narrative Goal、Experience Plan、Prompt Package、Memory Activation），扩展 Forbidden Terms，添加模块术语 |
| v2.0 | 2026-07-12 | - | 增加工程化元数据、治理规则、Forbidden Terms |
