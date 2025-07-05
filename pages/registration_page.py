import os
import sys

from selene.support.shared import browser
from selene import have, by, be, command
from selenium.webdriver import Keys


class RegistrationPage:
    def __init__(self):
        self.path_to_image = os.path.abspath("../resources/picta.png")
        self.date_of_birth_field = browser.element('#dateOfBirthInput')
        self.all_hobbies_field = browser.all('.custom-checkbox')
        self.state_field = browser.element('#state')

    def open(self):
        browser.open('/automation-practice-form')

        # Удаляем рекламу

        browser.driver.execute_script("""
            $('[id*=google_ads_iframe]').remove()
            $('#RightSide_Advertisement').remove();
            $('#fixedban').remove();
            $('footer').remove();
        """)

    def fill_first_name(self, value):
        browser.element('#firstName').type(value)

    def fill_last_name(self, value):
        browser.element('#lastName').type(value)

    def fill_email(self, value):
        browser.element('#userEmail').type(value)

    def fill_gender(self, value):
        browser.all('[name=gender]').element_by(have.value(value)).element("..").click()

    def fill_user_number(self, value):
        browser.element('#userNumber').type(value)

    def fill_date_of_birth(self, year, month, day):
        # browser.element('#dateOfBirth').click()
        # browser.element('.react-datepicker__month-select').type(month)
        # browser.element('.react-datepicker__year-select').type(year)
        # browser.element(f'.react-datepicker__day--0{day}').click()

        # На случай когда дата закешировалась и уже введена до нас другая

        self.date_of_birth_field.send_keys(
            Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL, 'a', Keys.DELETE
        ).type(f'{day}{month}{year}').press_enter()

    def fill_subjects(self, value):
        browser.element('#subjectsInput').type(value).press_tab()

    def fill_hobbies(self, value1, value2):
        self.all_hobbies_field.element_by(have.exact_text(value1)).click()
        self.all_hobbies_field.element_by(have.exact_text(value2)).click()

    def fill_image(self):
        browser.element('#uploadPicture').send_keys(self.path_to_image)

    def fill_address(self, value):
        browser.element('#currentAddress').click().type(value)

    def fill_state(self, value):
        # Добавил скролл для маленьких экранов до элемента
        self.state_field.perform(command.js.scroll_into_view)
        self.state_field.click().element(by.text(value)).click()

    def fill_city(self, value):
        browser.element('#city').click().element(by.text(value)).click()

    def submit(self):
        browser.element('#submit').perform(command.js.click)

    def should_registered_user_with(self, full_name, email, gender, mobile, date_of_birth, subject, hobbies, image_name, address,
                                    state_city):
        browser.element(".table").all('td').even.should(
            have.exact_texts(
                "Max Razzhivin",
                "max.nvo06@gmail.com",
                'Male',
                '9094618666',
                '06 April,1989',
                'Computer Science',
                'Sports, Reading',
                'picta.png',
                'somewhere in galaxy',
                'NCR Delhi',
        ))

    def button_close_should_be_clickable(self):
        browser.element('#closeLargeModal').should(be.clickable)


