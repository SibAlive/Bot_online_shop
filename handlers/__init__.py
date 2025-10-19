from aiogram import Router

from .admin import admin_router
from .other import other_router
from .settings import settings_router
from .user import user_router
from .moderator import moderator_router


router = Router()
router.include_routers(
settings_router,
    admin_router,
    moderator_router,
    user_router,
    other_router
    )