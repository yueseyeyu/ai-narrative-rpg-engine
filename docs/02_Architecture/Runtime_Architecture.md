# Runtime Architecture

**Version:** v1.0  
**Status:** Draft  
**Last Updated:** 2026-07-12  

## 1. Purpose（文档目的）
本文档定义 AI Narrative RPG Engine 的**运行时架构**（Runtime Architecture），即一次完整体验（Scene）如何在 Engine 内执行。

它是 Overall Architecture 的运行时细化，是所有具体模块（Scene Engine、Simulation Layer、Relationship Engine、Memory Architecture 等）的共同基础。

## 2. Responsibilities（职责）
- 定义一次 Scene 的完整生命周期
- 定义状态转换规则和运行时保证
- 定义模块调用顺序和数据流动路径

**不负责**：具体数据结构、Prompt 模板、UI 实现、模型优化。

## 3. Engine Mental Model（引擎心智模型）⭐
**AI Narrative RPG Engine 不是一个文本生成系统，而是一个拥有生成接口的状态模拟系统。**

- **Simulation** 是真实世界
- **Narrative Director** 是导演
- **LLM / Image Model** 是演员
- **Persistence** 是记忆与历史

文本和图片只是**表现层**，状态才是**事实层**。

## 4. Runtime Core Concepts（运行时核心概念）
- **Scene**：最小原子叙事模拟事务（Atomic Narrative Simulation Transaction）
- **State**：当前世界真实状态
- **Snapshot**：Scene 开始时的状态快照
- **Transition**：状态变更（由 Simulation 驱动）

## 5. Scene Lifecycle（Scene 生命周期）⭐⭐⭐
一次完整 Scene 的运行流程：

**Player Action**  
↓  
**Scene Start**  
↓  
**Context Assembly** (加载 Snapshot)  
↓  
**Simulation Tick**  
↓  
**Relationship Evaluation & Update**  
↓  
**Narrative Director Planning**  
↓  
**Generation** (LLM + Optional Image)  
↓  
**Evaluation**  
↓  
**Memory Extraction**  
↓  
**State Persistence** (Commit)  
↓  
**Scene Complete** → **Next Scene**

## 6. Scene State Machine（Scene 状态机）⭐⭐⭐
- Created
- Initialized
- Context Loaded
- Simulating
- Directing
- Generating
- Evaluating
- Memory Processing
- Committed
- Archived

## 7. Context Assembly（上下文组装）
从 Persistence 加载当前 Character State、Relationship State、World State、Relevant Memory 等。

## 8. Simulation Runtime（模拟运行时）
Simulation Layer 根据当前状态和玩家行动计算可能的事件、Relationship 变化趋势、Character 内部状态更新。

**Simulation Layer owns:**
- State transition
- Rule evaluation
- Relationship calculation

**Simulation Layer does NOT:**
- Generate dialogue
- Generate images
- Decide final narrative presentation

## 9. Relationship Runtime（关系运行时）⭐
Relationship State 是整个 Runtime 的核心驱动因素，直接影响 Event 概率、Dialogue 基调、Scene 类型等。

## 10. Narrative Director Runtime（叙事导演运行时）
**Input:** Current State, Relationship State, Timeline, Active Goals  
**Output:** Event Proposal, Scene Direction, Emotional Target, Generation Intent

负责高层决策，不负责文本生成。

## 11. Generation Runtime（生成运行时）
- Prompt Builder 将结构化状态转为 Prompt
- LLM 生成对话与叙述
- Image Model 生成 CG（异步）

**Generation output is temporary expression. Only committed state becomes permanent reality.**

## 12. Memory Runtime（记忆运行时）
Scene 结束后评估重要性、提取高价值经历并存入 Persistence。

## 13. Persistence Runtime（持久化运行时）
Scene 结束时统一 Commit 所有长期状态。

## 14. Failure Recovery（失败恢复）
定义 Generation Failed、Model Timeout、State Conflict 等的处理策略。

## 15. Hardware Runtime Strategy（硬件运行时策略）
针对 RTX 5060 8GB：
- LLM 与 Image Model 严格串行
- Image Generation 异步队列
- 非核心任务后台执行

## 16. Runtime Guarantees（运行时保证）
- 每个 Scene 必须完整 Commit 状态后才能进入下一 Scene
- 所有长期状态变更必须经过 Simulation Layer
- Relationship 和 Memory 永远保持一致性

## References
- **Depends On**：Overall Architecture, Glossary
- **Referenced By**：Scene Engine, Simulation Layer, Relationship Engine, Memory Architecture, Narrative Director 等

## Revision History
| Version | Date | Author | Description |
|---------|------|--------|-------------|
| v1.0 | 2026-07-12 | - | 初始版本 |
