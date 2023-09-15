from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import aiogram.utils.markdown as fmt
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.exceptions as aiogram_exceptions
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import logging
import time


storage = MemoryStorage()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token='6201369528:AAHmBXf4g0o-WDmw0S3bJiuhu8AfFu_04XE')
dp = Dispatcher(bot, storage=storage)


QUESTIONS = []

with open("questions.txt", "r") as file:
    for line in file:
        question = line.strip()
        QUESTIONS.append(question)


RESULTS = ['''Вы - счастливчик, процветаете и всё, что вам нужно, просто продолжать делать то, что делаете и жить так, как вы живете… 
Если баллы ближе к 15ти, то вы можете проанализировать свои ежедневные привычки (что вас выбивает из колеи, что помогает держаться на плаву). Также хорошо заботиться о качестве сна, принимаемой пищи и обеспечить достаточный уровень движения в течение дня (любой вид движения или спорта, что вам по душе), уделить внимание вдумчивому началу дня. Чем выше баллы (14-15), тем более вероятно, что сейчас идет активная адаптация к стрессу. Вы встречаетесь с вызовами, это нормально, ваш организм активно пытается приспособиться. Беспокоиться не о чем, но при этом уже пора предпринимать шаги для самопомощи. Если вы хотите знать больше, понимать как и что можно сделать с точки зрения профилактики и большей стрессоустойчивости, получить рекомендации по режиму дня, питанию, то записывайтесь на <a href="https://t.me/tankgirl2107">консультацию</a> и подписывайтесь на канал <a href="https://t.me/sparklive">Жить с огоньком!</a>''', 
           'Вы полны сил и энергии. Этакий электровеник. Куда бежать, за что хвататься. У вас ощущение энергии через край, но скорее всего вы чувствуете себя не лучшим образом. Возможно вы уже что-то не успеваете. Что-то забываете. Или, вдруг, пропустили важный dead line. В целом вы замечаете, что бываете невнимательны и рассеяны. Опасность в том, что вам кажется, что вы бодры и веселы и вы можете пропускать заботу о себе, меньше спать. Что ж, самые базовые рекомендации: меньше соли, меньше кофеина, ни в коем случае не пренебрегать сном, встречать утро с солнечными лучами, больше ходить, активная нагрузка утром, к вечеру замедляемся. Если вы хотите знать больше, понимать как и что можно сделать с точки зрения профилактики и большей стрессоустойчивости, получить рекомендации по режиму дня, питанию, то записывайтесь на <a href="https://t.me/tankgirl2107">консультацию</a> и подписывайтесь на канал <a href="https://t.me/sparklive">Жить с огоньком!</a>',
           'Пора обратиться за помощью! Вы на грани и тут вы можете не всегда адекватно оценивать свое состояние. Есть риски заболеть. Когда ежедневные ритмы не синхронизированы, вы можете столкнуться с парадоксальной комбинацией «напряжения и усталости». То вы бодры, то туман. Это приводит к состоянию постоянной усталости, неспособности заснуть, другим сложностям, даже если вы [пока] продуктивны на работе. Уровень энергии низок, даже если вы как-то пока держитесь. Мир враждебен, все что-то от вас хотят, а вы уже [не всегда] можете. Очень важны, критичны, границы, режим, расписание. Чем больше предсказуемости, тем лучше. Завтракать обязательно. Белок - да, углеводы лучше потом. Активное движение не более 2х раз в неделю и то ДО обеда. Если вы хотите знать больше, понимать как и что можно сделать с точки зрения профилактики и большей стрессоустойчивости, получить рекомендации по режиму дня, питанию, то записывайтесь на <a href="https://t.me/tankgirl2107">консультацию</a> и подписывайтесь на канал <a href="https://t.me/sparklive">Жить с огоньком!</a>',
           '''Истощение! Alarm! Сон есть, но он уже не восстанавливает. Нет сил, двигаться не хочется, делать ничего не хочется. Уже есть тревожные симптомы. Давление? Темнеет в глазах и/или кружится голова? Есть симптомы нарушения работы желудочно-кишечного тракта? Что ж… Пора передать дела и ответственность за дела другим. Хорошо “найти, где в жизни место подвигу, и держаться от него подальше»  (С. Майхилл). В идеале взять отпуск минимум на 7-10 дней или, хотя бы, дня три полежать. Представьте, что ваш родственник заболел, что вы ему посоветуете? Этот родственник - ВЫ! 
            Попросите помощи, делегируйте! Вам необходимы перерыв, помощь, забота. Если вы хотите знать больше, понимать как и что можно сделать с точки зрения профилактики и большей стрессоустойчивости, получить рекомендации по режиму дня, питанию, то записывайтесьна <a href="https://t.me/tankgirl2107">консультацию</a> и подписывайтесь на канал <a href="https://t.me/sparklive">Жить с огоньком!</a>''']

# Dictionary to store the state of each user's interaction with the bot
user_scores = {}

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=False)
markup.add("ни разу")
markup.add("раз в неделю или реже")
markup.add("Несколько раз в неделю или ежедневно")
markup.add("Несколько раз в день")
markup.add("Начать заново")

class Form(StatesGroup):
    text = State()
    result = State()

@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
        
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    
    await state.finish()
    
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text and 'Начать заново' in message.text)
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    greeting = '''Узнайте где вы сейчас в плане вашего стрессового отклика (опросник Алана Кристиансона). Примерно через 3 минуты вы узнаете, на какой стадии вы находитесь:

▪️ Процветание 
▪️ Стресс
▪️ Хронический стресс 
▪️ Выгорание 

После прохождения теста вы узнаете о некоторых практических шагах по образу жизни, которые можно предпринять для поддержки себя на каждом из этапов. Результаты вы получите сразу, конфиденциальность гарантирована.
'''


    markup = InlineKeyboardMarkup()
    #print(message.chat.id)
    #button2 = InlineKeyboardButton(text="❓ Мне нужна консультация по легализации", url=URL)
    button1 = InlineKeyboardButton(text="✅ начать тест", callback_data="test")
    markup.add(button1)
    #markup.add(button2)
    #print(user_scores)
    await bot.send_message(chat_id=message.chat.id, text=greeting, reply_markup=markup)

@dp.callback_query_handler()
async def process_callback_button_1(callback_query: CallbackQuery):
    global user_scores, markup
    
    if callback_query.data == "test":
        user_scores[f'{callback_query.from_user.id}'] = {'score': 0, 'question_number': 0}
        #print(user_scores)
        await bot.send_message(chat_id=callback_query.from_user.id, text='''Как часто вы замечали симптомы, которые последуют далее, за последнее время (несколько месяцев, месяц)?''')
        await Form.text.set()
        await bot.send_message(chat_id=callback_query.from_user.id, text=QUESTIONS[0], reply_markup=markup)
        

@dp.message_handler(state=Form.text)
async def process_text(message: types.Message, state: FSMContext):
    global user_scores, markup
    print(user_scores)
    #print(message)
    #print(user_scores[f'{message.chat.id}']['question_number'])
    question_number = user_scores[f'{message.chat.id}']['question_number']
    #print('question_number=', question_number)
    if question_number + 1 < len(QUESTIONS):
        if message.text == "Начать заново":
            await state.finish()
            await message.reply('Отменено', reply_markup=types.ReplyKeyboardRemove())

            markup_again = InlineKeyboardMarkup()
            button1 = InlineKeyboardButton(text="начнем тест с начала", callback_data="test")
            #button2 = InlineKeyboardButton(text="❓Мне все-таки нужна консультация по легализации", url=URL)
            markup_again.add(button1)
            #markup.add(button2)
            await bot.send_message(chat_id=message.chat.id, text="Что будем делать дальше?", reply_markup=markup_again)
        else:
            
            if message.text == 'ни разу':
                user_scores[f'{message.chat.id}']['question_number'] += 1
            if message.text == 'раз в неделю или реже':
                user_scores[f'{message.chat.id}']['score'] += 1
                user_scores[f'{message.chat.id}']['question_number'] += 1
            if message.text == 'Несколько раз в неделю или ежедневно':
                user_scores[f'{message.chat.id}']['score'] += 2
                user_scores[f'{message.chat.id}']['question_number'] += 1
            if message.text == 'Несколько раз в день':
                user_scores[f'{message.chat.id}']['score'] += 3
                user_scores[f'{message.chat.id}']['question_number'] += 1
            question_number += 1

            #if question_number > 0 and question_number < len(QUESTIONS) :
            try:
                await bot.send_message(chat_id=message.chat.id, text=QUESTIONS[question_number], reply_markup=markup)
            except:
            #else:
                pass
            
    else:
        await state.finish()
        await message.reply('Это был последний вопрос', reply_markup=types.ReplyKeyboardRemove())

        markup_again = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text="начнем тест с начала", callback_data="test")
        markup_again.add(button1)
        score = user_scores[f'{message.chat.id}']['score']

        await bot.send_message(chat_id=message.chat.id, text=f"Вы набрали {score} баллов.")
        if score < 16:
            await bot.send_message(chat_id=message.chat.id, text=RESULTS[0], reply_markup=markup_again, parse_mode=types.ParseMode.HTML)
        if score > 15 and score < 31:
            await bot.send_message(chat_id=message.chat.id, text=RESULTS[1], reply_markup=markup_again, parse_mode=types.ParseMode.HTML)
        if score > 30 and score < 46:
            await bot.send_message(chat_id=message.chat.id, text=RESULTS[2], reply_markup=markup_again, parse_mode=types.ParseMode.HTML)
        if score > 45:
            await bot.send_message(chat_id=message.chat.id, text=RESULTS[3], reply_markup=markup_again, parse_mode=types.ParseMode.HTML)
        
        
        #markup.add(button2)
        #await bot.send_message(chat_id=message.chat.id, text="Что будем делать дальше?", reply_markup=markup_again)
        

@dp.message_handler(state=Form.result)
async def process_result(message: types.Message, state: FSMContext):
    global user_scores
    await state.finish()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)

    markup.add("Начать заново")

    score = user_scores[f'{message.chat.id}']['score']
    await bot.send_message(chat_id=message.chat.id, text=f"Вы набрали {score} баллов", reply_markup=markup)


if __name__ == '__main__':
# Define your bot and other relevant code here
    while True:
        try:
            # Start your bot polling here
            executor.start_polling(dp, skip_updates=True)

        except aiogram_exceptions.RetryAfter as e:
            # Handle flood control errors here
            time.sleep(e.timeout)

        except aiogram_exceptions.TelegramAPIError as e:
            # Handle other Telegram API errors here
            print(f"Error: {e}")
            time.sleep(5)

        except Exception as e:
            # Handle all other exceptions here
            print(f"Unknown error: {e}")
            time.sleep(5)

        finally:
            # Stop your bot polling here
            executor.stop_polling()