from functools import cached_property
from pathlib import Path

class ProjectPathFinder:
    def _find_path_project(self) -> Path:
        current = Path(__file__).resolve()

        for parent in [current] + list(current.parents):
            if (parent / ".git").exists():
                return parent

        return current

    @cached_property
    def configs_path(self) -> Path:
        direction = self._find_path_project()
        return direction / "Configs"

    @cached_property
    def env_path(self) -> Path:
        direction = self._find_path_project()
        return direction / "tech.env"

    @cached_property
    def qr_path(self) -> Path:
        direction = self._find_path_project()
        return direction / "Images" / "Qr"

    @cached_property
    def references_path(self) -> Path:
        direction = self._find_path_project()
        return direction / "Images" / "References"