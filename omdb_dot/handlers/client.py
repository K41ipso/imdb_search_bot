from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message, InputFile
from data_base import sqlite_db
from omdbapi.movie_search import GetMovie

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup


movie = GetMovie(api_key='453547de')



class fsmsearch(StatesGroup):
	film = State()



async def commands_start(message : types.Message):
	await bot.send_message(message.from_user.id, 'Привет! Чтобы найти фильм - нажми кнопку ниже.', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Поиск фильма по названию', callback_data="search_film")))

async def callback_search(call):
	await call.message.edit_reply_markup(InlineKeyboardMarkup().add(InlineKeyboardButton(text='♻️', callback_data="loading")))
	await fsmsearch.film.set()
	await bot.send_message(chat_id=call.from_user.id, text='Введите название фильма на английском языке:')

async def send_film(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		mov = movie.get_movie(title=message.text)
		if mov == 'Movie not found!':
			mov_dict = 'Такой фильм не найден, попробуй ещё раз!'
		else:
			finaly = ''
			mov_dict = movie.get_data('title', 'director', 'writer', 'year', 'plot', 'genre', 'ratings', 'poster')
			data['title'] = mov_dict['title']
			data['director'] = mov_dict['director']
			data['writer'] = mov_dict['writer']
			data['year'] = mov_dict['year']
			data['plot'] = mov_dict['plot']
			data['genre'] = mov_dict['genre']
			data['ratings'] = f"{mov_dict['ratings']}"
			data['poster'] = mov_dict['poster']			
			for i in mov_dict['ratings']: finaly += f"\n{i['Source']}: {i['Value']}"
			mov_dict = f"Название: *{mov_dict['title']}* \n\nРежиссер: _{mov_dict['director']}_ \nСценарист: _{mov_dict['writer']}_ \nГод выхода: {mov_dict['year']} \n\nКраткий сюжет: _{mov_dict['plot']}_ \n\nЖанры: {mov_dict['genre']} \n\nРейтинг: {finaly} \n\n\nПостер: {mov_dict['poster']}"
	if mov == 'Movie not found!':
		pass
	else: 
		await sqlite_db.sql_add_film(state)
	await state.finish()
	await message.answer (f'{mov_dict}', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Поиск фильма по названию', callback_data="search_film")), parse_mode="Markdown")






def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(commands_start, commands=['start', 'help'])
	dp.register_callback_query_handler(callback_search, lambda c: c.data == 'search_film')
	dp.register_message_handler(send_film, state=fsmsearch.film)
