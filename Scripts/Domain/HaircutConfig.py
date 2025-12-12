from dataclasses import dataclass


@dataclass
class HaircutConfig:
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