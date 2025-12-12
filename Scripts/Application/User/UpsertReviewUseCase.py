from Scripts.Application.Interfaces.ReviewRepository import ReviewRepository


class UpsertReviewUseCase:
    def __init__(self, review_repo: ReviewRepository):
        self.review_repo = review_repo

    def execute(self, user_id: int, username: str, text_review: str, estimation: int):
        self.review_repo.upsert(user_id, username, text_review, estimation)