# Glossary（项目术语标准）

**Version:** v2.0  
**Status:** Active  
**Last Updated:** 2026-07-12  

## Purpose（文档目的）
本文档是 AI Narrative RPG Engine 项目的**唯一术语标准**（Glossary / 术语宪法）。所有其他文档必须严格引用本文件定义。

## Responsibilities（职责）
- 建立统一语言体系
- 消除术语歧义
- 保证跨文档一致性
- 为后续所有文档提供语义基础

## In Scope
核心概念的正式定义、命名规则、禁止术语

## Out of Scope
具体实现细节、代码示例、Prompt 模板

## Document Governance（文档治理）
**Owner:** Chief Architect  
**Reviewers:** Product Architect, Engine Architect  
**Approval:** Architecture Review Required  
**Update Policy:** Only update after ADR approval if core meaning changes.  
**Stability Level:** Stable（核心术语） / Experimental（新术语）

## Naming Principles（命名原则）
- 一个概念只能有一个正式名称（One Concept, One Name）
- 优先使用英文作为正式术语
- 避免同义词混用
- 变量/字段使用 snake_case
- 类/模块使用 PascalCase

## Forbidden Terms（禁止术语）
- Conversation → Scene
- Chat History → Memory
- Image Prompt → Image Blueprint
- NPC Memory → Character Memory

## Core Terminology（核心术语）

**Engine（引擎）**  
整个 AI Narrative RPG Engine 的统称。包含 Simulation、Narrative Director、Prompt Builder、Renderer、Persistence 等全部模块。Engine ≠ LLM。

**Character（角色）**  
玩家长期拥有的数字角色资产。具有持续身份、人格、成长能力和长期记忆。可跨世界复用，是项目最重要的长期资产之一。

**Relationship（关系）**  
角色之间持续演化的多维度长期状态（Trust、Affection、Dependence、Intimacy、Jealousy 等）。是剧情推进的核心驱动力。

**Scene（场景）**  
系统最小运行单位（Smallest Runtime Unit）。包含时间、地点、角色、状态、Dialogue、Event。所有长期状态在 Scene 结束时统一更新。

**Memory（记忆）**  
经过筛选的高价值经历集合。是玩家真正的长期资产，而非原始聊天记录。

**Narrative Director（叙事导演）**  
负责剧情规划、节奏控制、Event 选择、Relationship 演化策略。不负责自然语言生成。

**Mature Profile（成人体验配置）**  
Content Profile 的一种。面向成年用户，提供基于长期 Relationship 发展的亲密互动体验。核心原则：Story Before Intimacy、Emotion Before Content、Relationship Driven。

（其他术语如 Image Blueprint、Simulation、Prompt Builder、Persistence、Gallery 等可后续补充）

## References
- **Depends On**：Design Constitution, Project Vision
- **Referenced By**：PRD, Overall Architecture, All Layer Documents, Data Schemas

## Revision History
| Version | Date | Author | Description |
|---------|------|--------|-------------|
| v2.0 | 2026-07-12 | - | 增加工程化元数据、治理规则、Forbidden Terms |
