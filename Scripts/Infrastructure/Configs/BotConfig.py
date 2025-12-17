import os
from dotenv import load_dotenv

from Scripts.Application.Interfaces.TechConfigRepository import TechConfigRepository
from Scripts.Infrastructure.Services.ProjectPathFinder import ProjectPathFinder


class BotConfig(TechConfigRepository):
    def __init__(self, path_finder: ProjectPathFinder):
        self.env_path = path_finder.env_path
        load_dotenv(dotenv_path=self.env_path)

        self.__bot_token = os.getenv("BOT_KEY")
        self.__password = os.getenv("ADMIN_PASSWORD")

    def get_bot_token(self) -> str:
        return self.__bot_token

    def get_admin_password(self) -> str:
        return self.__password

    def change_password(self, new_password: str) -> bool:
        try:
            with open(self.env_path, 'r') as f:
                lines = f.readlines()

            with open(self.env_path, 'w') as f:
                for line in lines:
                    if line.startswith('ADMIN_PASSWORD='):
                        f.write(f'ADMIN_PASSWORD={new_password}\n')
                    else:
                        f.write(line)

            self.__password = new_password
            load_dotenv(dotenv_path=self.env_path, override=True)
            return True

        except Exception as e:
            print(f"Ошибка смены пароля: {e}")
            return False