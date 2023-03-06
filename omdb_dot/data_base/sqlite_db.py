import sqlite3 as sq
from create_bot import dp, bot

def sql_start():
	global base, cur
	base = sq.connect('omdb_bot.db')
	cur = base.cursor()
	if base:
		print('Data base reg is connected.')
	base.execute('CREATE TABLE IF NOT EXISTS stud(title TEXT, director TEXT, writer TEXT, year TEXT, plot TEXT, genre TEXT, ratings TEXT, poster TEXT)')
	base.commit()


async def sql_add_film(state):
	async with state.proxy() as data:
		cur.execute('INSERT INTO stud VALUES (?, ?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
		base.commit()	
