import aiofiles
import zipfile
import random
import os
import math
import shutil
from cryptography.fernet import Fernet
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from typing import Union


class HandleFile:
    def _rename_file(self, filename: str):
        _, file_extension = os.path.splitext(filename)
        filename = f'easy_split-{random.getrandbits(32)}{file_extension}'
        return filename

    async def _clip_video(self, key: bytes, file_path: str, clip_file_path, start, end):
        await self.decrypt(key=key, target=file_path)
        ffmpeg_extract_subclip(filename=file_path, t1=start,
                               t2=end, targetname=clip_file_path)
        await self.encrypt(key=key, target=file_path)

    async def encrypt(self, target: str, contents: Union[bytes, None] = None, key: bytes = Fernet.generate_key()):
        if contents is None:
            async with aiofiles.open(target, 'rb') as encrypted_file:
                contents = await encrypted_file.read()
        f = Fernet(key=key)
        contents = f.encrypt(data=contents)
        async with aiofiles.open(target, 'wb') as encrypted_file:
            await encrypted_file.write(contents)
        return key

    async def decrypt(self, key: bytes, target: str):
        f = Fernet(key=key)
        async with aiofiles.open(target, 'rb') as encrypted_file:
            encrypted = await encrypted_file.read()
        decrypted = f.decrypt(encrypted)
        async with aiofiles.open(target, 'wb') as decrypted_file:
            await decrypted_file.write(decrypted)

    def zip_file(self, zip_file_path: str, target: str):
        filename = os.path.basename(p=target)
        zip_file = zipfile.ZipFile(file=zip_file_path, mode='a')
        zip_file.write(filename=target, arcname=filename,
                       compress_type=zipfile.ZIP_DEFLATED)
        zip_file.close()

    async def split_video(self, key_uploaded_file: bytes, upload_folder: str, out_folder: str, filename: str, file_path: str):
        # Create video instance | Get video duration | File name and extension
        await self.decrypt(key=key_uploaded_file, target=file_path)
        video = VideoFileClip(filename=file_path)
        await self.encrypt(key=key_uploaded_file, target=file_path)
        video_duration = video.duration
        filename, file_extension = os.path.splitext(filename)
        path_clips = []

        # Generate key to encrypt files
        key = Fernet.generate_key()

        # Zip file location
        zip_file_name = f'{filename}.zip'
        zip_file_path = os.path.join(upload_folder, zip_file_name)

        # To calculate, seconds to cut
        last_time_cut = 0
        for sec in range(1, math.ceil(video_duration) + 1):
            # Cutting video for each 30 seconds
            if sec % 30 == 0:
                if sec > video_duration:
                    sec = video_duration
                # Get file location
                clip_file_path = os.path.join(
                    out_folder, f'{filename}-[{last_time_cut}-{sec}]{file_extension}')

                # Clip video
                await self._clip_video(key=key_uploaded_file, file_path=file_path, clip_file_path=clip_file_path, start=last_time_cut, end=sec)
                # Encrypt video
                await self.encrypt(target=clip_file_path, key=key)

                path_clips.append(clip_file_path)

                if sec == video_duration:
                    last_time_cut = sec
                    break
                else:
                    last_time_cut = sec

        # Cutting seconds remaining
        if last_time_cut < video_duration:
            clip_file_path = os.path.join(
                out_folder, f'{filename}-[{last_time_cut}-{video_duration}]{file_extension}')
            await self._clip_video(key=key_uploaded_file, file_path=file_path, clip_file_path=clip_file_path, start=last_time_cut, end=video_duration)
            await self.encrypt(target=clip_file_path, key=key)
            path_clips.append(clip_file_path)

        # Remove file upload
        os.remove(path=file_path)

        # Zip video
        for clip_path in path_clips:
            await self.decrypt(key=key, target=clip_path)
            self.zip_file(zip_file_path=zip_file_path, target=clip_path)
            await self.encrypt(key=key, target=clip_path)
            os.remove(path=clip_path)

        # Remove out folder
        shutil.rmtree(out_folder)

        return zip_file_path, zip_file_name


handle_file = HandleFile()
