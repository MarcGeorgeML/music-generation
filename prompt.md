# SECTION 1 — ROLE
- You are a senior Machine Learning Engineer implementing a complete Music AI project.
- Your responsibility is to implement the project one step at a time.
- The architecture has already been approved.
- The development roadmap has already been approved.
- If information required for implementation is missing, ask only the minimum number of questions necessary to proceed.
- Otherwise begin implementation immediately.

---

# SECTION 2 — ARCHITECTURE FREEZE

## Project Goal

Genre-conditioned symbolic music arrangement generation.
Generate multi-instrument symbolic arrangements conditioned on genre.
This is a portfolio-quality engineering project.

---

## Dataset

Dataset:
- LMD-Matched(subset of Lakh MIDI Dataset)
- LMD-Matched Metadata(Million Song Dataset HDF5 metadata)

Dataset Strategy:
- Single primary dataset.
- MIDI files sourced from LMD-Matched
- Genre labels derived from Million Song Dataset metadata

Instrument Family Detection:

- Detect instrument families present in every track.
- Preserve all instrument tracks during tokenization.
- Instrument families are used as track-level events during tokenization.
- No dominant instrument selection is performed.

---

## Genres

Supported Genre Tokens:
- <GENRE_ROCK>
- <GENRE_POP>
- <GENRE_ELECTRONIC>
- <GENRE_JAZZ>
- <GENRE_HIPHOP>


Multi-Genre Handling:
If a MIDI file is assigned multiple genres,
multiple training examples will be created.

Example:

Genres:
- Pop
- Rock

Produces:
<GENRE_POP> + sequence
<GENRE_ROCK> + sequence

Every sequence must begin with exactly one genre token.

---

## Tokenization

Tokenization Method:
REMI

Sequence Prefix Tokens:
<GENRE_*>

Sequence Prefix Format:
<GENRE_*>
followed by REMI events.

Instrument events appear inside the sequence body and identify
which instrument family produced subsequent note events.

REMI Events:
- BAR
- POSITION
- NOTE_ON
- DURATION
- VELOCITY
- END

Instrument Representation:

All supported instrument families are preserved.

Supported Instrument Events:

- INST_PIANO
- INST_GUITAR
- INST_BASS
- INST_STRINGS
- INST_DRUMS



Instrument Events:
- Instrument events are part of the REMI vocabulary and appear within the sequence body.
- They indicate which instrument family subsequent note events belong to.

Example:

INST_DRUMS
POSITION_0
NOTE_ON_36
DURATION_4

INST_BASS
POSITION_0
NOTE_ON_40
DURATION_16

INST_GUITAR
POSITION_0
NOTE_ON_64
DURATION_8

Polyphonic notes are preserved.
Do not use raw MIDI program numbers in the vocabulary.

Instrument Family Ordering:

Instrument families must be emitted in a deterministic order:
1. Drums
2. Bass
3. Guitar
4. Piano
5. Strings
This ordering must be used consistently during encoding and decoding.

---

## Model Architecture
Architecture Family:
Decoder-Only Transformer

Architecture Variant:
Music Transformer

Attention Mechanism:
Relative Positional Attention

Training Objective:
Autoregressive Next Token Prediction

Loss Function:
Cross Entropy Loss

During decoding, instrument events determine which MIDI track receives subsequent notes.

Generation Mode:
Generate complete multi-instrument arrangements from genre conditioning.
Not continuation-only generation.

---

## Training Stack

Framework:
PyTorch

Distributed / Training Utility:
HuggingFace Accelerate

Experiment Tracking:
MLflow

Precision:
FP16 Mixed Precision

Target Hardware:
RTX 4060 8GB

All implementation decisions should remain compatible with this hardware target.

---

## Supporting Components

Genre Classifier

Purpose:

- Dataset validation
- Baseline classification
- Generator evaluation

---

## Evaluation Metrics

Required Metrics:

- Training Loss
- Validation Loss
- Perplexity
- Genre Classification Accuracy
- Pitch Distribution Similarity
- Duration Distribution Similarity
- Rhythm Distribution Similarity

Human listening studies are not included.

---

## Interpretability

Required Components:

- Attention Extraction
- Attention Visualization
- Genre Influence Analysis
- Long-Range Dependency Analysis

---

## Explicitly Rejected

Do not introduce:

- Audio generation
- Lyrics generation
- Vocal synthesis
- Text-to-music
- Real-time generation
- Piano-roll representation
- MIDI-Like representation
- Learned genre embeddings
- Cross-attention conditioning
- FiLM conditioning
- Adapter conditioning
- Diffusion models
- GANs
- VAEs
- RLHF
- Preference optimization
- Retrieval augmentation
- Mood conditioning
- Composer conditioning
- Tempo conditioning
- VGM datasets
- Human listening studies
- Novel architecture research

These decisions are final.

---

# SECTION 3 — DEVELOPMENT PROTOCOL AND ROADMAP

## General Rules

- Follow the roadmap exactly.
- Never skip steps.
- Never reorder steps.
- Complete only one step at a time.
- Do not discuss future steps.
- Do not summarize future phases.
- Do not create implementation plans.
- Do not create new roadmaps.
- The roadmap is provided only for context.
- Only implement the Current Step specified in Section 4.

- Large steps must be broken into manageable substeps.
- Prefer iterative implementation and avoid code dumps larger than ~300 lines.

After every implementation:
1. Explain what was implemented.
2. List created files.
3. List modified files.
4. Provide verification instructions.
5. Stop.

Wait for human approval before proceeding.

---

## FINAL COMPLETION CHECKLIST

Project completion requires all of the following:

- Trained Music Transformer
- Trained Genre Classifier
- REMI Tokenizer
- REMI Vocabulary
- Dataset Processing Pipeline
- Generation Pipeline
- Evaluation Suite
- Attention Visualization Suite
- Reproducible Training Instructions
- README
- Experiment Documentation
- Sample Generated Multi-Instrument MIDIs
- Saved Checkpoints

Do not declare project completion until all items have been verified.

---

# SECTION 4 — CURRENT PROJECT STATE

Current Phase:
Phase 1 — Dataset Pipeline

Current Step:
Step 9 — Dataset Split Generation

Current Status:
NOT STARTED

---

## Completed Steps

✓ Step 1 — Repository Structure Setup
✓ Step 2 — Dataset Loader
✓ Step 3 — MIDI Validation Pipeline
✓ Step 4 — Genre Metadata Extraction
✓ Step 5 — Instrument Family Extraction
✓ Step 6 — Dataset Statistics Generation
✓ Step 7 — Dataset Cleaning Pipeline
✓ Step 8 — Duplicate Detection
✓ Tests Passing

---

## Current Repository Structure

music-generation/

├── data/
│   ├── raw/
│   │   ├── lmd_matched/
│   │   └── lmd_matched_h5/
│   │
│   ├── interim/
│   │   ├── midi_validation_results.csv
│   │   ├── genre_metadata.csv
│   │   ├── track_metadata.csv
│   │   ├── midi_durations.csv
│   │   └── instrument_families.csv
│   │
│   ├── reports/
│   │   ├── dataset_analysis.md
│   │   ├── dataset_cleaning_report.json
│   │   ├── dataset_summary.json
│   │   ├── genre_instrument_statistics.csv
│   │   ├── genre_statistics.csv
│   │   ├── instrument_statistics.csv
│   │   └── midi_duration_statistics.json
│   │
│   ├── processed/
│   │   ├── clean_dataset.csv
│   │   ├── clean_genre_metadata.csv
│   │   └── clean_instrument_families.csv
│   │
│   └── splits/
│
├── checkpoints/
├── logs/
├── outputs/
├── notebooks/
│
├── scripts/
│   ├── scan_dataset.py
│   ├── run_midi_validator.py
│   ├── run_genre_metadata_extraction.py
│   ├── run_metadata_extraction.py
│   ├── analyze_tags.py
│   ├── analyze_genres.py
│   ├── run_instrument_family_extraction.py
│   ├── run_dataset_statistics.py
│   └── run_dataset_cleaner.py
│
├── tests/
│   ├── data/
│   │   ├── test_dataset_loader.py
│   │   ├── test_midi_validator.py
│   │   ├── test_genre_metadata_extractor.py
│   │   ├── test_instrument_family_extractor.py
│   │   ├── test_dataset_statistics.py
│   │   ├── test_metadata_extractor.py
│   │   └── test_dataset_cleaner.py
│   │
│   ├── tokenization/
│   ├── classifier/
│   ├── transformer/
│   └── generation/
│
├── src/
│   ├── configs/
│   │   ├── dataset/
│   │   │   ├── common_config.py
│   │   │   ├── dataset_cleaner_config.py
│   │   │   ├── dataset_statistics_config.py
│   │   │   ├── genre_metadata_extractor_config.py
│   │   │   ├── instrument_family_extractor_config.py
│   │   │   └── metadata_extractor_config.py
│   │   │
│   │   ├── tokenizer/
│   │   ├── classifier/
│   │   ├── transformer/
│   │   └── generation/
│   │
│   ├── music_generation/
│   │   ├── data/
│   │   │   ├── dataset_loader.py
│   │   │   ├── midi_validator.py
│   │   │   ├── genre_metadata_extractor.py
│   │   │   ├── metadata_extractor.py
│   │   │   ├── instrument_family_extractor.py
│   │   │   ├── dataset_statistics.py
│   │   │   └── dataset_cleaner.py
│   │   │
│   │   ├── tokenization/
│   │   ├── classifier/
│   │   ├── transformer/
│   │   ├── generation/
│   │   ├── evaluation/
│   │   ├── interpretability/
│   │   └── utils/
│   │
│   └── music_generation.egg-info
│
├── pyproject.toml
├── uv.lock
└── .venv/

---

## Package Configuration

Project uses:
src-layout

Imports must use:
from music_generation.data.dataset_loader import DatasetLoader

Never:
from src...

---

## Current Dataset State

Initial Files:
113,324

Retained Files:
94,665

Retention Rate:
83.53%

## Available Input Artifact

File:
data/processed/clean_dataset.csv

Columns:
midi_path
track_id
genres
genre_source
instrument_families

Records:
94,665

## Current Step — Dataset Split Generation

Objective:
Create reproducible train, validation, and test splits from the cleaned dataset.

Output Directory:
data/processed/

Approved Inputs:
data/processed/clean_dataset.csv

Metadata Keys:
midi_path

Important:
* `midi_path` remains the canonical file-level identifier.
* Each MIDI file must appear in exactly one split.
* No overlap is allowed between train, validation, and test sets.

Split Requirements:
1. Generate train, validation, and test splits.
2. Random Seed: 42
3. Preserve genre distribution as closely as possible across splits.
4. Ensure every MIDI file appears in only one split.
5. Generate split statistics.

Recommended Split Ratio:
Train      80%
Validation 10%
Test       10%

Genre Stratification Strategy:
Use the first genre in the genres field as the primary genre.

Examples:
rock|pop -> rock
electronic|pop -> electronic
jazz -> jazz

Stratification should be performed using the primary genre only.

Expected Outputs:
data/processed/train.csv
data/processed/validation.csv
data/processed/test.csv
data/reports/dataset_split_report.json

Do NOT:
* Detect duplicates
* Perform additional dataset cleaning
* Implement tokenization
* Build vocabularies
* Implement REMI encoding
* Implement REMI decoding
* Create training sequences

Step 9 is a dataset partitioning stage only.

Step 9 Completion Requirements:

* Train split generated
* Validation split generated
* Test split generated
* No overlap between splits
* Split statistics generated
* Output artifacts saved

Implementation Protocol:

Begin with:
Part 1 — Goal
Part 2 — Design Review

Then wait for approval before writing code.

