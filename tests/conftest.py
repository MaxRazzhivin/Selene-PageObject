import platform

import pydantic
import pydantic_settings

import pytest

from selenium import webdriver
import subprocess
import time
from selene import browser
import os

from utils import attach

class Config(pydantic_settings.BaseSettings):
    base_url: str = 'https://demoqa.com'
    driver_name: str = 'chrome'
    hold_driver_at_exit: bool = False
    window_width: int = 1169
    window_height: int = 1800
    timeout: float = 4.0

config = Config()

@pytest.fixture(scope='function', autouse=True)
def browser_management():
    browser.config.window_height = config.window_height
    browser.config.window_width = config.window_width
    browser.config.base_url = config.base_url
    browser.config.timeout = config.timeout

    driver_options = webdriver.ChromeOptions()

    if os.getenv('CI'):
        driver_options.add_argument(
            '--headless=new')  # обязательно 'new' для последних версий Chrome
        driver_options.add_argument('--no-sandbox')
        driver_options.add_argument('--disable-dev-shm-usage')

        browser.config.driver = webdriver.Chrome(options=driver_options)

    browser.config.driver_options = driver_options


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
            '-i', '3',  # входной сигнал (дисплей) / 3 - без внешнего экрана
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