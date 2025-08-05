import requests
import os
import time
from datetime import datetime
import hashlib

class YandexDiskUpdater:
    def __init__(self, public_link, save_path="downloaded_file.xlsx", check_interval=300):
        self.public_link = public_link
        self.save_path = save_path
        self.check_interval = check_interval
        self.last_hash = None

    def get_file_hash(self, file_path):
        """Вычисляет хеш файла для обнаружения изменений"""
        if not os.path.exists(file_path):
            return None
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def download_file(self):
        """Скачивает файл с Яндекс.Диска"""
        try:
            # Получаем временную ссылку
            api_url = f"https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={self.public_link}"
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()

            download_url = response.json().get("href")
            if not download_url:
                print(f"[{datetime.now()}] Не удалось получить ссылку для скачивания")
                return False

            # Скачиваем файл
            file_response = requests.get(download_url, timeout=30)
            file_response.raise_for_status()

            # Проверяем изменился ли файл
            new_hash = hashlib.md5(file_response.content).hexdigest()
            if new_hash == self.last_hash:
                print(f"[{datetime.now()}] Файл не изменился")
                return False

            # Сохраняем новый файл
            with open(self.save_path, "wb") as f:
                f.write(file_response.content)

            self.last_hash = new_hash
            print(f"[{datetime.now()}] Файл успешно обновлён: {os.path.abspath(self.save_path)}")
            return True

        except Exception as e:
            print(f"[{datetime.now()}] Ошибка: {str(e)}")
            return False

    def run(self):
        """Запускает бесконечный цикл проверки обновлений"""
        print(f"Запуск монитора для {self.public_link}")

        # Первоначальная загрузка
        self.download_file()

        # Бесконечный цикл проверки
        while True:
            time.sleep(self.check_interval)
            self.download_file()


if __name__ == "__main__":

    # Настройки
    YANDEX_LINK = "https://disk.yandex.ru/i/xQPNW_-SjGvwOQ"
    SAVE_PATH = "BaseYandex.xlsx" #Имя файла
    CHECK_EVERY_MINUTES = 60   #Проверять каждые:
    # Создаем и запускаем монитор
    updater = YandexDiskUpdater(
        public_link=YANDEX_LINK,
        save_path=SAVE_PATH,
        check_interval=CHECK_EVERY_MINUTES * 1      #Проверять каждые:
    )

    try:
        updater.run()
    except KeyboardInterrupt:
        print("Мониторинг остановлен")
