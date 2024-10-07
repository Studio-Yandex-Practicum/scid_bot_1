import csv
import io

import aiohttp
from aiogram import Router

# Cоздание маршрутизатора
# __name__ - для идентификации в логировании
router = Router(name=__name__)
