import os

import allure
from allure_commons.types import AttachmentType

from pages.registration_page import RegistrationPage



def add_screenshot(browser):
    png = browser.driver.get_screenshot_as_png()
    allure.attach(body=png, name='screenshot', attachment_type=AttachmentType.PNG, extension='.png')


def add_logs(browser):
    log = "".join(f'{text}\n' for text in browser.driver.get_log(log_type='browser'))
    allure.attach(log, 'browser_logs', AttachmentType.TEXT, '.log')


def add_html(browser):
    html = browser.driver.page_source
    allure.attach(html, 'page_source', AttachmentType.HTML, '.html')

def add_video():
    video_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     '../resources/output.mp4'))
    with open(video_path, "rb") as video_file:
        allure.attach(video_file.read(), name="video", attachment_type=allure.attachment_type.MP4)