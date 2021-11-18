from abc import ABC, abstractmethod
from fastapi import UploadFile


class FileServiceInterface(ABC):
    """
     - file: bytes => file to upload;
     - folder: str => folder on local machine || bucket name on aws s3 or yandex storage
     - filename: str => file name 'images/example.jpg'
     - kwargs => for other attributes
    """

    @abstractmethod
    async def write_file(self, file: UploadFile, folder: str, filename: str, **kwargs): pass

    @abstractmethod
    async def read_file(self, folder: str, filename: str, **kwargs): pass

    @abstractmethod
    async def delete_image(self, folder: str, filename: str, **kwargs): pass


# ~ ex

# s3_client.upload_fileobj(file_obj, bucket, f"{folder}/{object_name}")
# s3_client.download_file('mybucket', 'hello.txt', '/tmp/hello.txt')
# s3_client.delete_object(Bucket='string',
# Key='string',
# MFA='string',
# VersionId='string',
# RequestPayer='requester',
# BypassGovernanceRetention=True|False,
# ExpectedBucketOwner='string')
