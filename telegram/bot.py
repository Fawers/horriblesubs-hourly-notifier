import os

import telepot


CHANNEL = os.getenv('TGCHANNEL')

BOT = telepot.Bot(os.getenv('TGBOT'))


def send_to_channel(message):
    BOT.sendMessage(CHANNEL, message, parse_mode='html')
