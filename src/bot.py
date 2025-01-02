import logging
import platform
import sys

import disnake
from disnake.ext import commands

from src.config import CONFIG

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s: | %(levelname)s: %(message)s")


class Bot(commands.InteractionBot):
    def __init__(self):
        self.config = CONFIG
        self.logger = logging

        super().__init__(test_guilds=self.config["test_guilds"])

    def load_extensions(self, path):
        loaded_exts_count = 0

        for ext in disnake.utils.search_directory(path):
            try:
                self.load_extension(ext)
                self.logger.info(f"Loaded extension: {ext}")
                loaded_exts_count += 1
            except Exception as exception:
                self.logger.info(f"{type(exception).__name__}: {exception}")

            self.logger.info(
                f'{loaded_exts_count} extension(s) loaded'
            )

    async def on_connect(self):
        self.logger.info(f"Connected to {len(self.guilds)} guilds")
        self.logger.info(f"Using Disnake version {disnake.__version__}")
        self.logger.info(f"Using Python version {sys.version}")
        self.logger.info(
            f"Using Platform {platform.system()} {platform.release()}")
        self.logger.info(
            f"Successfully logged in as {self.user} (ID: {self.user.id})")

    def main(self):
        self.load_extensions("src/exts")
        self.run(CONFIG["token"])
