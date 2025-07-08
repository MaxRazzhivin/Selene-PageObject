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

## Добавил в тест аллюр разметку с отчетами и файлами

```bash
- запуск через pytest tests/test_page_object.py
- посмотреть отчет через allure serve allure-results
```

## Добавление CI Github Actions 

```bash
1) Создаем в корне проекта папку .github -> в ней папку workflows
2) Создаем файлик test.yaml внутри workflows
3) Контент для .yaml файла - просто рабочий файл здесь размещу, надеюсь дальше хватит копирования его

name: Test

on:
  push:
    branches:
      - "main"
  workflow_dispatch:
    inputs:
       browser:
         description: 'Browser to use'
         required: false
         default: 'chrome'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Install ffmpeg
        run: sudo apt update && sudo apt install -y ffmpeg

      - name: Run tests
        run: pytest --alluredir=allure-results

      - name: Checkout gh-pages
        uses: actions/checkout@v2
        if: always()
        with:
          ref: gh-pages
          path: gh-pages

      - name: Allure Report action
        uses: simple-elf/allure-report-action@master
        if: always()
        with:
          allure_results: allure-results
          allure_history: allure-history
          keep_reports: 20

      - name: Deploy report to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        if: always()
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_branch: gh-pages
          publish_dir: allure-history

4) надо создать отдельную ветку, команды:
  git checkout --orphan gh-pages
  rm -rf ./*
  echo "Allure Reports" > README.md
  git add .
  git commit -m "init gh-pages"
  git push origin gh-pages
  
  Затем вернуться на свою ветку 
  git checkout main
  
5)  Включить разрешение на push из Actions
	1.	Перейди в:
GitHub → Repository → Settings → Actions → General
	2.	Найди блок:
Workflow permissions
	3.	Выбери:
✅ Read and write permissions
(по умолчанию стоит “Read-only”)
	4.	Нажми Save
 

```