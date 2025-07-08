import os
import sys

import allure
from selene.support.shared import browser
from selene import have, by, be, command
from selenium.webdriver import Keys


class RegistrationPage:
    def __init__(self):
        self.path_to_image = os.path.abspath(
                os.path.join(os.path.dirname(__file__),
                             '../resources/picta.png'))
        self.date_of_birth_field = browser.element('#dateOfBirthInput')
        self.all_hobbies_field = browser.all('.custom-checkbox')
        self.state_field = browser.element('#state')

    @allure.step('Открываем браузер и удаляем рекламу')
    def open(self):
        browser.open('/automation-practice-form')

        # Удаляем рекламу

        browser.driver.execute_script("""
            $('[id*=google_ads_iframe]').remove()
            $('#RightSide_Advertisement').remove();
            $('#fixedban').remove();
            $('footer').remove();
        """)
    @allure.step('Заполняем имя: {value}')
    def fill_first_name(self, value):
        browser.element('#firstName').type(value)

    @allure.step('Заполняем фамилию: {value}')
    def fill_last_name(self, value):
        browser.element('#lastName').type(value)

    @allure.step('Заполняем почту: {value}')
    def fill_email(self, value):
        browser.element('#userEmail').type(value)

    @allure.step('Выбираем пол: {value}')
    def fill_gender(self, value):
        browser.all('[name=gender]').element_by(have.value(value)).element("..").click()

    @allure.step('Заполняем номер телефона: {value}')
    def fill_user_number(self, value):
        browser.element('#userNumber').type(value)

    @allure.step('Заполняем дату рождения: {year} {month} {day}')
    def fill_date_of_birth(self, year, month, day):
        # browser.element('#dateOfBirth').click()
        # browser.element('.react-datepicker__month-select').type(month)
        # browser.element('.react-datepicker__year-select').type(year)
        # browser.element(f'.react-datepicker__day--0{day}').click()

        # На случай когда дата закешировалась и уже введена до нас другая

        expected_value = f'{day} {month} {year}'
        is_mac = sys.platform == 'darwin'
        modifier = Keys.COMMAND if is_mac else Keys.CONTROL

        for attempt in range(3):
            self.date_of_birth_field.click()

            # Принудительно стереть поле через JS
            browser.driver.execute_script("arguments[0].value = '';",
                                          self.date_of_birth_field())

            # Отправить DELETE на всякий случай
            self.date_of_birth_field.send_keys(modifier, 'a', Keys.DELETE)

            # Ввести дату
            self.date_of_birth_field.type(expected_value).press_enter()

            # Проверка
            try:
                self.date_of_birth_field.should(have.value(expected_value))
                return
            except AssertionError:
                if attempt == 2:
                    raise AssertionError(
                        f"Дата не установлена как '{expected_value}'")

    @allure.step('Выбираем предметы: {value}')
    def fill_subjects(self, value):
        browser.element('#subjectsInput').type(value).press_enter()

    @allure.step('Выбираем хобби: {value1} {value2}')
    def fill_hobbies(self, value1, value2):
        self.all_hobbies_field.element_by(have.exact_text(value1)).click()
        self.all_hobbies_field.element_by(have.exact_text(value2)).click()

    @allure.step('Загружаем картинку')
    def fill_image(self):
        browser.element('#uploadPicture').set_value(
            self.path_to_image)

    @allure.step('Заполняем адрес: {value}')
    def fill_address(self, value):
        browser.element('#currentAddress').click().type(value)

    @allure.step('Выбираем штат: {value}')
    def fill_state(self, value):
        # Добавил скролл для маленьких экранов до элемента
        self.state_field.perform(command.js.scroll_into_view)
        self.state_field.click().element(by.text(value)).click()

    @allure.step('Выбираем город: {value}')
    def fill_city(self, value):
        browser.element('#city').click().element(by.text(value)).click()

    @allure.step('Нажимаем кнопку "submit"')
    def submit(self):
        browser.element('#submit').perform(command.js.click)

    @allure.step('Проверяем результаты формы')
    def should_registered_user_with(self, full_name, email, gender, mobile, date_of_birth, subject, hobbies, image_name, address,
                                    state_city):
        browser.element(".table").all('td').even.should(
            have.exact_texts(
                full_name,
                email,
                gender,
                mobile,
                date_of_birth,
                subject,
                hobbies,
                image_name,
                address,
                state_city,
        ))

    @allure.step('Закрываем окно с результатами')
    def button_close_should_be_clickable(self):
        browser.element('#closeLargeModal').should(be.clickable)


