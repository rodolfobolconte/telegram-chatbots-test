#manipula os comandos cadastrados no chatbot
from telegram.ext import CommandHandler
#manipula as mensagens enviadas pelo Telegram
from telegram.ext import MessageHandler
#filtra o tipo de mensagem  que o MessageHandler manipula
from telegram.ext import Filters
#realiza a conexão entre Telegram e despachante
from telegram.ext import Updater

from conf.settings import BASE_API_URL, TELEGRAM_TOKEN

#update é uma instância da classe telegram.Update, contém informações do usuário que disparou a mensagem
#context é uma instância de telegram.ext.CallbackContext, facilita o acesso de argumentos para determinados comandos

#retorna mensagens para o cliente
def start(update, context):
    response_message = "=^._.^="
    context.bot.send_message(
        #especifica de quem a mensagem foi enviada
        chat_id=update.effective_chat.id,
        text=response_message
    )

def unknown(update, context):
    response_message = "Miau? =^-_-^="
    context.bot.send_message(
        chat_id=update.effective_chat_id,
        text=respone_messsage
    )

#pega a foto do código no site do httpcats e envia por mensagem
def http_cats(update, context):
    context.bot.sendPhoto(
        chat_id=update.effective_chat.id,
        #context.args são as mensagens passadas pelo comando
        #acessa o HTTP Cats passando o código que retorna a imagem
        photo=BASE_API_URL+context.args[0]
    )

def main():
    #conexão com a api do Telegram bot
    updater = Updater(token=TELEGRAM_TOKEN)

    #cadastro de comandos feito pelo despachante
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('http', http_cats))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    print('pressione CTRL + C para cancelar.')
    main()