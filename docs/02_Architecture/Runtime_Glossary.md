# Runtime Glossary

**Version:** v1.0 Draft  
**Status:** Draft  
**Last Updated:** 2026-07-14

**Purpose:** Unified terminology definitions for all Runtime Blueprints. Each term is defined exactly once. All Blueprints SHALL reference this Glossary instead of redefining terms.

**目的：** 所有 Runtime Blueprint 的统一术语定义。每个术语只定义一次。所有 Blueprint 应引用本词汇表，而非重新定义术语。

---

## How to Use（使用方式）

- When a Blueprint uses a term, it SHALL link to this Glossary: `[Term](./Runtime_Glossary.md#term)`
- If a term is not yet defined here, add it before using it in a Blueprint
- Definitions are authoritative — if a Blueprint's usage conflicts with this Glossary, the Glossary wins

---

## A. Architecture Concepts（架构概念）

### Authority

The right and responsibility to make decisions about a specific aspect of the Runtime. Each Authority layer owns exactly one decision domain. Authorities are non-overlapping and non-negotiable.

**权威。** 对运行时特定方面做出决策的权利和责任。每个权威层拥有且仅拥有一个决策域。权威之间不重叠、不可妥协。

*Reference: [Runtime Architecture Blueprint](./Runtime_Architecture_Blueprint.md)*

### Platform

The infrastructure layer that provides runtime environment capabilities — lifecycle, threading, snapshots, seeds, logs, replay, event bus. Platform serves; Platform does not decide.

**平台。** 提供运行时环境能力的基础设施层。平台服务；平台不决策。

*Reference: [Runtime Infrastructure Blueprint §1](./Runtime_Infrastructure_Blueprint.md)*

### Pipeline

The 5-Layer Authority Pipeline (Intent → Execution → Simulation → Reality → State) that defines what happens in the Runtime. Pipeline decides; Pipeline does not serve.

**流水线。** 五层权威流水线（Intent → Execution → Simulation → Reality → State），定义运行时中发生什么。流水线决策；流水线不服务。

*Reference: [Runtime Pipeline Blueprint](./Runtime_Pipeline_Blueprint.md)*

### Infrastructure

Synonym for Platform. Used interchangeably in Blueprints. See Platform.

**基础设施。** 平台的同义词。在 Blueprint 中互换使用。参见 Platform。

### Determinism

The guarantee that same inputs (State Snapshot + Action + Seed) always produce the same output (SimulationResult). The entire simulation is replayable.

**确定性。** 相同输入（状态快照 + Action + 种子）始终产生相同输出（SimulationResult）的保证。整个模拟可重放。

*Reference: [Runtime Infrastructure Blueprint §10.1](./Runtime_Infrastructure_Blueprint.md)*

---

## B. Authority Layers（权威层）

### Intent Authority

The first pipeline layer. Decides *what Action to attempt*. Owned by the Planner. Produces Action Objects.

**意图权威。** 流水线第一层。决定*尝试什么 Action*。由 Planner 拥有。产出 Action Object。

*Reference: [Runtime Pipeline Blueprint §3](./Runtime_Pipeline_Blueprint.md)*

### Execution Authority

The second pipeline layer. Decides *whether an Action is valid and how to execute it*. Owned by AEM. Produces Action Records.

**执行权威。** 流水线第二层。决定*Action 是否有效以及如何执行*。由 AEM 拥有。产出 Action Record。

*Reference: [Action Execution Model](./Action_Execution_Model.md)*

### Simulation Authority

The third pipeline layer. Decides *what happens when the Action meets the world*. Owned by the Simulation Layer. Produces SimulationResults.

**模拟权威。** 流水线第三层。决定*当 Action 遇到世界时发生什么*。由 Simulation Layer 拥有。产出 SimulationResult。

*Reference: [Simulation Layer Blueprint](./Simulation_Layer_Blueprint.md)*

### Reality Authority

The fourth pipeline layer. Decides *what becomes objective reality*. Owned by the Timeline Manager. Produces Event Objects.

**现实权威。** 流水线第四层。决定*什么成为客观现实*。由 Timeline Manager 拥有。产出 Event Object。

*Reference: [Event Object Schema](../03_Data/Event_Object_Schema.md)*

### State Authority

The fifth pipeline layer. Decides *how the world changes*. Owned by the State Management Layer. Produces State Mutations.

**状态权威。** 流水线第五层。决定*世界如何变化*。由 State Management Layer 拥有。产出状态变更。

*Reference: [Runtime State Model Blueprint](./Runtime_State_Model_Blueprint.md)*

---

## C. Runtime Objects（运行时对象）

### Action Object

A declarative expression of intent — "I want to do X." Contains no execution logic, no scheduling, no simulation parameters. Produced by Planner, consumed by AEM.

**Action Object。** 意图的声明式表达 — "我想做 X。" 不含执行逻辑、调度或模拟参数。由 Planner 产出，由 AEM 消费。

*Reference: [Action Object Schema](../03_Data/Action_Object_Schema.md) (Locked)*

### Action Record

A validated Action Object with execution metadata (record_id, status, lifecycle timestamps). Produced by AEM, dispatched to Simulation Layer via Dispatcher.

**Action Record。** 已验证的 Action Object，附带执行元数据（record_id、状态、生命周期时间戳）。由 AEM 产出，通过 Dispatcher 分发到 Simulation Layer。

*Reference: [Action Execution Model](./Action_Execution_Model.md)*

### Action Type

A registered type definition in the Action Registry. Defines schema, capabilities, handler binding, and validation rules for a category of Actions.

**Action Type。** Action Registry 中注册的类型定义。定义一类 Action 的 schema、能力、handler 绑定和验证规则。

*Reference: [Action Registry](./Action_Registry.md)*

### SimulationResult

The computed outcome of a Simulation Tick — what happened when an Action met the world. Contains deltas, narrative seed, and failure status. Transient: exists during a Scene, discarded after Timeline commit.

**SimulationResult。** 一次 Simulation Tick 的计算结果 — 当 Action 遇到世界时发生了什么。包含 delta、叙事种子和失败状态。瞬态：在 Scene 期间存在，Timeline 提交后丢弃。

*Reference: [SimulationResult Schema](../03_Data/SimulationResult_Schema.md)*

### Event Object

An immutable record of committed reality. Once committed to the Timeline, an Event is objective reality — it cannot be revoked, modified, or undone. Produced by Timeline Manager from SimulationResults.

**Event Object。** 已提交现实的不可变记录。一旦提交到 Timeline，Event 即为客观现实 — 不可撤销、修改或撤销。由 Timeline Manager 从 SimulationResult 产出。

*Reference: [Event Object Schema](../03_Data/Event_Object_Schema.md)*

### Runtime Log

An append-only infrastructure archive of Action Objects, Action Records, and SimulationResults. Used for replay, debugging, and profiling. Distinct from Event Timeline.

**Runtime Log。** Action Object、Action Record 和 SimulationResult 的只追加基础设施归档。用于重放、调试和性能分析。与 Event Timeline 不同。

*Reference: [Runtime Infrastructure Blueprint §4.6](./Runtime_Infrastructure_Blueprint.md)*

---

## D. Runtime Components（运行时组件）

### Runtime Manager

Top-level coordinator for engine lifecycle. Coordinates startup/shutdown ordering; does not execute component internals. Process Coordinator, not Component Manager.

**Runtime Manager。** 引擎生命周期的顶层协调器。协调启动/关闭顺序；不执行组件内部逻辑。进程协调器，非组件管理器。

*Reference: [Runtime Infrastructure Blueprint §4.1](./Runtime_Infrastructure_Blueprint.md)*

### Registry Manager

Manages Action Registry lifecycle — registration, snapshot creation, hot reload. Owns Registry snapshot lifecycle; does not own type definitions or validation rules.

**Registry Manager。** 管理 Action Registry 生命周期 — 注册、快照创建、热更新。拥有 Registry 快照生命周期；不拥有类型定义或验证规则。

*Reference: [Runtime Infrastructure Blueprint §4.2](./Runtime_Infrastructure_Blueprint.md)*

### Snapshot Manager

Manages Runtime State snapshots — creation, storage, fork, and archiving. Provides restore points; does not decide when to roll back. Snapshot is a storage representation, not a State model.

**Snapshot Manager。** 管理运行时状态快照 — 创建、存储、fork 和归档。提供恢复点；不决定何时回滚。快照是存储表示，不是状态模型。

*Reference: [Runtime Infrastructure Blueprint §4.3](./Runtime_Infrastructure_Blueprint.md)*

### Simulation Dispatcher

Transports validated Actions from AEM to the Simulation Layer. Transport only — never schedules, prioritizes, batches, retries, or transforms.

**Simulation Dispatcher。** 将已验证的 Action 从 AEM 传输到 Simulation Layer。仅传输 — 不调度、不排优、不批量、不重试、不转换。

*Reference: [Runtime Infrastructure Blueprint §4.4](./Runtime_Infrastructure_Blueprint.md)*

### Seed Manager

Generates and distributes deterministic seeds for Simulation Layer. Produces reproducible seed sequences; does not decide how seeds are used.

**Seed Manager。** 为 Simulation Layer 生成和分发确定性种子。产生可重现的种子序列；不决定种子如何使用。

*Reference: [Runtime Infrastructure Blueprint §4.5](./Runtime_Infrastructure_Blueprint.md)*

### Log Manager

Manages the Runtime Log stream — append ordering, retention, indexing. Owns the stream; does not own log entry semantics or payload schema.

**Log Manager。** 管理 Runtime Log 流 — 追加顺序、保留策略、索引。拥有流；不拥有日志条目语义或负载 schema。

*Reference: [Runtime Infrastructure Blueprint §4.6](./Runtime_Infrastructure_Blueprint.md)*

### Replay Manager

Manages Replay sessions — restoring historical context and re-executing Actions. Consumes Runtime Log (producer → consumer). Manages sessions; does not own verification logic.

**Replay Manager。** 管理重放会话 — 恢复历史上下文并重新执行 Action。消费 Runtime Log（生产者 → 消费者）。管理会话；不拥有验证逻辑。

*Reference: [Runtime Infrastructure Blueprint §4.7](./Runtime_Infrastructure_Blueprint.md)*

### Event Bus

Internal pub/sub message routing between Runtime components. Messages are delivery artifacts — notifications, not domain events. Event Bus is NOT observable reality.

**Event Bus。** 运行时组件间的内部发布/订阅消息路由。消息是递送产物 — 通知，不是领域事件。Event Bus 不是可观测现实。

*Reference: [Runtime Infrastructure Blueprint §4.8](./Runtime_Infrastructure_Blueprint.md)*

### Planner

The Intent Authority component. Converts player input and narrative goals into Action Objects. Decides what Action to attempt.

**Planner。** 意图权威组件。将玩家输入和叙事目标转化为 Action Object。决定尝试什么 Action。

*Reference: Future: Planner / Intent Parser Blueprint*

### AEM (Action Execution Model)

The Execution Authority component. Validates Action Objects against Registry definitions. Produces Action Records. Decides Action lifecycle (accept, cancel, reject).

**AEM（Action Execution Model）。** 执行权威组件。根据 Registry 定义验证 Action Object。产出 Action Record。决定 Action 生命周期（接受、取消、拒绝）。

*Reference: [Action Execution Model](./Action_Execution_Model.md)*

### Simulation Layer

The Simulation Authority component. Executes Simulation Ticks — computes what happens when an Action meets the world state. Produces SimulationResults.

**Simulation Layer。** 模拟权威组件。执行 Simulation Tick — 计算当 Action 遇到世界状态时发生什么。产出 SimulationResult。

*Reference: [Simulation Layer Blueprint](./Simulation_Layer_Blueprint.md)*

### Timeline Manager

The Reality Authority component. Commits SimulationResults as immutable Event Objects. Maintains the Timeline — the authoritative record of what happened.

**Timeline Manager。** 现实权威组件。将 SimulationResult 提交为不可变 Event Object。维护 Timeline — 已发生事件的权威记录。

*Reference: [Event Object Schema](../03_Data/Event_Object_Schema.md)*

### State Management Layer

The State Authority component. Applies Event Deltas to Runtime State. Produces State Mutations. Owns the state model.

**State Management Layer。** 状态权威组件。将 Event Delta 应用到运行时状态。产出状态变更。拥有状态模型。

*Reference: [Runtime State Model Blueprint](./Runtime_State_Model_Blueprint.md)*

---

## E. Runtime Concepts（运行时概念）

### Scene

The atomic runtime unit. A Scene begins from a validated snapshot, executes Simulation Ticks, and ends with a commit or rollback. Scene is the transaction boundary.

**Scene。** 原子运行时单位。Scene 从已验证的快照开始，执行 Simulation Tick，以提交或回滚结束。Scene 是事务边界。

*Reference: [Scene Engine Blueprint](./Scene_Engine_Blueprint.md)*

### Tick

A single simulation execution cycle. One Tick = one Action dispatched → one SimulationResult produced. Ticks are atomic — either complete or roll back.

**Tick。** 单次模拟执行周期。一个 Tick = 一个 Action 分发 → 一个 SimulationResult 产出。Tick 是原子的 — 要么完成，要么回滚。

### Dispatch

The act of transporting a validated Action from AEM to the Simulation Layer via the Dispatcher. Dispatch preserves ordering; it does not schedule or prioritize.

**Dispatch。** 通过 Dispatcher 将已验证的 Action 从 AEM 传输到 Simulation Layer 的行为。Dispatch 保持顺序；不调度或排优。

### Snapshot

An immutable, consistent copy of Runtime State at a point in time. Created by Snapshot Manager. Used as input for Simulation and as restore points for transactions.

**快照。** 某一时间点运行时状态的不可变、一致副本。由 Snapshot Manager 创建。用作模拟输入和事务恢复点。

### Fork

Creating a read-only snapshot copy for prediction purposes. Forking SHALL avoid full state duplication — structural sharing or equivalent mechanisms MAY be used.

**Fork。** 为预测目的创建只读快照副本。Fork 应避免全量状态复制 — 可使用结构共享或等效机制。

### Commit

The act of finalizing a Scene transaction. On commit, Event Objects are written to the Timeline and State Mutations are applied. After commit, the Scene's changes become permanent.

**提交。** 完成 Scene 事务的行为。提交时，Event Object 被写入 Timeline，状态变更被应用。提交后，Scene 的变更成为永久性的。

### Rollback

The act of discarding a Scene transaction and restoring to the snapshot taken before the Scene began. Rollback is a transaction-level decision, not a Snapshot Manager decision.

**回滚。** 丢弃 Scene 事务并恢复到 Scene 开始前快照的行为。回滚是事务级决策，不是 Snapshot Manager 的决策。

### Transaction

A Scene's execution lifecycle — from snapshot creation to commit or rollback. Transactions are atomic: either all changes are committed, or none are.

**事务。** Scene 的执行生命周期 — 从快照创建到提交或回滚。事务是原子的：要么所有变更提交，要么都不提交。

### Replay

The process of re-executing historical Actions to verify determinism or debug issues. Replay consumes Runtime Log and uses isolated snapshots and seeds. Replay SHALL NOT affect live Runtime state.

**重放。** 重新执行历史 Action 以验证确定性或调试问题的过程。重放消费 Runtime Log 并使用隔离的快照和种子。重放不得影响活跃运行时状态。

### Prediction

Simulating Actions on a forked snapshot to preview potential outcomes. Prediction results are never committed to the Timeline. Prediction is isolated from the main Runtime.

**预测。** 在 fork 快照上模拟 Action 以预览潜在结果。预测结果永远不会提交到 Timeline。预测与主运行时隔离。

### Hot Reload

The process of updating Action Types or Handlers at runtime without restarting the engine. Hot reload occurs at Scene boundaries. Uses build-then-swap: new snapshot is fully built before becoming visible.

**热更新。** 在运行时更新 Action Type 或 Handler 而不重启引擎的过程。热更新在 Scene 边界发生。使用 build-then-swap：新快照在可见之前完全构建。

### Timeline

The authoritative, append-only record of committed Event Objects. The Timeline represents objective reality — what actually happened in the world. Distinct from Runtime Log.

**Timeline。** 已提交 Event Object 的权威、只追加记录。Timeline 代表客观现实 — 世界上实际发生的事。与 Runtime Log 不同。

### Event Bus Message

A transient infrastructure notification routed through Event Bus. Messages are delivery artifacts (e.g., "Timeline committed"), not domain events. They carry no narrative content and are never Event Objects.

**Event Bus 消息。** 通过 Event Bus 路由的瞬态基础设施通知。消息是递送产物（如"Timeline 已提交"），不是领域事件。它们不携带叙事内容，永远不是 Event Object。

### Seed

A deterministic random number source used by the Simulation Layer. Seeds are reproducible — the same seed sequence produces the same simulation results. Managed by Seed Manager.

**种子。** Simulation Layer 使用的确定性随机数源。种子可重现 — 相同种子序列产生相同模拟结果。由 Seed Manager 管理。

### Handler

A function bound to an Action Type that executes the simulation logic for that type. Handlers are owned by the Simulation Layer; their bindings are managed by Registry Manager.

**Handler。** 绑定到 Action Type 的函数，执行该类型的模拟逻辑。Handler 由 Simulation Layer 拥有；其绑定由 Registry Manager 管理。

### Capability

A declared feature of an Action Type (e.g., `requires_target`, `is_dialogue`). Used by Planner for Discovery API filtering and by AEM for validation.

**能力。** Action Type 的声明特性（如 `requires_target`、`is_dialogue`）。Planner 用于 Discovery API 过滤，AEM 用于验证。

### Discovery

The process of querying the Action Registry to find available Action Types by capability, category, or metadata. Used by the Planner to determine what Actions are possible.

**发现。** 查询 Action Registry 以按能力、类别或元数据查找可用 Action Type 的过程。Planner 用于确定哪些 Action 是可能的。

---

## F. State Concepts（状态概念）

### Persistent State

State that survives across sessions — Character State, Relationship State, World State, Progression State, Timeline State. Persisted to save files.

**持久状态。** 跨会话存活的状态 — Character State、Relationship State、World State、Progression State、Timeline State。持久化到存档文件。

*Reference: [Runtime State Model Blueprint](./Runtime_State_Model_Blueprint.md)*

### Session State

State that exists only during a running session — Scene State, Runtime Events, Active Memory References, Runtime Metadata. Discarded on shutdown.

**会话状态。** 仅在运行会话期间存在的状态 — Scene State、Runtime Events、Active Memory References、Runtime Metadata。关闭时丢弃。

*Reference: [Runtime State Model Blueprint](./Runtime_State_Model_Blueprint.md)*

### Character State

The persistent state of a character — attributes, skills, status effects, inventory, etc. Owned by State Authority.

**角色状态。** 角色的持久状态 — 属性、技能、状态效果、物品栏等。由 State Authority 拥有。

*Reference: [Character State Schema](../03_Data/Character_State_Schema.md)*

### Relationship State

The persistent state of relationships between characters — trust, affinity, history, etc. The core driver of all experiences.

**关系状态。** 角色之间关系的持久状态 — 信任、好感度、历史等。所有体验的核心驱动器。

*Reference: [Relationship State Schema](../03_Data/Relationship_State_Schema.md)*

### World State

The persistent state of the game world — locations, factions, global flags, environmental conditions.

**世界状态。** 游戏世界的持久状态 — 地点、阵营、全局标志、环境条件。

### Memory

A stored meaningful experience, not raw conversation. Memories are created through importance evaluation, embedded, indexed, and retrieved for future context.

**记忆。** 存储的有意义经历，不是原始对话。记忆通过重要性评估创建，嵌入、索引，并在未来检索用于上下文。

*Reference: [Memory Architecture Blueprint](./Memory_Architecture_Blueprint.md)*

---

## G. Quality Attributes（质量属性）

### Determinism

Same State Snapshot + Same Action + Same Seed = Same SimulationResult. The entire simulation is replayable.

**确定性。** 相同状态快照 + 相同 Action + 相同种子 = 相同 SimulationResult。整个模拟可重放。

*Reference: [Runtime Infrastructure Blueprint §10.1](./Runtime_Infrastructure_Blueprint.md)*

### Consistency

All queries within a Scene transaction see the same snapshot. Runtime Log and Persistent State are consistent at shutdown.

**一致性。** Scene 事务内的所有查询看到相同快照。Runtime Log 和持久状态在关闭时一致。

*Reference: [Runtime Infrastructure Blueprint §10.2](./Runtime_Infrastructure_Blueprint.md)*

### Isolation

Replay sessions, predictions, and hot reloads do not affect live Runtime state or in-flight queries.

**隔离性。** 重放会话、预测和热更新不影响活跃运行时状态或进行中的查询。

*Reference: [Runtime Infrastructure Blueprint §10.3](./Runtime_Infrastructure_Blueprint.md)*

### Recoverability

Runtime starts cleanly, shuts down gracefully, and can restore to any valid Snapshot.

**可恢复性。** 运行时干净启动、优雅关闭，并可恢复到任何有效快照。

*Reference: [Runtime Infrastructure Blueprint §10.4](./Runtime_Infrastructure_Blueprint.md)*

### Observability

Runtime Log is queryable. Infrastructure provides profiling hooks. Replay supports deterministic re-execution.

**可观测性。** Runtime Log 可查询。基础设施提供性能分析钩子。重放支持确定性重新执行。

*Reference: [Runtime Infrastructure Blueprint §10.5](./Runtime_Infrastructure_Blueprint.md)*

---

## H. Design Patterns（设计模式）

### Build-then-Swap

A hot reload pattern: build a complete new snapshot before making it visible. Callers never see a partially built snapshot. In-flight queries complete on the old snapshot.

**Build-then-Swap。** 热更新模式：在可见之前完全构建新快照。调用者永远不会看到部分构建的快照。进行中的查询在旧快照上完成。

### Acyclic Data Flow

Data in the Runtime Pipeline flows strictly forward: Action → SimulationResult → Event → State. No layer may depend on a later layer's output.

**无环数据流。** 运行时流水线中的数据严格向前流动：Action → SimulationResult → Event → State。任何层不得依赖后续层的输出。

### Structural Sharing

A memory efficiency pattern for snapshots: avoid full state duplication by sharing unchanged portions between snapshots. Architecture requires "avoid full duplication"; specific mechanism is implementation-defined.

**结构共享。** 快照的内存效率模式：通过在快照间共享未变更部分来避免全量状态复制。架构要求"避免全量复制"；具体机制由实现定义。

### Declarative Intent

Actions express *what* the player wants to do, not *how* to execute it. The Action Object is a declaration; execution logic belongs to AEM and Simulation Layer.

**声明式意图。** Action 表达玩家*想做什么*，不是*如何执行*。Action Object 是声明；执行逻辑属于 AEM 和 Simulation Layer。

---

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| v1.0 Draft | 2026-07-14 | Initial Glossary: 40+ terms across 8 categories (Architecture Concepts, Authority Layers, Runtime Objects, Runtime Components, Runtime Concepts, State Concepts, Quality Attributes, Design Patterns). Each term defined exactly once with bilingual definition and Blueprint reference. |
