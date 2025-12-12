from Scripts.Application.Interfaces.ReviewRepository import ReviewRepository


class GetCountReviewsUseCase:
    def __init__(self,
                 review_repo: ReviewRepository):
        self.review_repo = review_repo

    def execute(self) -> int:
        return self.review_repo.get_count()
