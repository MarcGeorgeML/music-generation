from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from configs.dataset.dataset_cleaner_config import DatasetCleanerConstants, DatasetCleaningConfig, DatasetCleaningReport
from configs.dataset.instrument_family_extractor_config import InstrumentFamilyConstants
from music_generation.utils.utils import parse_list_value


LOGGER = logging.getLogger(__name__)


class DatasetCleaner:
    def __init__(self,config: DatasetCleaningConfig,) -> None:
        self.config = config

    def run(self) -> DatasetCleaningReport:
        self._create_directories()
        
        validation_df = pd.read_csv(self.config.validation_csv)
        genre_df = pd.read_csv(self.config.genre_csv)
        instrument_df = pd.read_csv(self.config.instrument_csv)
        track_df = pd.read_csv(self.config.track_metadata_csv)
        
        genre_df = genre_df.dropna(subset=["midi_path", "genres"])
        genre_df = genre_df[genre_df["genres"].astype(str).str.strip() != ""].copy()

        instrument_df = instrument_df.copy()
        instrument_df["instrument_families"] = (instrument_df["instrument_families"].apply(self._clean_instrument_families))
        instrument_df = instrument_df[instrument_df["instrument_families"] != ""].copy()
        instrument_df = instrument_df.drop(columns=["track_id"],errors="ignore",)

        all_paths = set(track_df["midi_path"])

        valid_paths = set(validation_df.loc[validation_df["is_valid"].astype(bool), "file_path"])
        genre_paths = set(genre_df["midi_path"])
        instrument_paths = set(instrument_df["midi_path"])

        retained_paths = all_paths & valid_paths & genre_paths & instrument_paths
        retained_files = len(retained_paths)

        genre_df = genre_df.drop_duplicates(subset=["midi_path"])
        clean_genres = genre_df[genre_df["midi_path"].isin(retained_paths)].copy()
        clean_instruments = instrument_df[instrument_df["midi_path"].isin(retained_paths)].copy()
        
        clean_dataset = pd.DataFrame({"midi_path": sorted(retained_paths)})
        clean_dataset = clean_dataset.merge(clean_genres,on="midi_path",how="left",)
        clean_dataset = clean_dataset.merge(clean_instruments,on="midi_path",how="left",)
        clean_dataset = clean_dataset.drop_duplicates(subset=["midi_path"])

        clean_dataset.to_csv(self.config.clean_dataset_csv,index=False,)
        clean_genres.to_csv(self.config.clean_genre_csv,index=False,)
        clean_instruments.to_csv(self.config.clean_instrument_csv,index=False,)


        report = DatasetCleaningReport(
            initial_files=len(all_paths),
            retained_files=retained_files,
            retention_rate=(retained_files / len(all_paths)) if all_paths else 0.0,
            removed_invalid_files=len(all_paths - valid_paths),
            removed_missing_genres=len((all_paths & valid_paths) - genre_paths),
            removed_empty_instrument_assignments=len((all_paths & valid_paths & genre_paths) - instrument_paths),
        )

        self._save_report(report)
        LOGGER.info("Retained %s/%s files",retained_files,len(all_paths),)
        return report

    def _clean_instrument_families(self,value: Any) -> str:
        families = parse_list_value(value)

        families = [
            family.lower()
            for family in families
            if family.lower()
            in DatasetCleanerConstants.SUPPORTED_INSTRUMENT_FAMILIES
        ]

        family_set = set(families)
        ordered = [f for f in InstrumentFamilyConstants.FAMILY_ORDER if f in family_set]
        return "|".join(ordered)

    def _create_directories(self,) -> None:
        self.config.clean_dataset_csv.parent.mkdir(parents=True,exist_ok=True,)
        self.config.clean_genre_csv.parent.mkdir(parents=True,exist_ok=True,)
        self.config.clean_instrument_csv.parent.mkdir(parents=True,exist_ok=True,)
        self.config.report_json.parent.mkdir(parents=True,exist_ok=True,)

    def _save_report(self,report: DatasetCleaningReport,) -> None:
        with open(self.config.report_json,"w",encoding="utf-8",) as f:
            json.dump(asdict(report),f,indent=2)

