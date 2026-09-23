import os
import shutil
from abc import ABC, abstractmethod
from fastapi import UploadFile
from pathlib import Path
from app.core.config import settings

class StorageBackend(ABC):
    @abstractmethod
    async def save_upload(self, file: UploadFile, dest_filename: str) -> str:
        pass

class LocalStorageBackend(StorageBackend):
    def __init__(self, base_path: str = "/app/storage"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
    async def save_upload(self, file: UploadFile, dest_filename: str) -> str:
        dest_path = self.base_path / dest_filename
        
        # Write chunks to disk
        with open(dest_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024 * 5): # 5MB chunks
                buffer.write(chunk)
                
        return str(dest_path)

# Easy to swap to MinIO/S3 by changing this instantiation later
storage_backend = LocalStorageBackend(base_path=settings.STORAGE_BUCKET)
