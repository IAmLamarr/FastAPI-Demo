from telebot import TeleBot, types


class BaseHandler:
    def __init__(self, bot: TeleBot, webhook_url):
        self.bot = bot
        self.webhook_url = webhook_url
        self.menu_handlers = []

    @staticmethod
    def format_pet(pet):
        return f"""
                    *ID*: {pet["pk"]} *Имя*: {pet["name"]} *Вид*: {pet["kind"]}
                """

    def __create_start_markup(self):
        markup = types.ReplyKeyboardMarkup(selective=True)

        for handle_item in self.menu_handlers:
            button = types.KeyboardButton(handle_item["text"])
            markup.row(button)

        return markup

    def start(self, chat_id):
        markup = self.__create_start_markup()
        self.bot.send_message(chat_id, 'Чем я могу помочь?', reply_markup=markup)