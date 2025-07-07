import pytest
from selenium import webdriver
import subprocess
import time
from selene import browser
import os


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    browser.config.window_height = os.getenv('window_height', 1800)
    browser.config.window_width = os.getenv('window_width', 1169)
    browser.config.base_url = os.getenv('base_url', 'https://demoqa.com')
    browser.config.timeout = float(os.getenv('timeout', '4'))
    driver_options = webdriver.ChromeOptions()
    browser.config.driver_options = driver_options


    # Функция для начала записи видео
    def start_recording():
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
            'output.mp4'  # имя выходного файла
        ]
        return subprocess.Popen(command)

    # Начало записи
    video_process = start_recording()
    time.sleep(2)  # Небольшая задержка для начала записи


    yield

    # Функция для остановки записи видео
    def stop_recording(process):
        process.terminate()  # Остановить процесс ffmpeg

    # Остановка записи
    stop_recording(video_process)

    browser.quit()
