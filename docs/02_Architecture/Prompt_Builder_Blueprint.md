# Prompt Builder Blueprint

**Version:** v2.0
**Status:** Draft
**Last Updated:** 2026-07-13

---

# 1. Purpose

Define the responsibilities, boundaries, runtime workflow, and interfaces of the Prompt Builder.

The Prompt Builder is the **translation layer** between the deterministic AI Narrative RPG Engine and generative AI models.

It transforms structured Runtime data into model-ready Prompt Packages without introducing new business logic.

**Core Definition**

Prompt Builder converts:

Simulation State

↓

Narrative Plan

↓

Prompt Package

↓

Renderer

↓

LLM / Image Model

It never creates facts.

It only describes facts.

---

# 2. Responsibilities

## Responsible For

- Transform structured Runtime data into Prompt Packages
- Assemble prompt blocks
- Apply Content Profiles
- Apply Prompt Templates
- Build Text Prompt Packages
- Build Image Prompt Packages
- Context Compression
- Token Budget Management
- Prompt Formatting
- Prompt Sanitization

## Not Responsible For

- World Simulation
- Relationship Calculation
- Narrative Planning
- State Modification
- Memory Retrieval
- Dialogue Generation
- Image Generation
- Model Inference

---

# 3. Document Governance

**Owner:** AI Runtime Architect

**Reviewers:**

- Runtime Architect
- Narrative Architect
- AI Infrastructure Architect

**Approval**

Architecture Review Required

**Update Policy**

Changes affecting Prompt Package structure, Builder interfaces, or Runtime workflow require ADR approval.

---

# 4. Design Principles

- Data Before Prompt
- Prompt Is Read-only
- Prompt Is Disposable
- No Business Logic
- Template Driven
- Model Agnostic
- Content Profile Driven
- Deterministic Assembly

---

# 5. Prompt Philosophy

Prompt is temporary.

Runtime State is persistent.

Narrative Plan is deterministic.

Prompt Builder never stores prompts.

Every Prompt Package is reconstructed from Runtime State.

The prompt is a temporary representation of the Engine,
not the Engine itself.

---

# 6. Boundary Definition

Prompt Builder owns:

- Prompt Templates
- Prompt Assembly
- Context Compression
- Token Budget
- Prompt Formatting
- Prompt Sanitization
- Prompt Package Construction

Prompt Builder does NOT own:

- World State
- Character Logic
- Relationship Logic
- Narrative Decisions
- Memory Selection
- LLM Output
- Image Generation

Prompt Builder is a **pure transformation layer**.

---

# 7. Runtime Position

Player Action

↓

Scene Engine

↓

Simulation Layer

↓

Relationship Engine

↓

Narrative Director

↓

Prompt Builder

↓

Renderer

↓

LLM / Image Model

Prompt Builder is the final Engine component before model inference.

---

# 8. Runtime Inputs

Prompt Builder receives:

- Narrative Plan
- Scene Context
- Character State
- Relationship State
- Behavior Tendencies
- Relevant Memory
- World State
- Active Quest
- Timeline
- Content Profile
- Runtime Configuration
- Token Budget

---

# 9. Prompt Assembly Pipeline

Prompt Builder assembles Prompt Packages through the following stages:

Input Validation

↓

Input Sanitization

↓

Template Selection

↓

Block Rendering

↓

Context Compression

↓

Instruction Assembly

↓

Constraint Injection

↓

Prompt Package Construction

↓

Renderer

Prompt Builder never communicates directly with language models.

---

# 10. Prompt Package Model

Prompt Builder outputs a structured Prompt Package.

Example structure:

- System Prompt
- Character Context
- Relationship Context
- Scene Context
- Memory Context
- Narrative Goal
- Style Instructions
- Constraints
- Output Schema
- Metadata

Renderer converts the Prompt Package into model-specific requests.

---

# 11. Prompt Block System

Prompt Packages are composed from reusable blocks.

Core Blocks include:

- System Block
- World Block
- Character Block
- Relationship Block
- Scene Block
- Memory Block
- Narrative Block
- Style Block
- Constraint Block
- Output Block

Blocks remain independent and reusable.

Blocks may be enabled or disabled according to runtime requirements.

---

# 12. Context Compression

Prompt Builder manages limited context windows.

Priority:

1. Current Scene
2. Narrative Goal
3. Relationship State
4. Active Quest
5. Relevant Memory
6. Character Summary
7. World Summary

Compression strategies include:

- Summarization
- Pruning
- Prioritization
- Structured Formatting

Prompt Builder never removes mandatory Runtime information.

---

# 13. Content Profiles

Presentation differs by Content Profile.

Examples:

General

Romance

Mature

All profiles share identical Runtime State.

Only presentation changes.

Business logic remains identical.

---

# 14. Multi-Modal Prompt Pipeline

Prompt Builder supports multiple prompt targets.

Text Prompt Package

↓

Renderer

↓

LLM

Image Prompt Package

↓

Renderer

↓

Image Model

Different output targets may use different templates while sharing identical Runtime State.

---

# 15. Prompt Sanitization

Prompt Builder validates all external text before prompt assembly.

Responsibilities include:

- Escaping reserved tokens
- Normalizing formatting
- Isolating Player Input
- Preventing prompt injection into template sections
- Protecting system instructions

Sanitization protects Prompt integrity.

It never changes Runtime State.

---

# 16. Runtime Guarantees

Prompt Builder guarantees:

- Deterministic Prompt Assembly
- Stable Prompt Structure
- No Runtime State Modification
- No Hidden Business Logic
- No Fabricated Facts
- Model-independent Prompt Packages
- Token Budget Compliance
- Reproducible Prompt Construction

---

# 17. Hardware Considerations

Target Platform:

RTX 5060 8GB

Responsibilities:

- Efficient Context Compression
- Minimize unnecessary token usage
- Support streaming generation
- Support asynchronous image generation
- Keep Builder latency negligible compared to model inference

Prompt Builder is CPU-oriented and independent of GPU scheduling.

---

# 18. Future Extensibility

Future extensions include:

- Prompt Cache
- Dynamic Prompt Optimization
- Few-shot Example Selection
- Tool Calling Support
- Function Calling Support
- Multi-Agent Prompt Composition
- Multi-Model Routing

These features must not violate the core principle:

Prompt Builder remains a pure transformation layer.

---

# References

**Depends On**

- Overall Architecture
- Runtime Architecture
- Narrative Director Blueprint
- Relationship Engine Blueprint
- Glossary

**Referenced By**

- Renderer Specification
- Prompt Templates
- LLM Runtime
- Image Pipeline
- Content Profile Specification

---

# Revision History

| Version | Date | Description |
|----------|------------|------------------------------------------------|
| v2.0 | 2026-07-13 | Unified architecture with Prompt Package, Prompt Philosophy, Multi-modal Pipeline, Sanitization, and deterministic transformation model |
| v1.0 | 2026-07-13 | Initial Blueprint |