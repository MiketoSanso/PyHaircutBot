from typing import List
from Scripts.Application.Interfaces.PhotoService import PhotoService
from Scripts.Infrastructure.Services.ProjectPathFinder import ProjectPathFinder


class GetQrUseCase:
    def __init__(self, photo_service: PhotoService,
                 path_finder: ProjectPathFinder):
        self.photo_service = photo_service
        self.path_finder = path_finder

    def execute(self) -> List[str]:
        path = self.path_finder.qr_path
        return self.photo_service.load_all_photoes(path)
