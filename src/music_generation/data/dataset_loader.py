from pathlib import Path

import pandas as pd


class DatasetLoader:
    def scan(self, root_dir: str) -> pd.DataFrame:
        root = Path(root_dir)

        if not root.exists():
            raise FileNotFoundError(root)

        files = list(root.rglob("*.mid"))

        return pd.DataFrame(
            {
                "file_id": range(len(files)),
                "track_id": [
                    f.parent.name
                    for f in files
                ],
                "path": [
                    str(f.resolve())
                    for f in files
                ],
                "filename": [
                    f.name
                    for f in files
                ],
            }
        )
