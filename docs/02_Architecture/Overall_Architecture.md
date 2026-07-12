# Overall Architecture

**Version:** v1.0  
**Status:** Draft  
**Last Updated:** 2026-07-12  

## 1. Purpose（文档目的）
本文档定义 **AI Narrative RPG Engine** 的整体技术架构。

它负责回答：
- Engine 由哪些核心层组成？
- 各模块承担什么职责？
- 数据如何流动？
- 一次完整体验如何运行？
- 为什么采用这种架构？

本文档是所有后续 Architecture、Data 和 Development 文档的最高级架构参考。

## 2. Responsibilities（职责）
- 定义系统整体结构与边界
- 定义运行时流程和核心数据流
- 保证产品 Vision 与技术实现一致

**不负责**：具体代码实现、数据库 schema、Prompt 模板、UI 设计。

## 3. Architecture Goals（架构目标）
- Long-term Immersion First
- Character & Relationship Persistence
- RTX 5060 8GB First
- Model Agnostic
- One Engine, Multiple Experiences

## 4. Core Architecture Principles（核心架构原则）
- Simulation Before Generation
- Narrative Director Before LLM
- Python Owns Logic, LLM Owns Expression
- Data First, Prompt Last
- Relationship Driven
- Scene as Smallest Runtime Unit
- **One Engine, Multiple Profiles**（General / Romance / Mature 共享同一套 Runtime）

## Mature Experience Principle
Mature Profile 不是独立的內容引擎，而是 **Relationship-driven experience layer**。  
成人体验只能从以下要素自然产生：
- Relationship State
- Character State
- Scene Context
- Narrative Progression

Engine 永远不将亲密内容作为孤立生成目标。

## 5. System Overview（系统概览）
整个 Engine 分为 **Logical Layers** 和 **Cross-cutting Infrastructure**。

## 6. Runtime Architecture（运行时架构）⭐
一次完整 Scene 的生命周期：

**Player Action**  
↓  
**Scene Initialization**  
↓  
**Context Loading**  
↓  
**Simulation Update**  
↓  
**Relationship Evaluation**  
↓  
**Narrative Director Decision**  
↓  
**Prompt Construction**  
↓  
**Model Generation**  
↓  
**Scene Result**  
↓  
**Memory Extraction**  
↓  
**State Persistence**  
↓  
**Next Scene**

## 7. Runtime Guarantees（运行时保证）
- 每个 Scene 完成后必须更新 Relationship 和 Memory，然后才能进入下一 Scene。
- 所有长期状态变化必须经过 Simulation Layer。
- 所有 Content Profile 共享同一 Runtime。

## 8. Logical Architecture（逻辑架构）
**Logical Layers**：
1. Player Layer
2. Simulation Layer
3. Narrative Director
4. Prompt Builder
5. Model Runtime Layer
6. Renderer Layer

**Cross-cutting Infrastructure**：
- Persistence
- GPU Scheduler
- Configuration
- Logging / Monitoring

## 9. Core Runtime Domain（核心运行域）⭐
- **Relationship State**（最高优先级）
- Character State
- World State
- Scene State
- Memory State
- Timeline State

## 10. Data Flow & Boundaries（数据流与边界）
- LLM 只能读取状态，不能直接修改持久化数据。
- 所有状态变更必须经过 Simulation Layer。

## 11. Cross-cutting Concerns（横切关注点）
- GPU Scheduling
- Content Profile
- Logging
- Configuration
- Error Handling

## 12. Hardware Constraint Design（硬件约束设计）
目标硬件为 RTX 5060 8GB。  
**Hardware Constraints are Product Constraints**。

**Generation Priority**：
1. LLM Interaction
2. Simulation
3. Image Generation（异步）
4. Background Tasks

Image Generation 不得阻塞核心叙事流程。

## 13. Extension Strategy（扩展策略）
支持未来更换 LLM、Image Model、增加新功能，而无需重构核心 Engine。

## References
- **Depends On**：Design Constitution, Project Vision, Glossary, PRD Blueprint
- **Referenced By**：Simulation Layer, Narrative Director, Character Schema, Relationship Schema, Scene Engine, Image Pipeline, GPU Scheduler 等

## Revision History
- v1.0：初始版本（Foundation + Runtime Architecture）