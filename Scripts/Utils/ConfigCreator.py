import logging
import os
import json
from dataclasses import dataclass, asdict
from typing import Optional, Any
from Scripts.Utils.ProjectPathFinder import ProjectPathFinder

class ConfigCreator:
    def __init__(self, path_finder: ProjectPathFinder):
        self.path_finder = path_finder
        self.configs_dir = self.path_finder.get_project_path() / "Configs"
        self.configs_dir.mkdir(exist_ok=True)
        self._config: Optional[Config] = None

        self.setup_logging()
        self.load_or_create_config()

    def setup_logging(self):
        self.root_logger = logging.getLogger()
        self.root_logger.setLevel(logging.INFO)


        if self.root_logger.handlers:
            return

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        app_log_file = self.configs_dir / "app.log"
        self.app_handler = logging.FileHandler(app_log_file, encoding='utf-8')
        self.app_handler.setLevel(logging.INFO)
        self.app_handler.setFormatter(formatter)
        self.root_logger.addHandler(self.app_handler)

        error_log_file = self.configs_dir / "errors.log"
        self.error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
        self.error_handler.setLevel(logging.ERROR)
        self.error_handler.setFormatter(formatter)
        self.root_logger.addHandler(self.error_handler)

    def load_or_create_config(self):
        if os.path.exists(self.configs_dir / "config.json"):
            try:
                with open(self.configs_dir / "config.json", 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._config = Config(**data)
            except Exception as e:
                self.create_default_config()
        else:
            self.create_default_config()

    def create_default_config(self):
        self._config = Config(
            count_haircuts_to_free = 3,
            count_referral_haircuts_to_bonus = 3,
            coins_for_one_referral = 100,
            coins_for_free_haircut = 300
        )

        self.save_config()

    def save_config(self):
        config_file = self.configs_dir / "config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self._config), f, indent=4, ensure_ascii=False)
            
    def change_haircuts_to_free(self, count: int):
        if count < 0 or count > 50:
            raise ValueError("count must be between 0 and 50")

        self._config.count_haircuts_to_free = count
        self.save_config()

    def get_config_value(self, key: str) -> Any:
        return getattr(self._config, key)

@dataclass
class Config:
    count_haircuts_to_free: int = 0
    count_referral_haircuts_to_bonus: int = 0
    coins_for_one_referral: int = 0
    coins_for_free_haircut: int = 0

    def __post_init__(self):
        if self.count_haircuts_to_free < 0 or self.count_haircuts_to_free > 50:
            raise ValueError("count must be between 0 and 50")
        if self.count_referral_haircuts_to_bonus < 0 or self.count_referral_haircuts_to_bonus > 50:
            raise ValueError("count must be between 0 and 50")
        if self.coins_for_one_referral < 0 or self.coins_for_one_referral > 1000:
            raise ValueError("count must be between 0 and 1000")
        if self.coins_for_free_haircut < 0 or self.coins_for_free_haircut > 10000:
            raise ValueError("count must be between 0 and 10000")
