from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

def train_bot():
    chatbot = ChatBot('Bot',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database='chatdb',
    database_uri='127.0.0.1:27017',
    trainer='chatterbot.trainers.ListTrainer')
    for file in os.listdir('/home/shashi/SRC/chat_bot/data/'):
        print(file)
        convData = open(r'/home/shashi/SRC/chat_bot/data/' + file, encoding='UTF-8').readlines()
        chatbot.set_trainer(ListTrainer)
        chatbot.train(convData)
    print("Training completed")
    

train_bot()

# Make sure to copy the db.sqlite3.db into the root folder i.e where manage.py is located 
# python chatbot_train.py
