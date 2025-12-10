from pathlib import Path

class ProjectPathFinder():
    def find_path(self) -> Path:
        current = Path(__file__).resolve()

        for parent in [current] + list(current.parents):
            if (parent / ".git").exists():
                return parent

        return current