from Scripts.Application.Interfaces.ReviewRepository import ReviewRepository
from Scripts.Infrastructure.Services.JsonConfigManager import JsonConfigManager


class GetReviewByIndexUseCase:
    def __init__(self,
                 review_repo: ReviewRepository,
                 config_creator: JsonConfigManager):
        self.review_repo = review_repo
        self.config_creator = config_creator

    def execute(self, index: int) -> tuple[str, str, int]:
        return self.review_repo.get_by_index(index)
