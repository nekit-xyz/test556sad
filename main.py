# import files
import tokens
# import tools for vk
from vkbottle.bot import Bot, Message
from vkbottle.tools import Keyboard
from vkbottle.api import API
# import libs
import datetime, asyncio, random, sqlite3, json, time

# connection to local database
connbd = sqlite3.connect('database/GAMES.db')
c = connbd.cursor()

# create dicts
rooms = {0: 'Столовая', 1: 'Навигация', 2: 'Оружейная', 3: 'Топливо', 4: 'Двигатель 1', 5: 'Двигатель 2'}
charcters = {1: 'Член Экипажа', 2: 'Предатель'}
errors = {1: 'Unknow error', 2: 'User is not playing', 3: 'User killed', 4: 'Event type not message', 5: 'Wrong type of event', 6: 'The room has already been created'}
commands = ('навигация', 'столовая', "оружейная", "топливо", "верхний двигатель", "нижний двигатель", "указать путь", "уничтожить камни", "заправить бак", "починить двигатель 1", "починить двигатель 2")

# create function
async def get_id_game():
	rid = random.randint(1000, 9999)
	if await select_db(rid, 'games', 'id_game') is None:
		return rid
	else:
		await get_id_game()

async def ridm():
	r = random.randint(1, 99999999999)
	return r

async def randomm(int1, int2):
	return random.randint(int1, int2)

async def delete_game(base):
	users = str((await select_db(base, 'games', 'id_game'))[1]).split(' ')
	print(users)
	for i in users:
		print(i)
		await update_db(i, 'users', 'game', 0, 'user_id')
	c.execute(f'DROP table game_{base}')
	connbd.commit()
	c.execute(f'DELETE FROM games WHERE id_game = {base}')
	connbd.commit()

async def select_db(user_id, base, key_colm):
	s = f'SELECT * FROM {base} WHERE {key_colm} = {user_id}'
	c.execute(s)
	res = c.fetchone()
	#print(res)
	return res

async def update_db(user_id, base, column, action, key_colm):
	u = f'UPDATE {base} SET {column} = "{action}" WHERE {key_colm} = {user_id}'
	c.execute(u)
	connbd.commit()

async def rnum(int1, int2):
	return random.randint(int1, int2)

async def get_button(one_time=False, inline=False, buts=None):
	keyb = Keyboard(one_time=one_time, inline=inline).schema(buts).get_json()
	#print(keyb)
	return keyb

async def room1(user_id):
	if (await select_db(user_id, f'game_{(await select_db(user_id, "users", "user_id"))[1]}', 'user_id'))[8] == 'Член экипажа':
		return (await get_button(one_time=True, buts=[
			[
		{'label': 'Репорт', 'type': 'text', "color": 'positive'}], [
		{'label': 'Навигация', 'type': 'text', "color": 'secondary'},
		{'label': 'Оружейная', 'type': 'text', "color": 'secondary'},
		{'label': 'Топливо', 'type': 'text', "color": "secondary"}], [
		{'label': 'Верхний двигатель', 'type': 'text', "color": 'secondary'},
		{'label': 'Выход из игры', 'type': 'text', "color": 'negative'},
		{'label': 'Нижний двигатель', 'type': 'text', "color": 'secondary'}]
		]
						  ))
	if (await select_db(user_id, f'game_{(await select_db(user_id, "users", "user_id"))[1]}', 'user_id'))[8] == 'Предатель':
		return (await get_button(one_time=True, buts=[
			[
		{'label': 'Репорт', 'type': 'text', "color": 'negative'},
		{'label': 'Убить', 'type': 'text', "color": 'positive'}], [
		{'label': 'Навигация', 'type': 'text', "color": 'secondary'},
		{'label': 'Оружейная', 'type': 'text', "color": 'secondary'},
		{'label': 'Топливо', 'type': 'text', "color": 'secondary'}], [
		{'label': 'Верхний двигатель', 'type': 'text', "color": 'secondary'},
		{'label': 'Выход из игры', 'type': 'text', "color": 'negative'},
		{'label': 'Нижний двигатель', 'type': 'text', "color": 'secondary'}]
		]
						  ))

async def room2(user_id):
	if (await select_db(user_id, f'game_{(await select_db(user_id, "users", "user_id"))[1]}', 'user_id'))[8] == 'Член экипажа':
		return (await get_button(one_time=True, buts=[
			[
		{'label': 'Указать путь', 'type': 'text', "color": 'positive'}], [
		{'label': 'Столовая', 'type': 'text', "color": 'secondary'}], [
		{'label': 'Выход из игры', 'type': 'text', "color": 'negative'}]
		]
						  ))
	if (await select_db(user_id, f'game_{(await select_db(user_id, "users", "user_id"))[1]}', 'user_id'))[8] == 'Предатель':
		return (await get_button(one_time=True, buts=[
			[
				{'label': 'Убить', 'type': 'text', "color": 'positive'}], [
				{'label': 'Столовая', 'type': 'text', "color": 'secondary'}], [
				{'label': 'Выход из игры', 'type': 'text', "color": 'negative'}]
			]
						  ))
async def room3(user_id):
	if (await select_db(user_id, f'game_{(await select_db(user_id, "users", "user_id"))[1]}', 'user_id'))[8] == 'Член экипажа':
			return (await get_button(one_time=True, buts=[
		[
			{'label': 'Уничтожить камни', 'type': 'text', "color": 'positive'}], [
			{'label': 'Столовая', 'type': 'text', "color": 'secondary'}], [
			{'label': 'Выход из игры', 'type': 'text', "color": 'negative'}]
		]
							  ))
	if (await select_db(user_id, f'game_{(await select_db(user_id, "users", "user_id"))[1]}', 'user_id'))[8] == 'Предатель':
		return (await get_button(one_time=True, buts=[
			[
				{'label': 'Убить', 'type': 'text', "color": 'negative'}], [
				{'label': 'Столовая', 'type': 'text', "color": 'secondary'}], [
				{'label': 'Выход из игры', 'type': 'text', "color": 'negative'}]
		]
						  ))

async def room4(user_id):
	if (await select_db(user_id, f'game_{(await select_db(user_id, "users", "user_id"))[1]}', 'user_id'))[8] == 'Член экипажа':
		return (await get_button(one_time=True, buts=[
			[
				{'label': 'Заправить бак', 'type': 'text', "color": 'positive'}], [
				{'label': 'Столовая', 'type': 'text', "color": 'secondary'}], [
				{'label': 'Выход из игры', 'type': 'text', "color": 'negative'}]
		]
						  ))
	if (await select_db(user_id, f'game_{(await select_db(user_id, "users", "user_id"))[1]}', 'user_id'))[8] == 'Предатель':
		return (await get_button(one_time=True, buts=[
			[
				{'label': 'Убить', 'type': 'text', "color": 'negative'}], [
				{'label': 'Столовая', 'type': 'text', "color": 'secondary'}], [
				{'label': 'Выход из игры', 'type': 'text', "color": 'negative'}]
		]
						  ))

async def room5(user_id):
	if (await select_db(user_id, f'game_{(await select_db(user_id, "users", "user_id"))[1]}', 'user_id'))[8] == 'Член экипажа':
		return (await get_button(one_time=True, buts=[
			[
				{'label': 'Починить двигатель 1', 'type': 'text', "color": 'positive'}], [
				{'label': 'Столовая', 'type': 'text', "color": 'secondary'}], [
				{'label': 'Выход из игры', 'type': 'text', "color": 'negative'}]
		]
						  ))
	if (await select_db(user_id, f'game_{(await select_db(user_id, "users", "user_id"))[1]}', 'user_id'))[8] == 'Предатель':
		return (await get_button(one_time=True, buts=[
			[
				{'label': 'убить', 'type': 'text', "color": 'negative'}], [
				{'label': 'Столовая', 'type': 'text', "color": 'secondary'}], [
				{'label': 'Выход из игры', 'type': 'text', "color": 'negative'}]
		]
						  ))

async def room6(user_id):
	if (await select_db(user_id, f'game_{(await select_db(user_id, "users", "user_id"))[1]}', 'user_id'))[8] == 'Член экипажа':
		return (await get_button(one_time=True, buts=[
			[
				{'label': 'Починить двигатель 2', 'type': 'text', "color": 'positive'}], [
				{'label': 'Столовая', 'type': 'text', "color": 'secondary'}], [
				{'label': 'Выход из игры', 'type': 'text', "color": 'negative'}]
		]
						  ))
	if (await select_db(user_id, f'game_{(await select_db(user_id, "users", "user_id"))[1]}', 'user_id'))[8] == 'Предатель':
		return (await get_button(one_time=True, buts=[
			[
				{'label': 'убить', 'type': 'text', "color": 'negative'}], [
				{'label': 'Столовая', 'type': 'text', "color": 'secondary'}], [
				{'label': 'Выход из игры', 'type': 'text', "color": 'negative'}]
		]
						  ))

async def get_name(user):
	users = await bot.api.users.get(user_ids=user)
	return f'{users[0].first_name} {users[0].last_name}'



async def check_reg(user_id):
	if (await select_db(user_id, 'users', 'user_id')) is None:
		c.execute(f'INSERT INTO users(user_id, game) VALUES({user_id}, 0)')
		connbd.commit()

async def kill(game, user_id):
	plaeyrs = (await select_db(game, 'games', 'id_game'))[4 + (await select_db(user_id, f'game_{game}', 'user_id'))[7]]
	plaeyrs = str(plaeyrs)
	plaeyrs = plaeyrs.split(' ')
	print(plaeyrs)
	dead_body = ''
	for i in plaeyrs:
		if str(i) != str(user_id):
			dead_body = i
	print(dead_body)
	lud = ''
	dlud = ''
	for i in plaeyrs:
		if i != dead_body:
			lud = f'{lud} {i}'
		print('lud', lud)
		print(i)
	for i in plaeyrs:
		if str(i) == str(dead_body):
			dlud = f'{i}'
		print('dlud', dlud)
		print(i)
	await update_db(game, 'games', f'room{1 + (await select_db(user_id, f"game_{game}", "user_id"))[7]}', lud, 'id_game')
	await update_db(game, 'games', f'rm{1 + (await select_db(user_id, f"game_{game}", "user_id"))[7]}_dead_body', dlud, 'id_game')
	await update_db(dead_body, f'game_{game}', 'state_life', 0, 'user_id')
	return dead_body

async def create_game(id_base, id_user, peer_id, chat, msg):
	await msg.answer(peer_id=msg.peer_id, message=f'&#129529; >> Подготавливаю комнату...')
	try:
		cr = f'CREATE TABLE game_{id_base} (id INTEGER PRIMARY KEY, user_id INTEGER, dvig1 INTEGER DEFAULT "0", dvig2 INTEGER DEFAULT "0", navig INTEGER DEFAULT "0", kamni INTEGER DEFAULT "0", fuel INTEGER DEFAULT "0", room INTEGER DEFAULT "0", charcter TEXT, dvig1_time INTEGER DEFAULT "0", dvig2_time INTEGER DEFAULT "0", navig_time INTEGER DEFAULT "0", kamni_time INTEGER DEFAULT "0", fuel_time INTEGER DEFAULT "0", state_life INTEGER DEFAULT "1", against INTEGER DEFAULT "0", state_voice INTEGER DEFAULT "0")'
		c.execute(cr)
		connbd.commit()
	except Exception as E:
		await msg.answer(peer_id=msg.peer_id, message=f'{errors.get(1)} or {errors.get(6)}, description: {E}')
		await msg.answer(peer_id=msg.peer_id, message=f'Возможно игра уже создана! Если нет, то прошу написать [id487334215|создателю бота]!')
		print(f'{errors.get(1)} or {errors.get(6)}, description: {E}')
		return
	c1 = f'INSERT INTO games(id_game) VALUES({id_base})'
	c.execute(c1)
	connbd.commit()
	await msg.answer(peer_id=msg.peer_id, message=f'&#128190; >> Собираю данные о игроке...')
	await update_db(id_base, 'games', 'creator', id_user, 'id_game')
	await update_db(id_base, 'games', 'chat', chat, 'id_game')
	await update_db(id_user, 'users', 'game', id_base, 'user_id')
	await reg_in_game_lobbi(id_user, id_base, peer_id, msg)
	await msg.answer(peer_id=msg.peer_id, message=f'&#8987; >> Лобби создано, ждем игроков...', keyboard=(await get_button(
		inline=True, buts=[[{"label": f'Присоедениться к лобби {id_base}', "type": "text", "color": 'positive'},
							{"label": f'Отмена', "type": "text", "color": "negative"}]]
	)))

async def run_game(base, peer_id, user_id, msg):
	await msg.answer(peer_id=msg.peer_id, message=f'&#127918; >> Игра началась! Проверьте личку с ботом!')
	users = (await select_db(base, 'games', 'id_game'))[1]
	print(users)
	await update_db(base, 'games', 'room1', users, 'id_game')
	users = users.split(' ')
	print(users)
	for i in users:
		print(i)
		await msg.answer(user_id=i, message=f'~~~ВЫ {(await select_db(i, f"game_{base}", "user_id"))[8]}~~~ \n&#128221; >> Ваши действия и доступные комнаты: ',
						 keyboard=(await room1(i)))
	rm = (await select_db(base, 'games', 'id_game'))[4]
	rmzh = rm.split(' ')
	lud = ''
	rm = (await select_db(base, 'games', 'id_game'))[9]
	rmdm = rm.split(' ')
	dlud = ''
	for i in rmzh:
		if i != 'Нет':
			lud = f'{lud} @id{i}'
		if len(rmzh) == 1 and 'Нет' in str(rmzh):
			lud = 'Нет'
	for i in rmdm:
		if i != 'Нет':
			dlud = f'{dlud} @id{i}'
		if len(rmdm) == 1 and 'Нет' in str(rmdm):
			dlud = 'Нет'
	await msg.answer(peer_id=msg.peer_id, message=f'Приятной игры!')

async def reg_in_game_lobbi (user_id, base, peer_id, msg):
	check = (await select_db(user_id, f'game_{base}', 'user_id'))
	imposter = (await select_db(base, 'games', 'id_game'))[3]

	if check is None:
		reg = 0

	else:
		reg = 1

	if reg == 0:
		users = str((await select_db(base, 'games', 'id_game'))[1])
		users = users.split(' ')
		if imposter is None:
			rand = random.randint(0, 100)
			if rand >= 50:
				cha = 'Член экипажа'
			else:
				cha = 'Предатель'
				await update_db(base, 'games', 'imposter', user_id, 'id_game')
		else:
			cha = 'Член экипажа'
		if imposter is None and len(users) == 2:
			cha = 'Предатель'
		i = f'INSERT INTO game_{base}(user_id, charcter) VALUES({user_id}, "{cha}")'
		await update_db(user_id, 'users', 'game', base, 'user_id')
		c.execute(i)
		connbd.commit()
		if (await select_db(base, 'games', 'id_game'))[1] is None:
			await update_db(base, 'games', 'users', f"{user_id}", 'id_game')
		else:
			await update_db(base, 'games', 'users', f"{(await select_db(base, 'games', 'id_game'))[1]} {user_id}", 'id_game')
		await msg.answer(peer_id=msg.peer_id, message=f'&#128279; >> Вы присоеденились к лобби {base}!')
	users = (await select_db(base, 'games', 'id_game'))[1]
	users = users.split(' ')
	if len(users) == 5:
		await run_game(base, peer_id, user_id, msg)

# connection to VK
bot = Bot(token=tokens.tg1[0])

# main cycle
@bot.on.chat_message()
async def chat_handler(msg: Message):
	try:
		user_id = msg.from_id
		msge = msg.text
		peer_id = msg.peer_id
	except Exception as E:
		user_id = 'None'
		msge = 'None'
		peer_id = 'None'
		print(f'ERROR: {errors.get(1)} or {errors.get(5)}, description: {E}')
	msge = str(msge)
	try:
		print(f'Text message: {msge}')
	except:
		print(f'ERROR: {errors.get(1)} or {errors.get(4)}')
	print(f'User id: {user_id}')
	print(f'Peer id: {peer_id}')

	await check_reg(msg.from_id)

	try:
		game = (await select_db(msg.from_id, 'users', 'user_id'))[1]
	except Exception as E:
		print(f'Error: {errors.get(2)}, description: \n{E}')

	try:
		if (await select_db(game, 'games', 'id_game'))[2] >= 90:
			await delete_game(game)
			await msg.answer(peer_id=msg.peer_id, message=f'&#127987; >> Члены экипажа победили!')
			return
		if msg.lower() in commands and (await select_db(msg.from_id, f'game_{game}', 'user_id'))[14] == 0:
			await msg.answer(peer_id=msg.peer_id, message=f'&#128481; >> Вы были убиты!')
			return
	except Exception as E:
		print(f'ERROR: {errors.get(1)} or {errors.get(2)}, description: \n{E}')

	if msg.text.lower() == 'создать лобби':
		if str((await select_db(msg.from_id, 'users', 'user_id'))[1]) == '0':
			await create_game((await get_id_game()), msg.from_id, msg.peer_id, msg.chat_id, msg)
		else:
			await msg.answer(peer_id_id=msg.peer_id, message=f'Вы уже играете!')
			return

	#elif msg.text == 'c':
	#	await msg.answer(chat_id=msg.chat_id, message=msg.chat_id)

	elif (msg.text.lower().startswith('[club193680681|@amoungusgamebot]') or
		  msg.text.lower().startswith('[club190588465|@prosmandovkicalacha]')) and 'присоедениться к лобби' in msg.text.lower():
		if (await select_db(msg.from_id, 'users', 'user_id'))[1] == 0:
			base = msg.text[60:]
			print(base)
			await reg_in_game_lobbi(user_id, base, peer_id, msg)
		else:
			await msg.answer(peer_id=msg.peer_id, message=f'&#128219; >> Вы уже в игре!')
			return

	elif msg.text.lower() == '[club193680681|@amoungusgamebot] отмена' or msg.text.lower() == 'отмена':
		if (await select_db(user_id, 'users', 'user_id'))[1] == 0:
			await msg.answer(peer_id=msg.peer_id, message=f'&#128219; >> Вы и так не играете!')
			return
		if str(msg.from_id) == str((await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[16]):
			await delete_game((await select_db(msg.from_id, 'users', 'user_id'))[1])
			await update_db(msg.from_id, 'users', 'game', 0, 'user_id')
			await msg.answer(peer_id=msg.peer_id, message=f'&#10062; >> Вы отменили создание игры')
		else:
			await msg.answer(peer_id=msg.peer_id, message=f'&#128219; >> Вы не создатель игры!')
		return

@bot.on.message()
async def handler(msg: Message):
	try:
		user_id = msg.from_id
		msge = msg.text
		peer_id = msg.peer_id
	except Exception as E:
		user_id = 'None'
		msge = 'None'
		peer_id = 'None'
		print(f'ERROR: {errors.get(1)} or {errors.get(5)}, description: {E}')
	msge = str(msge)
	try:
		print(f'Text message: {msge}')
	except:
		print(f'ERROR: {errors.get(1)} or {errors.get(4)}')
	print(f'User id: {user_id}')
	print(f'Peer id: {peer_id}')

	await check_reg(msg.from_id)

	if msg.text.lower() == 'навигация':
		if (await select_db(user_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[7] != 0:
			await msg.answer(peer_id=msg.peer_id,
							 message=f'&#128219; >> Вы не можете попасть в эту комнату! Проходить можно только через столовую!')
			return
		await update_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'room', 1, 'user_id')
		rm2_u = (await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[5]
		rm1_u = str((await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[4])
		base = (await select_db(msg.from_id, 'users', 'user_id'))[1]
		if rm2_u is None:
			rm2_u = str(msg.from_id)
		else:
			rm2_u = f'{rm2_u} {msg.from_id}'
		rm1_u = rm1_u.split(' ')
		rm1_u.remove(str(msg.from_id))
		rm1_u = ' '.join(rm1_u)
		await update_db(base, 'games', 'room1', rm1_u, 'id_game')
		await update_db(base, 'games', 'room2', rm2_u, 'id_game')
		rm = (await select_db(base, 'games', 'id_game'))[5]
		rmzh = rm.split(' ')
		lud = ''
		rm = (await select_db(base, 'games', 'id_game'))[11]
		rmdm = rm.split(' ')
		dlud = ''
		for i in rmzh:
			if i != 'Нет':
				lud = f'{lud} [id{i}|{(await get_name(i))}]'
			if len(rmzh) == 1 and 'Нет' in str(rmzh):
				lud = 'Нет'
		for i in rmdm:
			if i != 'Нет':
				dlud = f'{dlud} [id{i}|{(await get_name(i))}]'
			if len(rmdm) == 1 and 'Нет' in str(rmdm):
				dlud = 'Нет'
		await msg.answer(chat_id=(await select_db((await select_db(user_id, 'users', 'user_id'))[1], 'games', 'id_game'))[17],
						 message=f'&#128100; >> [id{msg.from_id}|{(await get_name(msg.from_id))}] перешел в: \n&#128752; >> Навигация')
		await msg.answer(user_id=msg.from_id,
						 message=f'\n&#128331; >> В комнате: \n&#10084; >> Живые: \n{lud}\n&#128420; >> Трупы: \n{dlud} \n&#128221; >> Доступные действия: ',
						 keyboard=(await room2(msg.from_id)))
		return

	elif msg.text.lower() == 'столовая':
		rm2_u = (await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[4]
		rm1_u = str((await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[
						4 + int((await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[7])])
		print(rm1_u)
		base = await (select_db(msg.from_id, 'users', 'user_id')[1])
		if rm2_u == 'Нет':
			rm2_u = str(msg.from_id)
		else:
			rm2_u = f'{rm2_u} {msg.from_id}'
		rm1_u = rm1_u.split(' ')
		print('rm2', rm2_u)
		print(rm1_u)
		print(str(msg.from_id))
		rm1_u1 = list()
		for i in rm1_u:
			if i != str(msg.from_id):
				rm1_u1.append(i)
		await update_db(base, 'games', 'room1', rm2_u, 'id_game')
		await update_db(base, 'games', 'room2', ' '.join(rm1_u1), 'id_game')
		await update_db(user_id, f'game_{(await select_db(user_id, "users", "user_id"))[1]}', 'room', 0, 'user_id')
		rm = (await select_db(base, 'games', 'id_game'))[4]
		rmzh = rm.split(' ')
		lud = ''
		rm = (await select_db(base, 'games', 'id_game'))[10]
		rmdm = rm.split(' ')
		dlud = ''
		for i in rmzh:
			if i != 'Нет':
				lud = f'{lud} [id{i}|{(await get_name(i))}]'
			if len(rmzh) == 1 and 'Нет' in str(rmzh):
				lud = 'Нет'
		for i in rmdm:
			if i != 'Нет':
				dlud = f'{dlud} [id{i}|{(await get_name(i))}]'
			if len(rmdm) == 1 and 'Нет' in str(rmdm):
				dlud = 'Нет'
		await msg.answer(chat_id=(await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[17],
						 message=f'&#128100; >> [id{msg.from_id}|{(await get_name(msg.from_id))}] перешел в: \n&#127869; >> Столовая')
		await msg.answer(user_id=msg.from_id,
						 message=f'\n&#128331; >> В комнате: \n&#10084; >> Живые: \n{lud}\n&#128420; >> Трупы: \n{dlud} \n&#128221; >> Доступные действия: ',
						 keyboard=(await room1(msg.from_id)))
		return

	elif msg.text.lower() == 'оружейная':
		if (await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[7] != 0:
			await msg.answer(peer_id=msg.peer_id,
							 message=f'Вы не можете попасть в эту комнату! Проходить можно только через столовую!')
			return
		await update_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'room', 2, 'user_id')
		rm2_u = (await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[5]
		rm1_u = str((await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[4])
		base = (await select_db(msg.from_id, 'users', 'user_id'))[1]
		if rm2_u is None:
			rm2_u = str(msg.from_id)
		else:
			rm2_u = f'{rm2_u} {msg.from_id}'
		rm1_u = rm1_u.split(' ')
		rm1_u.remove(str(msg.from_id))
		print('rm2', rm2_u)
		print(rm1_u)
		print(str(msg.from_id))
		rm1_u = ' '.join(rm1_u)
		await update_db(base, 'games', 'room1', rm1_u, 'id_game')
		await update_db(base, 'games', 'room3', rm2_u, 'id_game')
		rm = (await select_db(base, 'games', 'id_game'))[6]
		rmzh = rm.split(' ')
		lud = ''
		rm = (await select_db(base, 'games', 'id_game'))[12]
		rmdm = rm.split(' ')
		dlud = ''
		for i in rmzh:
			if i != 'Нет':
				lud = f'{lud} [id{i}|{(await get_name(i))}]'
			if len(rmzh) == 1 and 'Нет' in str(rmzh):
				lud = 'Нет'
		for i in rmdm:
			if i != 'Нет':
				dlud = f'{dlud} [id{i}|{(await get_name(i))}]'
			if len(rmdm) == 1 and 'Нет' in str(rmdm):
				dlud = 'Нет'
		await msg.answer(chat_id=(await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[17],
						 message=f'&#128100; >> [id{msg.from_id}|{(await get_name(msg.from_id))}] перешел в: \n&#9876; >> Оружейная')
		await msg.answer(user_id=msg.from_id,
						 message=f'\n&#128331; >> В комнате: \n&#10084; >> Живые: \n{lud}\n&#128420; >> Трупы: \n{dlud} \n&#128221; >> Доступные действия: ',
						 keyboard=(await room3(msg.from_id)))
		return

	elif msg.text.lower() == 'топливо':
		if (await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[7] != 0:
			await msg.answer(peer_id=msg.from_id,
							 message=f'Вы не можете попасть в эту комнату! Проходить можно только через столовую!')
			return
		await update_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'room', 3, 'user_id')
		rm2_u = (await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[5]
		rm1_u = str((await select_db(await select_db(msg.from_id, 'users', 'user_id')[1], 'games', 'id_game'))[4])
		base = (await select_db(msg.from_id, 'users', 'user_id'))[1]
		if rm2_u is None:
			rm2_u = str(msg.from_id)
		else:
			rm2_u = f'{rm2_u} {msg.from_id}'
		rm1_u = rm1_u.split(' ')
		rm1_u.remove(str(msg.from_id))
		rm1_u = ' '.join(rm1_u)
		await update_db(base, 'games', 'room1', rm1_u, 'id_game')
		await update_db(base, 'games', 'room4', rm2_u, 'id_game')
		rm = (await select_db(base, 'games', 'id_game'))[7]
		rmzh = rm.split(' ')
		lud = ''
		rm = (await select_db(base, 'games', 'id_game'))[13]
		rmdm = rm.split(' ')
		dlud = ''
		for i in rmzh:
			if i != 'Нет':
				lud = f'{lud} [id{i}|{(await get_name(i))}]'
			if len(rmzh) == 1 and 'Нет' in str(rmzh):
				lud = 'Нет'
		for i in rmdm:
			if i != 'Нет':
				dlud = f'{dlud} [id{i}|{(await get_name(i))}]'
			if len(rmdm) == 1 and 'Нет' in str(rmdm):
				dlud = 'Нет'
		await msg.answer(chat_id=(await select_db(await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game')[17],
						 message=f'&#128100; >> [id{msg.from_id}|{(await get_name(msg.from_id))}] перешел в: \n&#9981; >> Топливо')
		await msg.answer(user_id=msg.from_id,
						 message=f'\n&#128331; >> В комнате: \n&#10084; >> Живые: \n{lud}\n&#128420; >> Трупы: \n{dlud} \n&#128221; >> Доступные действия: ',
						 keyboard=(await room4(msg.from_id)))
		return

	elif msg.text.lower() == 'верхний двигатель':
		if (await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[7] != 0:
			await msg.answer(peer_id=msg.peer_id, message=f'Вы не можете попасть в эту комнату!')
			return
		await update_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'room', 4, 'user_id')
		rm2_u = (await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[5]
		rm1_u = str((await select_db((await select_db(user_id, 'users', 'user_id'))[1], 'games', 'id_game'))[4])
		base = (await select_db(user_id, 'users', 'user_id'))[1]
		if rm2_u is None:
			rm2_u = str(msg.from_id)
		else:
			rm2_u = f'{rm2_u} {msg.from_id}'
		rm1_u = rm1_u.split(' ')
		rm1_u.remove(str(msg.from_id))
		rm1_u = ' '.join(rm1_u)
		await update_db(base, 'games', 'room1', rm1_u, 'id_game')
		await update_db(base, 'games', 'room5', rm2_u, 'id_game')
		rm = (await select_db(base, 'games', 'id_game'))[8]
		rmzh = rm.split(' ')
		lud = ''
		rm = (await select_db(base, 'games', 'id_game'))[14]
		rmdm = rm.split(' ')
		dlud = ''
		for i in rmzh:
			if i != 'Нет':
				lud = f'{lud} [id{i}|{(await get_name(i))}]'
			if len(rmzh) == 1 and 'Нет' in str(rmzh):
				lud = 'Нет'
		for i in rmdm:
			if i != 'Нет':
				dlud = f'{dlud} [id{i}|{(await get_name(i))}]'
			if len(rmdm) == 1 and 'Нет' in str(rmdm):
				dlud = 'Нет'
		await msg.answer(chat_id=(await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[17],
						 message=f'&#128100; >> [id{msg.from_id}|{(await get_name(msg.from_id))}] перешел в: \n&#128640; >> Верхний двигатель')
		await msg.answer(user_id=msg.from_id,
						 message=f'\n&#128331; >> В комнате: \n&#10084; >> Живые: \n{lud}\n&#128420; >> Трупы: \n{dlud} \n&#128221; >> Доступные действия: ',
						 keyboard=(await room5(msg.from_id)))
		return

	elif msg.text.lower() == 'нижний двигатель':
		if (await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[7] != 0:
			await msg.answer(peer_id=msg.peer_id,
							 message='Вы не можете попасть в эту комнату! Проходить можно только через столовую!')
			return
		await update_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'room', 5, 'user_id')
		rm2_u = (await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[5]
		rm1_u = str((await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[4])
		base = (await select_db(msg.from_id, 'users', 'user_id'))[1]
		if rm2_u is None:
			rm2_u = str(msg.from_id)
		else:
			rm2_u = f'{rm2_u} {msg.from_id}'
		rm1_u = rm1_u.split(' ')
		rm1_u.remove(str(msg.from_id))
		rm1_u = ' '.join(rm1_u)
		await update_db(base, 'games', 'room1', rm1_u, 'id_game')
		await update_db(base, 'games', 'room6', rm2_u, 'id_game')
		rm = (await select_db(base, 'games', 'id_game'))[9]
		rmzh = rm.split(' ')
		lud = ''
		rm = (await select_db(base, 'games', 'id_game'))[15]
		rmdm = rm.split(' ')
		dlud = ''
		for i in rmzh:
			if i != 'Нет':
				lud = f'{lud} [id{i}|{(await get_name(i))}]'
			if len(rmzh) == 1 and 'Нет' in str(rmzh):
				lud = 'Нет'
		for i in rmdm:
			if i != 'Нет':
				dlud = f'{dlud} [id{i}|{(await get_name(i))}]'
			if len(rmdm) == 1 and 'Нет' in str(rmdm):
				dlud = 'Нет'
		await msg.answer(chat_id=(await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[17],
						 message=f'&#128100; >> [id{msg.from_id}|{(await get_name(msg.from_id))}] перешел в: \n&#128640; >> Нижний двигатель')
		await msg.answer(user_id=msg.from_id,
						 message=f'\n&#128331; >> В комнате: \n&#10084; >> Живые: \n{lud}\n&#128420; >> Трупы: \n{dlud} \n&#128221; >> Доступные действия: ',
						 keyboard=(await room6(msg.from_id)))
		return

	elif msg.text.lower() == 'указать путь':
		navig_time = round(time.time()) - (await select_db(msg.from_id, f'game_{(await select_db(msg.text, "users", "user_id"))[1]}', 'user_id'))[11]
		if (await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[4] == 2:
			await msg.answer(user_id=msg.from_id, message=f'&#128219; >> Вы уже указали путь корабля!')
			return
		elif navig_time < 15:
			await msg.answer(user_id=msg.from_id,
							 message=f"&#128219; >> Вы уже указывали путь корабля! \n&#9201; >> Вы сможете указать путь через {datetime.timedelta(seconds=int(navig_time))}")
			return
		else:
			await update_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'state_spaceship',
					  int((await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[2] + 2, 'id_game'))
			await update_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'navig',
					  (await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[4] + 1,
					  'user_id')
			await update_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'navig_time', round(time.time()),
					  'user_id')
			await msg.answer(user_id=msg.from_id,
							 message=f"&#128752; >> Вы направили корабль! \n&#128267; >> Состояние корабля: {(await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[2]}")
	elif msg.text.lower() == 'уничтожить камни':
		kamen_time = round(time.time()) - \
					 (await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[12]
		if (await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[5] == 2:
			await msg.answer(user_id=msg.from_id, message=f'&#128219; >> Вы уже разбили все камни!')
			return
		elif kamen_time < 15:
			await msg.answer(user_id=msg.from_id,
							 message=f"&#128219; >> Вы уже разбивали камни! \n&#9201; >> Вы сможете разбить камни через {datetime.timedelta(seconds=int(kamen_time))}")
			return
		else:
			await update_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'state_spaceship',
					  int((await select_db((await select_db(msg.from_id, 'users', 'user_id')[1]), 'games', 'id_game'))[2]) + 2, 'id_game')
			await update_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'kamni',
					  (await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[5] + 1,
					  'user_id')
			await update_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'kamni_time', round(time.time()),
					  'user_id')
			await msg.answer(user_id=msg.from_id,
							 message=f"&#9732; >> Вы разбили камни! \n&#128267; >> Состояние корабля: {(await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[2]}")

	elif msg.text.lower() == 'заправить бак':
		fill_time = round(time.time()) - \
					(await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[13]
		if (await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[6] == 2:
			await msg.answer(user_id=msg.from_id, message=f'&#128219; >> Вы уже полностью заправили бак!')
			return
		elif fill_time < 15:
			await msg.answer(user_id=msg.from_id,
							 message=f"&#128219; >> Вы уже заправляли бак! \n&#9201; >> Вы сможете заправить корабль через {datetime.timedelta(seconds=int(fill_time))}")
			return
		else:
			await update_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'state_spaceship',
					  int((await select_db((await select_db(msg.from_id, 'users', 'user_id')[1]), 'games', 'id_game'))[2]) + 2, 'id_game')
			await update_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'fuel',
					  (await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[6] + 1,
					  'user_id')
			await update_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'fuel_time', round(time.time()),
					  'user_id')
			await msg.answer(user_id=msg.from_id,
							 message=f"&#9981; >> Вы заправили бак! \n&#128267; >> Состояние корабля: {(await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[2]}")

	elif msg.text.lower() == 'починить двигатель 1':
		fill_time = round(time.time()) - \
					(await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[9]
		if (await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[2] == 2:
			await msg.answer(user_id=msg.from_id, message=f'&#128219; >> Вы уже починили первый двигатель!')
			return
		elif fill_time < 15:
			await msg.answer(user_id=msg.from_id,
							 message=f"&#128219; >> Вы уже чинили первый двигатель! \n&#9201; >> Вы сможете проверить его через {datetime.timedelta(seconds=int(fill_time))}")
			return
		else:
			await update_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'state_spaceship',
					  int((await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[2]) + 2, 'id_game')
			await update_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'dvig1',
					  (await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[2] + 1,
					  'user_id')
			await update_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'dvig1_time', round(time.time()),
					  'user_id')
			await msg.answer(user_id=msg.from_id,
							 message=f"&#128640; >> Вы починили первый двигатель! \n&#128267; >> Состояние корабля: {(await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[2]}")

	elif msg.text.lower() == 'починить двигатель 2':
		fill_time = round(time.time()) - \
					(await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[10]
		if (await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[3] == 2:
			await msg.answer(user_id=msg.from_id, message=f'&#128219; >> Вы уже починили второй двигатель!')
			return
		elif fill_time < 15:
			await msg.answer(user_id=msg.from_id,
							 message=f"&#128219; >> Вы уже чинили второй двигатель! \n&#9201; >> Вы сможете проверить его через {datetime.timedelta(seconds=int(fill_time))}")
			return
		else:
			await update_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'state_spaceship',
					  int((await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[2]) + 2, 'id_game')
			await update_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'dvig2',
					  (await select_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'user_id'))[3] + 1,
					  'user_id')
			await update_db(msg.from_id, f'game_{(await select_db(msg.from_id, "users", "user_id"))[1]}', 'dvig2_time', round(time.time()),
					  'user_id')
			await msg.answer(user_id=msg.from_id,
							 message=f"&#128640; >> Вы починили второй двигатель! \n&#128267; >> Состояние корабля: {(await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[2]}")

	elif msg.text.lower() == 'убить':
		dead_body = (await kill((await select_db(msg.from_id, "users", "user_id"))[1], msg.from_id))
		await msg.answer(peer_id=msg.peer_id, message=f'&#128481; >> Вы убили игрока [id{dead_body}|{(await get_name(dead_body))}]')
		await msg.answer(user_id=int(dead_body), message=f'&#128481; >> Вы были убиты!')

	elif msg.text.lower() == 'репорт':
		await update_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'state_game_vote', 1, 'id_game')
		users = str((await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[1])
		users = users.split(' ')
		print(users)
		id_users = []
		game = (await select_db(user_id, "users", "user_id"))[1]
		for i in users:
			if (await select_db(i, f'game_{game}', 'user_id'))[14] == 1:
				id_users.append((await select_db(i, f'game_{game}', 'user_id'))[0])
			else:
				print(errors.get(3))
		print(id_users)
		name_and_id = []
		for i in id_users:
			name_and_id.append(
				f'{i}. [id{(await select_db(i, f"game_{game}", "id"))[1]}|{(await get_name((await select_db(i, f"game_{game}", "id"))[1]))}]')
		name_and_id = ' '.join(name_and_id)
		await msg.answer(chat_id=(await select_db((await select_db(msg.from_id, 'users', 'user_id'))[1], 'games', 'id_game'))[17],
						 message=f'&#128101; >> Все участники по номерам: \n{name_and_id} \n&#128202; >> И так! Голосование: ',
						 keyboard=(await get_button(inline=True, buts=[[{"label": "1", "type": "text", "color": 'primary'},
															 {"label": "2", "type": "text", "color": 'primary'}],
															[{"label": "3", "type": "text", "color": 'primary'},
															 {"label": "4", "type": "text", "color": 'primary'}],
															[{"label": "5", "type": "text", "color": 'primary'}]])))

	elif msg.text.lower() == '[club193680681|@amoungusgamebot] 1' or msg.text.lower() == '[club193680681|@amoungusgamebot] 2' or msg.text.lower() == '[club193680681|@amoungusgamebot] 3' or msg.text.lower() == '[club193680681|@amoungusgamebot] 4' or msg.text.lower() == '[club193680681|@amoungusgamebot] 5':
		game = (await select_db(msg.from_id, 'users', 'user_id'))[1]
		if (await select_db(game, 'games', 'id_game'))[18] == 0:
			await msg.answer(chat_id=(await select_db(game, 'games', 'id_game'))[17],
							 message=f'&#128219; >> Голосование не запущенно!')
			return
		elif (await select_db(msg.from_id, f'game_{game}', 'user_id'))[16] == 1:
			await msg.answer(chat_id=(await select_db(game, 'games', 'id_game'))[17], message=f'&#128219; >> Вы уже голосовали!')
			return
		else:
			man_id = msg.text.lower()[33:]
			print('man_id', man_id)
			state_life = (await select_db(man_id, f'game_game', 'id'))[14]
			if state_life == 0:
				await msg.answer(peer_id=msg.peer_id, message=f'&#128219; >> Этот юзер уже убит!')
				return
			await update_db(man_id, f'game_{game}', 'against', (await select_db(man_id, f'game_{game}', 'id'))[15] + 1, 'id')
			await update_db(msg.from_id, f'game_{game}', 'state_voice', 1, 'user_id')
			await update_db(game, 'games', 'number_votes', (await select_db(game, 'games', 'id_game'))[19] + 1, 'id_game')
			await msg.answer(chat_id=(await select_db(game, 'games', 'id_game'))[17],
							 message=f'&#128229; >> [id{msg.from_id}|{(await get_name(msg.from_id))}] проголосовал за [id{(await select_db(man_id, f"game_{game}", "id"))[1]}|{(await get_name((await select_db(man_id, f"game_{game}", "id"))[1]))}]')
			if (await select_db(game, 'games', 'id_game'))[19] == 3:
				selectinfoondb = c.execute(f'SELECT * FROM game_{game}')
				res = c.fetchall()
				print('res', res)
				datb = {}
				for i in res:
					datb[i[0]] = [i[15], i[0]]
				print('datb', datb)
				p = -1
				top_dict = {}
				for k in range(0, 3):
					print(k)
					top = sorted(datb.values(), reverse=True)
					print('top', top)
					top_dict[top[k][1]] = top[k][0]
				print('top_dict', top_dict)
				manid = []
				for i in top_dict.keys():
					print('i', i)
					manid.append(i)
				print('manid, list', manid)
				if manid[0] == manid[1]:
					await msg.answer(peer_id=msg.peer_id, message=f'&#128202; >> Единого решения принято не было!')
					await update_db(game, 'games', 'state_game_vote', 0, 'id_game')
					await update_db(game, 'games', 'number_votes', 0, 'id_game')
					for i in range(1, 5):
						await update_db(i, f'game_{game}', 'against', 0, 'id')
						await update_db(i, f'game_{game}', 'state_voice', 0, 'id')
					await msg.answer(peer_id=msg.peer_id, message=f'&#9654; >> Продолжаем игру!')
					return
				else:
					await update_db(manid[0], f'game_{game}', 'state_life', 0, 'id')
					await update_db(game, 'games', 'state_game_vote', 0, 'id_game')
					await update_db(game, 'games', 'number_votes', 0, 'id_game')
					for i in range(1, 5):
						await update_db(i, f'game_{game}', 'against', 0, 'id')
						await update_db(i, f'game_{game}', 'state_voice', 0, 'id')
					await msg.answer(peer_id=msg.peer_id,
									 message=f'&#128202; >> Было принято решение изгнать [id{(await select_db(manid[0], f"game_{game}", "id"))[1]}|{(await get_name((await select_db(manid[0], f"game_{game}", "id"))[1]))}]')
					life_man = 0
					if str(msg.from_id) == str((await select_db(game, 'games', 'id_game'))[3]):
						await msg.answer(chat_id=(await select_db(game, 'games', 'id_game')[17]),
										 message=f'&#127937; >> Победили члены экипажа! \n&#128481; >> Импостером оказался - [id{(await select_db(game, "games", "id_game"))[3]}|{(await get_name((await select_db(game, "games", "id_game"))[3]))}]')
						await delete_game(game)
						return
					for i in range(1, 5):
						if (await select_db(i, f'game_{game}', 'id'))[14] == 1:
							life_man += 1
					if life_man <= 2:
						await msg.answer(chat_id=(await select_db(game, 'games', 'id_game'))[17],
										 message=f'&#127937; >> Игра окончена! \n&#128481; >> Победил [id{(await (game, f"game_{game}", "games")[3])}|Импостер]!')
					await delete_game(game)
					return

	elif msg.text.lower() == '[club193680681|@amoungusgamebot] 1' or msg.text.lower() == '[club193680681|@amoungusgamebot] 2' or msg.text.lower() == '[club193680681|@amoungusgamebot] 3' or msg.text.lower() == '[club193680681|@amoungusgamebot] 4' or msg.text.lower() == '[club193680681|@amoungusgamebot] 5':
		game = (await select_db(msg.from_id, 'users', 'user_id'))[1]
		if (await select_db(game, 'games', 'id_game'))[18] == 0:
			await msg.answer(chat_id=(await select_db(game, 'games', 'id_game'))[17],
							 message=f'&#128219; >> Голосование не запущенно!')
			return
		elif (await select_db(msg.from_id, f'game_{game}', 'user_id'))[16] == 1:
			await msg.answer(chat_id=(await select_db(game, 'games', 'id_game'))[17], message=f'&#128219; >> Вы уже голосовали!')
			return
		else:
			man_id = msg.text.lower()[0:]
			print('man_id', man_id)
			state_life = (await select_db(man_id, f'game_game', 'id'))[14]
			if state_life == 0:
				await msg.answer(peer_id=msg.peer_id, message=f'&#128219; >> Этот юзер уже убит!')
				return
			await update_db(man_id, f'game_{game}', 'against', (await select_db(man_id, f'game_{game}', 'id'))[15] + 1, 'id')
			await update_db(msg.from_id, f'game_{game}', 'state_voice', 1, 'user_id')
			await update_db(game, 'games', 'number_votes', (await select_db(game, 'games', 'id_game'))[19] + 1, 'id_game')
			await msg.answer(chat_id=(await select_db(game, 'games', 'id_game'))[17],
							 message=f'&#128229; >> [id{msg.from_id}|{(await get_name(msg.from_id))}] проголосовал за [id{(await select_db(man_id, f"game_{game}", "id"))[1]}|{(await get_name((await select_db(man_id, f"game_{game}", "id"))[1]))}]')
			if (await select_db(game, 'games', 'id_game'))[19] == 3:
				selectinfoondb = c.execute(f'SELECT * FROM game_{game}')
				res = c.fetchall()
				print('res', res)
				datb = {}
				for i in res:
					datb[i[0]] = [i[15], i[0]]
				print('datb', datb)
				p = -1
				top_dict = {}
				for k in range(0, 3):
					print(k)
					top = sorted(datb.values(), reverse=True)
					print('top', top)
					top_dict[top[k][1]] = top[k][0]
				print('top_dict', top_dict)
				manid = []
				for i in top_dict.keys():
					print('i', i)
					manid.append(i)
				print('manid, list', manid)
				if manid[0] == manid[1]:
					await msg.answer(peer_id=msg.peer_id, message=f'&#128202; >> Единого решения принято не было!')
					await update_db(game, 'games', 'state_game_vote', 0, 'id_game')
					await update_db(game, 'games', 'number_votes', 0, 'id_game')
					for i in range(1, 5):
						await update_db(i, f'game_{game}', 'against', 0, 'id')
						await update_db(i, f'game_{game}', 'state_voice', 0, 'id')
					await msg.answer(peer_id=msg.peer_id, message=f'&#9654; >> Продолжаем игру!')
					return
				else:
					await update_db(manid[0], f'game_{game}', 'state_life', 0, 'id')
					await update_db(game, 'games', 'state_game_vote', 0, 'id_game')
					await update_db(game, 'games', 'number_votes', 0, 'id_game')
					for i in range(1, 5):
						await update_db(i, f'game_{game}', 'against', 0, 'id')
						await update_db(i, f'game_{game}', 'state_voice', 0, 'id')
					await msg.answer(peer_id=msg.peer_id,
									 message=f'&#128202; >> Было принято решение изгнать [id{(await select_db(manid[0], f"game_{game}", "id"))[1]}|{(await get_name((await select_db(manid[0], f"game_{game}", "id"))[1]))}]')
					life_man = 0
					if str(msg.from_id) == str((await select_db(game, 'games', 'id_game'))[3]):
						await msg.answer(chat_id=(await select_db(game, 'games', 'id_game')[17]),
										 message=f'&#127937; >> Победили члены экипажа! \n&#128481; >> Импостером оказался - [id{(await select_db(game, "games", "id_game"))[3]}|{(await get_name((await select_db(game, "games", "id_game"))[3]))}]')
						await delete_game(game)
						return
					for i in range(1, 5):
						if (await select_db(i, f'game_{game}', 'id'))[14] == 1:
							life_man += 1
					if life_man <= 2:
						await msg.answer(chat_id=(await select_db(game, 'games', 'id_game'))[17],
										 message=f'&#127937; >> Игра окончена! \n&#128481; >> Победил [id{(await (game, f"game_{game}", "games")[3])}|Импостер]!')
					await delete_game(game)
					return

	elif msg.text.lower() == 'выход из игры':
		game = (await select_db(msg.from_id, 'users', 'user_id'))[1]
		if str(msg.from_id) == str((await select_db(game, 'games', 'id_game'))[3]):
			await msg.answer(chat_id=(await select_db(game, "games", "id_game"))[17],
							 message=f'&#127987; >> Победили члены экипажа! [id{(await select_db(game, "games", "id_game"))[3]}|Предатель] вышел из игры!')
			await delete_game(game)
			await msg.answer(user_id=msg.from_id, message=f'Вы вышли из игры!')
			return
		if str(msg.from_id) == str((await select_db(game, 'games', 'id_game'))[16]):
			await msg.answer(chat_id=(await select_db(game, "games", "id_game"))[17],
							 message=f'&#128219; >> Создатель комнаты вышел из игры!')
			await delete_game(game)
			await msg.answer(user_id=msg.from_id, message=f'&#10062; >> Вы вышли из игры!')
			return
		users = str((await select_db(game, 'games', 'id_game'))[1])
		users = users.split(' ')
		users.remove(str(msg.from_id))
		users = ' '.join(users)
		await update_db(game, 'games', 'users', users, 'id_game')
		c.execute(f'DELETE FROM game_{game} WHERE user_id={msg.from_id}')
		connbd.commit()
		await update_db(msg.from_id, 'users', 'game', 0, 'user_id')
		await msg.answer(user_id=msg.from_id, message=f'&#10062; >> Вы вышли из игры!')
		await msg.answer(chat_id=(await select_db(game, "games", "id_game"))[17], message=f'[id{msg.from_id}|Игрок] вышел из игры!')
		return

	elif msg.text.lower() == 'помощь' or msg.text.lower() == 'меню' or msg.text.lower() == 'команды' or msg.text.lower() == 'начать' or msg.text.lower() == 'привет':
		await msg.answer(peer_id=msg.peer_id,
						 message='ДЛЯ ИГРЫ НАДО НАПИСАТЬ В ЛИЧКУ БОТУ ХОТЯ БЫ 1 РАЗ ЛЮБОЕ СООБЩЕНЕ '
                                 '\n Также для игры пригодится беседа с минимум 5 людьми '
                                 '\n Походу игры в функционале можно разобраться '
                                 '\n Команды бота: '
                                 '\n Создать лобби - создает игру '
                                 '\n Отмена - удаляет игру '
                                 '\n Выход из игры - вы выходите из игры '
                                 '\n остальные команды можно найти по ходу игры!')
		return

	elif msg.text.lower() == 'создать лобби' or msg.text.lower() == 'отмена':
		await msg.answer(message=f'Эта команда работает только в беседах!')
		return 

if __name__ == '__main__':
	bot.run_forever()