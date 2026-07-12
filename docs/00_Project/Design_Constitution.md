# Design Constitution（项目设计宪法）

**Version:** v1.0
**Status:** Draft
**Last Updated:** 2026-07-12

---

# Purpose（文档目的）

本文档是 **AI Narrative RPG Engine** 项目的最高设计原则（Project Design Constitution）。

它不是产品需求文档（PRD），不是系统架构文档，也不是开发规范。

它定义的是整个项目未来所有设计必须遵守的核心原则。

所有产品设计、架构设计、数据结构、Prompt 设计、Image Pipeline、模型接入、GPU 调度等，都必须首先符合本宪法。

当不同设计发生冲突时，应优先遵循本宪法。

本宪法原则上保持长期稳定，仅当项目核心理念发生根本变化时才应修改。

---

# Article 0 — Why This Project Exists（项目为什么存在）

本项目致力于在**消费级硬件**上，为玩家创造属于自己的、能够长期演化的数字人生。

我们不是在开发一个 AI 聊天工具。

我们是在构建一个**本地 AI Narrative RPG Engine（AI 叙事 RPG 引擎）**。

在这个世界中：

* 角色能够成长；
* 关系能够自然演化；
* 故事能够持续推进；
* 世界能够留下痕迹；
* 回忆能够永久保存。

玩家不是在使用 AI。

玩家是在经历一段值得回忆的人生。

---

# Design Principles（设计原则）

---

## Article 1 — Long-term Immersion First（长期沉浸优先）

长期沉浸体验是整个项目的最高目标。

所有设计都应首先回答一个问题：

> **它是否能够提升玩家长期体验？**

如果答案是否定的，则降低其优先级。

模型能力、回复质量、生成速度都只是实现沉浸体验的手段，而不是目标。

---

## Article 2 — Simulation Before Generation（模拟优先于生成）

系统应始终遵循：

> **Simulation → Narrative Director → Prompt → LLM**

而不是：

> Prompt → LLM → Story

世界、关系、剧情、事件首先由结构化模拟系统维护，再由 Narrative Director 决策，最后由 LLM 负责自然语言表达。

AI 不负责创造世界。

AI 负责表达世界。

---

## Article 3 — Relationship First（关系优先）

Relationship 是整个系统最重要的长期状态。

剧情推进、角色成长、Quest、Scene、CG、Memory，都必须围绕 Relationship 演化。

玩家真正记住的，不是地图，而是人与人之间发生的故事。

---

## Article 4 — Character Is a Persistent Asset（角色是永久资产）

Character 是整个项目最重要的数字资产。

角色不是 Prompt。

不是聊天记录。

不是 JSON。

角色应具备：

* 长期成长；
* 人格一致；
* 持续记忆；
* 长期关系；
* 跨世界复用能力。

未来，无论进入任何世界，角色都应保持自身连续性。

---

## Article 5 — Story Before Intimacy（剧情先于亲密）

所有亲密互动都必须建立在剧情发展与关系成长基础之上。

任何亲密场景都应来源于：

* Relationship
* Scene
* Quest
* Event

而不是通过 Prompt 直接生成。

故事推动关系。

关系推动情感。

情感推动亲密。

---

## Article 6 — Emotion Before Content（情感优先于内容）

系统应优先构建真实、自然、长期发展的情感过程。

例如：

* 信任；
* 羞涩；
* 依赖；
* 吃醋；
* 占有欲；
* 救赎；
* 成长；
* 告白。

在 Mature Profile 下，这一原则尤为重要。

真正优秀的成人体验，并非来源于内容本身，而是来源于长期情感积累后的自然释放。

**情感是推动内容发展的原因，而内容只是情感发展的结果。**

---

## Article 7 — Scene Is the Smallest Runtime Unit（Scene 是最小运行单位）

系统运行的最小单位不是 Message，而是 Scene。

每个 Scene 都应包含：

* 时间；
* 地点；
* 参与角色；
* 当前目标；
* 情绪状态；
* Relationship Snapshot；
* Memory Snapshot。

所有长期状态统一在 Scene 结束后更新。

---

## Article 8 — Narrative Director Controls Story（Narrative Director 掌控故事）

Narrative Director 是整个系统的剧情控制中心。

Narrative Director 负责：

* 剧情推进；
* 节奏控制；
* Scene 规划；
* Quest 演化；
* Relationship 调整；
* CG Trigger。

LLM 不负责长期规划。

LLM 负责生动表达。

Python 永远拥有故事控制权。

---

## Article 9 — CG Is a Story Reward（CG 是剧情奖励，也是回忆载体）

CG 属于剧情，而不是聊天配图。

每一张 CG 都应记录一个值得纪念的重要时刻。

CG 必须绑定：

* Scene；
* Character Snapshot；
* Relationship Snapshot；
* Emotion；
* Image Blueprint。

玩家未来重新浏览 Gallery 时，应能够重新回忆当时发生的故事，而不仅仅是看到一张图片。

CG 是玩家长期数字回忆的重要组成部分。

---

## Article 10 — Consumer Hardware First（消费级硬件优先）

本项目默认开发目标为消费级 PC。

当前参考平台为：

* NVIDIA RTX 5060 8GB
* 32GB RAM

所有设计必须首先保证：

* 单模型运行；
* GPU 串行调度；
* 本地离线运行；
* 显存安全；
* 可接受的响应速度。

任何超过硬件预算的设计，都必须提供降级方案。

---

## Article 11 — Python Owns Logic, LLM Owns Expression（Python 管逻辑，LLM 管表达）

Python 负责：

* World；
* Relationship；
* Quest；
* Timeline；
* Event；
* Memory；
* Narrative Director。

LLM 负责：

* Dialogue；
* Description；
* Emotion；
* Narrative Rendering。

LLM 永远不是游戏引擎。

---

## Article 12 — Data Before Prompt（数据优先于 Prompt）

所有长期状态必须保存为结构化数据。

Prompt 只是渲染层，而不是数据层。

Character、Relationship、World、Scene、Quest、Memory、Image Blueprint 等核心状态，都必须独立保存。

未来更换任何模型，都应继续使用同一套数据资产。

---

## Article 13 — Content Profile Is Configuration（内容模式只是配置）

General、Romance、Mature 等属于同一套 Narrative Engine。

它们不是不同系统，而是不同的 Content Profile。

**Mature Profile 是本项目的重要产品方向之一。**

它面向成年玩家，目标是提供高质量、长期沉浸式的角色互动与剧情体验。

Mature Profile 必须通过以下模块共同实现：

* Relationship Engine；
* Narrative Director；
* Scene Engine；
* Image Pipeline；
* Image Blueprint。

严禁依赖独立代码分支或 Prompt 堆砌实现 Mature 功能。

所有 Mature 体验都必须严格遵循：

* Story Before Intimacy；
* Emotion Before Content。

---

## Article 14 — Efficient GPU Scheduling（高效 GPU 调度）

GPU 是整个系统最宝贵的资源。

所有 GPU 任务都应采用：

* 串行执行；
* 异步排队；
* 智能调度；
* 显存预算管理。

目标是在消费级硬件限制下，最大化 GPU 利用率，同时尽可能减少玩家等待时间，保护沉浸体验。

---

## Article 15 — Model Agnostic & Forward Compatibility（模型无关与向前兼容）

整个引擎必须保持模型无关（Model Agnostic）。

未来可以自由替换：

* LLM；
* 图片模型；
* LoRA；
* 推理框架；
* GPU Backend。

而无需修改：

* Narrative Engine；
* Data Schema；
* Business Logic。

模型会不断进步。

引擎必须保持稳定。

---

# Closing Statement（结语）

AI Narrative RPG Engine 希望构建的，不是一个聊天软件。

而是一个能够陪伴玩家长期成长、共同创造故事、记录回忆，并最终形成属于玩家自己的数字世界的本地 AI 叙事引擎。

角色会成长。

关系会变化。

故事会继续。

世界会留下痕迹。

而那些重要的瞬间，将以剧情、关系、回忆与 CG 的形式，永久属于玩家。

**模型会不断更新，算法会不断进步，而属于玩家的故事、角色与回忆，应当能够一直延续。**
