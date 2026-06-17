# uv run python scripts/run_instrument_family_extraction.py

import pandas as pd
from tqdm import tqdm

from music_generation.data.instrument_family_extractor import InstrumentFamilyExtractor
from configs.dataset.common_config import DatasetPaths, DatasetFiles



def main() -> None:

    track_metadata_path = (DatasetPaths.INTERIM_DIR/ DatasetFiles.TRACK_METADATA_CSV)
    validation_path = (DatasetPaths.INTERIM_DIR/ DatasetFiles.MIDI_VALIDATION_CSV)
    output_path = (DatasetPaths.INTERIM_DIR/ DatasetFiles.INSTRUMENT_FAMILIES_CSV)

    track_metadata = pd.read_csv(track_metadata_path)
    validation = pd.read_csv(validation_path)
    valid_paths = set(
        validation.loc[
            validation["is_valid"],
            "file_path",
        ]
    )

    dataset = track_metadata[track_metadata["midi_path"].isin(valid_paths)]
    extractor = InstrumentFamilyExtractor()
    records = []

    for row in tqdm(dataset.itertuples(index=False), total=len(dataset), desc="Extracting instrument families",):
        families = extractor.extract_families(str(row.midi_path))

        records.append(
            {
                "track_id": row.track_id,
                "midi_path": row.midi_path,
                "instrument_families": "|".join(
                    families
                ),
            }
        )

    pd.DataFrame(records).to_csv(output_path,index=False,)
    print(f"Saved {len(records)} records to {output_path}")


if __name__ == "__main__":
    main()
