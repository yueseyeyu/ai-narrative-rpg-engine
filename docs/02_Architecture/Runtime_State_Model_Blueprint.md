# Runtime State Model Blueprint

**Version:** v1.0  
**Status:** Draft  
**Last Updated:** 2026-07-13

---

## 1. Purpose（文档目的）

Define the structure, ownership, lifecycle, and mutation rules of Runtime State in the AI Narrative RPG Engine.

定义 AI Narrative RPG Engine 中 Runtime State 的结构、归属、生命周期和变更规则。

### Core Definition（核心定义）

Runtime State is the **single source of ground truth** for the entire Engine at runtime.

Runtime State 是引擎运行时的**唯一事实来源**。

It encompasses all persistent game data and all transient runtime data that exist during a Scene execution.

它涵盖 Scene 执行期间存在的所有持久化游戏数据和所有瞬态运行时数据。

### Core Philosophy（核心理念）

Runtime State is fact. Generated content is expression.

Runtime State 是事实，生成内容是表达。

The Engine reads Runtime State to produce experiences, and writes back to Runtime State only through Simulation Layer.

引擎读取 Runtime State 产生体验，仅通过 Simulation Layer 写回 Runtime State。

---

## 2. Responsibilities（职责）

### Responsible For（负责）

- Defining the structure of Runtime State
- Defining the boundary between Persistent State and Session State
- Defining ownership and access rights for each state domain
- Defining state mutation rules and guarantees
- Serving as the parent blueprint for all future schema documents

### Not Responsible For（不负责）

- Specific data schema implementation
- Database schema or storage format
- Prompt templates
- Module call order (see Runtime Architecture Blueprint)
- Scene lifecycle management (see Scene Engine Blueprint)

---

## 3. Document Governance（文档治理）

**Owner:** Runtime Architect

**Reviewers:**

- Engine Architect
- Simulation Architect
- Memory Architect

**Approval:** Architecture Review Required

**Update Policy:** Changes affecting state domain structure, ownership boundaries, or snapshot/branch semantics require ADR approval.

---

## 4. Design Principles（设计原则）

| Principle | Description |
|-----------|-------------|
| State Is Fact | 状态是唯一事实来源。Runtime State is the single source of truth. |
| Simulation Owns Mutation | 只有 Simulation Layer 可以变更 Runtime State。Only Simulation Layer may mutate Runtime State. |
| Persistent vs Session Separation | 持久状态与会话状态严格分离。Persistent State survives across sessions; Session State is transient. |
| Reference, Not Own | Runtime State 引用记忆，不拥有记忆数据库。Runtime State references memories, not owns the Memory database. |
| Deterministic Snapshot | 相同状态 + 相同输入 = 相同输出。Identical state + identical input = identical output. |
| Branchable | 状态支持分支与回滚。State supports branching and rollback for deterministic simulation and replay. |

---

## 5. Runtime State Structure（Runtime State 结构）

Runtime State is divided into two layers: **Persistent State** and **Session State**.

```mermaid
flowchart TD
    RS[Runtime State]
    RS --> PS[Persistent State]
    RS --> SS[Session State]

    PS --> CS[Character State]
    PS --> RLS[Relationship State]
    PS --> WS[World State]
    PS --> PS2[Progression State]
    PS --> TS[Timeline State]

    SS --> SESS[Scene State]
    SS --> EVT[Runtime Events]
    SS --> AMR[Active Memory References]
    SS --> RM[Runtime Metadata]
```

### 5.1 Persistent State（持久状态）

Persistent State is long-lived game data that survives across sessions, scenes, and engine restarts.

持久状态是跨会话、跨 Scene、跨引擎重启存活的长期游戏数据。

| Domain | Description | Key Fields |
|--------|-------------|------------|
| Character State | 角色状态 — 人格、情绪、目标、内部状态 | personality, mood, goals, internal_state |
| **Relationship State** | **关系状态（核心）** — 多维度关系数据 | trust, affection, dependence, intimacy, respect, jealousy, attachment |
| World State | 世界状态 — 时间、地点、环境、全局事件 | time, location, environment, global_events |
| Progression State | 进度状态 — 任务、解锁、故事推进 | quest_progress, unlock_status, story_progression |
| Timeline State | 时间线状态 — 连续事件时间线 | timeline_entries, current_epoch |

**Relationship State is the core driver of the entire Engine.**

**Relationship State 是整个引擎的核心驱动。**

### 5.2 Session State（会话状态）

Session State is transient runtime data that exists only during the current Scene execution. It is discarded or committed at Scene completion.

会话状态是仅在当前 Scene 执行期间存在的瞬态运行时数据，在 Scene 完成时丢弃或提交。

| Domain | Description | Key Fields |
|--------|-------------|------------|
| Scene State | 场景状态 — 当前 Scene 执行状态 | scene_phase, active_participants, current_objective |
| Runtime Events | 运行时事件 — 当前 Tick 产生的瞬态事件 | trigger, actor, action, consequence, narrative_weight, priority |
| Active Memory References | 活跃记忆引用 — 当前 Scene 激活的记忆引用列表 | memory_id, activation_level, retrieval_priority |
| Runtime Metadata | 运行时元数据 — 标识和追踪当前执行上下文 | see Section 7 |

#### Scene State（场景状态）

Scene State tracks the execution progress of the current Scene.

| Field | Description |
|-------|-------------|
| scene_phase | Current phase (Created, Simulating, Planning, Generating, Completed) |
| active_participants | Characters involved in the current Scene |
| current_objective | The objective of the current Scene |

#### Runtime Events（运行时事件）

Runtime Events are **transient**. They exist only within the current Scene execution.

运行时事件是**瞬态的**，仅存在于当前 Scene 执行期间。

Historical events are not stored in Runtime State. They belong to the **Memory System**.

历史事件不存储在 Runtime State 中，它们属于 **Memory System**。

| Field | Description |
|-------|-------------|
| trigger | 触发条件 |
| actor | 参与者 |
| action | 行为 |
| consequence | 后果 |
| narrative_weight | 叙事权重 |
| priority | 优先级 |

#### Active Memory References（活跃记忆引用）

Runtime State does **NOT** own the Memory database. Instead, it holds a lightweight reference to memories activated for the current Scene.

Runtime State **不拥有** 记忆数据库。它持有当前 Scene 激活的记忆的轻量引用。

| Field | Description |
|-------|-------------|
| memory_id | Reference to a Memory Object in the Memory System |
| activation_level | 激活级别 (0.0 – 1.0) |
| retrieval_priority | 检索优先级 |

**Rule:** Memory Objects themselves are owned and managed by the Memory System. Runtime State only holds references.

**规则：** Memory Object 本身由 Memory System 拥有和管理，Runtime State 只持有引用。

---

## 6. Boundary Definition（边界定义）

### Owns（拥有）

- Persistent State structure definition
- Session State structure definition
- State mutation rules
- Snapshot / Branch semantics
- Runtime Metadata definition

### Does NOT Own（不拥有）

- Memory Objects (owned by Memory System)
- Historical Event Log (owned by Memory System)
- Prompt data (owned by Prompt Builder)
- Narrative plans (owned by Narrative Director)
- LLM output (owned by LLM Runtime)

---

## 7. Runtime Metadata（运行时元数据）

Runtime Metadata identifies and tracks the current execution context. It is part of Session State.

| Field | Description |
|-------|-------------|
| game_id | 当前游戏存档的唯一标识 |
| runtime_version | 引擎运行时版本 |
| save_version | 存档格式版本 |
| scene_id | 当前 Scene 的唯一标识 |
| tick | 当前 Simulation Tick 编号 |
| seed | 当前确定性种子 |
| created_at | 当前 Session 创建时间戳 |
| updated_at | 最近一次状态更新时间戳 |

Runtime Metadata is used for:

- Deterministic replay
- Save/load compatibility checking
- Debugging and observability
- Version migration

---

## 8. Runtime Ownership（运行时归属）

This section explicitly defines which module owns each runtime domain and which modules have read-only access.

### Ownership Matrix（归属矩阵）

| State Domain | Owner (Read/Write) | Read-Only Access |
|--------------|-------------------|-----------------|
| Character State | Simulation Layer | Narrative Director, Prompt Builder, Memory System, LLM Runtime |
| **Relationship State** | **Relationship Engine** (via Simulation Layer) | Narrative Director, Prompt Builder, Memory System |
| World State | Simulation Layer | Narrative Director, Prompt Builder, Memory System |
| Progression State | Simulation Layer | Narrative Director, Prompt Builder |
| Timeline State | Simulation Layer | Narrative Director, Prompt Builder, Memory System |
| Scene State | Scene Engine | Simulation Layer, Narrative Director |
| Runtime Events | Simulation Layer | Narrative Director, Prompt Builder |
| Active Memory References | Memory System | Narrative Director, Prompt Builder, Simulation Layer |
| Runtime Metadata | Scene Engine | All modules (read-only) |

### Ownership Rules（归属规则）

| Rule | Description |
|------|-------------|
| Simulation Layer is the sole state mutation authority | 只有 Simulation Layer 可以变更 Persistent State。Only Simulation Layer may mutate Persistent State. |
| Relationship Engine mutates Relationship State via Simulation Layer | Relationship Engine 通过 Simulation Layer 变更 Relationship State。 |
| Memory System manages Active Memory References | Memory System 负责激活和更新记忆引用，但不修改 Persistent State。 |
| Scene Engine manages Scene State and Runtime Metadata | Scene Engine 管理场景执行状态和元数据，但不修改 Persistent State。 |
| All other modules are read-only consumers | 所有其他模块只读消费 Runtime State。 |

---

## 9. Snapshot & Branch Semantics（快照与分支语义）

### 9.1 Snapshot（快照）

A Snapshot captures the complete Runtime State at a specific point in time.

快照捕获特定时间点的完整 Runtime State。

Every Scene begins from a Snapshot. If Scene execution fails, the Engine rolls back to the Snapshot.

每个 Scene 从快照开始。如果 Scene 执行失败，引擎回滚到快照。

### 9.2 Branch / Fork（分支 / 分叉）

Runtime State supports **Branch / Fork** semantics beyond simple snapshots.

Runtime State 支持超越简单快照的**分支 / 分叉**语义。

```mermaid
flowchart TD
    MAIN[Main State Branch] --> SNAPSHOT[Snapshot at Scene Start]
    SNAPSHOT --> SIM[Simulation Tick]
    SIM --> VALID{Validation}
    VALID -->|Pass| COMMIT[Commit to Main Branch]
    VALID -->|Fail| ROLLBACK[Rollback to Snapshot]

    SNAPSHOT --> FORK[Fork for Planning]
    FORK --> PLAN[Narrative Planning - Read-only]
    FORK --> REPLAY[Replay for Debugging]
    FORK --> FUTURE[Future State Projection]
```

| Operation | Description |
|-----------|-------------|
| Snapshot | 捕获当前完整状态。Capture complete current state. |
| Branch | 从快照创建一个可独立演化的状态分支。Create an independently evolving state branch from a snapshot. |
| Fork | 复制当前状态用于只读推演或规划。Copy current state for read-only projection or planning. |
| Commit | 将分支变更合并回主分支。Merge branch changes back to main branch. |
| Rollback | 丢弃分支变更，恢复到快照。Discard branch changes, restore to snapshot. |

### 9.3 Use Cases（使用场景）

| Use Case | Branch Type | Description |
|----------|-------------|-------------|
| Scene Transaction | Snapshot + Rollback | Scene 失败时回滚到快照 |
| Deterministic Replay | Fork | 从历史快照重放，不影响主分支 |
| Future State Projection | Fork | Narrative Director 或 Simulation 预演未来可能状态 |
| Save / Load | Snapshot | 持久化当前状态到存档 |
| Debugging | Fork | 创建调试分支，不影响游戏主分支 |

---

## 10. State Transition Rules（状态转换规则）

All state transitions must satisfy:

| Property | Description |
|----------|-------------|
| Deterministic | 确定性 — 相同输入产生相同输出 |
| Traceable | 可追溯 — 每次转换都有记录 |
| Replayable | 可重放 — 支持从任意快照重新执行 |
| Recoverable | 可恢复 — 支持 Scene 失败时回滚 |
| Validated | 一致性验证 — 转换结果必须通过验证 |
| Branchable | 可分支 — 支持从任意快照创建分支 |

LLM 不允许直接修改任何 Runtime State。

---

## 11. Runtime Guarantees（运行时保证）

Runtime State Model guarantees:

- All Persistent State mutations go through Simulation Layer.
- Session State is discarded or committed at Scene completion.
- Runtime State never owns Memory Objects — it only holds references.
- Historical events are not stored in Runtime State — they belong to Memory System.
- Every Scene begins from a validated Snapshot.
- Failed Scene execution rolls back to the Snapshot without corrupting Persistent State.
- Runtime Metadata is always present and versioned.
- State transitions are deterministic, traceable, and replayable.

---

## 12. Relationship to Other Blueprints（与其他 Blueprint 的关系）

This Blueprint is the **parent blueprint** for all future schema documents.

本 Blueprint 是所有未来 Schema 文档的**父 Blueprint**。

| Blueprint | Relationship |
|-----------|-------------|
| Runtime Architecture Blueprint | 定义 Runtime State 如何在运行时流转 |
| Simulation Layer Blueprint | 定义谁可以变更 Runtime State |
| Scene Engine Blueprint | 定义 Scene 事务如何保护 Runtime State |
| Relationship Engine Blueprint | 定义 Relationship State 的演化规则 |
| Memory Architecture Blueprint | 定义 Memory System 与 Runtime State 的引用关系 |
| Narrative Director Blueprint | 消费 Runtime State（只读） |
| Prompt Builder Blueprint | 消费 Runtime State（只读） |
| LLM Runtime Blueprint | 不直接访问 Runtime State |

Future schema documents (Character Schema, Relationship Schema, World Schema, etc.) must conform to the structure and ownership defined in this Blueprint.

---

## 13. Hardware Considerations（硬件考量）

**Target Hardware:** RTX 5060 8GB / 32GB RAM

| Consideration | Description |
|---------------|-------------|
| In-memory State | Runtime State 应在内存中维护，避免频繁磁盘 I/O |
| Snapshot Compression | 快照应支持压缩以减少内存占用 |
| Branch Efficiency | 分支应使用 Copy-on-Write 语义，避免完整复制 |
| Background Persistence | 持久化应在后台异步执行，不阻塞 Scene 执行 |

---

## References

**Depends On:**

- Overall Architecture Blueprint
- Runtime Architecture Blueprint
- Glossary

**Referenced By:**

- Simulation Layer Blueprint
- Scene Engine Blueprint
- Relationship Engine Blueprint
- Memory Architecture Blueprint
- Narrative Director Blueprint
- Prompt Builder Blueprint
- Future Schema Documents (Character Schema, Relationship Schema, World Schema, etc.)

---

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| v1.0 | 2026-07-13 | Initial Blueprint: Persistent/Session split, Active Memory References, Runtime Metadata, Branch/Fork semantics, Runtime Ownership matrix |
