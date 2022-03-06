#carregando as variáveis de ambiente especificadas no arquivo .env

import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

BASE_API_URL = os.getenv("BASE_API_URL")

KEY_API_VAGALUME = os.getenv("KEY_API_VAGALUME")