#manipula os comandos cadastrados no chatbot
from telegram.ext import CommandHandler
#manipula as mensagens enviadas pelo Telegram
from telegram.ext import MessageHandler
#filtra o tipo de mensagem  que o MessageHandler manipula
from telegram.ext import Filters
#realiza a conexão entre Telegram e despachante
from telegram.ext import Updater

import requests

from pprint import pprint

from conf.settings import BASE_API_URL, TELEGRAM_TOKEN, KEY_API_VAGALUME

#update é uma instância da classe telegram.Update, contém informações do usuário que disparou a mensagem
#context é uma instância de telegram.ext.CallbackContext, facilita o acesso de argumentos para determinados comandos

#retorna mensagens para o cliente
def start(update, context):
    response_message = "Bem-Vindx!\n\nPara pesquisar uma letra de música digite na seguinte ordem, sem os colchetes:\n\n[nome-música] - [nome-artista]"
    context.bot.send_message(
        #especifica de quem a mensagem foi enviada
        chat_id=update.effective_chat.id,
        text=response_message
    )

def letra(update, context):
    #pesquisa letra quando é passado o comando letra ou l
    musica, artista = ' '.join(context.args).split(sep=' - ')
    
    resposta = requests.get("https://api.vagalume.com.br/search.php?art={}&mus={}&apikey={}".format(artista, musica, KEY_API_VAGALUME))
    resposta_json = resposta.json()

    artista_nome = resposta_json['art']['name']
    musica_nome = resposta_json['mus'][0]['name']
    musica_letra = resposta_json['mus'][0]['text']

    musica_completa = musica_nome + ' - ' + artista_nome + '\n\n' + musica_letra
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text = musica_completa
    )

def pesquisa_letra(update, context):
    try:
        musica, artista = update.message.text.split(sep=' - ')

        resposta = requests.get("https://api.vagalume.com.br/search.php?art={}&mus={}&apikey={}".format(artista, musica, KEY_API_VAGALUME))
        resposta_json = resposta.json()

        artista_nome = resposta_json['art']['name']
        musica_nome = resposta_json['mus'][0]['name']
        musica_letra = resposta_json['mus'][0]['text']

        musica_completa = musica_nome + ' - ' + artista_nome + '\n\n' + musica_letra
    except:
        musica_completa = 'Não foi possível localizar!'
    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text = musica_completa
    )

def unknown(update, context):
    response_message = "Comando não encontrado!"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_message
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
    #dispatcher.add_handler(CommandHandler('l', letra))
    #dispatcher.add_handler(CommandHandler('letra', letra))
    dispatcher.add_handler(MessageHandler(Filters.text, pesquisa_letra))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    print('Pressione CTRL + C para cancelar.')
    main()