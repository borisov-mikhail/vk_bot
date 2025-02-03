# VK Bot
Этот бот принимает изображения от пользователей и отправляет их же ответным сообщением


## Установка 
1) Клонируйте репозиторий:
```
git clone git@github.com:borisov-mikhail/vk_bot.git
cd vk_bot
```
2) Установите зависимости:
```
pip install -r requirements.txt
```
3) Заполните конфигурацию в файле `config.py`.
* GROUP_TOKEN - токен сообщества вк
* GROUP_ID - id сообщества вк
* DATABASE_NAME - название базы данных (менять не обязательно)

GROUP_TOKEN можно создать в настройках сообщества

4) Запустите бота:
```
python3 main.py
```
