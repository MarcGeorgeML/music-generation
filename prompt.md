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

Dataset Cleaning Requirements:

- Remove corrupted MIDI files
- Remove MIDI files with no instruments
- Remove MIDI files with no notes
- Remove unlabeled MIDI files
- Remove extremely short MIDI files
- Remove extremely long MIDI files

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
Step 7 — Dataset Cleaning Pipeline

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
✓ Tests Passing

---

## Current Repository Structure

music-generation/
├── configs/
│   ├── dataset/
│   ├── tokenizer/
│   ├── classifier/
│   ├── transformer/
│   └── generation/
│
├── data/
│   ├── raw/
│   │   ├── lmd_matched/
│   │   └── lmd_matched_h5/
│   │
│   ├── interim/
│   │   ├── midi_validation_results.csv
│   │   ├── genre_metadata.csv
│   │   ├── track_metadata.csv
│   │   └── instrument_families.csv
│   │
│   ├── reports/
│   │   ├── dataset_analysis.md
│   │   ├── dataset_summary.json
│   │   ├── genre_instrument_statistics.csv
│   │   └── genre_statistics.csv
│   │   └── instrument_statistics.csv
│   │
│   ├── processed/
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
│   └── run_dataset_statistics.py
│
├── tests/
│   ├── data/
│   │   ├── test_dataset_loader.py
│   │   ├── test_midi_validator.py
│   │   ├── test_genre_metadata_extractor.py
│   │   ├── test_instrument_family_extractor.py
│   │   └── test_dataset_statistics.py
│   │
│   ├── tokenization/
│   ├── classifier/
│   ├── transformer/
│   └── generation/
│
├── src/
│   ├── music_generation/
│   │   ├── data/
│   │   │   ├── dataset_loader.py
│   │   │   ├── midi_validator.py
│   │   │   ├── genre_metadata_extractor.py
│   │   │   ├── metadata_extractor.py
│   │   │   ├── instrument_family_extractor.py
│   │   │   └── dataset_statistics.py
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

## Dataset Information

Dataset:
Lakh MIDI Dataset — Matched Subset (LMD-Matched)

Associated Metadata:
LMD-Matched HDF5 Metadata

Total Metadata Records:
113,324

Validated MIDI Files:
115,182

Invalid MIDI Files:
1,007

Unique Tracks:
30,898

---

## MIDI Validation Pipeline Status

Implemented Components:
✓ MidiValidationResult
✓ MidiValidator
✓ run_midi_validator.py

Validation Output:
data/interim/midi_validation_results.csv

Output Schema:
file_id
track_id
file_path
is_valid
failure_reason

Failure Reasons:
- parse_error
- no_instruments
- no_notes

---

## Genre Metadata Extraction Status

Implemented Components:
✓ GenreMetadataExtractor
✓ MetadataExtractor
✓ run_genre_metadata_extraction.py
✓ run_metadata_extraction.py
✓ analyze_tags.py
✓ analyze_genres.py

Metadata Output:
data/interim/track_metadata.csv

Output Schema:
track_id
midi_path
artist_terms
musicbrainz_tags

Genre Output:
data/interim/genre_metadata.csv

Output Schema:
track_id
midi_path
genres
genre_source

Records Created:
113,324

Genre Records Saved:
94,951

Final Genre Distribution:
- Rock: 52,101 (46.46%)
- Pop: 28,900 (25.77%)
- Electronic: 19,876 (17.72%)
- Jazz: 6,697 (5.97%)
- Hip Hop: 4,570 (4.08%)

---

## Instrument Family Extraction Status

Implemented Components:
✓ InstrumentFamilyExtractor
✓ run_instrument_family_extraction.py
✓ test_instrument_family_extractor.py

Output:
data/interim/instrument_families.csv

Output Schema:
track_id
midi_path
instrument_families

Records Created:
113,324

Raw Extracted Families:
- piano
- guitar
- bass
- strings
- drums
- other

Architecture Decision:
The "other" family will not be used by downstream components.
Approved Instrument Families Going Forward:

- piano
- guitar
- bass
- strings
- drums

"other" will be removed during the Dataset Cleaning Pipeline.

---

## Dataset Statistics Generation Status

Implemented Components:
✓ DatasetStatisticsConfig
✓ DatasetStatisticsResult
✓ dataset_statistics.py
✓ run_dataset_statistics.py
✓ test_dataset_statistics.py

Outputs:
data/reports/dataset_summary.json
data/reports/genre_statistics.csv
data/reports/instrument_statistics.csv
data/reports/genre_instrument_statistics.csv

Dataset Statistics Summary:
- Total MIDI Files: 113,324
- Total Unique Tracks: 30,574
- Genre Classes: 5
- Instrument Families: 6 (raw extraction)
- Average Instrument Families per MIDI: 4.56

Most Common Instrument Combination:
drums + bass + guitar + piano + strings + other

Dataset Assessment:
* Dataset size sufficient for Music Transformer training.
* Multi-instrument arrangements dominate the dataset.
* Genre coverage is acceptable across all target genres.
* Instrument family extraction validated successfully.
* Dataset approved to proceed to cleaning stage.

---

## Current Step — Dataset Cleaning Pipeline

Objective:
Create the cleaned training corpus using previously generated metadata artifacts.

Output Directory:
data/processed/

Approved Inputs:
data/interim/midi_validation_results.csv
data/interim/genre_metadata.csv
data/interim/instrument_families.csv
data/interim/track_metadata.csv

Cleaning Requirements:
1. Remove invalid MIDI files.
2. Remove MIDI files without genre labels.
3. Remove the "other" instrument family from all instrument assignments.
4. Remove MIDI files that contain no supported instrument families after filtering.
5. Remove extremely short MIDI files.
6. Remove extremely long MIDI files.
7. Generate cleaning statistics and retention reports.

Metadata Keys:
track_id
midi_path

Important:
track_id is NOT unique.
midi_path remains the canonical file-level identifier throughout cleaning.

Expected Outputs:
data/processed/clean_dataset.csv
data/processed/clean_genre_metadata.csv
data/processed/clean_instrument_families.csv
data/reports/dataset_cleaning_report.json

Do NOT:
- Detect duplicates
- Create train/validation/test splits
- Build tokenization components
- Implement REMI encoding
- Implement REMI decoding

Step 7 is a dataset filtering and retention stage only.

Step 7 Completion Requirements:
- Invalid files removed
- Unlabeled files removed
- "other" family removed
- Empty instrument assignments removed
- Cleaning statistics generated
- Cleaned metadata artifacts saved

Implementation Protocol:

Begin with:
Part 1 — Goal
Part 2 — Design Review

Then wait for approval before writing code.
