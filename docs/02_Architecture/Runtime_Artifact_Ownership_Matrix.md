# Runtime Artifact Ownership Matrix

**Version:** v1.1  
**Status:** Active  
**Last Updated:** 2026-07-14

---

## 1. Purpose（文档目的）

This document is the **single authoritative reference** for Runtime Artifact ownership across the entire Engine. It defines who produces, owns, consumes, and persists every Runtime Object in the system.

本文档是整个引擎中**运行时制品归属的唯一权威参考**。它定义了谁生产、谁拥有、谁消费、谁持久化每个运行时对象。

### Why This Matrix Exists（本矩阵存在的理由）

> "Who owns this thing?" — Every architecture review eventually reduces to this question.
>
> "谁拥有这个东西？" — 每次架构审查最终都会归结为这个问题。

This Matrix is the intersection of three Blueprint families:

本矩阵是三套 Blueprint 的交汇点：

- **Pipeline Blueprint** — defines *when* artifacts are produced
- **Infrastructure Blueprint** — defines *where* artifacts are persisted
- **Data Schemas** — defines *what* artifacts look like

Together, they answer *who* does what with each artifact.

它们共同回答了*谁*对每个制品做什么。

---

## 2. How to Read This Matrix（如何阅读本矩阵）

| Column | Meaning |
|--------|---------|
| **Artifact** | The Runtime Object or data entity |
| **Produced By** | The Authority layer or component that creates this artifact |
| **Owned By** | The Authority layer or component that controls its lifecycle (creation, mutation, deletion) |
| **Consumed By** | Components that read this artifact as input |
| **Persisted By** | The Infrastructure component responsible for durable storage |
| **Lifecycle** | Transient (exists during Scene) or Persistent (survives across sessions) |
| **Confidence** | Confidence level (see below) |
| **Schema** | Authoritative Data Schema document (if applicable) |

### Confidence Levels（置信度级别）

| Level | Meaning | Criteria |
|-------|---------|----------|
| **Confirmed** | Architecture Reality — structure and ownership are settled | Backed by an RC or Locked Blueprint/Schema, or a Draft Schema referenced by multiple Current Blueprints |
| **Provisional** | Architecture Intention — defined but not yet Pipeline-aligned | Backed by a Draft/Partial Blueprint; structure may change during Phase B migration |
| **Future** | Architecture Vision — no Blueprint exists yet | Referenced as "Future" in existing documents; no authoritative definition |

> **Why Confidence Matters:** Without this column, readers may assume every row represents settled architecture. In reality, some artifacts (e.g., Behavior Tendency, Memory Object) are defined by Partial Blueprints that will change during Phase B migration. Others (e.g., Timeline Store) have no Blueprint at all. The Confidence column prevents these from being mistaken for Architecture Reality.

> **为什么置信度重要：** 没有这一列，读者可能假设每一行都代表已定架构。实际上，一些制品（如行为倾向、记忆对象）由待迁移的 Partial Blueprint 定义，将在 Phase B 期间变化。另一些（如 Timeline Store）根本没有 Blueprint。Confidence 列防止这些被误认为架构现实。

> **Key Distinction:** "Produced By" and "Owned By" may differ. An artifact can be produced by one layer but owned by another. For example, Event Objects are produced by the Timeline Manager but owned by the Reality Authority layer.

> **关键区分：** "生产者"和"拥有者"可能不同。一个制品可以由一层生产但由另一层拥有。例如，事件对象由时间线管理器生产，但由现实权威层拥有。

---

## 3. Core Pipeline Artifacts（核心流水线制品）

These are the 5 artifacts that flow through the Authority Pipeline. Each is produced by exactly one Authority layer.

这些是流经权威流水线的 5 个制品。每个由且仅由一个权威层生产。

| # | Artifact | Produced By | Owned By | Consumed By | Persisted By | Lifecycle | Confidence | Schema |
|---|----------|-------------|----------|-------------|--------------|-----------|------------|--------|
| 1 | **Action Object** | Planner (Intent Authority) | Planner | AEM, Log Manager | Log Manager (Runtime Log) | Transient → Archived | ✅ Confirmed | [Action Object Schema](../03_Data/Action_Object_Schema.md) |
| 2 | **Action Record** | AEM (Execution Authority) | AEM | Simulation Layer, Log Manager | Log Manager (Runtime Log) | Transient → Archived | ✅ Confirmed | Defined in AEM |
| 3 | **SimulationResult** | Simulation Layer (Simulation Authority) | Simulation Layer | Timeline Manager, Narrative Director, Log Manager | Log Manager (Runtime Log) | Transient → Archived | ✅ Confirmed | [SimulationResult Schema](../03_Data/SimulationResult_Schema.md) |
| 4 | **Event Object** | Timeline Manager (Reality Authority) | Timeline Manager | State Management, Narrative Director, Memory System, Event Bus subscribers | Log Manager (Runtime Log) + Future Timeline Storage | Persistent (immutable) | ✅ Confirmed | [Event Object Schema](../03_Data/Event_Object_Schema.md) |
| 5 | **State Mutation** | State Management (State Authority) | State Management | Runtime State, Snapshot Manager | Snapshot Manager (next Scene snapshot) | Persistent | ✅ Confirmed | State Schemas (see §4) |

### Pipeline Data Flow

```
Action Object → Action Record → SimulationResult → Event Object → State Mutation
     ①              ②                  ③                 ④              ⑤
   Intent         Execution         Simulation         Reality         State
```

> **Acyclic Rule:** Each artifact flows strictly forward. No artifact may reference or depend on a downstream artifact. See [Pipeline Blueprint §6](./Runtime_Pipeline_Blueprint.md).

---

## 4. State Artifacts（状态制品）

These are the persistent state domains that constitute Runtime State. All are mutated exclusively through State Authority (Layer ⑤).

这些是构成运行时状态的持久状态域。全部通过状态权威层（第⑤层）变更。

| # | Artifact | Produced By | Owned By | Consumed By (Read-Only) | Persisted By | Lifecycle | Confidence | Schema |
|---|----------|-------------|----------|------------------------|--------------|-----------|------------|--------|
| 6 | **Character State** | State Management | State Management (via Simulation Layer) | Narrative Director, Prompt Builder, Memory System, LLM Runtime | Snapshot Manager + Save System | Persistent | ✅ Confirmed | [Character State Schema](../03_Data/Character_State_Schema.md) |
| 7 | **Relationship State** | State Management (via Relationship Engine) | State Management (via Simulation Layer) | Narrative Director, Prompt Builder, Memory System | Snapshot Manager + Save System | Persistent | ✅ Confirmed | [Relationship State Schema](../03_Data/Relationship_State_Schema.md) |
| 8 | **World State** | State Management | State Management (via Simulation Layer) | Narrative Director, Prompt Builder, Memory System | Snapshot Manager + Save System | Persistent | 🔮 Future | Future: World State Schema |
| 9 | **Progression State** | State Management | State Management (via Simulation Layer) | Narrative Director, Prompt Builder | Snapshot Manager + Save System | Persistent | 🔮 Future | Future: Progression Schema |
| 10 | **Timeline State** | State Management (via Timeline Manager) | State Management | Narrative Director, Prompt Builder, Memory System | Log Manager + Future Timeline Storage | Persistent (append-only) | 🔮 Future | Future: Timeline Schema |

### State Mutation Authority Rule

> **All Persistent State mutations flow through State Authority (Layer ⑤).** The Relationship Engine computes relationship deltas, but the actual state mutation is performed by State Management. No module may directly write to Persistent State.

> **所有持久状态变更通过状态权威层（第⑤层）流转。** 关系引擎计算关系增量，但实际状态变更由状态管理层执行。任何模块不得直接写入持久状态。

---

## 5. Session Artifacts（会话制品）

These artifacts exist only during Scene execution and are discarded or committed at Scene completion.

这些制品仅在 Scene 执行期间存在，在 Scene 完成时丢弃或提交。

| # | Artifact | Produced By | Owned By | Consumed By | Persisted By | Lifecycle | Confidence |
|---|----------|-------------|----------|-------------|--------------|-----------|------------|
| 11 | **Scene State** | Scene Engine | Scene Engine | Simulation Layer, Narrative Director | None (transient) | Session | ⚠️ Provisional |
| 12 | **Runtime Metadata** | Scene Engine | Scene Engine | All modules (read-only) | Snapshot Manager (in snapshot) | Session | ⚠️ Provisional |
| 13 | **Active Memory References** | Memory System | Memory System | Narrative Director, Prompt Builder, Simulation Layer | None (transient) | Session | ⚠️ Provisional |
| 14 | **Narrative Plan** | Narrative Director | Narrative Director | Prompt Builder, Image Pipeline | None (transient, but archived in Log) | Session | ⚠️ Provisional |
| 15 | **Behavior Tendency** | Relationship Engine (within Simulation) | Relationship Engine | Narrative Director | None (transient) | Session | ⚠️ Provisional |
| 16 | **Relationship Constraints** | Relationship Engine (within Simulation) | Relationship Engine | Narrative Director | None (transient) | Session | ⚠️ Provisional |

> **Provisional Artifacts:** Items 11–16 are defined by Partial Blueprints that have not yet been aligned to the 5-Layer Authority Pipeline. Their ownership and structure may change during Phase B migration. Do not treat them as frozen architecture decisions.

> **Provisional 制品：** 第 11–16 项由尚未对齐五层权威流水线的 Partial Blueprint 定义。其归属和结构可能在 Phase B 迁移期间变化。不要将其视为已冻结的架构决策。

---

## 6. Infrastructure Artifacts（基础设施制品）

These artifacts are produced and managed by Runtime Infrastructure. Infrastructure serves; it does not decide.

这些制品由运行时基础设施生产和管理。基础设施服务；它不决策。

| # | Artifact | Produced By | Owned By | Consumed By | Persisted By | Lifecycle | Confidence |
|---|----------|-------------|----------|-------------|--------------|-----------|------------|
| 17 | **Runtime Log** | Log Manager | Log Manager | Replay Manager, Debug Tools | Log Manager (durable log store) | Persistent (append-only) | ✅ Confirmed |
| 18 | **Snapshot** | Snapshot Manager | Snapshot Manager | Simulation Layer (input), Replay Manager, Save System | Snapshot Manager (snapshot store) | Persistent (versioned) | ✅ Confirmed |
| 19 | **Deterministic Seed** | Seed Manager | Seed Manager | Simulation Layer, Replay Manager | Log Manager (in Runtime Log) | Session → Archived | ✅ Confirmed |
| 20 | **Replay Session** | Replay Manager | Replay Manager | Debug Tools, Testing | None (ephemeral) | Transient | ✅ Confirmed |

### Infrastructure Ownership Rule

> **Infrastructure components own their storage representations, not the data's meaning.** The Log Manager owns the Runtime Log stream, but the Action Records within it are owned by AEM. The Snapshot Manager owns the snapshot format, but the state within it is owned by State Management.

> **基础设施组件拥有其存储表示，而非数据的含义。** 日志管理器拥有运行时日志流，但其中的行动记录由 AEM 拥有。快照管理器拥有快照格式，但其中的状态由状态管理层拥有。

---

## 7. Generation Artifacts（生成制品）

These artifacts are produced by generation systems (LLM, Image). They are expressions of state, not state itself.

这些制品由生成系统（LLM、图像）生产。它们是状态的表达，而非状态本身。

| # | Artifact | Produced By | Owned By | Consumed By | Persisted By | Lifecycle | Confidence |
|---|----------|-------------|----------|-------------|--------------|-----------|------------|
| 21 | **Prompt Package** | Prompt Builder | Prompt Builder | LLM Runtime | None (transient) | Session | ⚠️ Provisional |
| 22 | **LLM Output** | LLM Runtime | LLM Runtime | Renderer, Memory System (for extraction) | None (transient, content extracted to Memory) | Session | ⚠️ Provisional |
| 23 | **Image Output** | Image Pipeline | Image Pipeline | Renderer, Gallery System | Save System (if Gallery entry) | Persistent (if committed) | 🔮 Future |
| 24 | **CG Request** | Narrative Director | Narrative Director | Image Pipeline | None (transient) | Session | ⚠️ Provisional |

---

## 8. Memory Artifacts（记忆制品）

| # | Artifact | Produced By | Owned By | Consumed By | Persisted By | Lifecycle | Confidence |
|---|----------|-------------|----------|-------------|--------------|-----------|------------|
| 25 | **Memory Object** | Memory System (extraction) | Memory System | Relationship Engine, Narrative Director, Prompt Builder, Simulation Layer | Memory System (long-term storage) | Persistent (evolving) | ⚠️ Provisional |
| 26 | **Memory Quality Attributes** | Memory System | Memory System | Memory System (internal retrieval) | Memory System | Persistent (evolving) | ⚠️ Provisional |

> **Memory objects are immutable in content but evolving in quality.** The original experience cannot be modified, but Strength, Accuracy, Accessibility, and Emotional Weight evolve over time.

> **记忆对象内容不可变，但质量演化。** 原始经历不可修改，但强度、准确度、可访问性和情感权重随时间演化。

---

## 9. Authority-to-Artifact Summary（权威层与制品关系总览）

This view shows which Authority layer is responsible for which artifacts.

此视图展示哪个权威层负责哪些制品。

| Authority Layer | Produces | Owns (Lifecycle) | Archives Via | Confidence |
|----------------|----------|-------------------|--------------|------------|
| ① Intent | Action Object | Action Object | Log Manager | ✅ Confirmed |
| ② Execution | Action Record | Action Record | Log Manager | ✅ Confirmed |
| ③ Simulation | SimulationResult, Behavior Tendency, Relationship Constraints | SimulationResult (transient) | Log Manager | SimulationResult: ✅ Confirmed; Behavior Tendency & Constraints: ⚠️ Provisional |
| ④ Reality | Event Object | Event Object (immutable), Timeline | Log Manager + Future Timeline Storage | Event Object: ✅ Confirmed; Timeline Storage: 🔮 Future |
| ⑤ State | State Mutation | Character State, Relationship State, World State, Progression State, Timeline State | Snapshot Manager + Save System | Character/Relationship State: ✅ Confirmed; World/Progression/Timeline State: 🔮 Future |
| Infrastructure | Runtime Log, Snapshot, Seed, Replay Session | Runtime Log, Snapshot Store, Seed Stream, Replay Session | Self-managed | ✅ Confirmed |
| Generation | Prompt Package, LLM Output, Image Output, CG Request | Prompt Package, LLM Output, Image Output | Save System (Gallery only) | Prompt/LLM/CG: ⚠️ Provisional; Image: 🔮 Future |
| Memory | Memory Object, Memory Quality Attributes | Memory Object, Memory Quality Attributes | Memory System | ⚠️ Provisional |

---

## 10. Conflict Resolution Rules（冲突解决规则）

When ownership is ambiguous, these rules resolve the conflict:

当归属不明确时，以下规则解决冲突：

| Rule | Description |
|------|-------------|
| **Authority Precedence** | If an artifact is produced by an Authority layer, that layer owns it — even if Infrastructure persists it. |
| **Infrastructure Serves** | Infrastructure components own their storage format and stream, but never the data's semantic meaning. |
| **Transient vs Persistent** | Transient artifacts are owned by their producer. Persistent artifacts are owned by the Authority layer that authorizes their mutation. |
| **State Owns Mutation** | No module may directly mutate Persistent State. All mutations flow through State Authority (Layer ⑤). Simulation Authority (Layer ③) computes deltas; State Authority applies them. |
| **Event Immutability** | Once committed to the Timeline, an Event Object cannot be modified by any module — including the one that produced it. |
| **Confidence-Weighted Interpretation** | Provisional and Future artifacts may change during Phase B migration. Confirmed artifacts are stable and may be treated as architectural facts. |

> **新增规则：** 置信度加权解释。Provisional 和 Future 制品可能在 Phase B 迁移期间变化。Confirmed 制品是稳定的，可以作为架构事实对待。

---

## 11. Cross-Reference Validation（交叉引用验证）

This Matrix should be used during Consistency Audit (Phase C) to validate:

本矩阵应在一致性审计（Phase C）期间用于验证：

| Check | What to Verify |
|-------|---------------|
| Producer Consistency | Does the Blueprint that claims to produce an artifact match this Matrix? |
| Consumer Consistency | Does every Blueprint that claims to consume an artifact match this Matrix? |
| Persistence Consistency | Does the Infrastructure Blueprint's component responsibility match this Matrix? |
| Lifecycle Consistency | Is each artifact's Transient/Persistent classification consistent across all Blueprints? |
| Schema Consistency | Does each artifact with a Schema reference the correct schema document? |
| Confidence Consistency | Has every Provisional artifact been re-evaluated after its parent Blueprint was migrated? |

---

## References

**Depends On:**

- [Runtime Pipeline Blueprint](./Runtime_Pipeline_Blueprint.md) — defines when artifacts are produced
- [Runtime Infrastructure Blueprint](./Runtime_Infrastructure_Blueprint.md) — defines where artifacts are persisted
- [Runtime State Model Blueprint](./Runtime_State_Model_Blueprint.md) — defines state domain ownership
- All Data Schemas — define artifact structure

**Referenced By:**

- [Architecture Migration Matrix](./Architecture_Migration_Matrix.md)
- RC Freeze Checklist
- Future Consistency Audit Report
- Future Authority Matrix

---

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| v1.0 | 2026-07-14 | Initial Artifact Ownership Matrix. 26 artifacts across 7 categories (Pipeline, State, Session, Infrastructure, Generation, Memory). Authority-to-Artifact summary. Conflict resolution rules. Cross-reference validation checklist. |
| v1.1 | 2026-07-14 | Governance refinement based on joint Architecture Review (GPT + CatPaw): Added Confidence column (Confirmed / Provisional / Future) to all artifact tables and Authority-to-Artifact Summary. Marked 5 core Pipeline artifacts as Confirmed, 10 session/generation/memory artifacts as Provisional, 5 state/generation artifacts as Future. Renamed "Timeline Store" to "Future Timeline Storage" to reflect that no Blueprint defines it. Added Confidence-Weighted Interpretation conflict resolution rule. Added Confidence Consistency cross-reference validation check. |
