from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.enums import UserRole
from bot.services import UserService


class LocaleFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery, translations: dict[[str, str]]):
        locales = list(translations.keys())
        if not isinstance(callback, CallbackQuery):
            raise ValueError(
                f"LocaleFilter: expected 'CallbackQuery', got {type(callback).__name__}"
            )
        return callback.data in locales


class ButtonCartFilter(BaseFilter):
    async def __call__(self, message: Message, i18n: dict):
        return message.text == i18n.get('button_cart')


class ButtonCategoryFilter(BaseFilter):
    async def __call__(self, message: Message, i18n: dict):
        return message.text == i18n.get('button_category')


class ButtonContactsFilter(BaseFilter):
    async def __call__(self, message: Message, i18n: dict):
        return message.text == i18n.get('button_contacts')


class IsDelItemCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, int]:
        if callback.data.endswith("_del"):
            product_id_to_delete = int(callback.data[:-4])
            return {'product_id_to_delete': product_id_to_delete}
        return False


class IsAnyCategoryCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool | dict[str, int]:
        if callback.data.startswith("category_"):
            category_id = int(callback.data.split('_')[1])
            return {'category_id': category_id}
        return False


class IsCorrectNameMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, str]:
        name = message.text.strip()
        if name.isalpha() and len(name) >= 2:
            return {'name': name}
        return False


class IsCorrectNumberMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, str]:
        phone = message.text.strip()
        if phone.isdigit() and phone.startswith('7') and len(phone) == 11:
            return {'phone': phone}
        return False


class UserRoleFilter(BaseFilter):
    def __init__(self, *roles: str | UserRole):
        if not roles:
            raise ValueError("At least one role must be provided to UserRoleFilter.")

        self.roles = frozenset(
            UserRole(role) if isinstance(role, str) else role
            for role in roles
            if isinstance(role, (str, UserRole))
        )

        if not self.roles:
            raise ValueError("No valid roles provided to `UserRoleFilter`.")

    async def __call__(self, event: Message | CallbackQuery, session: AsyncSession) -> bool:
        user = event.from_user
        if not user:
            return False

        user_service = UserService(session)
        role = await user_service.get_user_role(user_id=user.id)
        if role is None:
            return False

        return role in self.roles