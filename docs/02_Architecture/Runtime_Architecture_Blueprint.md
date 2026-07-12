# Runtime Architecture Blueprint

**Version:** v1.0  
**Status:** Draft  
**Last Updated:** 2026-07-12  

## 1. Purpose（文档目的）
定义 AI Narrative RPG Engine 的运行时生命周期和核心运行机制。

它回答：
- 一个 Scene 如何完整运行？
- 世界状态、Relationship、Memory 如何演化？
- Narrative Director 如何决策？
- 数据如何在各模块间流动并持久化？

本文档是所有具体 Layer 文档（Scene Engine、Simulation Layer、Relationship Engine 等）的运行时基础。

## 2. Responsibilities（职责）
- 定义 Runtime Flow 和 State Transition
- 定义 Scene 生命周期
- 定义模块调用顺序和职责边界
- 定义运行时保证（Runtime Guarantees）

**不负责**：
- 具体数据 Schema
- Prompt 模板
- UI 实现
- 模型具体优化

## 3. Runtime Principles（运行时原则）
- Simulation Before Generation
- State Before Text（状态是事实，文本是表现）
- Scene Is Atomic Unit（Scene 是最小不可分割运行单位）
- Memory Is Selected History（保存有价值经历，而非全部对话）
- Relationship Is Core Driver（关系驱动一切体验）

## 4. Runtime Lifecycle（运行时生命周期）

一次完整 Scene 的运行流程：

**Player Action**  
↓  
**Scene Start**  
↓  
**Context Assemble** (加载 State)  
↓  
**Simulation Tick**  
↓  
**Relationship Update**  
↓  
**Narrative Planning**  
↓  
**Generation** (LLM + Image)  
↓  
**Evaluation**  
↓  
**Memory Extraction**  
↓  
**Persistence**  
↓  
**Scene Complete** → **Next Scene**

## 5. Runtime State Model（运行时状态模型）
核心状态包括：
- Character State
- **Relationship State**（核心）
- World State
- Scene State
- Memory State
- Timeline State

## 6. Scene State Machine（Scene 状态机）
- Created
- Initialized
- Simulating
- Planning
- Generating
- Completed
- Archived

## 7. Relationship Runtime（关系运行时）
定义 Relationship 如何影响：
- Event Probability
- Dialogue Tone
- Scene Availability
- Character Behavior

## 8. Narrative Director Runtime（叙事导演运行时）
负责：
- Goal Selection
- Event Selection
- Story Pacing
- Emotional Timing

**不负责**：文本生成

## 9. Generation Pipeline（生成流水线）
- LLM：负责表达（Dialogue、Description）
- Image Model：负责视觉呈现（CG）
- **禁止**：模型直接改变世界状态

## 10. Memory Pipeline（记忆流水线）
- Experience → Importance Evaluation → Memory Creation → Embedding/Index → Future Retrieval

## 11. Failure Handling（失败处理）
定义 Generation Failed、Model Timeout、State Conflict 等的恢复策略。

## 12. Hardware Considerations（硬件考量）
针对 RTX 5060 8GB：
- Sequential Generation
- Model Switching
- Image Async Queue

## 13. Runtime Guarantees（运行时保证）
- 每个 Scene 完成后必须更新 Relationship 和 Memory
- 所有长期状态变化必须经过 Simulation Layer
- State 必须可恢复、可追溯

## References
- **Depends On**：Overall Architecture, Glossary, Project Vision
- **Referenced By**：Scene Engine, Simulation Layer, Relationship Engine, Memory Architecture, Narrative Director, Image Pipeline

## Revision History
| Version | Date | Author | Description |
|---------|------|--------|-------------|
| v1.0 | 2026-07-12 | - | 初始 Blueprint |
