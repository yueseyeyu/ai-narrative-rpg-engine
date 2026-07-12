# PRD Blueprint - AI Narrative RPG Engine

**Version:** v2.1
**Status:** Approved Blueprint
**Last Updated:** 2026-07-12

---

# Document Purpose

本文档定义 PRD（Product Requirements Document）的最终结构、章节职责与边界。

PRD 用于回答：

- 我们要创造什么产品？
- 为什么玩家需要它？
- 它应提供什么体验？
- 它遵循哪些产品原则？
- MVP 的边界是什么？

PRD 描述的是 **产品**，而不是 **实现方式**。

所有系统设计、数据结构、Prompt、架构实现均应引用 PRD，而不是在 PRD 中展开。

---

# Foundation（基础）

## 1. Purpose

### Responsibilities

说明 PRD 的作用及其在整个文档体系中的定位。

### In Scope

- PRD 与 Design Constitution 的关系
- PRD 与 Project Vision 的关系
- PRD 的适用范围

### Out of Scope

- 技术实现
- 数据结构
- API
- Prompt

---

## 2. Product Definition

### Responsibilities

一句话定义产品。

明确：

- 产品是什么
- 产品不是什么
- 产品定位

### Future References

- README
- Project Vision
- MVP
- Marketing

---

## 3. Project Philosophy

### Responsibilities

提炼产品坚持的核心理念。

例如：

- Character First
- Relationship First
- Story Before Intimacy
- Simulation Before Generation
- Memory Is Player Asset

本章只描述理念，不解释实现。

---

## 4. Target Users

### Responsibilities

定义主要目标用户。

包括：

- 用户画像
- 用户需求
- 用户痛点
- 使用场景

---

## 5. Player Value Proposition

### Responsibilities

回答：

为什么玩家应该长期使用本产品？

重点包括：

- 长期陪伴
- 数字人生
- 专属角色
- 私密体验
- 本地拥有
- 永久资产
- 长期成长

---

# Product Principles（产品原则）

## 6. Product Principles

### Responsibilities

定义产品设计原则。

例如：

- Scene Before Message
- Simulation Before Prompt
- Character Before Dialogue
- Relationship Before Intimacy
- Story Before Reward
- Memory Before History
- Data Before Prompt
- CG As Story Reward

本章将成为整个项目引用率最高的产品文档之一。

---

# Product Experience（产品体验）

## 7. Core Assets

### Responsibilities

定义玩家真正拥有的长期资产。

包括：

- Character
- Relationship
- Relationship Snapshot
- Memory
- Gallery
- Timeline
- Story Archive
- Image Blueprint

原则：

模型可以升级。

这些资产必须长期保留。

未来引用：

- Character.md
- Relationship.md
- Memory.md
- Image Blueprint.md

---

## 8. Core Systems Overview

### Responsibilities

列出支撑产品体验的主要系统。

包括：

- Character
- Relationship
- Scene
- Event
- Quest
- Memory
- Timeline
- World
- Narrative Director
- Image Pipeline

仅描述职责。

不描述实现。

---

## 9. Engine Modes

### Responsibilities

定义产品运行模式。

包括：

### Character Mode（MVP）

单角色长期成长体验。

### World Mode（Future）

开放世界、多角色、多组织、多事件模拟。

两者必须共享：

- Character
- Relationship
- Scene
- Memory
- Narrative Director

而不是维护两套系统。

---

## 10. Core Experience

### Responsibilities

定义玩家整体体验目标。

重点包括：

- 长期沉浸
- 情感成长
- 剧情连续
- 回忆积累
- 身份认同
- 数字人生

描述体验。

不讨论实现。

---

## 11. Gameplay Loop

### Responsibilities

定义产品核心循环。

例如：

Scene

↓

Interaction

↓

Relationship Update

↓

Event / Quest

↓

Memory Update

↓

Narrative Director

↓

Next Scene

所有功能最终都应服务于这一循环。

---

## 12. Relationship-Driven Mature Experience

### Responsibilities

定义 Mature Profile 的产品体验目标。

重点不是成人内容。

而是：

Relationship 的长期成长。

设计原则：

真正高质量的成人体验来自：

Relationship

↓

Emotion

↓

Story

↓

Intimacy

↓

CG

而不是：

Prompt

↓

Adult Content

Mature Profile 属于：

Content Profile 的一种配置策略。

所有实现必须建立在：

- Relationship
- Scene
- Narrative Director
- Image Blueprint

共同驱动之上。

不得采用：

- 独立 Prompt
- 独立代码分支
- 独立运行逻辑

Mature Experience 的目标不是增加成人内容。

而是延长 Relationship 生命周期。

让玩家拥有值得长期投入的情感体验。

这是本项目最重要的产品差异化之一。

---

# Product Boundaries（产品边界）

## 13. Hardware Constraints

### Responsibilities

定义产品必须遵守的硬件约束。

目标平台：

- Windows
- RTX 5060 8GB
- 32GB RAM

核心原则：

Hardware Constraints are Product Constraints.

产品体验必须首先适配目标硬件。

不得先设计高配方案再进行删减。

未来引用：

- GPU Scheduler
- Image Pipeline
- Renderer Layer

---

## 14. Engine Responsibilities

### Responsibilities

定义各模块职责。

包括：

Python

负责：

- Simulation
- State
- Logic
- Rules

Narrative Director

负责：

- Story Planning
- Scene Selection
- Narrative Strategy

Prompt Builder

负责：

- Prompt Rendering

LLM

负责：

- Natural Language Expression

Image Pipeline

负责：

- Blueprint
- Rendering
- Gallery

职责边界必须长期保持稳定。

---

## 15. Non-Goals

第一阶段明确不做：

- MMO
- 联机
- 实时开放世界
- 无限 NPC 模拟
- 云端服务
- 多 GPU 集群

保持产品聚焦。

---

# Development Plan（开发计划）

## 16. MVP Scope

明确：

Must Have

Should Have

Could Have

Won't Have

所有开发工作均应以 MVP 为最高优先级。

---

## 17. Roadmap

规划：

Phase 1

Character RPG Engine

↓

Phase 2

Multiple Characters

↓

Phase 3

World Simulation

↓

Phase 4

Open Narrative Platform

---

## 18. Success Metrics

定义产品成功标准。

包括：

### Product Metrics

- Relationship Depth
- Character Consistency
- Memory Continuity
- Story Coherence
- Scene Quality
- Player Retention

### Experience Metrics

- Emotional Engagement
- Immersion Duration
- CG Meaningfulness
- Long-term Replayability

原则：

CG 数量不是目标。

值得回忆的 CG 才是目标。

Relationship 深度比成人内容数量更重要。

长期沉浸比短期刺激更重要。

---

# Closing Statement

PRD 定义的是产品。

Architecture 定义的是实现。

Data 定义的是资产。

Engine 定义的是能力。

所有设计最终都应服务于同一个目标：

**让玩家拥有一段真正属于自己的数字人生。**