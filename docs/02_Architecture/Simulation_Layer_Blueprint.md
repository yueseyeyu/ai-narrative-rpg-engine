# Simulation Layer Blueprint

**Version:** v1.0  
**Status:** Draft  
**Last Updated:** 2026-07-12  

## 1. Purpose（文档目的）
定义 Simulation Layer 在 AI Narrative RPG Engine 中的职责、边界和运行机制。

Simulation Layer 是 Runtime Architecture 的**核心状态模拟系统**，负责维护和演化世界状态、Character 状态与 Relationship 状态。

它不是叙事系统，不是对话系统，不是生成系统。它是 Engine 中唯一有权改变长期状态的规则驱动层。

## 2. Responsibilities（职责）
**负责**：
- 维护世界状态的完整性与一致性
- 执行 Simulation Tick，计算状态变更
- 评估 Rule Engine 规则并产生 Event
- 驱动 Relationship 演化
- 确保所有长期状态变更经过 Simulation Layer

**不负责**：
- Narrative 决策
- 对话或文本生成
- 图像生成
- Memory 的提取与存储
- UI 更新

## 3. Document Governance（文档治理）
**Owner:** Simulation Architect  
**Reviewers:** Engine Architect, Runtime Architect  
**Approval:** Architecture Review Required  

**Update Policy:**  
Changes affecting state transition rules, simulation tick logic, or domain boundaries require ADR approval.

## 4. Design Principles（设计原则）
- **Simulation Before Generation** — 状态必须先于表现被确定
- **State Is Fact** — 状态是唯一的事实来源，文本只是表现
- **Deterministic Tick** — 同一输入必须产生同一输出
- **Simulation Owns State** — 只有 Simulation Layer 可以修改长期状态
- **Rule-Driven, Not Prompt-Driven** — 规则是硬约束，AI 是软表达

## 5. Boundary Definition（边界定义）
**Simulation Layer is a Rule-Driven State Machine.**

**It does NOT own:**
- Narrative Planning
- Dialogue Generation
- Image Generation
- Memory Extraction
- Scene Orchestration

外部模块只能通过 Simulation Layer 的公开接口查询或触发状态变更。

## 6. Core Runtime Responsibilities（核心运行时职责）
- 维护 Character State、Relationship State、World State
- 每次 Scene 中执行 Simulation Tick
- 评估 Rule Engine 规则
- 产生 Event 候选项供 Narrative Director 决策
- 确保 Scene 结束时状态一致性

## 7. State Domains（状态域）
- **Character State**：人格、情绪、当前目标、内部状态
- **Relationship State**（核心）：Trust、Affection、Dependence、Intimacy、Jealousy 等多维度状态
- **World State**：时间、地点、环境条件、全局事件状态
- **Game State**：Quest 进度、Timeline 状态、解锁条件

## 8. Simulation Tick（模拟 Tick）
Simulation Tick 是每次 Scene 中 Simulation Layer 的核心执行单元：

**Tick Start**  
↓  
**Character State Update**  
↓  
**Relationship Evaluation**  
↓  
**Rule Engine Evaluation**  
↓  
**Event Resolution**  
↓  
**State Transition**  
↓  
**Tick Complete**

Tick 执行完成后，结果将输入 Narrative Director 进行叙事决策。

## 9. State Transition（状态转换）
所有状态转换必须遵循：

- **确定性的** — 相同输入、相同状态、相同规则，产生相同结果
- **可追溯的** — 每次转换都有记录
- **可回滚的** — 支持 Scene 失败时的状态恢复

## 10. Rule Engine（规则引擎）
Rule Engine 是 Simulation Layer 的规则评估子系统。

**负责**：
- 定义和评估状态转换规则
- 计算 Event 触发条件
- 管理 World Rule 和 Character Rule

**规则类型**：
- World Rules（世界规则）
- Character Rules（角色规则）
- Relationship Rules（关系规则）
- Event Rules（事件规则）

## 11. Event Resolution（事件解析）
Simulation Tick 产生的 Event 由 Event Resolution 处理：

- **Trigger**：什么条件触发了事件
- **Actor**：谁参与事件
- **Action**：发生了什么
- **Consequence**：事件造成的状态变化
- **Priority**：事件的紧急程度

解析结果将传递给 Narrative Director 决定最终叙事呈现。

## 12. Runtime Guarantees（运行时保证）
- 每个 Scene 必须且仅执行一次 Simulation Tick
- Scene 结束时所有状态必须一致
- 所有长期状态变更必须经过 Simulation Layer
- State Transition 必须可追溯、可回滚
- Rule Engine 必须是确定性的

## 13. Hardware Considerations（硬件考量）
针对 RTX 5060 8GB：
- Simulation Tick 是纯 CPU 计算，不占用 GPU
- Rule Engine 必须轻量高效
- 状态计算延迟应远低于生成延迟

## References
- **Depends On**：Runtime Architecture, Overall Architecture, Glossary
- **Referenced By**：Scene Engine, Relationship Engine, Narrative Director, Memory Architecture

## Revision History
| Version | Date | Author | Description |
|---------|------|--------|-------------|
| v1.0 | 2026-07-12 | - | 初始 Blueprint |
