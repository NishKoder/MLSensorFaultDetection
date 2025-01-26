from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionArtifactEntity:
    trained_file_path: Path
    test_file_path: Path
