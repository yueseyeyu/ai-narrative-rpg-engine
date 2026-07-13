# Memory Architecture Blueprint

**Version:** v1.3  
**Status:** Draft  
**Last Updated:** 2026-07-13

---

# 1. Purpose

Define the responsibilities, boundaries, runtime behavior, and architecture of the Memory System.

The Memory System is the **Long-term Experience Persistence Layer** of the AI Narrative RPG Engine.

It transforms completed Scenes into structured, evolving memories that influence future simulation, relationship evolution, and narrative generation.

Memory is one of the core runtime domains of the Engine.

It provides persistent cognitive continuity across scenes, gameplay sessions, and long-term character development.

## Core Philosophy

Memory is **not conversation history**.

Memory is structured experience with quality attributes that simulate human cognitive processes including:

- Encoding
- Retrieval
- Reinforcement
- Decay
- Activation
- Distortion

The Engine remembers experiences rather than conversations.

---

# 2. Responsibilities

## Responsible For

- Memory Extraction
- Memory Classification
- Importance Evaluation
- Memory Quality Modeling
- Memory Persistence
- Memory Retrieval
- Memory Consolidation
- Memory Activation
- Memory Lifecycle Management
- Memory Ownership Management
- Memory Visibility Control

## Memory Ownership

Every Memory belongs to one or more runtime entities.

Possible owners include:

- Character
- NPC
- Player
- Organization
- World

Ownership determines:

- who can retrieve the memory
- who may update memory quality
- who may reference the memory during Runtime

## Memory Visibility

Memories may be:

- Private
- Shared
- Public
- World-level

Visibility determines retrieval scope rather than storage location.

## Not Responsible For

The Memory System does **NOT** perform:

- Relationship Calculation
- World Simulation
- Narrative Planning
- Prompt Construction
- Dialogue Generation
- Image Generation
- Raw Chat Log Storage

Raw conversation history belongs to Persistence Layer rather than Memory System.

---

# 3. Document Governance

**Owner**

Memory Architect

**Reviewers**

- Runtime Architect
- Simulation Architect
- AI Runtime Architect

**Approval**

Architecture Review Required

## Update Policy

The following changes require ADR approval:

- Memory lifecycle changes
- Retrieval mechanism changes
- Memory quality model changes
- Persistence strategy changes
- Ownership model changes
- Visibility model changes

Implementation tuning does not require ADR.

---

# 4. Design Principles

## Experience Before Conversation

The Engine remembers experiences rather than dialogue transcripts.

---

## Selective Persistence

Not every Scene becomes a Memory.

Only meaningful experiences above the persistence threshold are stored.

---

## Structured Memory

Memory is runtime data.

It is not free-form text.

---

## Retrieval Before Generation

Relevant memories must be retrieved before Prompt Builder constructs prompts.

---

## Memory Evolves

Memory changes over time through:

- reinforcement
- decay
- activation
- consolidation
- distortion

---

## Quality-aware Retrieval

Retrieval depends on Memory Quality rather than semantic similarity alone.

---

## Rule-driven Importance

Importance evaluation must be deterministic.

LLM never decides whether a memory should exist.

---

## Ownership First

Every Memory has an explicit Owner.

Ownership determines accessibility and runtime authority.

---

## Runtime Independence

Memory exists independently from any specific LLM.

Replacing models must not invalidate stored memories.

---

# 5. Boundary Definition

## Memory System OWNS

- Memory Objects
- Memory Index
- Memory Metadata
- Memory Quality Attributes
- Memory Retrieval Logic
- Memory Consolidation Logic
- Memory Activation Logic
- Ownership Metadata
- Visibility Metadata

## Memory System DOES NOT OWN

- Character State
- Relationship State
- World State
- Narrative Planning
- Prompt Construction
- Simulation Rules
- Raw Chat History

The Memory System provides information.

It never changes Runtime State directly.

---

# 6. Runtime Position

The Memory System operates in two independent runtime phases.

## Write Pipeline

Scene Execution

↓

Scene Complete

↓

Memory Extraction

↓

Importance Evaluation

↓

Memory Classification

↓

Async Persistence

---

## Read Pipeline

Scene Initialization

↓

Context Query

↓

Memory Activation

↓

Memory Retrieval

↓

Prompt Builder

↓

LLM

---

Memory writing and memory retrieval are completely decoupled.

Memory persistence must never block Scene completion.

Memory retrieval must complete before Prompt Builder begins prompt assembly.

The Memory System serves as the cognitive bridge between past experiences and future behavior.
# 7. Memory Lifecycle

Every Memory follows a strict lifecycle:

1. **Experience**
   - A Scene completes and produces structured runtime results.

2. **Evaluation**
   - The Importance Score is calculated using deterministic rules.

3. **Extraction**
   - Structured Memory Objects are generated from Scene Results.

4. **Classification**
   - Memories are categorized (Episodic, Relationship, World, Personal, etc.).

5. **Persistence**
   - Memory Objects are written asynchronously into long-term storage.

6. **Activation**
   - Runtime triggers dynamically increase or decrease recall probability.

7. **Retrieval**
   - Relevant memories are recalled during future Scene execution.

8. **Consolidation**
   - Similar memories may be merged into higher-level abstractions.

9. **Decay**
   - Memory Quality attributes gradually evolve over time.

10. **Archive**
    - Inactive memories move into cold storage or subconscious layers.

---

# 8. Memory Types

The Memory System supports multiple memory domains.

## Episodic Memory

Specific experiences.

Examples:

- First Meeting
- First Kiss
- Battle at Dawn
- Festival Night

---

## Relationship Memory

Experiences that directly influence interpersonal relationships.

Examples:

- Saved My Life
- Betrayed Trust
- Shared Secret
- Confession

---

## World Memory

Important changes in the game world.

Examples:

- Kingdom Fell
- War Began
- City Destroyed
- New Era Started

---

## Personal Memory

Character-specific experiences.

Examples:

- Childhood Trauma
- Learned Swordsmanship
- Overcame Fear
- Lost Family

---

## Shared Memory

Memories simultaneously owned by multiple characters.

Examples:

- Vacation
- Graduation
- Wedding
- Team Victory

---

# 9. Importance Evaluation

Not every Scene becomes a Memory.

The Memory System evaluates every completed Scene using deterministic rules.

Evaluation Factors include:

- Emotional Impact
- Relationship Change
- Narrative Importance
- Character Growth
- World Impact
- Player Choice Significance
- Future Narrative Potential

Only memories exceeding the persistence threshold become long-term memories.

Importance Evaluation is entirely rule-driven.

LLMs never decide what should be remembered.

---

# 10. Memory Retrieval

Memory Retrieval is Context-Aware Recall.

The system searches for memories using multiple runtime signals.

## Retrieval Inputs

- Current Scene Context
- Character State
- Relationship State
- Narrative Goal
- Emotional Context
- Active Quest
- Character Personality
- Timeline Position

Retrieval produces an ordered candidate list instead of a single result.

Ranking considers:

- Semantic Relevance
- Memory Quality
- Runtime Context
- Narrative Needs
- Recency

The exact scoring algorithm is implementation-defined and intentionally left open for future optimization.

---

# 10.5 Memory Quality Model (Key Feature)

Every Memory contains quality attributes that evolve over time.

These attributes simulate human cognition rather than database storage.

## Strength

Represents how firmly the memory is encoded.

Higher Strength makes memories resistant to forgetting.

---

## Accuracy

Represents how faithfully the stored memory reflects the original event.

Accuracy may decrease because of:

- Time
- Conflicting experiences
- False beliefs
- Dreams
- Gaslighting
- Narrative mechanics

Characters may confidently remember something incorrectly.

---

## Emotional Weight

Represents emotional intensity.

High Emotional Weight increases retrieval priority.

Traumatic and joyful memories often remain emotionally strong.

---

## Accessibility

Represents how easily a memory can be recalled.

Accessibility naturally decreases over time.

Repeated retrieval increases Accessibility.

---

## Recency

Represents how recently the memory was created or recalled.

Recent memories receive temporary retrieval priority.

---

## Behavioral Effects

### Forgetting

When Accessibility becomes extremely low, memories move into subconscious storage instead of immediate retrieval.

---

### Flashbulb Memory

Highly emotional memories resist decay.

Examples:

- Death
- Trauma
- Marriage
- First Love

---

### Distortion

A memory may have:

High Strength

+

Low Accuracy

The character strongly believes something that is objectively incorrect.

This enables future mechanics such as:

- unreliable narration
- lies
- manipulation
- memory alteration
- dream sequences

---

### Reinforcement

Whenever a memory is recalled or reinforced by new experiences:

- Strength increases
- Accessibility increases
- Emotional Weight may increase or decrease

Memory quality continuously evolves throughout gameplay.

---

# 11. Memory Consolidation

To prevent unlimited memory growth, the system continuously consolidates memories.

Consolidation simulates long-term human learning.

Process:

1. Pattern Matching
2. Similarity Detection
3. Abstraction
4. Memory Merge
5. Quality Adjustment

Example:

Five individual memories:

"He helped me."

↓

One abstract memory:

"He is reliable."

Detailed events become generalized knowledge.

Consolidation preserves meaning while reducing storage complexity.

---

# 11.5 Memory Activation (Key Feature)

Memory Activation determines which memories become active during runtime reasoning.

Unlike traditional retrieval systems, Activation simulates subconscious recall.

Activation does not retrieve memories directly.

Instead, it adjusts their probability of participating in runtime reasoning.

## Activation Triggers

### Current Scene

Objects, locations or atmosphere may activate related memories.

Example:

Fireworks

↓

First Date

---

### Emotional Context

Current emotions bias recall.

Example:

Fear

↓

Past Trauma

---

### Relationship State

Relationship changes activate related interpersonal memories.

Example:

High Trust

↓

Shared Secret

---

### Narrative Goal

Certain memories become more relevant depending on story objectives.

Example:

Reconciliation

↓

Previous Conflict

---

### Player Action

Player choices may awaken forgotten experiences.

Example:

Giving Flowers

↓

Past Romance

---

### Environmental Trigger

Visual, audio or environmental cues increase activation probability.

Examples:

- Rain
- Music
- Smell
- Childhood Home
- Festival

---

## Runtime Behavior

Activation modifies retrieval priority.

It does not change historical facts.

It does not create new memories.

It only determines which existing memories are most likely to influence current reasoning.

This allows the Runtime to simulate natural, context-sensitive recall rather than deterministic database queries.
# 12. Memory Influence

Retrieved memories serve as structured inputs to other runtime systems.

**Relationship Engine**
- Updates Trust, Affection, Respect, and other relationship dimensions based on recalled experiences.
- Enables long-term relationship evolution beyond immediate interactions.

**Narrative Director**
- Uses recalled memories to influence pacing, emotional tone, callbacks, and scene selection.
- Ensures narrative continuity across long play sessions.

**Prompt Builder**
- Injects only the highest-priority memories into prompt context.
- Converts structured memories into concise prompt-ready representations.

**Simulation Layer**
- May reference historical memories when evaluating certain rules or event triggers.
- Historical facts remain immutable.

**Rule**

Memory never changes historical facts.

It only influences future reasoning, simulation, and presentation.

---

# 13. Runtime Guarantees

The Memory System guarantees:

- **Immutability**
  - Historical memory content cannot be modified after persistence.
  - Only quality attributes and accessibility may evolve.

- **Asynchronous Persistence**
  - Memory writing must never block Scene completion.
  - Persistence failures may be retried asynchronously.

- **Deterministic Extraction**
  - Identical Scene Results always produce identical Memory Objects.

- **Deterministic Retrieval**
  - Given the same runtime context and activation state,
    retrieval order is reproducible.

- **Isolation**
  - Memory failures must not interrupt Runtime execution.

- **Data Integrity**
  - Corrupted memory records must not crash the engine.
  - Invalid memories may be skipped or quarantined.

---

# 14. Architecture & Hardware

## Architecture

The Memory System is implementation-agnostic.

Possible storage technologies include:

- Vector Index
  - Semantic retrieval

- Structured Storage
  - Memory metadata
  - Quality attributes
  - Runtime indexes

- Graph Index (Optional)
  - Relationship between memories
  - Story event graph
  - Character memory graph

Implementations may choose:

- SQLite
- DuckDB
- PostgreSQL
- Neo4j
- Other equivalent technologies

without changing this Blueprint.

---

## Hardware Considerations

Target Hardware:

RTX 5060 8GB (Reference Platform)

Design Goals:

- CPU-oriented indexing and retrieval
- Low-latency activation
- Background persistence
- Scalable memory storage
- Minimal runtime overhead

Target Retrieval Latency:

Memory Activation + Retrieval

< 200 ms

under normal gameplay conditions.

---

# 15. Future Extensibility

The architecture is designed for future expansion.

Possible future modules include:

## Semantic Memory

Stores abstract knowledge instead of experiences.

Example:

"The capital of the kingdom is Aster."

---

## Procedural Memory

Stores learned skills and habits.

Example:

"Knows how to play piano."

---

## False Memory

Supports narrative devices such as:

- Brainwashing
- Hallucination
- Dream sequences
- Memory implantation

---

## Dream Processing

Allows memories to consolidate during sleep or downtime.

Dream processing may:

- strengthen memories
- weaken memories
- merge memories
- distort memories

without modifying historical facts.

---

## Memory Graph

Represents relationships between memories.

Supports:

- causal reasoning
- emotional chains
- thematic clustering
- long-term story analysis

---

# References

## Depends On

- Overall Architecture
- Runtime Architecture
- Scene Engine Blueprint
- Simulation Layer Blueprint
- Relationship Engine Blueprint
- Glossary

---

## Referenced By

- Prompt Builder Blueprint
- Narrative Director Blueprint
- Relationship Engine Blueprint
- Memory Schema (Future)
- LLM Runtime Blueprint (Future)

---

# Revision History

| Version | Date | Description |
|----------|------------|------------------------------------------------------------|
| v1.2 | 2026-07-13 | Added Memory Activation, refined Accuracy definition, clarified asynchronous persistence, storage-agnostic architecture, deterministic retrieval guarantees |
| v1.1 | 2026-07-13 | Added Memory Quality Model (Strength, Accessibility, Emotional Weight, etc.) |
| v1.0 | 2026-07-13 | Initial Engineering Blueprint |