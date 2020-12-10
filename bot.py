import config
import telebot
import Menu
import input_data
from telebot import types

# Create token variable
TG_BOT_TOKEN = config.TOKEN

# Init bot
bot = telebot.TeleBot(TG_BOT_TOKEN)
menu = Menu.Menu()

data = input_data.DATA_ARR

# Start command decorator
@bot.message_handler(commands = ['start'])
def start_command(message):
    categories = data.keys()
    menu.clear()
    infoMessage = f"<b>{message.from_user.first_name}, добро пожаловать в наше заведение</b>\n\nВот Ваше меню\nЗдсь Вы можете ознакомиться со всем нашим ассортиментом блюд и выбрать то, что Вам будет по душе\n\nДля вызова администратора используйте команду /help"
    bot.send_message(message.chat.id, infoMessage, parse_mode='html', reply_markup=createMarkup(categories, False))
    
# Help command decorator
@bot.message_handler(commands = ['help'])
def help_command(message):
    infoMessage = f"<b><u>Твой личный администратор</u></b>\n\nДля того, чтобы попросить меню выберите команду /start"
    bot.send_message(message.chat.id, infoMessage, parse_mode='html')

# Process user mesage
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Назад':
        menu.clear()
        categories = data.keys()
        infoMessage = f"<b>Возвращаемся в меню</b>"
        bot.send_message(message.chat.id, infoMessage, parse_mode='html', reply_markup=createMarkup(categories, False))
    elif menu.getLevel() == 0:
        # Categories menu level
        categoryItems = data.get(message.text)
        createCategoryMessage(message, categoryItems)
    elif menu.getLevel() == 1:
        # Products menu level
        product = data[menu.getCategory()].get(message.text)
        createProductCard(message, product)

def createProductCard(message, product):
    productName = f"<b><u>{ product['Name'] }</u></b>"
    productImage = open(product['img'], 'rb')
    productStructure = product['structure']
    productEnergy = 'Энергетическая ценность продукта'
    infoMessage = f"{ productName }\n\n{ productStructure }\n\nВес готового продукта - <b>{ product['weigth'] }</b>\n\n{ productEnergy } - <b>{ product['energy'] }</b>"
    bot.send_photo(message.chat.id, productImage, caption=infoMessage, parse_mode='html')

# Pattern for messages in categories
def createCategoryMessage(message, categoryItems):
    if categoryItems == None:
        infoMessage = f"<b>Данная категория находится в разработке</b>\n\nПодождите немного, мы готовим для Вас кое-что интесное\n\n/start"
        bot.send_message(message.chat.id, infoMessage, parse_mode='html')
    else:
        infoMessage = f"<b><u>{ message.text }</u></b>\n\nВ этом разделе представлены все позиции по категории { message.text }"
        menu.incLevel()
        menu.setCategory(message.text)
        bot.send_message(message.chat.id, infoMessage, parse_mode='html', reply_markup=createMarkup(categoryItems))

# Create markup from arr of properties
def createMarkup(data_arr, back_btn = True):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    for elem in data_arr:
        markup.add(types.KeyboardButton(elem))
    if back_btn:
        markup.add(types.KeyboardButton('Назад'))
    return markup

bot.polling(none_stop=True)