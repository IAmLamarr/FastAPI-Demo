from BaseHandler import BaseHandler

from requests import get, post, patch


class EditPetHandler:
    def __init__(self, base: BaseHandler):
        self.__base = base
        self.__create_mode = dict()
        self.__curr_name = dict()
        self.__curr_kind = dict()
        self.__pet_id = dict()
        self.handlers = [
            {
                "text": "Добавить животное",
                "handler": self.__create_pet,
            },
            {
                "text": "Изменить информацию о животном",
                "handler": self.__patch_pet,
            },
        ]
        self.query_handlers = [
            {
                "text": "Перешлите ID животного",
                "handler": self.__req_pet_data,
            },
            {
                "text": "Ответьте на это сообщение именем животного",
                "handler": self.__set_name,
            },
            {
                "text": "Ответьте на это сообщение видом животного",
                "handler": self.__set_kind,
            },
        ]

    def __name_info(self, chat_id, user_id):
        if user_id in self.__curr_name:
            self.__base.bot.send_message(chat_id, f"Текущее имя: {self.__curr_name[user_id]}")
            self.__base.bot.send_message(chat_id, "Если хотите оставить текущее имя, перешлите -")
        self.__base.bot.send_message(chat_id, self.query_handlers[1]["text"])

    def __kind_info(self, chat_id, user_id):
        if user_id in self.__curr_kind:
            self.__base.bot.send_message(chat_id, f"Текущий вид: {self.__curr_kind[user_id]}")
            self.__base.bot.send_message(chat_id, "Если хотите оставить текущий вид, пришлите любое недопустимое значение")

        self.__base.bot.send_message(chat_id, "Допустимые значения: bulldog, terrier, dalmatian")
        self.__base.bot.send_message(chat_id, self.query_handlers[2]["text"])

    def __set_name(self, chat_id, user_id, name):
        if name != '-':
            self.__curr_name[user_id] = name
        self.__kind_info(chat_id, user_id)

    def __set_kind(self, chat_id, user_id, kind):
        if kind in ['bulldog', 'terrier', 'dalmatian']:
            self.__curr_kind[user_id] = kind
        self.__finish_edit(chat_id, user_id)

    def __finish_edit(self, chat_id, user_id):
        data = {
            "kind": self.__curr_kind[user_id],
            "name": self.__curr_name[user_id],
        }
        if self.__create_mode[user_id]:
            post(f"{self.__base.webhook_url}/dog", json=data, timeout=2)
        else:
            patch(f"{self.__base.webhook_url}/dog/{self.__pet_id[user_id]}", json=data, timeout=2)
        self.__base.bot.send_message(chat_id, "Данные успешно сохранены")

        if not self.__create_mode[user_id]:
            del self.__pet_id[user_id]
        del self.__curr_kind[user_id]
        del self.__curr_name[user_id]

        self.__base.start(chat_id)

    def __create_pet(self, chat_id, user_id):
        self.__create_mode[user_id] = True
        self.__name_info(chat_id, user_id)

    def __patch_pet(self, chat_id, user_id):
        self.__create_mode[user_id] = False
        self.__base.bot.send_message(chat_id, self.query_handlers[0]["text"])

    def __req_pet_data(self, chat_id, user_id, pet_id):
        dog_req = get(f"{self.__base.webhook_url}/dog/{pet_id}", timeout=2)
        if dog_req.status_code == 200:
            self.__pet_id[user_id] = pet_id
            dog = dog_req.json()
            self.__curr_name[user_id] = dog["name"]
            self.__curr_kind[user_id] = dog["kind"]
            self.__name_info(chat_id, user_id)
        else:
            self.__base.bot.send_message(chat_id, "Не найдено")
            self.__base.start(chat_id)
