from .image_utils_interface import FileServiceInterface
from fastapi import UploadFile
import aiofiles
from pathlib import Path


class LocalImageUploadService(FileServiceInterface):

    async def write_file(self, file: UploadFile, folder: str, filename: str, **kwargs):
        path_to_images = f'{folder}/{filename}'
        async with aiofiles.open(path_to_images, mode='wb') as f:
            content = await file.read()
            await f.write(content)

    async def read_file(self, filename: str, folder: str, **kwargs):
        url = str(folder) + '/' + filename
        async with aiofiles.open(url, mode='rb') as f:
            obj = await f.read()
        return obj

    async def delete_image(self, folder: str, filename: str, **kwargs):
        file = Path(str(folder) + '/' + filename)
        try:
            file.unlink()
        except OSError as error:
            raise OSError('Image not found in directory')
            # handle error
