# Бот для Telegram и VK на основе Dialogflow

Программа по реализации бота для условного онлайн-издательства, помогающего продвигать авторские блоги и публиковать книги.

Бот умеет отвечать на все типичные вопросы, а те что-то посложнее – перенаправляет на операторов.

По предварительной оценке, это на 70% сократит время ожидания ответа и на 90% повысит довольство жизнью сотрудников службы поддержки.

#### Пример результата для Telegram:

![demo_tg_bot](https://user-images.githubusercontent.com/99894266/197346997-9f2121c0-f1b1-4d48-b0c9-8e33fa84c8a1.gif)

#### Пример результата для ВКонтакте:

![demo_vk_bot](https://user-images.githubusercontent.com/99894266/197347013-d05f1e6c-f3c0-41f6-8da6-58387d7c25c1.gif)]

##### Примеры работающих ботов: *[Бот Telegram](https://t.me/SpacePhotoRussianSwordbot)*, *[Бот Vk](https://vk.com/write-215288801)*
<br>

### Что такое Dialogflow

[Dialogflow](https://dialogflow.cloud.google.com) — это платформа от Google для понимания естественного языка, которую можно использовать для создания омниканальных чат-ботов.

Если описать работу платформы несколькими фразами, то это выглядит примерно так. Dialogflow пытается распознать намерения пользователя на основе обучающих фраз, которые ему дают на этапе проектирования. Основываясь на этих обучающих фразах, Dialogflow понимает, какой ответ дать на тот или иной вопрос пользователя.
***
### Из чего состоит программа:

* В модуле ***vk_bot.py*** реализовано взаимодествие пользователя через сообщество Вконтакте
* В модуле ***tg_bot.py*** реализовано взаимодествие пользователя через интерфейс telegram
* В пакете ***dialogflow_helpers.py*** реализованы методы взаимодействия с сервисом Dialogflow:
* В модуле ***logger.py*** реализован класс собственного обработчика логов

### В dialogflow_helpers.py

  ***detect_intent_texts*** - получение ответного сообщения от сервиса Dialogflow на сообщение пользователя

  ***create_intent*** - загрузка обучающих фраз из [json-файла](https://github.com/Sergryap/verb_game/blob/master/google_methods/questions.json) с ответами и создание intents на их основе

### Необходимые переменные окружения и файлы:

Для работы программы необходимо создать файл `.env` в корне проекта, содержащий переменные окружения:
```
VK_TOKEN=<Ключ доступа для группы с ботом Vk>
TGM_TOKEN=<Токен от основного бота Tg>
TGM_ID=<Id чата Tg для получения сообщений от логгера>
GOOGLE_APPLICATION_CREDENTIALS=<Путь до файла в формате json с ключами доступа к проекту в сервисе Google Cloud>
DIALOGFLOW_ID=<Id проекта в Google Cloud>
```

В Google Cloud в разделе **[IAM&Admin>Service accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)** для проекта необходимо получить файл в формате json с ключами доступа и разместить его по пути, указанному в GOOGLE_APPLICATION_CREDENTIALS.
<br>Файл должен иметь следующий вид:
```
{
  "type": "service_account",
  "project_id": "your app XXXXXX",
  "private_key_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "private_key": "-----BEGIN PRIVATE KEY-----xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "client_email": "xxxxxxxxxxxxxxx@xxxxxxxxxxxxxxxxxx.iam.gserviceaccount.com",
  "client_id": "xxxxxxxxxxxxxxxxxxxxxxxxx",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/xxxxxxxxxxxx.iam.gserviceaccount.com"
}
```
***
## Пример установки
#### Загрузите репозиторий проекта:
`git clone https://github.com/Sergryap/verb_game.git`
#### Создайте и активируйте виртуальное окружение в корневой папке проекта:
```
cd verb_game/
python3 -m venv venv
source venv/bin/activate
```
#### Установите необходимые зависимости:
`pip install -r requirements.txt`

#### Создайте в корне проекта файл `.env` и запишите в него необходимые ключи:
`nano .env`

#### Разместите файл json с ключами доступа в корне проекта


#### Чтобы запустить тренировку бота выполните команду:
`python3 google_methods/create_intents.py`

Этой командой создадутся Intents в сервие DialogFlow на основании данных файла `/google_methods/questions.json`

#### Запустите бота для tg и vk:
`python3 bot_tg.py | python3 bot_vk.py`

#### После запуска ботов вам придут сообщения от логгера в Tg:
![img.png](img.png)