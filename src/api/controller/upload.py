import magic
import os
import tempfile
import shutil
from utils.handle_file import handle_file


class ControllerUpload:
    _allowed = ['ISO Media, MP4 v2 [ISO 14496-14]']
    _max_file_size = 500 * 1048576  # 500Mb to bytes

    def _create_upload_folder(self):
        tmp_dir = tempfile.mkdtemp()
        out_folder_location = self._create_out_folder(upload_folder=tmp_dir)
        return tmp_dir, out_folder_location

    def _create_out_folder(self, upload_folder):
        out_folder_location = os.path.join(upload_folder, 'out')
        already_exist_out_folder = os.path.exists(out_folder_location)
        if not already_exist_out_folder:
            os.mkdir(out_folder_location)
        return out_folder_location

    def is_valid_file(self, contents: bytes) -> bool:
        type = magic.from_buffer(buffer=contents)
        for allowed_type in self._allowed:
            if type == allowed_type:
                return True
        return False

    def is_valid_size(self, contents: bytes) -> bool:
        size = len(contents)
        if size > self._max_file_size:
            return False
        return True

    async def save(self, filename: str, contents: bytes):
        upload_folder, out_folder_location = self._create_upload_folder()
        filename = handle_file._rename_file(filename=filename)
        file_path = os.path.join(upload_folder, filename)
        key = await handle_file.encrypt(target=file_path, contents=contents)
        info = {
            'upload_folder': upload_folder,
            'out_folder': out_folder_location,
            'filename': filename,
            'file_path': file_path,
            'key': key
        }
        return info

    def remove(self, upload_folder: str):
        if os.path.exists(upload_folder):
            shutil.rmtree(upload_folder)

    def download(self, upload_folder: str, file_path: str):
        if os.path.exists(file_path):
            pass
        self.remove(upload_folder=upload_folder)


controller_uploader = ControllerUpload()
