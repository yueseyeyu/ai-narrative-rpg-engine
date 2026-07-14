# Architecture Baseline

**Version:** v1.0  
**Status:** Frozen  
**Frozen Date:** 2026-07-14

---

## 1. Purpose（文档目的）

This document formally declares the Architecture Baseline v1.0 — the frozen architectural specification for the AI Narrative RPG Engine. It defines what is frozen, what may change freely, and what requires Architecture Decision Record (ADR) approval.

本文档正式声明 Architecture Baseline v1.0 — AI Narrative RPG Engine 的冻结架构规范。它定义了什么被冻结、什么可以自由变更、什么需要 ADR 批准。

---

## 2. Baseline Scope（基线范围）

This baseline encompasses all documents produced during Phase A (Governance), Phase B-1 (Legacy Rewrite), and Phase B-2 (Partial Sync).

| Phase | Scope | Documents |
|-------|-------|-----------|
| Phase A | Governance Framework | 6 governance documents (Pipeline, Infrastructure, Glossary, Migration Matrix, Ownership Matrix, Freeze Checklist) |
| Phase B-1 | Runtime Core Rewrite | 3 core Blueprints (Simulation Layer, State Model, Scene Engine) |
| Phase B-2 | Global Sync | 10 Partial Blueprints synced + 10-item consistency audit |

**Total:** 19 architecture documents + 4 data schemas, all aligned to a single Authority model.

---

## 3. Core Runtime Principles（核心运行时原则）

The following five principles are the immutable foundation of the Runtime Architecture. No implementation may violate these.

以下五项原则是 Runtime Architecture 的不可变基础。任何实现不得违反。

| Principle | Description |
|-----------|-------------|
| **Simulation computes** | Simulation Authority (Layer ③) computes what happens — produces SimulationResult with deltas. It does not mutate state. |
| **State mutates** | State Authority (Layer ⑤) is the sole authority for Persistent State mutation. It applies deltas computed by Simulation. |
| **Scene Engine orchestrates** | Scene Engine is the Transaction Container and Pipeline Coordinator. It orchestrates *when* things happen, not *what* happens. It is NOT an Authority layer. |
| **Generation expresses** | Narrative Director, LLM, and Image Pipeline produce expressions from committed facts. They are post-Pipeline. Generation results are regenerable. |
| **Memory extracts** | Memory System extracts Memory Objects from committed Events and State. It never mutates Persistent State. |
| **Replayability is first-class** | Replayability is a first-class architectural capability, not merely a debugging feature. It SHALL be usable for: Save Validation, Regression Testing, AI Benchmark, Story Replay, QA. Every SimulationResult SHALL be replayable from its inputs. |

### 5-Layer Authority Pipeline

```
① Intent → ② Execution → ③ Simulation → ④ Reality → ⑤ State
```

Each layer has exactly one Authority. Data flows strictly forward. No layer may bypass another.

> **Logical, Not Physical:** Authority Layers are a logical architecture, not necessarily a physical module boundary. Implementation MAY combine layers into a single function call for trivial actions, as long as the logical separation is preserved and testable.
>
> **逻辑而非物理：** 权威层是逻辑架构，不一定是物理模块边界。实现可以将层合并为单个函数调用用于简单操作，只要逻辑分离被保留且可测试。

---

## 4. Frozen Elements（冻结元素）

The following are **frozen**. Any change requires ADR approval.

| Frozen Element | Description |
|----------------|-------------|
| Authority Layers | The 5-Layer Authority Pipeline (①-⑤). No new Authority may be created. |
| Mutation Boundary | Only State Authority (Layer ⑤) may mutate Persistent State. |
| Artifact Ownership | The 26-artifact ownership defined in [Artifact Ownership Matrix v1.1](../02_Architecture/Runtime_Artifact_Ownership_Matrix.md). |
| Pipeline Data Flow | Data flows strictly forward: Action → SimulationResult → Event → State Mutation. Acyclic. |
| Scene Transaction Model | Scene is atomic. BEGIN → EXECUTE → COMMIT or ROLLBACK. |
| SimulationResult Contract | Self-contained, immutable, sole external output of Simulation Layer. |
| Handler Purity | Handlers are functionally pure — no Persistent State side effects. |
| Memory Boundary | Memory extraction SHALL NOT mutate Persistent State. **Only the boundary is frozen — algorithms (importance scoring, decay curves, retrieval formulas) are implementation-defined and MAY change freely.** |
| Generation Boundary | Generation is post-Pipeline. Generation retry SHALL NOT re-run Simulation. |
| Infrastructure Serves | Infrastructure provides platform services. It never participates in Authority decisions. |

### Design Assumptions (Not Frozen)（设计假设 — 未冻结）

The following are **design assumptions** validated at current scale. They are NOT frozen. If scale or requirements change, they MAY be revisited via ADR.

| Assumption | Current Rationale | Revisit When |
|-----------|-----------------|-------------|
| **Domain-Oriented State (not ECS)** | Projected ~20-50 active entities. Relationship State is inherently relational (edge data), not suitable for ECS component bags. Domain clarity > cache performance at this scale. | Entity count exceeds ~1000, or performance profiling shows state access as bottleneck. ECS is currently not selected because projected scale does not justify its complexity. |
| **5-Layer Pipeline** | Each layer has distinct decision semantics. Merging would lose meaningful separation of concerns. | MVP validation shows certain layers are always trivial pass-throughs. Logical layers remain; physical implementation MAY fold. |
| **Memory Quality Model** | Strength, Accuracy, Accessibility, Emotional Weight, Recency — aligned with cognitive science. | MVP validation shows simpler model suffices. Algorithms are NOT frozen; only the boundary (Memory SHALL NOT mutate State) is frozen. |

---

## 5. Change Policy（变更策略）

| Change Type | Approval Required | Examples |
|-------------|-------------------|---------|
| **Breaking** (Architecture) | ADR required | Adding/removing Authority layers, changing mutation boundary, modifying Pipeline data flow, changing artifact ownership |
| **Non-breaking** (Documentation) | Changelog only | Terminology unification, example updates, formatting, cross-reference additions, Governance field updates |
| **Implementation** | No approval | Code, algorithms, data structures, performance tuning (as long as they conform to Blueprint contracts) |

---

## 6. Non-Blocking Residuals（非阻塞残留项）

The following items were identified during the B-2.Audit as non-blocking. They should be resolved during RC phase but do not block implementation.

| # | Item | Priority | Status |
|---|------|----------|--------|
| 1 | Governance field updates for Current documents | P1 | ✅ Done (2026-07-14) |
| 2 | Migration Matrix assessment of Memory Architecture is outdated | P2 | RC phase |
| 3 | Overall Architecture Overview "Python 管逻辑" terminology | P3 | ✅ Done (2026-07-14) |

---

## 7. Future Audit Items（未来审计项）

The following audit is recommended for the RC (Release Candidate) phase, before final Freeze:

### Runtime Artifact Traceability Audit

For each Runtime Artifact, verify:

| Trace | Description |
|-------|-------------|
| Producer | Which module/component produces this artifact |
| Consumer | Which modules consume this artifact |
| Owner | Which Blueprint owns this artifact |
| Persistence | Is this artifact persisted? (Yes/No) |
| Replayability | Is this artifact replayable? (Yes/No) |

**Example traces:**

| Artifact | Producer | Consumer | Owner | Persist? | Replay? |
|----------|----------|----------|-------|----------|---------|
| SimulationResult | Simulation Authority ③ | Timeline Manager, Narrative Director, Log Manager | Simulation Layer Blueprint | No (transient, archived by Log) | Yes |
| Event Object | Event Factory (inside Simulation ③) | Timeline Manager ④, State Authority ⑤, Memory System | Event Object Schema | Yes (committed to Timeline) | Yes |
| Behavior Tendency | Relationship Engine (inside Simulation ③) | Narrative Director | Relationship Engine Blueprint | No (session artifact) | Yes |
| Narrative Plan | Narrative Director | Prompt Builder, Image Pipeline | Narrative Director Blueprint | No (session artifact) | Yes |
| Memory Object | Memory System | Relationship Engine, Narrative Director, Prompt Builder | Memory Architecture Blueprint | Yes | Yes |

---

## 8. Architecture Gaps（架构缺口）

| # | Gap | Impact | Handling |
|---|-----|--------|----------|
| 1 | **Background Simulation** — NPC routines, world evolution, time-skip | Medium | Future ADR: define "Background Tick" |
| 2 | **Fast Path** — trivial actions may not need full 5-layer processing | Low | Implementation optimization, logical layers preserved |
| 3 | **State Migration** — save file version compatibility | Low | Runtime Metadata has `save_version` |
| 4 | **Nested Tick** — chain triggers (attack → counter → passive) | Low | Future ADR |

These gaps do not block implementation.

---

## 9. Implementation Priority（实现优先级）

| Priority | Task | Rationale |
|----------|------|----------|
| 1 | **Runtime Contract Test Specification** | Define verifiable architecture contracts before code. Contract tests protect architecture better than more documentation. |
| 2 | **Minimal Viable Pipeline (MVP)** | Action → Simulation → SimulationResult → State. Validate determinism and contract. |
| 3 | **Implementation Roadmap** | Refine phases based on MVP feedback. |
| 4 | **ADR Directory** | Record real architecture decisions from implementation. |

> **MVP Principle:** MVP should validate contracts, not completeness. The goal is to verify: Action → Simulation → SimulationResult → Commit → Replay → Deterministic. Once this holds, Relationship, Memory, Narrative, and Image are all post-Pipeline extensions. This prevents scope creep.

---

## 10. Governance（治理）

**Owner:** Chief Architect  
**Architecture Reviewers:** All Architects  
**Architecture Approval:** ADR Required for any Breaking change  
**Last Reviewed:** 2026-07-14  

---

## 9. Revision History

| Version | Date | Description |
|---------|------|-------------|
| v1.0 | 2026-07-14 | Architecture Baseline frozen. Encompasses Phase A + Phase B-1 + Phase B-2. 5 Core Runtime Principles declared. 10 frozen elements defined. Change policy established. |
| v1.0 (Rev 1) | 2026-07-14 | Refinements (User review): (1) Added "Logical, Not Physical" note to Authority Layers. (2) Added "Replayability is first-class" principle. (3) Clarified Memory Boundary: only boundary frozen, algorithms are implementation-defined. (4) Added "Design Assumptions (Not Frozen)" section for ECS, 5-Layer, Memory Quality Model. (5) Added identified architecture gaps. (6) Added implementation priority. (7) Updated non-blocking residuals (P1/P3 completed). |
