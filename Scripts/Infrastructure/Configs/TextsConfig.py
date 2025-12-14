from Scripts.Application.Interfaces.TechConfigRepository import TechConfigRepository
from Scripts.Infrastructure.Services.ProjectPathFinder import ProjectPathFinder


class BotConfig(TechConfigRepository):
    def __init__(self, path_finder: ProjectPathFinder):
        self.__all_texts = {
            "a": "1"
        }