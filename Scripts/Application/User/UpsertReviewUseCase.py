from Scripts.Infrastructure.Database.UserRequests.ReviewRequests import SqliteReviewRequests

from Scripts.Application.Interfaces.ReviewRepository import ReviewRepository
from Scripts.Infrastructure.Services.JsonConfigManager import JsonConfigManager


class UpsertReviewUseCase:
    def __init__(self,
                 review_repo: ReviewRepository,
                 config_creator: JsonConfigManager):
        self.review_repo = review_repo
        self.config_creator = config_creator

    def execute(self, user_id: int, username: str, text_review: str, estimation: int):
        self.review_repo.upsert(user_id, username, text_review, estimation)