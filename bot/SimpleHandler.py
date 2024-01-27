from BaseHandler import BaseHandler
from requests import get, post


class SimpleHandler:
    def __init__(self, base: BaseHandler):
        self.__base = base
        self.handlers = [
            {
                "text": "Добавить timestamp в БД",
                "handler": self.__create_timestamp,
            },
            {
                "text": "Проверить работоспособность",
                "handler": self.__check_status,
            },
            {
                "text": "Получить список всех животных",
                "handler": self.__get_list,
            },
        ]

    def __check_status(self, chat_id, user_id):
        try:
            get(f"{self.__base.webhook_url}", timeout=2)
            self.__base.bot.send_message(chat_id, "Сервис работает корректно")
        except Exception:
            self.__base.bot.send_message(chat_id, "Ошибка работы сервиса")
        self.__base.start(chat_id)

    def __get_list(self, chat_id, user_id):
        dogs_req = get(f"{self.__base.webhook_url}/dog", timeout=2)
        dogs = dogs_req.json()

        if len(dogs) == 0:
            self.__base.bot.send_message(chat_id, "База данных пуста")
        else:
            for dog in dogs:
                md = self.__base.format_pet(dog)
                self.__base.bot.send_message(chat_id, md, parse_mode="Markdown")
        self.__base.start(chat_id)

    def __create_timestamp(self, chat_id, user_id):
        post(f"{self.__base.webhook_url}", timeout=2)
        self.__base.bot.send_message(chat_id, "Успешно создан timestamp")
        self.__base.start(chat_id)