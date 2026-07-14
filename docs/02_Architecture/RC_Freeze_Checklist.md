# RC Freeze Checklist

**Version:** v1.1  
**Status:** Active  
**Last Updated:** 2026-07-14

---

## 1. Purpose（文档目的）

This document defines the **entry criteria for Architecture Freeze**. It is split into two reusable parts:

本文档定义**架构冻结的准入条件**。分为两个可复用部分：

- **Part A — Collection Checklist:** Validates the entire Blueprint collection as a system
- **Part B — Document Checklist:** Reusable template for validating each individual Blueprint

> **Usage:** Part A is run once before Freeze. Part B is run for every document in the collection. A document cannot enter "Frozen" status until it passes Part B. The collection cannot enter "Frozen" status until it passes Part A and every document passes Part B.

> **使用方式：** Part A 在冻结前运行一次。Part B 对集合中每份文档运行。文档在通过 Part B 前不得进入"Frozen"状态。集合在通过 Part A 且每份文档通过 Part B 前不得进入"Frozen"状态。

### Check Severity Levels（检查严重度级别）

| Level | Meaning | Blocks Freeze? |
|-------|---------|----------------|
| 🔴 **Blocking** | Must pass before Freeze. Failure blocks the document or collection from entering Frozen status. | Yes |
| 🟡 **Non-blocking Warning** | Should pass before Freeze. Failure is recorded but does not block. | No |

> **Rationale:** Some checks (e.g., Referenced By reciprocity) are valuable for navigation but should not block Freeze if a single cross-reference is missing. Blocking checks are architectural invariants; Non-blocking Warnings are quality improvements.

> **理由：** 一些检查（如 Referenced By 互惠）对导航有价值，但如果缺少单个交叉引用不应阻塞冻结。Blocking 检查是架构不变量；Non-blocking Warning 是质量改进。

---

# Part A: Collection Checklist（集合级清单）

Validates that the Blueprint collection is internally consistent and architecturally complete.

验证 Blueprint 集合内部一致且架构完整。

## A1. Migration Completeness（迁移完整性）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| A1.1 | All documents classified in [Migration Matrix](./Architecture_Migration_Matrix.md) | 🔴 | ☐ | No document left unclassified |
| A1.2 | All ❌ Legacy documents have been rewritten | 🔴 | ☐ | Currently: Simulation Layer, Scene Engine |
| A1.3 | All ⚠️ Partial documents have been updated | 🔴 | ☐ | 10 documents need Pipeline/Glossary alignment |
| A1.4 | All ✅ Current documents have passed Part B | 🔴 | ☐ | 8 documents currently Current |
| A1.5 | ⬜ Stub documents have been created or deferred with rationale | 🔴 | ☐ | GPU Scheduler, Image Pipeline, Renderer Layer |

## A2. Pipeline Consistency（流水线一致性）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| A2.1 | All Blueprints reference [Runtime Pipeline Blueprint](./Runtime_Pipeline_Blueprint.md) where appropriate | 🔴 | ☐ | |
| A2.2 | No Blueprint defines a data flow that contradicts the 5-Layer Authority Pipeline | 🔴 | ☐ | |
| A2.3 | No Blueprint defines a module call order that contradicts the Pipeline | 🔴 | ☐ | Check all Mermaid flowcharts |
| A2.4 | The Acyclic Data Flow Rule (Action → SimulationResult → Event → State) is respected in all documents | 🔴 | ☐ | No reverse or skip flow |
| A2.5 | Every Authority layer (① Intent → ⑤ State) has exactly one authoritative Blueprint | 🔴 | ☐ | |

## A3. Artifact Ownership Consistency（制品归属一致性）

These checks define **rules**. The [Artifact Ownership Matrix](./Runtime_Artifact_Ownership_Matrix.md) provides **evidence** that the rules are satisfied. The Checklist is the standard; the Matrix is the evidence.

这些检查定义**规则**。[Artifact Ownership Matrix](./Runtime_Artifact_Ownership_Matrix.md) 提供**证据**证明规则被满足。Checklist 是标准；Matrix 是证据。

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| A3.1 | Every artifact produced by a Blueprint has exactly one identified owner | 🔴 | ☐ | Single owner rule *(Evidence: Artifact Ownership Matrix)* |
| A3.2 | Every artifact consumed by a Blueprint has an identified producer | 🔴 | ☐ | No orphan consumers *(Evidence: Artifact Ownership Matrix)* |
| A3.3 | Every persistent artifact has an identified persistence authority | 🔴 | ☐ | Infrastructure serves persistence *(Evidence: Artifact Ownership Matrix)* |
| A3.4 | No two Blueprints claim ownership of the same artifact | 🔴 | ☐ | Ownership exclusivity *(Evidence: Artifact Ownership Matrix)* |
| A3.5 | Infrastructure components are listed as persistence providers only, never as semantic owners of pipeline artifacts | 🔴 | ☐ | "Infrastructure serves. Infrastructure does not decide." *(Evidence: Artifact Ownership Matrix)* |
| A3.6 | Every Provisional artifact has been re-evaluated after its parent Blueprint migration | 🟡 | ☐ | Confidence re-assessment *(Evidence: Artifact Ownership Matrix Confidence column)* |

## A4. Terminology Consistency（术语一致性）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| A4.1 | All terms used across Blueprints are defined in [Runtime Glossary](./Runtime_Glossary.md) | 🔴 | ☐ | |
| A4.2 | No Blueprint defines a term that contradicts the Glossary definition | 🔴 | ☐ | |
| A4.3 | No Blueprint uses deprecated terminology (e.g., "Conversation History" instead of "Memory Object") | 🔴 | ☐ | |
| A4.4 | Bilingual definitions are consistent between Glossary and Blueprints | 🔴 | ☐ | |

## A5. Cross-Reference Integrity（交叉引用完整性）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| A5.1 | All "Depends On" references point to existing documents | 🔴 | ☐ | No broken links |
| A5.2 | All "Referenced By" references are reciprocated | 🟡 | ☐ | If A says "Referenced By B", B should say "Depends On A". Non-blocking: missing reciprocity is recorded but does not block Freeze |
| A5.3 | All inline cross-references (`[text](./file.md)`) resolve to existing files | 🔴 | ☐ | |
| A5.4 | No circular dependencies exist between Blueprints | 🔴 | ☐ | A → B → A is forbidden |
| A5.5 | The Pipeline Blueprint's Document Map (§7) lists all existing Blueprints | 🔴 | ☐ | |
| A5.6 | Every Blueprint listed in the Pipeline Document Map has its Depends On, Produces, and Consumes artifacts identified | 🔴 | ☐ | Dependency information must be explicit, not implied |

## A6. Boundary Non-Overlap（边界不重叠）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| A6.1 | No two Blueprints claim ownership of the same state domain | 🔴 | ☐ | |
| A6.2 | No two Blueprints claim ownership of the same runtime decision | 🔴 | ☐ | |
| A6.3 | Every Blueprint's "Owns" and "Does NOT Own" sections are consistent with every other Blueprint | 🔴 | ☐ | |
| A6.4 | No Blueprint's "Not Responsible For" is contradicted by another Blueprint's "Responsible For" | 🔴 | ☐ | |

## A7. Infrastructure Alignment（基础设施对齐）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| A7.1 | No Blueprint assigns Infrastructure components decision-making authority | 🔴 | ☐ | "Infrastructure serves. Infrastructure does not decide." |
| A7.2 | All Blueprints that need Infrastructure support reference [Runtime Infrastructure Blueprint](./Runtime_Infrastructure_Blueprint.md) | 🔴 | ☐ | |
| A7.3 | No Blueprint duplicates Infrastructure component definitions | 🔴 | ☐ | If a Blueprint mentions Snapshot Manager, it should reference Infrastructure, not redefine it |
| A7.4 | Quality Attributes (Determinism, Consistency, Isolation, Recoverability, Observability) are referenced where applicable | 🔴 | ☐ | |

## A8. Schema Alignment（Schema 对齐）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| A8.1 | Every pipeline artifact has a corresponding Data Schema (or explicitly marked "Future") | 🔴 | ☐ | |
| A8.2 | Blueprint definitions of artifacts match their Data Schema definitions | 🔴 | ☐ | |
| A8.3 | All Data Schemas reference their parent Blueprint | 🔴 | ☐ | |
| A8.4 | No Data Schema introduces fields that contradict Blueprint ownership rules | 🔴 | ☐ | |

## A9. Governance Completeness（治理完整性）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| A9.1 | Every Blueprint has a Document Governance section (Owner, Architecture Reviewers, Architecture Approval, Last Reviewed, Update Policy) | 🔴 | ☐ | Field names use "Architecture Reviewers" and "Architecture Approval" (not PR-style "Reviewers"/"Approval") |
| A9.2 | Every Blueprint has a Revision History | 🔴 | ☐ | |
| A9.3 | All ADRs referenced by Blueprints exist in `docs/00_Project/ADR/` | 🔴 | ☐ | |
| A9.4 | An ADR Index exists and is up to date | 🔴 | ☐ | |
| A9.5 | Version numbers are consistent between document header and Revision History | 🔴 | ☐ | |

## A10. Architecture Health（架构健康度）

These are the most fundamental health indicators for the entire Blueprint collection. They are suitable for automated CI checking.

这些是整个 Blueprint 集合最基础的健康指标。适合 CI 自动化检查。

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| A10.1 | No duplicate authority — no two Blueprints claim the same Authority layer | 🔴 | ☐ | Authority exclusivity |
| A10.2 | No duplicate artifact ownership — no two Blueprints claim ownership of the same artifact | 🔴 | ☐ | Ownership exclusivity |
| A10.3 | No cyclic dependency — the Blueprint dependency graph is a DAG (Directed Acyclic Graph) | 🔴 | ☐ | No A → B → A cycles |
| A10.4 | No orphan Blueprint — every Blueprint is referenced by at least one other document or the Pipeline Document Map | 🔴 | ☐ | No disconnected nodes |

---

# Part B: Document Checklist（文档级清单）

**Reusable template** — run this for every Blueprint before it can enter "Frozen" status.

**可复用模板** — 对每份 Blueprint 运行，通过后方可进入"Frozen"状态。

## B1. Structure（结构完整性）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| B1.1 | Document has a clear title and version header | 🔴 | ☐ | |
| B1.2 | Document has a Purpose section defining what it is and what it is NOT | 🔴 | ☐ | |
| B1.3 | Document has a Document Governance section | 🔴 | ☐ | Must include: Owner, Architecture Reviewers, Architecture Approval, Last Reviewed, Update Policy |
| B1.4 | Document has a Boundary Definition section (Owns / Does NOT Own) | 🔴 | ☐ | |
| B1.5 | Document has Design Principles | 🔴 | ☐ | |
| B1.6 | Document has Runtime Position or Authority role | 🔴 | ☐ | |
| B1.7 | Document has References section (Depends On / Referenced By) | 🔴 | ☐ | |
| B1.8 | Document has Revision History | 🔴 | ☐ | |
| B1.9 | Document has an explicit lifecycle status (Draft / RC / Locked / Deprecated) | 🔴 | ☐ | Must appear in both header and Document Governance section |

## B2. Pipeline Alignment（流水线对齐）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| B2.1 | Document references [Runtime Pipeline Blueprint](./Runtime_Pipeline_Blueprint.md) if it participates in the Pipeline | 🔴 | ☐ | |
| B2.2 | Document's Authority role is explicitly stated (e.g., "Simulation Authority — Layer ③") | 🔴 | ☐ | |
| B2.3 | Document's inputs and outputs match the Pipeline's stage definition | 🔴 | ☐ | |
| B2.4 | Document does not define data flow that contradicts the Pipeline | 🔴 | ☐ | |
| B2.5 | Document does not claim Authority that belongs to another layer | 🔴 | ☐ | |

## B3. Terminology（术语）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| B3.1 | All technical terms used in the document are defined in [Runtime Glossary](./Runtime_Glossary.md) | 🔴 | ☐ | |
| B3.2 | Term usage is consistent with Glossary definitions | 🔴 | ☐ | |
| B3.3 | No deprecated or informal terminology is used | 🔴 | ☐ | |
| B3.4 | Bilingual translations (if present) are accurate and consistent | 🔴 | ☐ | |

## B4. Ownership Clarity（归属清晰度）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| B4.1 | Every artifact the document produces is listed in [Artifact Ownership Matrix](./Runtime_Artifact_Ownership_Matrix.md) | 🔴 | ☐ | |
| B4.2 | Every artifact the document consumes is listed in the Artifact Ownership Matrix | 🔴 | ☐ | |
| B4.3 | "Owns" and "Does NOT Own" sections are explicit and non-overlapping with other Blueprints | 🔴 | ☐ | |
| B4.4 | No ownership claim contradicts the Artifact Ownership Matrix | 🔴 | ☐ | |

## B5. Implementation Independence（实现独立性）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| B5.1 | Document does not prescribe specific technologies (e.g., "use SQLite") unless in a clearly marked "Implementation Notes" section | 🔴 | ☐ | |
| B5.2 | Document does not contain code snippets that imply implementation decisions | 🔴 | ☐ | Interface signatures are OK; implementation code is not |
| B5.3 | Document uses requirement-level language ("must support", "shall guarantee") not implementation-level language ("use Copy-on-Write", "use mutex") | 🔴 | ☐ | |
| B5.4 | Hardware Considerations section describes constraints, not solutions | 🔴 | ☐ | |

## B6. Infrastructure References（基础设施引用）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| B6.1 | If the document uses Infrastructure components (Snapshot, Log, Dispatcher, etc.), it references [Runtime Infrastructure Blueprint](./Runtime_Infrastructure_Blueprint.md) | 🔴 | ☐ | |
| B6.2 | The document does not redefine Infrastructure component responsibilities | 🔴 | ☐ | |
| B6.3 | The document does not assign decision-making authority to Infrastructure components | 🔴 | ☐ | |
| B6.4 | Quality Attributes are referenced from Infrastructure §10 where applicable | 🔴 | ☐ | |

## B7. Internal Consistency（内部一致性）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| B7.1 | Mermaid diagrams are consistent with text descriptions | 🔴 | ☐ | |
| B7.2 | Tables do not contradict prose | 🔴 | ☐ | |
| B7.3 | Section numbering is sequential and complete | 🔴 | ☐ | |
| B7.4 | No section is marked "TODO" or "TBD" | 🔴 | ☐ | |
| B7.5 | The document's "Not Responsible For" list is comprehensive | 🔴 | ☐ | Should cover all areas that might cause confusion |

## B8. Cross-Reference Validity（交叉引用有效性）

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| B8.1 | All "Depends On" references point to existing documents | 🔴 | ☐ | |
| B8.2 | All "Referenced By" entries are reciprocated in the referenced document | 🟡 | ☐ | Non-blocking: missing reciprocity is a warning, not a blocker |
| B8.3 | All inline links resolve to existing files | 🔴 | ☐ | |
| B8.4 | The document is listed in the Pipeline Blueprint's Document Map (§7) | 🔴 | ☐ | |

## B9. Decision Ownership（决策归属）

These checks verify that the Blueprint explicitly declares which **decisions** it owns and which it delegates. This is distinct from artifact ownership (B4) — decisions are about *logic authority*, not *data ownership*.

这些检查验证 Blueprint 是否显式声明它拥有哪些**决策**以及委托了哪些决策。这与制品归属（B4）不同——决策关注的是*逻辑权威*，不是*数据归属*。

| # | Check | Severity | Status | Notes |
|---|-------|----------|--------|-------|
| B9.1 | Every Authority decision described by this Blueprint is explicitly attributed to an Authority layer | 🔴 | ☐ | E.g., "Simulation Authority decides what happens when Action meets world" |
| B9.2 | Every decision outside this Blueprint's scope is explicitly delegated to another Blueprint or marked "Future" | 🔴 | ☐ | No implicitly assumed decisions |
| B9.3 | The "Does NOT Own" section covers decision domains, not just artifact domains | 🔴 | ☐ | E.g., "Does NOT own: Action validation (owned by AEM), Event commit (owned by Timeline Manager)" |

---

## Governance Freeze Declaration（治理层冻结声明）

> **As of 2026-07-14, the Governance Layer is frozen.** No new governance documents will be created. No new sections will be added to existing governance documents. The governance layer consists of:
>
> 1. [Runtime Pipeline Blueprint](./Runtime_Pipeline_Blueprint.md) — entry point, pipeline definition
> 2. [Runtime Infrastructure Blueprint](./Runtime_Infrastructure_Blueprint.md) — platform definition
> 3. [Runtime Glossary](./Runtime_Glossary.md) — terminology
> 4. [Architecture Migration Matrix](./Architecture_Migration_Matrix.md) — one-time migration tool (to be archived after migration)
> 5. [Runtime Artifact Ownership Matrix](./Runtime_Artifact_Ownership_Matrix.md) — artifact constitution (long-term, with Confidence column)
> 6. [RC Freeze Checklist](./RC_Freeze_Checklist.md) — governance standard (long-term)
>
> **Future governance changes require a documented governance defect that affects the entire document collection.** Routine Blueprint issues should be fixed in the Blueprint, not in the governance layer.

> **自 2026-07-14 起，治理层已冻结。** 不再新增治理文档。不再向现有治理文档添加新章节。治理层由以上 6 份文档组成。未来治理变更需要有影响整个文档集的已记录治理缺陷。常规 Blueprint 问题应在 Blueprint 中修复，而非治理层。

---

## Freeze Status Tracker（冻结状态追踪）

### Current Collection Status

| Phase | Status | Date Completed |
|-------|--------|----------------|
| Phase A: Architecture Migration Matrix | ✅ Complete | 2026-07-14 |
| Phase A: Artifact Ownership Matrix | ✅ Complete (v1.1 with Confidence) | 2026-07-14 |
| Phase A: RC Freeze Checklist | ✅ Complete (v1.1 with B9/A10/A5.6) | 2026-07-14 |
| Governance Freeze | ✅ Declared | 2026-07-14 |
| Phase B-1.1: Rewrite Simulation Layer Blueprint | ⬜ Not Started | — |
| Phase B-1.1a: Sync Update Runtime State Model | ⬜ Not Started | — |
| Phase B-1.2: Rewrite Scene Engine Blueprint | ⬜ Blocked by B-1.1 | — |
| Phase B-2: Update Partial Blueprints (10) | ⬜ Blocked by B-1 | — |
| Phase C: Cross-Blueprint Consistency Audit | ⬜ Blocked by B-1 | — |
| Phase D: Architecture Constitution | ⬜ Blocked by C | — |
| Phase E: Freeze | ⬜ Blocked by D | — |

### Per-Document Freeze Status

| Document | Migration Status | Part B Passed | Freeze Status |
|----------|-----------------|---------------|---------------|
| Runtime Pipeline Blueprint | ✅ Current | ☐ | Pending Review |
| Runtime Infrastructure Blueprint | ✅ Current (RC2) | ☐ | Pending Review |
| Runtime Glossary | ✅ Current | ☐ | Pending Review |
| Action Registry | ✅ Current (RC2) | ☐ | Pending Review |
| Action Execution Model | ✅ Current (RC1) | ☐ | Pending Review |
| Runtime State Model Blueprint | ⚠️ Partial | ☐ | Blocked: Sync update with Simulation Layer |
| Simulation Layer Blueprint | ❌ Legacy | ☐ | Blocked: Rewrite needed (B-1.1) |
| Scene Engine Blueprint | ❌ Legacy | ☐ | Blocked: Rewrite needed (B-1.2) |
| Runtime Architecture Blueprint | ⚠️ Partial | ☐ | Blocked: Update needed |
| Overall Architecture Blueprint | ⚠️ Partial | ☐ | Blocked: Update needed |
| Narrative Director Blueprint | ⚠️ Partial | ☐ | Blocked: Update needed |
| Relationship Engine Blueprint | ⚠️ Partial | ☐ | Blocked: Update needed (B-2) |
| Memory Architecture Blueprint | ⚠️ Partial | ☐ | Blocked: Update needed |
| LLM Runtime Blueprint | ⚠️ Partial | ☐ | Blocked: Update needed |
| Prompt Builder Blueprint | ⚠️ Partial | ☐ | Blocked: Update needed |
| Action Object Schema | ✅ Current (Locked) | ☐ | Pending Review |
| SimulationResult Schema | ⚠️ Partial | ☐ | Blocked: Review needed |
| Event Object Schema | ✅ Current (RC4) | ☐ | Pending Review |
| Character State Schema | ✅ Current (RC) | ☐ | Pending Review |
| Relationship State Schema | ✅ Current (RC3) | ☐ | Pending Review |
| GPU Scheduler | ⬜ Stub | ☐ | Deferred |
| Image Pipeline | ⬜ Stub | ☐ | Deferred |
| Renderer Layer | ⬜ Stub | ☐ | Deferred |

---

## References

**Depends On:**

- [Architecture Migration Matrix](./Architecture_Migration_Matrix.md)
- [Runtime Artifact Ownership Matrix](./Runtime_Artifact_Ownership_Matrix.md)
- [Runtime Pipeline Blueprint](./Runtime_Pipeline_Blueprint.md)
- [Runtime Glossary](./Runtime_Glossary.md)
- [Runtime Infrastructure Blueprint](./Runtime_Infrastructure_Blueprint.md)

**Referenced By:**

- All Blueprints (Part B is run for each)
- Future Consistency Audit Report
- Future Architecture Constitution

---

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| v1.0 | 2026-07-14 | Initial RC Freeze Checklist. Part A: 9 sections, 41 checks. Part B: 8 sections, 33 checks. Per-document freeze status tracker. |
| v1.1 | 2026-07-14 | Governance refinement based on joint Architecture Review (GPT + CatPaw): (1) Added Check Severity Levels (Blocking / Non-blocking Warning) and applied to A5.2 and B8.2 (Referenced By reciprocity downgraded to Non-blocking). (2) Rewrote A3 as rule-based checks with Artifact Ownership Matrix as evidence, not as the standard itself. (3) Added A3.6 (Confidence re-assessment for Provisional artifacts). (4) Added A5.6 (dependency information must be explicit in Pipeline Document Map). (5) Added A10 Architecture Health (4 checks: no duplicate authority, no duplicate ownership, no cyclic dependency, no orphan Blueprint). (6) Added B1.9 (explicit lifecycle status required). (7) Added B9 Decision Ownership (3 checks: decision attribution, decision delegation, non-overlap of decision domains). (8) Updated A9.1 and B1.3 to use "Architecture Reviewers" and "Architecture Approval" and require "Last Reviewed" field. (9) Added Governance Freeze Declaration. (10) Updated Phase B tracker to include B-1.1a (State Model sync) and reflect Relationship Engine in B-2. Part A: 10 sections, 48 checks (7 new). Part B: 9 sections, 38 checks (5 new). |
