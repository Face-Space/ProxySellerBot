from aiogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAnimation


class MediaService:

    @staticmethod
    def convert_to_media(media_id: str, caption: str) -> InputMediaPhoto | InputMediaVideo | InputMediaAnimation:
        category_media_type = media_id[0]
        category_media_id = media_id[1:]
        if category_media_type == "0":
            media = InputMediaPhoto(media=category_media_id, caption=caption)
        elif category_media_type == "1":
            media = InputMediaVideo(media=category_media_id, caption=caption)
        else:
            media = InputMediaAnimation(media=category_media_id, caption=caption)
        return media