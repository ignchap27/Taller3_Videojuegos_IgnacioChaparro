from src.engine.services.images_service import ImagesService
from src.engine.services.sounds_service import SoundService


class ServiceLocator:
    images_service = ImagesService()
    sounds_service = SoundService()