from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "25831730"))
    API_HASH = getenv("API_HASH", "92474aac5af1b860d25e3b213a062332")
    BOT_TOKEN = getenv("BOT_TOKEN", "6734079442:AAGevJ3NspUmkTN6JT027Tyc83MZtmYBwkE")

config = Config()
