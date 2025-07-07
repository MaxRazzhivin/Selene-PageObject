from pages.registration_page import RegistrationPage


def test_complete_do():
    # GIVEN:
    registration_page = RegistrationPage()
    registration_page.open()

    # WHEN
    registration_page.fill_first_name('Max')
    registration_page.fill_last_name('Razzhivin')
    registration_page.fill_email('max.nvo06@gmail.com')
    registration_page.fill_gender('Male')

    registration_page.fill_user_number('9094618666')

    # Выбираем дату рождения:
    registration_page.fill_date_of_birth('1989', 'Apr', '06')

    # Предметы
    registration_page.fill_subjects('Computer Science')


    # Хобби
    registration_page.fill_hobbies('Sports', 'Reading')

    registration_page.fill_image()

    registration_page.fill_address('somewhere in galaxy')

    registration_page.fill_state('NCR')
    registration_page.fill_city('Delhi')

    registration_page.submit()

    # THEN
    registration_page.should_registered_user_with("Max Razzhivin",
            "max.nvo06@gmail.com",
            'Male',
            '9094618666',
            '06 April,1989',
            'Computer Science',
            'Sports, Reading',
            'picta.png',
            'somewhere in galaxy',
            'NCR Delhi',)

    registration_page.button_close_should_be_clickable()

