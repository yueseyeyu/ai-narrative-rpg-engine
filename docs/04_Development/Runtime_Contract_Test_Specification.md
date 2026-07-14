# Runtime Contract Test Specification

**Version:** v0.1 Draft  
**Status:** Draft  
**Last Updated:** 2026-07-14

**Depends On:** [Architecture Baseline v1.0](../00_Project/Architecture_Baseline.md), [Simulation Layer Blueprint](../02_Architecture/Simulation_Layer_Blueprint.md), [SimulationResult Schema](../03_Data/SimulationResult_Schema.md)

---

## 1. Purpose（文档目的）

Define verifiable architecture contracts that protect the Runtime Architecture during implementation. These contracts are not test code — they are **executable specifications** that any implementation must satisfy.

定义可验证的架构契约，在实现过程中保护 Runtime Architecture。这些契约不是测试代码——它们是任何实现必须满足的**可执行规范**。

> **Philosophy:** Contract tests protect architecture better than more documentation. Once these tests pass, any refactoring, optimization, LLM swap, or prompt change that breaks them is a regression.

> **理念：** 契约测试比更多文档更能保护架构。一旦这些测试通过，任何重构、优化、LLM 替换或 Prompt 变更导致它们失败就是回归。

---

## 2. Contract Categories（契约分类）

| Category | What It Verifies | Frozen? |
|----------|------------------|---------|
| **Determinism** | Same input → Same output | ✅ Frozen |
| **Mutation Boundary** | Only State Authority mutates Persistent State | ✅ Frozen |
| **Immutability** | SimulationResult and Event Candidates are immutable | ✅ Frozen |
| **Handler Purity** | Handlers produce no side effects on Persistent State | ✅ Frozen |
| **Pipeline Flow** | Data flows strictly forward (acyclic) | ✅ Frozen |
| **Scene Atomicity** | Failed Scene rolls back completely | ✅ Frozen |
| **Generation Isolation** | Generation retry does NOT re-run Simulation | ✅ Frozen |
| **Replayability** | SimulationResult can be regenerated from inputs | ✅ Frozen |

---

## 3. Test Case Format（测试用例格式）

Each contract test case follows this structure:

```
Case-NNN: [Name]
  Category: [Determinism | Mutation | Immutability | ...]
  Architecture Rule: [Which frozen element this tests]

  Given:
    - Initial State: [description]
    - Action: [description]
    - Seed: [value]

  When:
    - [operation performed]

  Then:
    - Expected SimulationResult: [status, deltas, events]
    - Expected State After Commit: [what changed]
    - Expected Events: [what was committed]
    - Invariants: [what must remain true]
```

---

## 4. Contract Test Cases（契约测试用例）

### Case-001: Basic Determinism

```
Category: Determinism
Architecture Rule: Same Snapshot + Same Action + Same Seed = Same SimulationResult

Given:
  - Character A: { trust: 30, affection: 20, mood: "neutral" }
  - Character B: { trust: 30, affection: 20, mood: "neutral" }
  - Relationship A→B: { trust: 40, affection: 30 }
  - Action: { type: "say_hello", actor: "A", target: "B" }
  - Seed: 42

When:
  - Execute Simulation Tick

Then:
  - SimulationResult.status = "success"
  - SimulationResult.valid_deltas contains:
    { target: "B", op: "add", path: "trust", val: +1 }
  - SimulationResult.event_candidates contains 1 event
  - Invariant: Running twice with identical inputs produces byte-identical SimulationResult
```

### Case-002: Mutation Boundary

```
Category: Mutation Boundary
Architecture Rule: Only State Authority (Layer ⑤) may mutate Persistent State

Given:
  - Any valid initial state
  - Any valid Action

When:
  - Execute Simulation Tick
  - Inspect state before and after Simulation (before Commit)

Then:
  - Persistent State is IDENTICAL before and after Simulation
  - SimulationResult.valid_deltas contains the proposed changes
  - State only changes AFTER Commit Pipeline applies deltas
  - Invariant: No module except State Authority writes to Persistent State
```

### Case-003: SimulationResult Immutability

```
Category: Immutability
Architecture Rule: SimulationResult SHALL NOT be modified after production

Given:
  - Any valid SimulationResult

When:
  - Attempt to modify any field (valid_deltas, event_candidates, status, etc.)

Then:
  - Modification SHALL fail or be silently ignored
  - Original SimulationResult remains unchanged
  - Exception: commit_metadata may be updated by Commit Pipeline only
```

### Case-004: Handler Purity

```
Category: Handler Purity
Architecture Rule: Handlers are functionally pure — no Persistent State side effects

Given:
  - Character State: { A: { mood: "happy" } }
  - Action: { type: "say_hello", actor: "A", target: "B" }

When:
  - Execute Handler

Then:
  - Character State A.mood is STILL "happy" (unchanged)
  - Handler returns: { deltas: [...], diagnostics: {...} }
  - No Infrastructure access occurred (no DB write, no log write, no dispatch)
  - Invariant: Handler input → output only, no side effects
```

### Case-005: Acyclic Data Flow

```
Category: Pipeline Flow
Architecture Rule: Data flows strictly forward — no circular references

Given:
  - A committed SimulationResult

When:
  - Inspect all references in SimulationResult

Then:
  - SimulationResult does NOT reference Event Objects (downstream)
  - SimulationResult does NOT reference State Mutation (downstream)
  - SimulationResult does NOT reference Memory Objects (downstream)
  - SimulationResult does NOT reference Narrative Output (downstream)
  - Invariant: All references point to upstream or self-contained data
```

### Case-006: Scene Atomicity — Failure Rollback

```
Category: Scene Atomicity
Architecture Rule: Failed Scene execution rolls back to Snapshot

Given:
  - Snapshot S1: { A: { trust: 50 }, B: { trust: 50 } }
  - Action that will FAIL (e.g., invalid precondition)

When:
  - Begin Scene with Snapshot S1
  - Execute Simulation (fails)
  - Scene rolls back

Then:
  - Persistent State is IDENTICAL to S1
  - No Events were committed
  - No Memory was extracted
  - SimulationResult with status="failure" was archived to Log
```

### Case-007: Generation Isolation

```
Category: Generation Isolation
Architecture Rule: Generation retry SHALL NOT re-run Simulation

Given:
  - Committed SimulationResult SR1
  - Committed State after SR1
  - First Narrative generation failed

When:
  - Retry Narrative generation

Then:
  - Simulation is NOT re-executed
  - Retry uses the same committed State and SR1
  - New Narrative output may differ (LLM is non-deterministic)
  - But underlying facts (State, Events) are identical
```

### Case-008: Replayability

```
Category: Replayability
Architecture Rule: SimulationResult can be regenerated from inputs

Given:
  - Original SimulationResult SR1 with:
    - input_snapshot_id: S1
    - source_action_id: A1
    - seed: 42
    - validated_state_hash: H1

When:
  - Load historical Snapshot S1 from Log
  - Load historical Action A1 from Log
  - Load historical Seed 42 from Log
  - Re-execute Simulation

Then:
  - Regenerated SimulationResult SR2 has:
    - Same status as SR1
    - Same valid_deltas as SR1
    - Same event_candidates as SR1
    - Same validated_state_hash as SR1 (H1 == H2)
  - If hash mismatch → determinism violation (bug)
```

### Case-009: Relationship Delta Flow

```
Category: Mutation Boundary
Architecture Rule: Relationship Engine computes deltas, State Authority applies them

Given:
  - Relationship A→B: { trust: 40 }
  - Action: { type: "give_gift", actor: "A", target: "B", gift: "flower" }

When:
  - Relationship Engine computes relationship delta
  - Delta is included in SimulationResult.valid_deltas
  - Commit Pipeline applies delta

Then:
  - Relationship Engine did NOT directly modify Relationship State
  - Relationship State only changed AFTER Commit
  - Delta path: RelationshipEngine → SimulationResult.valid_deltas → CommitPipeline → StateAuthority → PersistentState
```

### Case-010: Memory Boundary

```
Category: Mutation Boundary
Architecture Rule: Memory extraction SHALL NOT mutate Persistent State

Given:
  - Committed Events from a Scene
  - Committed Runtime State

When:
  - Memory System extracts Memory Objects

Then:
  - Memory Objects are produced (new artifacts)
  - Character State is UNCHANGED
  - Relationship State is UNCHANGED
  - World State is UNCHANGED
  - Invariant: Memory reads, never writes to Persistent State
```

### Case-011: Event Candidate Immutability

```
Category: Immutability
Architecture Rule: Event Candidates are immutable once packaged

Given:
  - SimulationResult with Event Candidates

When:
  - Timeline Manager processes Event Candidates
  - Timeline Manager rejects some candidates

Then:
  - Rejected candidates are NOT modified (only their lifecycle_state changes)
  - Accepted candidates are NOT modified (only committed to Timeline)
  - Candidate content (deltas, metadata) is byte-identical to what Event Factory produced
```

### Case-012: Partial Success

```
Category: Scene Atomicity
Architecture Rule: partial_success allows subset commit of valid deltas only

Given:
  - Action that produces 3 deltas: 2 valid, 1 invalid

When:
  - Execute Simulation Tick

Then:
  - SimulationResult.status = "partial_success"
  - valid_deltas contains 2 deltas
  - invalid_deltas contains 1 delta with rejection reason
  - Commit Pipeline commits only the 2 valid deltas
  - Invalid delta's target state is UNCHANGED
```

---

## 5A. Contract Coverage Matrix（契约覆盖矩阵）

This matrix maps each Frozen Element (from [Architecture Baseline §4](../00_Project/Architecture_Baseline.md)) to its Contract Test Cases. It ensures every frozen rule has at least one test.

此矩阵将每个冻结元素映射到其契约测试用例。确保每条冻结规则至少有一个测试。

| Frozen Element | Contract Cases | Coverage |
|----------------|---------------|----------|
| **Authority Layers (①-⑤)** | Case-005 (Acyclic Flow) | ✅ |
| **Mutation Boundary** | Case-002, Case-009, Case-010 | ✅ |
| **Artifact Ownership** | Case-005 (no downstream refs) | ✅ |
| **Pipeline Data Flow** | Case-005 | ✅ |
| **Scene Transaction Model** | Case-006, Case-012 | ✅ |
| **SimulationResult Contract** | Case-003, Case-008 | ✅ |
| **Handler Purity** | Case-004 | ✅ |
| **Memory Boundary** | Case-010 | ✅ |
| **Generation Boundary** | Case-007 | ✅ |
| **Infrastructure Serves** | (implicit in all — no Infra in tests) | ✅ |
| **Replayability** | Case-001, Case-008 | ✅ |

> **Rule:** When a new Frozen Element is added to Architecture Baseline, a Contract Test Case MUST be added here. When a new Contract Test is added, it MUST map to at least one Frozen Element.

---

## 6. Determinism Verification Protocol（确定性验证协议）

### Round-Trip Test

```
1. Create initial Snapshot S1
2. Execute Action A1 with Seed 42 → SimulationResult SR1
3. Record SR1.validated_state_hash as H1
4. Commit SR1 → State becomes S2
5. Load S1 from Log (historical)
6. Re-execute A1 with Seed 42 → SimulationResult SR2
7. Compare:
   - SR1.status == SR2.status ✓
   - SR1.valid_deltas == SR2.valid_deltas ✓
   - SR1.event_candidates == SR2.event_candidates ✓
   - SR2.validated_state_hash == H1 ✓
8. If any mismatch → DETERMINISM VIOLATION
```

### Cross-Version Test

```
1. Run test case with Handler v1.0 → Record SimulationResult
2. Upgrade Handler to v1.1
3. Run same test case → Record SimulationResult
4. If results differ → Handler version change introduced non-determinism
5. Resolution: Handler version is recorded in SimulationResult for replay
```

---

## 6. Contract Test Execution Rules（契约测试执行规则）

| Rule | Description |
|------|-------------|
| **No LLM required** | Contract tests verify deterministic simulation, not LLM generation. LLM is tested separately. |
| **No GPU required** | Contract tests run on CPU. Simulation is CPU-first. |
| **No Network required** | Contract tests are fully local. No external API calls. |
| **Fast execution** | Each test case should complete in < 100ms. |
| **Isolated** | Each test case creates its own state. No shared fixtures. |
| **Reproducible** | Same test on same code always produces same result. |
| **Regression protection** | Any code change that breaks a contract test is a regression. |

---

## 7. Adding New Contract Tests（添加新契约测试）

New contract tests MAY be added during implementation without ADR approval, as long as they:

1. Test a **frozen** architecture rule (see Architecture Baseline §4)
2. Do NOT test implementation details (algorithms, data structures)
3. Are **deterministic** (no randomness except through Seed Manager)
4. Do NOT require LLM, GPU, or Network

Contract tests that test **non-frozen** design assumptions (ECS, Memory algorithms, 5-layer physical separation) are allowed but MUST be marked as `Category: Design Assumption` and MAY be removed if the assumption changes.

---

## 8. Future Contract Tests（未来契约测试）

The following contract tests will be added as implementation progresses:

| Test | When | Category |
|------|------|----------|
| Background Simulation Tick | When Background Tick ADR is approved | New |
| Nested Simulation Tick | When Nested Tick ADR is approved | New |
| State Migration (old save → new) | When save_version changes | New |
| Prediction Fork Isolation | When Prediction is implemented | Isolation |
| Memory Quality Evolution | When Memory Quality Model is implemented | Design Assumption |

---

## 9. Revision History

| Version | Date | Description |
|---------|------|-------------|
| v0.1 Draft | 2026-07-14 | Initial specification: 12 contract test cases covering Determinism, Mutation Boundary, Immutability, Handler Purity, Pipeline Flow, Scene Atomicity, Generation Isolation, Replayability. Determinism verification protocol defined. |
