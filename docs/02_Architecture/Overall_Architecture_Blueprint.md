# Overall Architecture Blueprint

**Version:** v2.0  
**Status:** Draft  
**Last Updated:** 2026-07-12  

## Purpose（文档目的）
定义 AI Narrative RPG Engine 的整体架构框架，为所有后续 Architecture、Data 和 Development 文档提供最高指导。

## Responsibilities（职责）
- 定义系统分层、边界和数据流
- 确保架构与 Design Constitution 和 Project Vision 一致
- 为后续模块设计提供统一蓝图

## In Scope
分层架构、运行时流程、核心资产、模块职责、数据流、硬件约束

## Out of Scope
具体代码实现、数据库 schema、Prompt 模板、UI 设计

## Document Governance（文档治理）
**Owner:** Chief Architect  
**Reviewers:** Product Architect, Engine Architect  
**Approval:** Architecture Review Required  
**Update Policy:** Only update after ADR approval if architectural principles change.

## Assumptions（假设）
- Offline First
- Windows Platform
- RTX 5060 8GB + 32GB RAM
- Local LLM & Image Generation

## Design Goals（架构目标）
- Long-term Immersion First
- Character & Relationship Persistence
- Hardware Constraints First
- Model Agnostic
- One Engine, Multiple Experiences

## Architecture Principles（架构原则）
- Simulation Before Generation
- Narrative Director Before LLM
- Python Owns Logic, LLM Owns Expression
- Data First, Prompt Last
- Relationship Driven
- Scene as Smallest Runtime Unit

## Constraint Hierarchy（约束层级）
- Product Constraints
- Architecture Constraints
- Hardware Constraints (RTX 5060 8GB)
- Implementation Constraints

## Runtime Architecture（运行时架构）⭐
描述一次完整 Scene 的生命周期（核心流程）。

## Architecture Views（架构视图）
- Conceptual View
- Logical View
- Runtime View
- Data View
- Deployment View (未来)

## Core Runtime Domain（核心运行域）
**Relationship** 作为核心驱动（提升一级），Character、Scene、Memory、Timeline 等围绕 Relationship 展开。

## Module Responsibilities（模块职责）
明确 Python、Narrative Director、LLM、Image Pipeline、Persistence 等的边界。

## Data Flow（数据流）
定义数据流动方向和禁止跨层行为。

## Cross-cutting Concerns（横切关注点）
GPU Scheduling、Content Profile、Logging、Configuration、Error Handling 等。

## Quality Attributes（质量属性）
Consistency、Maintainability、Extensibility、Offline First、Privacy、Determinism。

## Runtime Guarantees（运行时保证）
- Every Scene must update Relationship & Memory before Next Scene
- All long-term state changes must go through Simulation Layer

## Extensibility（可扩展性）
支持未来新模型、新 Profile 的机制。

## One Engine Principle
**One Engine. One Runtime. Multiple Experiences.**  
General / Romance / Mature 等 Profile 共享同一套 Simulation、Narrative Director、Relationship、Memory、Scene。禁止 Fork Engine 或独立 Mature Engine。

## References
- **Depends On**：Design Constitution, Project Vision, Glossary, PRD Blueprint
- **Referenced By**：Simulation Layer, Narrative Director, Character Schema, Relationship Schema, Scene Engine, Image Pipeline 等

## Open Questions
（待后续讨论）

## Revision History
| Version | Date | Author | Description |
|---------|------|--------|-------------|
| v2.0 | 2026-07-12 | - | 增加工程化元数据、Constraint Hierarchy、Quality Attributes、Runtime Guarantees、One Engine Principle |
