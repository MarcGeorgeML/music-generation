# Architecture Decisions and Design Rationale

This document records the major architectural decisions made during project planning, the alternatives considered, and the rationale behind each choice.

The goal of this project is not to reproduce a research paper exactly, but to build a complete, production-quality Music AI portfolio project that demonstrates competence in symbolic music generation, deep learning, and music representation learning.

---

# 1. Project Goal


Build a genre-conditioned symbolic music generation system capable of generating complete piano MIDI compositions.

---

# 2. Generation Scope

Generate single-track piano music.

## Why This Was Chosen

Piano-only generation dramatically simplifies:

* Dataset processing
* Representation design
* Training
* Debugging

while still demonstrating all core Music AI concepts.

The project focuses on learning symbolic music generation rather than orchestration.

## Alternatives Considered

### Multi-Track Generation

#### Pros

* More realistic music
* Richer arrangements
* Stronger commercial relevance

#### Cons

* Complex preprocessing
* Instrument mapping requirements
* Longer token sequences
* Increased training cost

## Final Reasoning

The additional complexity of multitrack generation does not provide enough additional learning value for a first Music AI project.

---

# 3. Dataset Strategy

## Decision

Use the Lakh MIDI Dataset as the primary dataset.

## Why This Was Chosen

The dataset provides:

* Large scale
* Multiple genres
* Widespread use in symbolic music research

It is large enough to support Transformer training while remaining accessible.

## Filtering Strategy

Keep only files that are:

* Valid MIDI
* Piano-based
* Genre labeled
* Reasonable length

Remove:

* Corrupted files
* Extremely short pieces
* Extremely long pieces
* Duplicates

## Alternatives Considered

### MAESTRO

#### Pros

* Extremely clean
* High-quality performances

#### Cons

* Primarily classical music
* Poor genre diversity

### Custom Curated Dataset

#### Pros

* Full control over quality

#### Cons

* Significant manual effort
* Difficult to scale

## Final Reasoning

Lakh MIDI provides the best balance between size, genre diversity, and practicality.

---

# 4. Genre Set

## Decision

Use four genres:

* Classical
* Jazz
* Pop
* Rock

## Why This Was Chosen

These genres are:

* Commonly represented
* Distinct from one another
* Easy to evaluate

Strong genre separation makes conditioning easier to validate.

## Alternatives Considered

### Video Game Music (VGM)

#### Pros

* Personally interesting
* Relevant to Music AI

#### Cons

* Inconsistent metadata
* Smaller available datasets
* Ambiguous genre boundaries

## Final Reasoning

Rock provides cleaner and more reliable training data than VGM.

---

# 5. Symbolic Representation

## Decision

Use REMI (Revamped MIDI Representation).

## Why This Was Chosen

REMI explicitly models musical structure through:

* Bar tokens
* Position tokens
* Note events
* Duration events
* Velocity events

This representation is widely used in modern symbolic music generation research.

## Advantages

* Structure-aware
* Transformer-friendly
* Beat-aware
* Bar-aware

## Alternatives Considered

### Piano Roll

#### Pros

* Easy to visualize

#### Cons

* Large and sparse
* Poor fit for Transformers

### MIDI-Like Representation

#### Pros

* Simple
* Easy implementation

#### Cons

* Long sequences
* Musical structure is implicit

## Final Reasoning

REMI provides the strongest balance between musical structure and implementation complexity.

---

# 6. Conditioning Method

## Decision

Use genre prefix tokens.

Example:

<GENRE_JAZZ>

followed by the REMI token sequence.

## Why This Was Chosen

Genre tokens are:

* Simple
* Effective
* Easy to implement
* Easy to explain

The Transformer can attend to the genre token throughout generation.

## Alternatives Considered

### Learned Genre Embeddings

#### Pros

* Stronger conditioning signal

#### Cons

* Additional complexity
* Unnecessary for only four genres

### Cross-Attention Conditioning

#### Pros

* Powerful and flexible

#### Cons

* Overkill for project scope

## Final Reasoning

A genre token provides sufficient conditioning while minimizing architectural complexity.

---

# 7. Transformer Architecture

## Decision

Use a Music Transformer architecture with relative positional attention.

## Why This Was Chosen

Music contains long-range dependencies:

* Motifs
* Repeated phrases
* Recurring rhythmic patterns

Relative positional attention is better suited for these relationships than absolute positional encoding.

## Advantages

* Music-specific design
* Better long-term structure modeling
* Strong Music AI relevance

## Alternatives Considered

### Vanilla GPT-Style Transformer

#### Pros

* Easier implementation
* Well understood

#### Cons

* Less specialized for music

## Final Reasoning

The additional implementation complexity is justified by the stronger Music AI relevance and portfolio value.

---

# 8. Evaluation Strategy

## Decision

Use automatic evaluation only.

### Training Metrics

* Training Loss
* Validation Loss
* Perplexity

### Conditioning Metrics

* Genre Classification Accuracy

### Music Statistics

* Pitch Distribution Similarity
* Duration Distribution Similarity
* Rhythm Distribution Similarity

## Why This Was Chosen

These metrics evaluate:

* Model learning
* Genre control
* Musical consistency

without requiring human studies.

## Alternatives Considered

### Human Evaluation

#### Pros

* Direct assessment of musical quality

#### Cons

* Subjective
* Difficult to scale
* Poor reproducibility

## Final Reasoning

Automatic metrics provide a sufficiently rigorous evaluation framework for a portfolio project.

---

# 9. Supporting Genre Classifier

## Decision

Build a genre classification model.

## Why This Was Chosen

The classifier serves three purposes:

1. Baseline classification task
2. Dataset validation
3. Generator evaluation

It provides a measurable way to determine whether generated music matches the intended genre.

## Final Reasoning

The classifier naturally complements the generator and strengthens the overall project.

---

# 10. Analysis Components

## Decision

Include Transformer attention visualization.

## Why This Was Chosen

Attention visualization helps answer:

* What patterns does the model learn?
* Does it attend across musical phrases?
* Does it capture long-range structure?

## Alternatives Considered

### Novel Architectures

#### Pros

* More research-oriented

#### Cons

* Increased complexity
* Higher risk of failure

## Final Reasoning

Interpretability provides stronger educational and interview value than adding unnecessary architectural complexity.

---

# Final Project Summary

Genre-Conditioned Piano Music Generation using:

* Lakh MIDI Dataset
* REMI Representation
* Genre Prefix Tokens
* Music Transformer
* Relative Positional Attention

with evaluation through:

* Perplexity
* Genre Classification Accuracy
* Musical Distribution Metrics

and additional analysis through:

* Genre Classification
* Attention Visualization
