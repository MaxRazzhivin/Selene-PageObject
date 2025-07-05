# Подход PageObject

## Подход Page Object (POM — Page Object Model) — это один из самых мощных и широко используемых архитектурных шаблонов в автоматизации UI-тестирования.

```bash
Page Object — это шаблон проектирования, в котором каждая страница сайта представляется 
как отдельный класс, и в нем инкапсулируются:

	🔹 локаторы элементов;
	🔹 действия с этими элементами;
	🔹 логика валидации.
```

```bash
Преимущества:

✅ Повторное использование - методы страниц можно вызывать в разных тестах
✅ Чистые тесты - тесты читаются как сценарии, не как скрипты
✅ Упрощение поддержки - изменился селектор → меняешь в одном месте
✅ Инкапсуляция логики - можно добавить логику валидации прямо в PageObject
✅ Разделение ответственности - тесты проверяют бизнес-логику, а не детали реализации

```

```bash
Был тест в одном месте следующего вида:

    browser.element('#firstName').type('Max')
    browser.element('#lastName').type('Razzhivin')
    browser.element('#userEmail').type('max.nvo06@gmail.com')
    browser.all('[name=gender]').element_by(have.value('Male')).element("..").click()
    browser.element('#userNumber').type('9094618666')
    
Выносим техническую информацию в папку pages и файл registration_page:

    class RegistrationPage:
    

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
            
            
Далее в файле с тестом создаем объект для класса и вызываем через него функции, спрятав технические детали: 

def test_complete_do():
    registration_page = RegistrationPage()

    registration_page.fill_first_name('Max')
    registration_page.fill_last_name('Razzhivin')
    registration_page.fill_email('max.nvo06@gmail.com')
    registration_page.fill_gender('Male')

    registration_page.fill_user_number('9094618666')
```
