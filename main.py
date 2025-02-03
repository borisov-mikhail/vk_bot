import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from config import GROUP_TOKEN, GROUP_ID, DATABASE_NAME
import sqlite3
from datetime import datetime


def init_db():
    # Инициализация БД для отслеживания новых пользователей 
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users 
            (
            user_id INTEGER PRIMARY KEY,
            first_message_time DATETIME NOT NULL
            )
        ''')
    conn.commit()
    conn.close()

def is_new_user(user_id):
    # Проверка наличия пользователя в БД
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result is None:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO users (user_id, first_message_time) VALUES (?, ?)', (user_id, current_time))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False


def main():
    init_db()
    
    vk_session = vk_api.VkApi(token=GROUP_TOKEN)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.message['from_id']
            message_id = event.message['id']
            attachments = event.message.get('attachments', [])
            print(attachments)

            if is_new_user(user_id):
                vk.messages.send(
                    user_id=user_id,
                    message="Привет! Это простой бот, который отправляет обратно все полученные изображения.",
                    random_id=get_random_id()
                )

            # Поиск изображений во вложениях
            photo_attachments = []
            for attachment in attachments:
                if attachment['type'] == 'photo':
                    photo = attachment['photo']
                    access_key = photo.get('access_key', '')
                    photo_attachments.append(f"photo{photo['owner_id']}_{photo['id']}_{access_key}")

            # Если есть изображения, отправляем их обратно
            if photo_attachments:
                attachments = ",".join(photo_attachments)
                vk.messages.send(
                    user_id=user_id,
                    reply_to=message_id,
                    attachment=attachments,
                    random_id=get_random_id()
                )

if __name__ == '__main__':
    main()