import platform
import tempfile

import dotenv

import pytest

from selenium import webdriver
import subprocess
import time
from selene import browser
import os

from config import Config

from utils import attach


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    dotenv.load_dotenv()
    config = Config()
    browser.config.window_height = config.window_height
    browser.config.window_width = config.window_width
    browser.config.base_url = config.base_url
    browser.config.timeout = config.timeout
    browser.config.driver_name = config.driver_name
    browser.config.hold_driver_at_exit = config.hold_driver_at_exit

    if os.getenv('CI'):
        if config.driver_name == 'chrome':
            options = webdriver.ChromeOptions()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")
            browser.config.driver_options = options

        elif config.driver_name == 'firefox':
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless')
            browser.config.driver_options = options


    # Функция для начала записи видео
    def start_recording():
        if platform.system() != 'Darwin':
            print("⚠️ ffmpeg-запись отключена: не macOS")
            return None
        command = [
            'ffmpeg',
            '-y',  # перезаписать файл без подтверждения
            '-f', 'avfoundation',  # захват экрана
            '-s', '1920x1440',  # размер экрана
            '-i', '5',  # входной сигнал (дисплей) / 3 - без внешнего экрана
            # 5 или 6 с внешним экраном
            # команда для получения номеров кодеков - ffmpeg -f avfoundation -list_devices true -i ""
            '-c:v', 'libx264',  # кодек
            '-preset', 'ultrafast',  # скорость кодирования
            os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         '../resources/output.mp4'))
        ]
        return subprocess.Popen(command)

    # Начало записи
    video_process = start_recording()
    time.sleep(2)  # Небольшая задержка для начала записи


    yield

    # Функция для остановки записи видео
    def stop_recording(process):
        if process:
            process.terminate()  # Остановить процесс ffmpeg

    # Остановка записи
    stop_recording(video_process)


    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video()

    browser.quit()