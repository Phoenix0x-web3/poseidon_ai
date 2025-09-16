import sys

from libs.eth_async.classes import Singleton
from data.config import SETTINGS_FILE
from data.config import LOG_FILE, SETTINGS_FILE
from loguru import logger
import yaml


class Settings(Singleton):
    def __init__(self):
        with open(SETTINGS_FILE, 'r') as file:
            json_data = yaml.safe_load(file) or {}

        self.check_git_updates = json_data.get("check_git_updates", True)
        self.threads = json_data.get("threads", 4)
        self.range_wallets_to_run = json_data.get("range_wallets_to_run", [])
        self.exact_wallets_to_run = json_data.get("exact_wallets_to_run", [])
        self.shuffle_wallets = json_data.get("shuffle_wallets", True)
        self.show_email_in_logs = json_data.get("show_email_in_logs", True)
        self.log_level = json_data.get("log_level", "INFO")
        self.random_pause_start_wallet_min = json_data.get("random_pause_start_wallet", {}).get("min")
        self.random_pause_start_wallet_max = json_data.get("random_pause_start_wallet", {}).get("max")
        self.random_pause_between_wallets_min = json_data.get("random_pause_between_wallets",{}).get("min")
        self.random_pause_between_wallets_max = json_data.get("random_pause_between_wallets", {}).get("max")
        self.random_pause_between_actions_min = json_data.get("random_pause_between_actions", {}).get("min")
        self.random_pause_between_actions_max = json_data.get("random_pause_between_actions", {}).get("max")
        self.random_pause_wallet_after_completion_min = json_data.get("random_pause_wallet_after_completion", {}).get('min')
        self.random_pause_wallet_after_completion_max = json_data.get("random_pause_wallet_after_completion", {}).get('max')

        self.games_min = json_data.get("games", {}).get('min')
        self.games_max = json_data.get("games", {}).get('max')

        self.eleven_labs_api_key = json_data.get("eleven_labs_api_key", "")
        self.capmonster_api_key = json_data.get("capmonster_api_key", "")
        self.headless_mode = json_data.get("headless_mode", False)

        self.invite_codes = json_data.get("invite_codes", [])
        self.only_settings_invite_codes = json_data.get("only_settings_invite_codes", False)
        self.tg_bot_id = json_data.get("tg_bot_id", "")
        self.tg_user_id = json_data.get("tg_user_id", "")
        self.retry = json_data.get("retry", 3)


# Configure the logger based on the settings
settings = Settings()

if settings.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
    raise ValueError(f"Invalid log level: {settings.log_level}. Must be one of: DEBUG, INFO, WARNING, ERROR")
logger.remove()  # Remove the default logger
logger.add(sys.stderr, level=settings.log_level)

logger.add(LOG_FILE, level="DEBUG")
