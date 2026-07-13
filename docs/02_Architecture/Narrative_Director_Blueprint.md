# Narrative Director Blueprint

**Version:** v2.2  
**Status:** Draft  
**Last Updated:** 2026-07-13

---

# 1. Purpose

Define the responsibilities, boundaries, runtime behavior, and decision-making process of the Narrative Director.

The Narrative Director is the **story orchestration layer** of the AI Narrative RPG Engine.

It transforms simulation results into coherent, emotionally engaging narrative experiences.

It is **not** responsible for changing world state.

---

# 2. Responsibilities

## Responsible For

- Story Planning
- Narrative Goal Selection
- Scene Pacing
- Emotional Rhythm
- Event Prioritization
- Dialogue Intent Planning
- CG Trigger Decision
- Narrative Continuity
- Experience Quality

## Not Responsible For

- World Simulation
- Relationship Calculation
- Character State Update
- Memory Storage
- Prompt Rendering
- Dialogue Generation
- Image Generation

---

# 3. Document Governance

**Owner:** Narrative Architect

**Reviewers:**
- Runtime Architect
- Simulation Architect
- Product Architect

**Approval:**
Architecture Review Required

**Update Policy**

Changes affecting narrative decision flow, planning logic, or module boundaries require ADR approval.

---

# 4. Design Principles

## Story Follows State

Narrative never changes reality.

Simulation determines what happened.

Narrative determines how the player experiences what happened.

---

## Simulation Before Narrative

Narrative Director always consumes Simulation Output.

It never modifies Simulation Results.

---

## Emotion Before Information

Narrative should optimize emotional experience rather than maximize information delivery.

---

## Relationship Driven

Relationship State is the primary driver of narrative tone, pacing, and scene selection.

---

## Player Agency Matters

Player choices influence future narrative through Simulation.

Narrative never invalidates meaningful player decisions.

---

## One Story, Multiple Expressions

The same Simulation Result may be expressed differently depending on:

- Character Personality
- Relationship State
- Narrative Goal
- Content Profile

---

# 5. Boundary Definition

Narrative Director is a Planning Layer.

It owns:

- Story Planning
- Emotional Planning
- Scene Flow
- Narrative Goal
- Event Ordering

It does NOT own:

- World Rules
- State Transition
- Relationship Calculation
- Prompt Rendering
- LLM Output

---

# 6. Runtime Position

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

LLM

↓

Renderer

Narrative Director sits between deterministic simulation and probabilistic generation.

---

# 7. Runtime Inputs

The Director consumes the following data:

- **Scene Context:** Current location, participants, environment.
- **Character State:** Health, status, inventory of involved characters.
- **Relationship State:** Affinity, trust, active conflicts.
- **Behavior Tendency:** (From Relationship Engine) e.g., "Hostile", "Flirty".
- **Player Intent:** Derived from the last player action (e.g., "Aggressive", "Inquisitive").
- **Player Experience Profile:** User preferences (e.g., prefers slow-burn romance, high combat tension).
- **Quest State:** Current active objectives, critical path flags.
- **Simulation Events:** List of things that just happened (e.g., "Sword broke", "Entered combat").
- **Timeline:** Current story epoch.

---

# 8. Narrative Goal

Every Scene has exactly one Primary Narrative Goal.

Examples:

- Build Trust
- Increase Suspense
- Reveal Character
- Resolve Conflict
- Create Romance
- Deepen Relationship
- Deliver Reward
- Prepare Future Plot

Narrative Goal affects presentation only.

It never changes Simulation Result.

---

# 9. Narrative Planning

Narrative Planning determines:

- Which event appears first
- Which emotions are emphasized
- Which character receives focus
- Which memories are recalled
- Which dialogue style should be used

It never invents events that Simulation rejected.

---

# 10. Emotional Orchestration

Narrative Director controls emotional rhythm.

Possible emotional curves include:

- Calm → Warm
- Warm → Romantic
- Suspense → Relief
- Conflict → Reconciliation
- Mystery → Revelation
- Hope → Failure → Determination

Emotion is pacing.

Emotion is not state.

---

# 11. Event Selection

Simulation may produce multiple candidate events.

Example:

- Character notices player injury
- Character remembers previous promise
- Phone rings
- Rain starts
- Enemy approaches

Narrative Director chooses:

- which event occurs first
- which event is delayed
- which event is omitted
- which event becomes the narrative focus

It cannot create invalid events.

---

# 12. Relationship Influence

Relationship Engine provides structured Behavior Tendencies.

Example:

- willingness_to_help
- openness
- trust_level
- emotional_distance
- jealousy
- dependency

Narrative Director converts these tendencies into narrative decisions.

Example:

High Trust

↓

Friendly Tone

↓

Longer Conversation

↓

Private Scene

Low Trust

↓

Short Answers

↓

More Distance

↓

Guarded Body Language

---

# 13. Content Profile Adaptation

Different Content Profiles use the same Narrative Plan.

General Profile

↓

Adventure-oriented expression

Romance Profile

↓

Relationship-oriented expression

Mature Profile

↓

Adult emotional expression

Simulation State remains identical.

Only presentation changes.

---

# 14. CG Planning

Narrative Director determines whether a Scene deserves a CG.

Evaluation considers:

- Emotional Peak
- Story Importance
- Relationship Milestone
- Visual Value
- Gallery Progression

It outputs:

CG Requested

or

No CG

Image generation is performed later.

---

# 15. Failure Handling

If:

- Prompt Builder fails
- LLM fails
- Image generation fails

Narrative Director remains unchanged.

Planning results can be reused.

Planning must be deterministic.

Generation may be retried.

---

# 16. Runtime Guarantees

Narrative Director guarantees:

- Never modifies Simulation State
- Never modifies Relationship State
- Never bypasses Scene Engine
- Never bypasses Prompt Builder
- Produces deterministic Narrative Plans
- Supports replay using identical runtime state

---

# 17. Hardware Considerations

Designed for CPU execution.

No GPU dependency.

Planning latency should remain negligible compared with LLM generation.

Image generation remains asynchronous.

---

# 18. Future Extensibility

Future extensions include:

- Dynamic Story Arcs
- Multi-thread Narrative
- Parallel Character Goals
- Director Personalities
- AI Dungeon Master Mode
- Cooperative Multiplayer Narrative

---

# References

**Depends On**

- Overall Architecture
- Runtime Architecture
- Scene Engine Blueprint
- Simulation Layer Blueprint
- Relationship Engine Blueprint
- Glossary

**Referenced By**

- Prompt Builder Blueprint
- Prompt Templates
- Scene Engine
- Image Pipeline
- Future Narrative Planner

---

# Revision History

| Version | Date | Description |
|----------|------------|----------------------------------------------|
| v2.2 | 2026-07-13 | Strengthened narrative planning boundaries and runtime workflow |
| v2.1 | 2026-07-13 | Added Relationship Influence and Content Profile adaptation |
| v2.0 | 2026-07-13 | Initial Engineering Blueprint |