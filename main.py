# discord :OOO
import discord
from discord.ext import commands

# jakies gowno wazne i niewazne
from os import getenv

# do brania info
from lxml import html
import requests

# baza danych zeby zarejestrowac sb
from replit import db

from strona import keep_alive

keep_alive()

# opis
description = "bot dla jejaków"

# database:

#  ___________________________________
# |                    |              |
# | uzytkownik discord | nick na jeja |
# |____________________|______________|


# bot
bot = commands.Bot(command_prefix='j!')

class Uzytkownik():
	def __init__(self, user: str):
		self.link = "https://www.jeja.pl/user,{}".format(user)
		jeja = requests.get(self.link)
		strona = html.fromstring(jeja.content)
		
		# nazwa użytkownika
		self.nick = strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[1]/div[2]/text()')[0]

		# zdjęcie profilowe
		self.avek = strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/img/@src')[0]

		# poziom doświadczenia
		self.lvl = strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[3]/div[2]/div[2]/div[1]/strong/text()')[0]

		# liczba punktów doświadczenia
		self.pkt = strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[3]/div[2]/div[2]/div[2]/strong/text()')[0]

		# ilość strzałek w górę
		self.strzalki = strona.xpath('//*[@id="wrapper-wrap"]/div[1]/div/div[1]/div[5]/div[2]/div[1]/text()')[0]
		


# jeśli bot dołączy
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# wysyła ilość strzałek w górę
@bot.command()
async def strzalki(ctx, user: str):
	try:
		
		uzytkownik = Uzytkownik(user)
		await ctx.send(f"{uzytkownik.nick} ma `{uzytkownik.strzalki}` strzałek w górę")
	except:
		await ctx.send(f"Nie ma użytkownika o nazwie `{user}`")

@bot.command()
async def pd(ctx, user: str):
	try:
		uzytkownik = Uzytkownik(user)
		await ctx.send(f"{uzytkownik.nick} ma poziom `{uzytkownik.lvl}` i `{uzytkownik.pkt}` punktów doświadczenia")
	except:
		await ctx.send(f"Nie ma użytkownika o nazwie `{user}`")

@bot.command()
async def avek(ctx, user: str):
	try:
		uzytkownik = Uzytkownik(user)
		await ctx.send(f"Zdjęcie profilowe użytkownika {uzytkownik.nick}")
		await ctx.send(uzytkownik.avek)
	except:
		await ctx.send(f"Nie ma użytkownika o nazwie `{user}`")

@bot.command(aliases=['profil'])
async def link(ctx, user: str):
	try:
		uzytkownik = Uzytkownik(user)
		await ctx.send(f"link do profilu: {uzytkownik.link}")
	except:
		await ctx.send(f"Nie ma użytkownika o nazwie `{user}`")

# dziala bot
bot.run(getenv('token'))