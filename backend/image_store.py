import os
from fastapi import APIRouter,UploadFile
from typing import List
import shutil

router = APIRouter()

@router.post('/upload_file', tags=['Profile_pic'])
async def upload_files(request: List[UploadFile] = None):
    file_backup_path = "./file_backup"
    # backupfiles_path = "./backupfiles"

    # Create the backupfiles directory if it doesn't exist
    os.makedirs(file_backup_path, exist_ok=True)
    # os.makedirs(backupfiles_path, exist_ok=True)

    # file_backup_len = len(os.listdir(file_backup_path))

    # if file_backup_len > 1:
    #     for filename in os.listdir(file_backup_path):
    #         source_path = os.path.join(file_backup_path, filename)
    #         destination_path = os.path.join(backupfiles_path, filename)
    #         shutil.move(source_path, destination_path)
    #     print(f"{file_backup_len} files moved to backupfiles folder")
    #     for filename in os.listdir(file_backup_path):
    #         file_path = os.path.join(file_backup_path, filename)
    #         os.remove(file_path)
    #     print("Files removed from file_backup folder")
    # Save new files in file_backup
    for data1 in request:
        filename = data1.filename
        file_path = os.path.join(file_backup_path, filename)
        try:
            with open(file_path, "wb") as f:
                shutil.copyfileobj(data1.file, f)
            print("File saved successfully")
        except Exception as e:
            print("Exception raised: ", e)
