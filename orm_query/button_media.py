from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from enums.keyboard_button import KeyboardButton
from models.button_media import ButtonMediaDTO, ButtonMedia


class ButtonMediaRepository:

    @staticmethod
    async def get_by_button(button: KeyboardButton, session: AsyncSession) -> ButtonMediaDTO:
        query = select(ButtonMedia).where(ButtonMedia.button == button)
        button_media = await session.execute(query)
        return ButtonMediaDTO.model_validate(button_media.scalar_one(), from_attributes=True)

