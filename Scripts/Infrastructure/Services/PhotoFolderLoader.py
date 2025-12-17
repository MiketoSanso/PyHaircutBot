import os
from pathlib import Path
from typing import List
from Scripts.Application.Interfaces.PhotoService import PhotoService


class PhotoFolderLoader(PhotoService):
    def load_all_photoes(self, folder_path: Path) -> List[str]:
        photos = []

        if not folder_path.exists():
            return photos

        for filename in sorted(folder_path.iterdir()):
            if filename.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                photos.append(str(filename))

        return photos