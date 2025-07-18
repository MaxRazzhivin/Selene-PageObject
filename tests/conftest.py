import platform

import pytest

from selenium import webdriver
import subprocess
import time
from selene import browser
import os

from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.service import Service

from utils import attach


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    browser.config.window_height = os.getenv('window_height', 1800)
    browser.config.window_width = os.getenv('window_width', 1169)
    browser.config.base_url = os.getenv('base_url', 'https://demoqa.com')
    browser.config.timeout = float(os.getenv('timeout', '4'))

    driver_options = webdriver.ChromeOptions()

    if os.getenv('CI'):
        driver_options.add_argument(
            '--headless=new')  # обязательно 'new' для последних версий Chrome
        driver_options.add_argument('--no-sandbox')
        driver_options.add_argument('--disable-dev-shm-usage')

        # Указание пути к ChromeDriver вручную
        service = Service(executable_path='/usr/local/bin/chromedriver')
        browser.config.driver = webdriver.Chrome(service=service,
                                                 options=driver_options)

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
