from aiogram import Router, F, types

# Cоздание маршрутизатора
# __name__ - для идентификации в логировании
router = Router(name=__name__)

any_media_filter = F.photo | F.video | F.document
