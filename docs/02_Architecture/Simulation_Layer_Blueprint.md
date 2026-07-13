# Simulation Layer Blueprint

**Version:** v1.1  
**Status:** Draft  
**Last Updated:** 2026-07-13  

## 1. Purpose（文档目的）

定义 Simulation Layer 在 AI Narrative RPG Engine 中的职责、边界和运行机制。

**Simulation Layer is the Ground Truth Authority of the Engine.**

它是 Engine 中唯一有权演化长期状态（Persistent Runtime State）的核心模块。

所有长期状态变化必须首先由 Simulation Layer 计算和验证，然后才能进入 Narrative Director、LLM 或其他生成系统。

Simulation Layer 不是叙事系统，不是生成系统，也不是 UI 系统。

它负责维护世界的真实状态（Ground Truth）。

---

## 2. Responsibilities（职责）

**负责：**

- World State Evolution（世界状态演化）
- Character State Evolution（角色状态演化）
- Relationship State Evolution（关系状态演化）
- Event Consequence Evaluation（事件结果计算）
- Rule Evaluation（规则评估）
- State Validation（一致性验证）
- Runtime State Transition（运行时状态转换）

**不负责：**

- Narrative Planning
- Dialogue Generation
- Prompt Construction
- Image Generation
- Memory Extraction
- Persistence Commit
- UI Rendering

---

## 3. Document Governance（文档治理）

**Owner:** Simulation Architect

**Reviewers:**
- Engine Architect
- Runtime Architect

**Approval:**
Architecture Review Required

**Update Policy:**

Changes affecting state transition rules, simulation tick logic, runtime guarantees, or module boundaries require ADR approval.

---

## 4. Design Principles（设计原则）

Simulation Layer 必须遵循以下设计原则：

- **Simulation Before Generation**
- **State Is Fact**
- **Ground Truth First**
- **Deterministic State Transition**
- **Relationship First**
- **Rule-Driven, Not Prompt-Driven**
- **Simulation Owns State**
- **Scene Is Atomic**

所有生成内容都建立在已经确定的状态之上，而不能反向决定状态。

---

## 5. Boundary Definition（边界定义）

**Simulation Layer is a Rule-Driven State Machine.**

Simulation Layer 是唯一允许修改长期运行状态（Persistent Runtime State）的模块。

所有其它模块都是：

- Consumers（消费者）
- Coordinators（协调者）
- Presenters（表现层）

Simulation Layer **does NOT own**：

- Narrative Planning
- Story Pacing
- Dialogue Generation
- Image Generation
- Memory Extraction
- Scene Orchestration
- UI

任何模块都不得绕过 Simulation Layer 修改长期状态。

---

## 6. Runtime Position（运行时定位）

在 Runtime 中：

```
Player Action
        ↓
Scene Engine
        ↓
Simulation Layer
        ↓
Narrative Director
        ↓
Prompt Builder
        ↓
LLM / Image Model
        ↓
Persistence
```

Simulation Layer 位于所有内容生成之前。

它产生事实（Facts），而不是故事（Stories）。

---

## 7. Core Runtime Responsibilities（核心运行职责）

Simulation Layer 在每一个 Scene 中负责：

- 加载当前 Runtime State
- 更新 Character State
- 更新 Relationship State
- 更新 World State
- 执行 Rule Evaluation
- 解析 Event Consequences
- 产生新的 State Transition
- 验证状态一致性

**Simulation produces facts.**

**Narrative Director produces stories.**

**LLM produces expressions.**

---

## 8. Core State Domains（核心状态域）

Simulation Layer 管理以下长期状态：

### Character State

角色人格、情绪、目标、内部状态。

### Relationship State（Core）

Relationship 是 Engine 的核心驱动。

包括：

- Trust
- Affection
- Dependence
- Intimacy
- Respect
- Jealousy
- Attachment

### World State

包括：

- Time
- Location
- Environment
- Global Events

### Progression State

包括：

- Quest Progress
- Unlock Status
- Story Progression

### Timeline State

保证所有事件具有连续时间顺序。

---

## 9. Simulation Tick（模拟 Tick）

Simulation Tick 是 Simulation Layer 的最小执行单元。

执行流程：

```
Tick Start
        ↓
Load Current State
        ↓
Apply Player Action
        ↓
Character Update
        ↓
Relationship Evaluation
        ↓
Rule Evaluation
        ↓
Event Resolution
        ↓
State Transition
        ↓
Validation
        ↓
Tick Complete
```

### Tick Rules

A Scene must execute exactly **one** Simulation Tick.

A Simulation Tick must produce exactly **one** validated State Transition.

A State Transition must be committed exactly **once**.

---

## 10. State Transition（状态转换）

所有状态转换必须满足：

- Deterministic（确定性）
- Traceable（可追溯）
- Replayable（可重放）
- Recoverable（可恢复）
- Validated（一致性验证）

LLM 不允许直接修改任何长期状态。

---

## 11. Rule Engine（规则引擎）

Rule Engine 是 Simulation Layer 的核心计算子系统。

负责：

- Rule Evaluation
- State Validation
- Event Trigger
- State Transition Calculation

### Rule Categories

- Relationship Rules
- Character Rules
- World Rules
- Progression Rules
- Environment Rules

未来支持：

- Plugin Rules
- Custom Rules

---

## 12. Event Resolution（事件解析）

Simulation Layer 负责决定：

- Trigger
- Actor
- Action
- Consequence

并计算：

- Narrative Weight
- Importance
- Priority

Narrative Director 根据这些结果决定如何呈现故事。

---

## 13. Runtime Guarantees（运行时保证）

Simulation Layer 保证：

- Every Scene executes exactly one Simulation Tick.
- Every Tick produces one validated State Transition.
- Persistent State can only be modified by Simulation Layer.
- State Transition must be deterministic.
- State Transition must be replayable.
- State Transition must be recoverable.
- Simulation output must be independent from LLM responses.
- Long-term assets must never be corrupted.

---

## 14. Hardware Considerations（硬件考量）

目标硬件：

- RTX 5060 8GB
- 32GB RAM
- Offline First

设计要求：

- CPU-first
- GPU Independent
- Lightweight Rule Evaluation
- Low Latency
- Background Friendly

Simulation Layer 必须能够在**没有任何 AI 模型加载**的情况下独立运行。

---

## References

**Depends On**

- Overall Architecture
- Runtime Architecture
- Scene Engine Blueprint
- Glossary

**Referenced By**

- Relationship Engine
- Narrative Director
- Memory Architecture
- Character System
- Quest System
- Scene Engine

---

## Revision History

| Version | Date | Description |
|----------|------------|-------------------------------|
| v1.1 | 2026-07-13 | Engineering refinement, Ground Truth Authority, Runtime Position, Core State Domains, Runtime Guarantees |
| v1.0 | 2026-07-12 | Initial Blueprint |