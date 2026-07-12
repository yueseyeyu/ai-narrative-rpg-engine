# Scene Engine Blueprint

**Version:** v1.1  
**Status:** Draft  
**Last Updated:** 2026-07-12  

## 1. Purpose（文档目的）
定义 Scene Engine 在 AI Narrative RPG Engine 中的职责、边界和运行机制。

Scene Engine 是 Runtime Architecture 的**核心执行容器**，负责协调一次完整叙事模拟事务（Atomic Narrative Simulation Transaction）。

## 2. Responsibilities（职责）
**负责**：
- 创建和管理 Scene 的完整生命周期
- 协调 Runtime 各模块的调用顺序
- 确保 Scene 作为原子事务的完整性和一致性
- 管理 Scene Context 的组装与提交

**不负责**：
- Relationship 演化规则
- Memory 重要性判断
- 文本或图像生成
- 世界规则计算

## 3. Document Governance（文档治理）
**Owner:** Engine Architect  
**Reviewers:** Runtime Architect, Simulation Architect  
**Approval:** Architecture Review Required  

**Update Policy:**  
Changes affecting Scene lifecycle, transaction rules, or module boundaries require ADR approval.

## 4. Boundary Definition（边界定义）
**Scene Engine is an Orchestration Layer.**

**It does NOT own:**
- World Simulation Logic
- Relationship Calculation
- Narrative Decision Logic
- Content Generation Logic

Scene Engine 只负责编排执行顺序和事务完整性。

## 5. Scene Definition（Scene 定义）
**Scene 是 Atomic Narrative Simulation Transaction** —— 系统最小不可分割的叙事模拟事务。

一个 Scene 代表一次完整的"数字人生事件"。

## 6. Scene Transaction Model（Scene 事务模型）
Scene 遵循 Transaction Pattern：

**BEGIN**  
↓  
**LOAD SNAPSHOT**  
↓  
**EXECUTE SIMULATION**  
↓  
**GENERATE EXPERIENCE**  
↓  
**VALIDATE RESULT**  
↓  
**COMMIT STATE**

If validation fails → **ROLLBACK** to previous Snapshot.

## 7. Scene Lifecycle（Scene 生命周期）
- Created
- Initialized
- Context Loaded
- Simulating
- Directing
- Generating
- Evaluating
- Memory Processing
- Committing
- Completed
- Archived

## 8. Scene Context Model（Scene 上下文模型）
**输入**：
- Character State
- Relationship State
- World State
- Relevant Memory
- Active Quests
- Player Action

## 9. Scene Event Model（Scene 事件模型）
Event 包含 Trigger、Actor、Action、Consequence。

## 10. Scene Result（Scene 结果）
**输出**：
- State Changes
- New Memory Entries
- Timeline Update
- Optional Gallery Entry (CG)

## 11. Scene Commit Rules（Scene 提交规则）
必须满足：
- State Validated
- Memory Extracted
- Persistence Completed

## 12. Runtime Guarantees（运行时保证）
- Every Scene must start from a valid State Snapshot.
- Every Scene must produce deterministic State Transition.
- No external module can modify Scene State directly.
- Scene Commit is the only entry point for persistent state update.
- Failed Scene execution must not corrupt long-term assets.

## 13. Failure Recovery（失败恢复）
定义 Generation Failed、Simulation Error、State Conflict 时的回滚与重试策略。

## 14. Hardware Considerations（硬件考量）
针对 RTX 5060 8GB：
- Image Generation 必须异步
- 非核心计算可后台执行

## References
- **Depends On**：Runtime Architecture, Overall Architecture, Glossary
- **Referenced By**：Simulation Layer, Relationship Engine, Memory Architecture, Narrative Director, Image Pipeline

## Revision History
| Version | Date | Author | Description |
|---------|------|--------|-------------|
| v1.1 | 2026-07-12 | - | 增加 Document Governance、Boundary Definition、Transaction Model、Runtime Guarantees |
| v1.0 | 2026-07-12 | - | 初始 Blueprint |
