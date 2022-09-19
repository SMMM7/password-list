import time

from bs4 import BeautifulSoup
from telebot.types import *
from pytube import YouTube
from telebot import *
import requests
import itertools
from random import randint
import re
import sqlite3

token = '5641097612:AAG8f2wmFdo_Btmv4AR0PiPtKnL8dBKJic4'
bot = telebot.TeleBot(token, parse_mode='MarkDown')


@bot.message_handler(content_types=['text'], func=lambda message:True)
def messages(message):
	if message.text == '/start':
		bot.send_message(message.chat.id, f'Hi *{message.chat.first_name}*,\nSend /passlist to generate a password list.')

	elif message.text == '/passlist':
		m = bot.send_message(message.chat.id, 'Send Characters:len-of-password(integer)\n*Example:* `abcdDFFd%6:5`')
		bot.register_next_step_handler(m, generate)
	else:
		bot.send_message(message.chat.id, 'Invalid command!\nSend */passlist* to make a password list')


def generate(message):
	num = random.randint(0, 1000)
	loading = bot.send_message(message.chat.id, 'Checking the input ...')
	try:
		chars = str(message.text).split(':')[0]
		passlen = str(message.text).split(':')[1]
		passlen = int(passlen)
		if passlen > 11 or len(chars) > 13:
			bot.send_message(message.chat.id, 'Len must be smaller than 11 and the len of characters must be smaller than 14 for no bug and crash!')
		else:
			try:

				bot.delete_message(message.chat.id, loading.message_id)
				generating = bot.send_message(message.chat.id, 'Generating the password list ...')
				passl = list(map("".join, itertools.product(chars, repeat=int(passlen))))
				file_name = f'{num}-{message.chat.id}.txt'
				saving = bot.edit_message_text('Saving the password list in txt file ...', message.chat.id,
											   generating.message_id)
				with open(file_name, 'w+') as file:
					for lines in passl:
						file.write(f'\n{lines}')
					file.close()

					saved = bot.edit_message_text('File saved!\nUploading to telegram ...', message.chat.id,
												  saving.message_id)
					time.sleep(4)
					password_list = open(file_name, 'r+')
					bot.send_document(message.chat.id, password_list)
					bot.delete_message(message.chat.id, saved.message_id)
					os.remove(file_name)

			except:
				bot.send_message(message.chat.id, '*Error:*\n*Input must be like this:* `abcded@s:5`')

	except:
		bot.delete_message(message.chat.id, loading.message_id)
		bot.send_message(message.chat.id, 'Password len must be integer!')


bot.polling()
