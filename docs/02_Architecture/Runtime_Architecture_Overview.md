# Runtime Architecture Overview

**Version:** v1.1  
**Status:** Active  
**Last Updated:** 2026-07-14

---

## Purpose（文档目的）

本文档是 AI Narrative RPG Engine 运行时架构的**入口概览**。

它提供 Scene 生命周期、状态流转和模块调用顺序的快速参考。

详细工程规范请参阅 [Runtime Architecture Blueprint](Runtime_Architecture_Blueprint.md)。

---

## Engine Mental Model（引擎心智模型）

AI Narrative RPG Engine 不是一个文本生成系统，而是一个**拥有生成接口的状态模拟系统**。

| Role | Module |
|------|--------|
| 真实世界 | Simulation Layer |
| 导演 | Narrative Director |
| 演员 | LLM / Image Model |
| 记忆与历史 | Persistence & Memory System |

文本和图片只是**表现层**，状态才是**事实层**。

---

## Core Runtime Principles（核心运行时原则）

以下五项原则是 Runtime Architecture 的不可变基础：

| Principle | Description |
|-----------|-------------|
| **Simulation computes** | 模拟计算。Simulation Authority (Layer ③) computes what happens — produces SimulationResult with deltas. |
| **State mutates** | 状态变更。State Authority (Layer ⑤) is the sole authority for Persistent State mutation. |
| **Scene Engine orchestrates** | 事务编排。Scene Engine is the Transaction Container and Pipeline Coordinator. NOT an Authority layer. |
| **Generation expresses** | 生成表达。Narrative Director, LLM, and Image Pipeline produce expressions from committed facts. Post-Pipeline. Regenerable. |
| **Memory extracts** | 记忆提取。Memory System extracts Memory Objects from committed Events and State. Never mutates Persistent State. |

> **Architecture Baseline:** These principles are frozen in [Architecture Baseline v1.0](../00_Project/Architecture_Baseline.md). Any change requires ADR approval.

---

## Scene Lifecycle（Scene 生命周期）

```mermaid
flowchart TD
    A[Player Action] --> B[Scene Start]
    B --> C[Context Assembly]
    C --> D[Simulation Tick]
    D --> E[Relationship Update]
    E --> F[Narrative Planning]
    F --> G[Generation - LLM + Image]
    G --> H[Evaluation]
    H --> I[Memory Extraction]
    I --> J[Persistence]
    J --> K[Scene Complete]
    K --> L[Next Scene]
```

---

## Scene State Machine（Scene 状态机）

```mermaid
flowchart LR
    A[Created] --> B[Initialized]
    B --> C[Simulating]
    C --> D[Planning]
    D --> E[Generating]
    E --> F[Completed]
    F --> G[Archived]
```

---

## Runtime State Model（运行时状态模型）

| State | Description |
|-------|-------------|
| Character State | 角色状态 |
| **Relationship State** | **关系状态（核心）** |
| World State | 世界状态 |
| Scene State | 场景状态 |
| Memory State | 记忆状态 |
| Timeline State | 时间线状态 |

---

## Runtime Guarantees（运行时保证）

- 每个 Scene 完成后必须更新 Relationship 和 Memory，然后才能进入下一 Scene。
- 所有长期状态变化必须经过 Simulation Layer。
- State 必须可恢复、可追溯。

---

## Hardware Strategy（硬件策略）

目标硬件：RTX 5060 8GB

| Strategy | Description |
|----------|-------------|
| Sequential Generation | LLM 与 Image Model 严格串行 |
| Image Async Queue | 图像生成异步队列 |
| Background Tasks | 非核心任务后台执行 |

---

## References

**Detailed Specification:** [Runtime Architecture Blueprint](Runtime_Architecture_Blueprint.md)

**Depends On:**

- [Runtime Pipeline Blueprint](./Runtime_Pipeline_Blueprint.md) — defines 5-Layer Authority Pipeline
- [Runtime Architecture Blueprint](./Runtime_Architecture_Blueprint.md) — detailed specification
- [Runtime Glossary](./Runtime_Glossary.md) — defines terminology
- Overall Architecture Overview

**Referenced By:**

- [Scene Engine Blueprint](./Scene_Engine_Blueprint.md)
- [Simulation Layer Blueprint](./Simulation_Layer_Blueprint.md)
- [Relationship Engine Blueprint](./Relationship_Engine_Blueprint.md)
- [Memory Architecture Blueprint](./Memory_Architecture_Blueprint.md)
- [Narrative Director Blueprint](./Narrative_Director_Blueprint.md)

---

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| v1.1 | 2026-07-14 | Phase B-2 sync: added Pipeline Blueprint and Glossary to Depends On; expanded Referenced By with links. Overview content references Pipeline-aligned Blueprint. |
| v1.0 | 2026-07-13 | Created as Overview; detailed spec moved to Blueprint |
