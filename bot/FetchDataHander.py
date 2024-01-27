from BaseHandler import BaseHandler
from requests import get


class FetchDataHandler:
    def __init__(self, base: BaseHandler):
        self.__base = base
        self.handlers = [
            {
                "text": "Получить информацию о животном",
                "handler": self.__get_pet_data,
            },
        ]
        self.query_handlers = [
            {
                "text": "Ответьте на это сообщение ID животного",
                "handler": self.__req_pet_data,
            },
        ]

    def __get_pet_data(self, chat_id):
        self.__base.bot.send_message(chat_id, self.query_handlers[0]["text"])

    def __req_pet_data(self, chat_id, user_id, pet_id):
        dog_req = get(f"{self.__base.webhook_url}/dog/{pet_id}", timeout=2)
        if dog_req.status_code == 200:
            dog = dog_req.json()
            md = self.__base.format_pet(dog)
            self.__base.bot.send_message(chat_id, md, parse_mode="Markdown")
        else:
            self.__base.bot.send_message(chat_id, "Не найдено")
        self.__base.start(chat_id)