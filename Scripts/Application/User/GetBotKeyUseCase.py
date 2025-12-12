from Scripts.Application.Interfaces.TechConfigRepository import TechConfigRepository


class GetBotKeyUseCase:
    def __init__(self,
                 tech_config_repo: TechConfigRepository):
        self.tech_config_repo = tech_config_repo

    def execute(self) -> str:
        return self.tech_config_repo.get_bot_token()
