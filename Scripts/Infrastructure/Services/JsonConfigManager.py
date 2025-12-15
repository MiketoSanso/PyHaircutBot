import os
import json
from dataclasses import asdict
from typing import Optional, Any
from Scripts.Application.Interfaces.HaircutConfigRepository import HaircutConfigRepository
from Scripts.Infrastructure.Configs.HaircutConfig import HaircutConfig
from Scripts.Infrastructure.Services.ProjectPathFinder import ProjectPathFinder

class JsonConfigManager(HaircutConfigRepository):
    def __init__(self, path_finder: ProjectPathFinder):
        self.path_finder = path_finder
        self.configs_dir = self.path_finder.configs_path
        self.configs_dir.mkdir(exist_ok=True)
        self._config: Optional[HaircutConfig] = None

        self.load_or_create_config()

    def load_or_create_config(self):
        if os.path.exists(self.configs_dir / "config.json"):
            try:
                with open(self.configs_dir / "config.json", 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._config = HaircutConfig(**data)
            except Exception as e:
                self.create_default_config()
        else:
            self.create_default_config()

    def create_default_config(self):
        self._config = HaircutConfig(
            count_haircuts_to_free = 3,
            count_ref_haircuts_to_bonus= 3,
            coins_for_referral= 100,
            coins_for_free_haircut = 300
        )

        self.save_config()

    def save_config(self):
        config_file = self.configs_dir / "config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self._config), f, indent=4, ensure_ascii=False)
            
    def change_haircuts_to_free(self, count: int) -> bool:
        if count < 0 or count > 50:
            return False

        self._config.count_haircuts_to_free = count
        self.save_config()
        return True

    def change_ref_haircuts_to_bonus(self, count: int)-> bool:
        if count < 0 or count > 50:
            return False

        self._config.count_ref_haircuts_to_bonus = count
        self.save_config()
        return True

    def change_coins_for_ref(self, count: int)-> bool:
        if count < 0 or count > 1000:
            return False

        self._config.coins_for_referral = count
        self.save_config()
        return True

    def change_coins_for_free_haircut(self, count: int) -> bool:
        if count < 0 or count > 10000:
            return False

        self._config.coins_for_free_haircut = count
        self.save_config()
        return True

    def get_config_value(self, key: str) -> Any:
        return getattr(self._config, key)