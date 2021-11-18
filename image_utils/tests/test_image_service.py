import pytest
from ..local_image_service import LocalImageUploadService
from fastapi import UploadFile
from settings_config import get_settings


class TestImageService:
    image_service = LocalImageUploadService()

    @pytest.mark.asyncio
    async def test_write_file(self, tmpdir_factory):
        base_temp = tmpdir_factory.getbasetemp()  # '/.../fastapi_blog/image_utils/tests',
        await self.image_service.write_file(file=UploadFile(get_settings().test_image_path), folder=str(base_temp),
                                            filename='os11.jpeg')

    @pytest.mark.asyncio
    async def test_failure_delete_file(self, tmpdir_factory):
        base_temp = tmpdir_factory.getbasetemp()  # '/.../fastapi_blog/image_utils/tests'
        with pytest.raises(OSError) as error:
            await self.image_service.delete_image(folder=str(base_temp), filename='osa11.jpeg')
        assert str(error.value) == 'Image not found in directory'

    @pytest.mark.asyncio
    async def test_get_file(self, tmpdir_factory):
        base_temp = tmpdir_factory.getbasetemp()  # '/.../fastapi_blog/image_utils/tests'
        await self.image_service.read_file(filename='os11.jpeg', folder=str(base_temp))

    @pytest.mark.asyncio
    async def test_successful_delete_file(self, tmpdir_factory):
        base_temp = tmpdir_factory.getbasetemp()  # '/.../fastapi_blog/image_utils/tests'
        await self.image_service.delete_image(folder=str(base_temp), filename='os11.jpeg')
