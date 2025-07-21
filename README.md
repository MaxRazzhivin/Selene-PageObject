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
  
5) Включить разрешение на push из Actions
	1.	Перейди в:
GitHub → Repository → Settings → Actions → General
	2.	Найди блок:
Workflow permissions
	3.	Выбери:
✅ Read and write permissions
(по умолчанию стоит “Read-only”)
	4.	Нажми Save
 

```

## Подключение библиотеки Pydantic 

```bash
Pydantic помогает создавать, проверять и преобразовывать данные (в том числе ввод пользователя, JSON и т. д.) 
с минимальными усилиями. Она делает это, используя типизацию Python’а (str, int, float, list, и т.д.).

Представь, что Pydantic — это строгий контролёр на входе в систему: он проверяет, что все данные 
пришли в нужном виде, и если что-то не так — сразу говорит об этом, с точной диагностикой.
```

```bash
✅ Что именно делает Pydantic?
	1.	Валидация входных данных
	  •	Преобразует типы ("123" → 123)
	  •	Проверяет допустимость (age не может быть "abc")
	  
	2.	Автоматическое приведение типов
	  •	BaseModel(name="John", age="25") — age автоматически станет int.
	  
	3.	Поддержка вложенных структур
	  •	Можно описывать сложные модели с вложенными объектами и списками.
	  
	4.	Работа с JSON
	  •	Легко сериализует/десериализует данные из JSON и обратно.
	  
	5.	Поддержка IDE и автодополнения
	  •	Благодаря аннотациям типов, редакторы типа PyCharm подсказывают структуру данных.
```

```bash

from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

# Пример использования
user = User(name="Alice", age="30", email="alice@example.com")
print(user.age)  # 30 — уже как int

# Ошибка: age — не число
user = User(name="Bob", age="тридцать", email="bob@example.com")
# ValidationError: value is not a valid integer
```

```bash
Установка pydantic

pip install pydantic
либо 
from pydantic import BaseModel

pip install pydantic-settings
либо 
from pydantic_settings import BaseSettings

```

```bash
Добавляем в requirements.txt 

pydantic>=2.0
```

```bash
Проверить версию pydantic можно через 

print(pydantic.__version__)
```

```bash
Установка pydantic через poetry

poetry add pydantic
```

```bash
Что изменяет для нас в жизни pydantic: 

Было в файле conftest ряд опций, которые передавали через переменные среды,
т.е. могли при запуске теста указать кастомно какой-то из них в консоли:

env -S "driver_name=firefox timeout=4.0" pytest tests

    browser.config.window_height = os.getenv('window_height', 1800)
    browser.config.window_width = os.getenv('window_width', 1169)
    browser.config.base_url = os.getenv('base_url', 'https://demoqa.com')
    browser.config.timeout = float(os.getenv('timeout', '4'))
    browser.config.driver_name = os.getenv('driver_name', 'chrome')
    browser.config.hold_driver_at_exit = (
      os.getenv('hold_driver_at_exit', false).lower() == 'true'
    ) 

Теперь в начале пишем: 

import pydantic
import pydantic_settings

Далее определяем класс для собственных опций, например Config

class Config(pydantic_settings.BaseSettings):
    base_url: str = 'https://demoqa.com'
    driver_name: str = 'chrome'
    hold_driver_at_exit: bool = False
    window_width: int = 1169
    window_height: int = 1800
    timeout: float = 4.0
    
    
Создаем объект этого класса: 

config = Config()

И можно сделать рефакторинг настроек в conftest:

    browser.config.window_height = config.window_height
    browser.config.window_width = config.window_width
    browser.config.base_url = config.base_url
    browser.config.timeout = config.timeout
    browser.config.driver_name = config.driver_name
    browser.config.hold_driver_at_exit = config.hold_driver_at_exit
    ) 
      
      
      
В дальнейшем для конфига этого принято создавать файлик отдельный config.py и в него выносить: 


```

```bash
Env-файлы для установки настроек заранее через файл, а не консоль

1) Устанавливаем пакет python-dotenv

2) Создаем в корне проекта файл .env 
Переменные среды будут созданы из этого файла

3) В conftest дописываем import dotenv 

4) внутри функции-фикстуры дописываем 

dotenv.load_dotenv()



```