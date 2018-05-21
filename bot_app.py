# -*- coding: utf-8 -*-

import telebot
import math
import numpy
import sympy as sympy
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
from sympy import simplify
from sympy import apart
from sympy import diff
from sympy import init_session
import wolframalpha
import ssl


from sympy.parsing.sympy_parser import parse_expr

#ссскномер
#import Image

import parser		  
import config
import graphics
import dworker


token=config.token
bot=telebot.TeleBot(token)

wolfram_app_id = config.wolfram_app_id
client = wolframalpha.Client(wolfram_app_id)


def rstr(message): #Удаление команды из строки
    if message.text[0]=='/':
        if len(message.text)==0:
            bot.send_message(message.chat.id, "Введите аргументы команды!")
            return ''
        #temp='\\'+command+' '
        #message.text=message.text.replace(temp,'')
        message.text=message.text.split(" ")
        result=''
        i=1
        while i<len(message.text):
            result=result+message.text[i]
            if (i<len(message.text)-1):
                 result += ' '
            i=i+1
    return result


@bot.message_handler(commands=['echo'])
def handle_echo(message):
    message.text=rstr(message)
    if(len(message.text)!=0):
        bot.send_message(message.chat.id, message.text)

@bot.message_handler(commands=['lim'])
def handle_lim(message):
	try:
		message.text=rstr(message)
		if(len(message.text)!=0):
			s=sympy.limit(message.text.split(', ')[0], message.text.split(', ')[1], message.text.split(', ')[2])
			lat=sympy.latex(s)
			plt.text(0, 0.6, r"$%s$" % lat, fontsize = 50)
			plt.axis('off')
			plt.savefig('plot.png')
			photo = open('plot.png', 'rb')
			bot.send_photo(message.chat.id,photo, s)
			plt.close()
	except BaseException:
		bot.send_message(message.chat.id, 'Ошибка при вводе предела!')

@bot.message_handler(commands=['diff'])
def handle_diff(message):
	try:
		message.text=rstr(message)
		if(len(message.text)!=0):
			plt.close()
			if (message.text.find(', ')==-1):
				k = 1
				sk = 'x'
			else: 
				k=message.text.split(', ')[2]
				sk=message.text.split(', ')[1]
			s=diff(message.text.split(', ')[0], sk, k)
			lat=sympy.latex(s)
			plt.text(0, 0.6, r"$%s$" % lat, fontsize = 50)
			plt.axis('off')
			plt.savefig('plot.png')
			photo = open('plot.png', 'rb')
			bot.send_photo(message.chat.id,photo, s)
			plt.close()
	except BaseException:
		bot.send_message(message.chat.id, 'Ошибка при вводе функции!')

@bot.message_handler(commands=['together'])
def handle_together(message):
	try:
		message.text=rstr(message)
		if(len(message.text)!=0):
			s=sympy.together(message.text)
			lat=sympy.latex(s)
			plt.text(0, 0.6, r"$%s$" % lat, fontsize = 50)
			plt.axis('off')
			plt.savefig('plot.png')
			photo = open('plot.png', 'rb')
			bot.send_photo(message.chat.id,photo, s)
			plt.close()
	except BaseException:
		bot.send_message(message.chat.id, 'Ошибка при вводе дробей!')

@bot.message_handler(commands=['integrate'])
def handle_integrate(message):
	try:
		message.text=rstr(message)
		if(len(message.text)!=0):
			plt.close()
			s=sympy.integrate(message.text)
			lat=sympy.latex(s)
			plt.text(0, 0.6, r"$%s$" % lat, fontsize = 50)
			plt.axis('off')
			plt.savefig('int.png')
			photo = open('int.png', 'rb')
			bot.send_photo(message.chat.id,photo, s)
			plt.close()
	except BaseException:
		bot.send_message(message.chat.id, 'Ошибка при вводе функции!')

@bot.message_handler(commands=['fact'])
def handle_fact(message):
	try:
		message.text=rstr(message)
		if(len(message.text)!=0):
			res = int('1') 
			n = int(message.text) 
			for k in range (1,n+1): 
				res = res * k
				bot.send_message(message.chat.id, str(res)) 
	except BaseException:
		bot.send_message(message.chat.id, 'Ошибка при вводе числа')


@bot.message_handler(commands=['simplify'])
def handle_simplify(message):
	try:
		message.text=rstr(message)
		if(len(message.text)!=0):
			s=simplify(message.text)
			lat=sympy.latex(s)
			plt.text(0, 0.6, r"$%s$" % lat, fontsize = 50)
			plt.axis('off')
			plt.savefig('plot.png')
			photo = open('plot.png', 'rb')
			bot.send_photo(message.chat.id,photo, s)
			plt.close()
	except BaseException:
		bot.send_message(message.chat.id, 'Ошибка при вводе выражения!')


@bot.message_handler(commands=['apart'])
def handle_apart(message):
	try:
		message.text=rstr(message)
		if(len(message.text)!=0):
			s=apart(message.text)
			lat=sympy.printing.latex(s)
			plt.text(0, 0.3, r"$%s$" % lat, fontsize = 30)
			plt.axis('off')
			plt.savefig('plot.png')
			photo = open('plot.png', 'rb')
			bot.send_photo(message.chat.id,photo, s)
			plt.close()
	except BaseException:
		bot.send_message(message.chat.id, 'Ошибка при вводе дроби!')

@bot.message_handler(commands=['solve'])
def handle_solve(message):
	try:
		message.text=rstr(message)
		if(len(message.text)!=0):
			bot.send_message(message.chat.id, parser.eval_(message.text))
	except BaseException:
		bot.send_message(message.chat.id, 'Ошибка при вводе выражения!')

@bot.message_handler(commands=['sqrt'])
def handle_sqrt(message):
	try:
		message.text=rstr(message)
		if(len(message.text)!=0):
			hui = message.text.split(" ")[0]
			c = complex(hui)
			n = int(message.text.split(" ")[1])
			l = math.pow(c.real**2+c.imag**2,1/n)
			alpha = math.atan(c.imag/c.real)
			s = ''
			for i in range (0,n):
				p1 = l*math.cos((alpha+2*math.pi*i)/n)
				p2 = l*math.sin((alpha+2*math.pi*i)/n)
				p = complex(p1,p2)
				k = p2/abs(p2)
				out = ''
				if (p1!=0):
					out = out + str(p1)
				if (k==1): 
					out = out + '+'
				else:
					out = out + '-'
				if (p2!=0):
					out = out + str(p2) + '*j'
				if (len(out)==0): 
					out = '0'
				if i != n-1:
					s = s + out + ' , '
				else: s= s + out
				out=''
			bot.send_message(message.chat.id, s)
	except BaseException:
		bot.send_message(message.chat.id, 'Ошибка при вводе выражения!')

funct = ''
a=-10
b=10
@bot.message_handler(commands=['plot'])
def handle_plot(message):
	try:
		message.text=rstr(message)
		photo = graphics.simple_graph (message.text)
		bot.send_photo(message.chat.id, photo)
	except BaseException:
		bot.send_message(message.chat.id, 'Ошибка при вводе функции')

'''def get_a(message):
	a = int(message.text)
	bot.send_message(message.chat.id,"Введите правую границу интервала: ")
	bot.register_next_step_handler(message, get_b)

def get_b(message):
	b = int(message.text)
	photo = graphics.simple_graph(funct, a, b)
	bot.send_photo(message.chat.id, photo)'''

@bot.message_handler(commands=['photo'])
def handle_photo(message):
    photo = open('image1.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['animate'])
def handle_animate(message):
	try:
		message.text=rstr(message)
		if(len(message.text)!=0):
			if 'z' in message.text:
				bot.send_message(message.chat.id, "Поверхность должна быть задана в явном виде!")
				return
			graphics.movie_graph(message.text)
			photo = open('movie.gif', 'rb')
			bot.send_document(message.chat.id, photo)
	except BaseException:
		bot.send_message(message.chat.id, 'Ошибка при вводе поверхности')

@bot.message_handler(func=lambda message: message.text!='')
def handle_wolfram(message):
	try:							  
	#	message.text=str(message)
		if(len(message.text)!=0):
			res = client.query(message.text)
			s = next(res.results).text
			bot.send_message(message.chat.id, s)
			#lat=sympy.printing.latex(s)
			#plt.text(0, 0.3, r"$%s$" % lat, fontsize = 30)
			#plt.axis('off')
			#plt.savefig('plot.png')
			#photo = open('plot.png', 'rb')
			#bot.send_photo(message.chat.id,photo, s)

	except BaseException:
		bot.send_message(message.chat.id, 'Неверный запрос к базе знаний Wolfram Alpha')

if __name__ == '__main__':
    bot.polling(none_stop=True)

