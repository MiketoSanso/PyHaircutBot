from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class PhotoService(ABC):
    @abstractmethod
    def load_all_photoes(self, folder_path: Path) -> List[str]:
        pass
