
## PHASE 1 — DATASET PIPELINE

STEP 1 — Repository Structure Setup
STEP 2 — Dataset Loader
STEP 3 — MIDI Validation Pipeline
STEP 4 — Genre Metadata Extraction
STEP 5 — Instrument Family Extraction
STEP 6 — Dataset Statistics Generation
STEP 7 — Dataset Cleaning Pipeline
STEP 8 — Duplicate Detection
STEP 9 — Train / Validation / Test Split Creation
MILESTONE 1 — Dataset Ready

Deliverables:

- Clean dataset
- Genre distributions
- Split files
- Dataset report

Human approval required.

---

## PHASE 2 — TOKENIZATION PIPELINE

STEP 10 — REMI Vocabulary Design
STEP 11 — REMI Encoder
STEP 12 — REMI Decoder
STEP 13 — Round-Trip MIDI Reconstruction Testing
STEP 14 — Vocabulary Builder

MILESTONE 2 — Tokenization Pipeline Complete

Deliverables:
- REMI encoder
- REMI decoder
- Vocabulary
- Reconstruction tests

Human approval required.

---

## PHASE 3 — GENRE CLASSIFIER

STEP 15 — Genre Classifier Dataset Pipeline
STEP 16 — Genre Classifier Architecture
STEP 17 — Genre Classifier Training Pipeline
STEP 18 — Genre Classifier Evaluation

Target:
70%+ Accuracy

MILESTONE 3 — Genre Classifier Complete

Deliverables:
- Trained classifier
- Accuracy report
- Confusion matrix
- Saved checkpoint

Human approval required.

---

## PHASE 4 — MUSIC TRANSFORMER

STEP 19 — Relative Position Attention Module
STEP 20 — Transformer Block
STEP 21 — Music Transformer Architecture
STEP 22 — Autoregressive Dataset Loader
STEP 23 — Training Loop
STEP 24 — Checkpointing System
STEP 25 — Experiment Tracking
STEP 26 — Model Training

MILESTONE 4 — Music Transformer Trained

Deliverables:
- Trained checkpoints
- Loss curves
- Perplexity curves

Human approval required.

---

## PHASE 5 — GENERATION PIPELINE

STEP 27 — Sampling Strategies

Implement:
- Temperature Sampling
- Top-k Sampling
- Top-p Sampling

STEP 28 — MIDI Generation Pipeline
STEP 29 — Generation CLI

MILESTONE 5 — Generation System Complete

Deliverables:
- Genre-conditioned generation
- Generated MIDI samples
- Generation documentation

Human approval required.

---

## PHASE 6 — EVALUATION PIPELINE

STEP 30 — Perplexity Evaluation
STEP 31 — Genre Classification Evaluation
STEP 32 — Pitch Distribution Analysis
STEP 33 — Duration Distribution Analysis
STEP 34 — Rhythm Distribution Analysis
STEP 35 — Evaluation Report Generation

MILESTONE 6 — Evaluation Complete

Deliverables:
- Evaluation report
- Metric tables
- Statistical comparison figures

Human approval required.

---

## PHASE 7 — INTERPRETABILITY

STEP 36 — Attention Extraction
STEP 37 — Attention Visualization
STEP 38 — Genre Token Influence Analysis
STEP 39 — Long-Range Dependency Analysis

MILESTONE 7 — Interpretability Complete

Deliverables:

- Attention heatmaps
- Attention analysis report
- Genre influence analysis
- Long-range dependency examples

Human approval required.

---

## PHASE 8 — PROJECT COMPLETION

STEP 40 — README Creation
STEP 41 — Experiment Documentation
STEP 42 — Final Project Packaging

---















### Validation Metadata

**File:**
`data/interim/midi_validation_results.csv`

**Contents:**
file_id
track_id
file_path
is_valid
failure_reason

Used to identify valid MIDI files.

---

### Track Metadata

**File:**
`data/interim/track_metadata.csv`

**Contents:**
track_id
midi_path
artist_terms
musicbrainz_tags

Contains metadata extracted from LMD-Matched.

---

### Genre Metadata

**File:**
`data/interim/genre_metadata.csv`

**Contents:**
track_id
midi_path
genres
genre_source

Supported genres:
* Rock
* Pop
* Electronic
* Jazz
* Hip-hop

Records: 94,951

---

### Instrument Family Metadata

**File:**
`data/interim/instrument_families.csv`

**Contents:**
track_id
midi_path
instrument_families

Supported instrument families:
* Drums
* Bass
* Guitar
* Piano
* Strings

---

### Dataset Statistics

**Files:**
data/reports/dataset_summary.json
data/reports/genre_statistics.csv
data/reports/instrument_statistics.csv
data/reports/genre_instrument_statistics.csv

Dataset summary:
Total MIDI Files: 113,324
Total Unique Tracks: 30,574
Genre Classes: 5

---