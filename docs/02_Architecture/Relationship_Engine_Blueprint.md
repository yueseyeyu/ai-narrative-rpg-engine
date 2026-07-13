# Relationship Engine Blueprint

**Version:** v2.2
**Status:** Draft
**Last Updated:** 2026-07-13

---

# 1. Purpose

Define the responsibilities, boundaries, runtime mechanisms, and data model of the Relationship Engine.

The Relationship Engine is the **long-term relationship simulation core** of the AI Narrative RPG Engine.

It transforms interactions, memories, and time into persistent relationship states, providing the foundation for character behavior, narrative progression, and emotional consistency.

Relationship is **not dialogue**, **not prompt**, and **not a single score**.

It is a continuously evolving runtime domain.

---

# 2. Responsibilities

## Responsible For

- Managing persistent Relationship State
- Calculating relationship evolution
- Maintaining relationship consistency
- Producing Behavior Tendencies
- Producing Relationship Constraints
- Applying decay and recovery
- Resolving relationship conflicts
- Supporting long-term emotional progression

## Not Responsible For

- World Simulation
- Character Internal Simulation
- Dialogue Generation
- Image Generation
- Memory Storage
- Narrative Writing

---

# 3. Document Governance

**Owner:** Relationship Architect

**Reviewers:**

- Runtime Architect
- Simulation Architect

**Approval**

Architecture Review Required

**Update Policy**

Adding relationship dimensions requires ADR.

Changing evolution rules requires ADR.

Parameter tuning (weights, decay, caps) only requires changelog updates.

---

# 4. Design Principles

- Multi-dimensional Relationship
- Relationship Before Narrative
- Simulation Before Generation
- Deterministic Evolution
- State Is Ground Truth
- Long-term Consistency
- Rule-driven Evolution

---

# 5. Boundary Definition

Relationship Engine owns:

- Relationship Dimensions
- Relationship Rules
- Behavior Tendency
- Relationship Constraints
- Evolution Logic

Relationship Engine does NOT own:

- Dialogue
- Story Writing
- Images
- UI
- Prompt Construction
- Character Internal State

---

# 6. Runtime Position

Relationship Engine is a core subsystem inside the Simulation Layer.

```
Player Action
        │
        ▼
Simulation Layer
        │
        ▼
Relationship Engine
        │
        ▼
Updated Relationship State
        │
        ▼
Behavior Tendency
        │
        ▼
Narrative Director
```

Narrative Director consumes Relationship outputs but never modifies Relationship State directly.

---

# 7. Runtime Model

Relationship Runtime follows a deterministic pipeline.

```
Interaction

↓

Current Relationship State

↓

Rule Evaluation

↓

Dimension Update

↓

Decay / Recovery

↓

Conflict Resolution

↓

Behavior Inference

↓

Relationship Constraints

↓

Updated Relationship State
```

---

# 8. Relationship State Model

Relationship State consists of multiple independent dimensions.

## Core Dimensions

- Trust
- Respect
- Familiarity
- Attachment
- Affection
- Intimacy

## Dynamic Dimensions

- Emotional Momentum
- Dependency
- Fear
- Curiosity
- Jealousy

## Derived Metrics

- Relationship Score (UI only)
- Future Expectation
- Stability Index

Relationship Score is never used as the source of truth.

---

# 9. Relationship Graph

Relationship Engine internally maintains a dynamic social graph.

Each Relationship represents one edge between runtime entities.

```
Character A
      │
 Trust
      │
Character B
```

Future supported entities include:

- Character
- Player
- Faction
- Organization
- Guild
- Kingdom
- Pet
- World Event

Current implementation focuses on Character relationships while keeping the data model extensible.

---

# 10. Relationship Evolution

Relationship changes are driven by:

- Direct Interaction
- Time Passage
- Shared Events
- Memory Recall
- Character Personality
- World Events

Example:

```
New Value

=

Old Value

+

Interaction Impact

+

Memory Bonus

-

Time Decay
```

Different dimensions have different decay rates.

For example:

- Familiarity decays slowly
- Emotional Momentum changes quickly
- Attachment rarely decreases naturally

---

# 11. Rule Engine

Relationship evolution is rule-driven.

Rule Types:

- Interaction Rules
- Personality Rules
- World Rules
- Event Rules
- Constraint Rules

Future:

- Plugin Rules
- Mod Rules

LLM cannot bypass Rule Engine.

---

# 12. Behavior Tendency

Behavior Tendency is the primary runtime output.

Example:

```json
{
  "willingness_to_help": 0.82,
  "hostility": 0.05,
  "openness": 0.63,
  "initiative": 0.71,
  "tone_modifier": "friendly_but_cautious",
  "suggested_actions": [
    "share_secret",
    "invite_walk"
  ]
}
```

Behavior Tendency guides Narrative Director.

It does not generate dialogue.

---

# 13. Relationship Constraints

Relationship Engine also produces hard runtime constraints.

Example:

```json
{
  "constraints": [
    "cannot_confess",
    "cannot_share_secret",
    "cannot_invite_home"
  ]
}
```

Constraints prevent Narrative Director from violating relationship logic.

Examples:

- Low Trust → Cannot Share Secret
- Low Respect → Refuse Orders
- Low Intimacy → No Romantic Actions

Constraints are mandatory.

Narrative Director must respect them.

---

# 14. Relationship Influence

Relationship State directly influences:

- Narrative Planning
- Dialogue Tone
- Scene Availability
- Character Behavior
- Quest Unlock
- CG Trigger
- Event Probability

Relationship never directly generates text.

---

# 15. Runtime Guarantees

Relationship Engine guarantees:

- Atomic State Updates
- Deterministic Results
- Traceable Changes
- Replayable Evolution
- Persistent Consistency

No external module may modify Relationship State directly.

---

# 16. Hardware Considerations

Target Platform:

RTX 5060 8GB

Relationship Engine is:

- CPU-first
- Lightweight
- GPU Independent
- High Frequency
- Background Friendly

---

# 17. Future Extensibility

Future features include:

- Group Relationships
- Social Networks
- Family Trees
- Political Systems
- Reputation Systems
- Mod-defined Relationship Dimensions

---

# References

**Depends On**

- Simulation Layer Blueprint
- Runtime Architecture
- Overall Architecture
- Glossary

**Referenced By**

- Narrative Director Blueprint
- Character System Blueprint
- Relationship State Schema
- Scene Engine
- Memory Architecture

---

# Revision History

| Version | Date | Description |
|----------|------|-------------|
| v2.2 | 2026-07-13 | Added Relationship Graph, Constraints, Runtime Model, Future Extensibility |
| v2.1 | 2026-07-13 | Added Behavior Tendency and detailed dimensions |
| v2.0 | 2026-07-13 | Initial Engineering Blueprint |