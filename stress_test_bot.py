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
import config


storage = MemoryStorage()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=storage)


QUESTIONS = []

with open("questions.txt", "r") as file:
    for line in file:
        question = line.strip()
        QUESTIONS.append(question)


RESULTS = [
    """0-20 баллов. Что ж, вы - редкий счастливчик. Всё, что вам нужно, продолжать делать то, что делаете и жить так, как живете… Еще можете поделиться с другими, так как это весьма редко в наши времена, с чем поздравляю! Но чтобы еще чуть причинить добра, то вот рекомендации, если баллы 15 и выше. Проанализируйте свои ежедневные привычки на предмет того, что выбивает из колеи, а что помогает держаться на плаву. Первое оптимизировать, второе усилить. И фокус на базу: сон, движение, качество питания. Чем выше баллы, тем выше шанс, что ваш организм уже в легком стрессе и начал адаптацию, просто немного помогите себе. А если вы хотите понимать как и что можно сделать с точки зрения большей стрессоустойчивости, то записывайтесь на консультацию по <a href="https://t.me/+THRMWlFSEkw2NGEy">ссылке.</a>""",
    '21-40 баллов. Вы всё еще бодры и, возможно, даже веселы.  Энергии достаточно или даже много. Возможно, вы чувствуете, что готовы свернуть горы.  Но... вероятно, что есть первые звоночки усталости. Что-то вылетает из головы, где-то пропустили важный dead line. Невнимательность, сложность с концентрацией внимания тоже могут уже проявляться. Сложность этого периода в том, что на волне ощущения «бодры и веселы» вы можете пропускать заботу о себе, меньше спать, долго засиживаться за делами. И тут, конечно, первый фокус на базовые истории: сон, качество питания и движение. Что именно? Сон в достатке (вы лучше знаете сколько, но базовые рекомендации ложиться до 12:00 и спать 7-8 часов и больше, но не уходить в «запой» по 10-12 часов сна). Соли меньше, а кофеин в первой половине дня. Утром побыть на солнце минут 5-10 (не через окно) или, хотя бы, включить sad лампу. Больше ходить. Если активно тренируетесь, то лучше в первой половине дня, а к вечеру замедлиться. А если вы хотите понимать как и что можно сделать с точки зрения большей стрессоустойчивости, то записывайтесь на консультацию по <a href="https://t.me/+THRMWlFSEkw2NGEy">ссылке.</a>',
    '41-50 баллов. Ситуация сложная. Игнорировать нельзя! Может страдать адекватность оценки состояния. Есть риск заболеть. Спросите обратную связь у близких, как они видят вас, все ли Ок по их мнению? Уже идет разбалансировка ритмов и вы то бодры, то туман. Ощущение измотанности и состояние постоянной усталости. Возможно появились сложности со сном, хотя продуктивность на работе может быть еще вполне норм. Вы срываетесь по пустякам, ощущение небезопасности и враждебности мира и людей вокруг, близких, коллег. Вы можете хорошо держаться и даже гордиться этим, но ваше состояние опасно и пора позаботиться о себе! Что делать? Границы, режим, расписание! Чем более предсказуема ваша реальность, тем лучше. Особенно в базовых моментах: сон, движение, питание. Сон: засыпайте в одно и тоже время, лучше до 12:00 ночи, медитируйте до сна, спите 7-8 часов и дольше. Движение лучше размеренное, ходьба, йога. А если важно иметь активные занятия, то не более 2х раз в неделю и в первой половине дня. Питание: завтракайте, меньше соли, больше белка, кофе в первой половине дня и минимум. А если вы хотите понимать как и что можно сделать с точки зрения большей стрессоустойчивости, то записывайтесь на консультацию  по <a href="https://t.me/+THRMWlFSEkw2NGEy">ссылке.</a>',
    """51 балл и выше… Истощение! Alarm! Мало что помогает. Сил мало, делать ничего не хочется. Возможно, уже есть физиологические сбои. Давление? Темнеет в глазах? Болит голова? Есть симптомы нарушения работы желудочно-кишечного тракта? Что ж… Чемодан. Вокзал. СПА! В идеале взять отпуск минимум на 7-10 дней или, хотя бы, дня три, пожалуйста. Важно в эти дни не начать переделывать все дела, что вы не успели сделать пока работали, а уехать, уединиться. Не можете? Ну, возьмите хотя бы ДЕНЬ, но уедьте из дома, долго медленно гуляйте, да просто лежите и смотрите вдаль, лучше на виды природы, а не в телевизор. Любые источники информации оптимально исключить, включая тв, книги, радио… если никак, оставьте спокойную музыку, не более. Дела делегируйте! Помощь просите и берите. А если вы хотите понимать как и что можно сделать с точки зрения большей стрессоустойчивости, то записывайтесь на консультацию  по <a href="https://t.me/+THRMWlFSEkw2NGEy">ссылке.</a>""",
]

# Dictionary to store the state of each user's interaction with the bot
user_scores = {}

markup = types.ReplyKeyboardMarkup(
    resize_keyboard=True, selective=True, one_time_keyboard=False
)
markup.add("Никогда")
markup.add("Иногда")
markup.add("Часто")
markup.add("Очень часто, почти всегда")
markup.add("Начать заново")


class Form(StatesGroup):
    text = State()
    result = State()


@dp.message_handler(state="*", commands="cancel")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)

    await state.finish()

    await message.reply("Cancelled.", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text and "Начать заново" in message.text)
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    greeting = """Здравствуйте, меня зовут Лара Марченко, я автор канала по <a href="https://t.me/laramarchenko">Career Upgrade</a>, где можно узнать про то, как найти себя, работу и себя на работе, а еще много интересного про карьеру, спорт и котиков…

Хорошо, когда ваши жизнь и карьера (работа, дело) уравновешены, стресс, если и есть, то здоровый и адаптивный, нет выгорания!

Ниже тест, благодаря которому вы можете узнать, где вы сейчас в плане вашего стрессового отклика на физиологическом уровне (опросник Алана Кристиансона), а также получить практические рекомендации по тому, что можно поменять в образе жизни, чтобы жить более сбалансированной и наполненной жизнью без выгорания. 

Результаты вы получите сразу, конфиденциальность гарантирована.

Примерно через 3 минуты вы узнаете, на какой стадии вы находитесь:

▪️ Процветание - очень редкие случаи, но вдруг…
▪️ Стресс - если вы тут, то не переживайте, обычно это норма, просто стоит узнать о рекомендациях и внедрить их в жизнь
▪️ Хронический стресс - тут точно стоит что-то поменять, рекомендации вам в помощь
▪️ Выгорание - срочно позаботьтесь о себе! Как? Узнаете из рекомендаций по результатам теста."""

    markup = InlineKeyboardMarkup()
    # print(message.chat.id)
    # button2 = InlineKeyboardButton(text="❓ Мне нужна консультация по легализации", url=URL)
    button1 = InlineKeyboardButton(text="✅ начать тест", callback_data="test")
    markup.add(button1)
    # markup.add(button2)
    # print(user_scores)
    await bot.send_message(chat_id=message.chat.id, text=greeting, reply_markup=markup)


@dp.callback_query_handler()
async def process_callback_button_1(callback_query: CallbackQuery):
    global user_scores, markup

    if callback_query.data == "test":
        user_scores[f"{callback_query.from_user.id}"] = {
            "score": 0,
            "question_number": 0,
        }
        # print(user_scores)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="""Как часто вы замечали симптомы, которые последуют далее, за последнее время (несколько месяцев, месяц)?""",
        )
        await Form.text.set()
        await bot.send_message(
            chat_id=callback_query.from_user.id, text=QUESTIONS[0], reply_markup=markup
        )


@dp.message_handler(state=Form.text)
async def process_text(message: types.Message, state: FSMContext):
    global user_scores, markup
    print(user_scores)
    # print(message)
    # print(user_scores[f'{message.chat.id}']['question_number'])
    question_number = user_scores[f"{message.chat.id}"]["question_number"]
    # print('question_number=', question_number)
    if question_number + 1 < len(QUESTIONS):
        if message.text == "Начать заново":
            await state.finish()
            await message.reply("Отменено", reply_markup=types.ReplyKeyboardRemove())

            markup_again = InlineKeyboardMarkup()
            button1 = InlineKeyboardButton(
                text="начнем тест с начала", callback_data="test"
            )
            # button2 = InlineKeyboardButton(text="❓Мне все-таки нужна консультация по легализации", url=URL)
            markup_again.add(button1)
            # markup.add(button2)
            await bot.send_message(
                chat_id=message.chat.id,
                text="Что будем делать дальше?",
                reply_markup=markup_again,
            )
        else:
            if message.text == "Никогда":
                user_scores[f"{message.chat.id}"]["question_number"] += 1
            if message.text == "Иногда":
                user_scores[f"{message.chat.id}"]["score"] += 1
                user_scores[f"{message.chat.id}"]["question_number"] += 1
            if message.text == "Часто":
                user_scores[f"{message.chat.id}"]["score"] += 2
                user_scores[f"{message.chat.id}"]["question_number"] += 1
            if message.text == "Очень часто, почти всегда":
                user_scores[f"{message.chat.id}"]["score"] += 3
                user_scores[f"{message.chat.id}"]["question_number"] += 1
            question_number += 1

            # if question_number > 0 and question_number < len(QUESTIONS) :
            try:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=QUESTIONS[question_number],
                    reply_markup=markup,
                )
            except:
                # else:
                pass

    else:
        await state.finish()
        await message.reply(
            "Это был последний вопрос", reply_markup=types.ReplyKeyboardRemove()
        )

        markup_again = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(
            text="начнем тест с начала", callback_data="test"
        )
        markup_again.add(button1)
        score = user_scores[f"{message.chat.id}"]["score"]

        await bot.send_message(
            chat_id=message.chat.id, text=f"Вы набрали {score} баллов."
        )
        if score < 21:
            await bot.send_message(
                chat_id=message.chat.id,
                text=RESULTS[0],
                reply_markup=markup_again,
                parse_mode=types.ParseMode.HTML,
            )
        if score > 20 and score < 41:
            await bot.send_message(
                chat_id=message.chat.id,
                text=RESULTS[1],
                reply_markup=markup_again,
                parse_mode=types.ParseMode.HTML,
            )
        if score > 40 and score < 51:
            await bot.send_message(
                chat_id=message.chat.id,
                text=RESULTS[2],
                reply_markup=markup_again,
                parse_mode=types.ParseMode.HTML,
            )
        if score > 50:
            await bot.send_message(
                chat_id=message.chat.id,
                text=RESULTS[3],
                reply_markup=markup_again,
                parse_mode=types.ParseMode.HTML,
            )

        # markup.add(button2)
        # await bot.send_message(chat_id=message.chat.id, text="Что будем делать дальше?", reply_markup=markup_again)


@dp.message_handler(state=Form.result)
async def process_result(message: types.Message, state: FSMContext):
    global user_scores
    await state.finish()
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, selective=True, one_time_keyboard=True
    )

    markup.add("Начать заново")

    score = user_scores[f"{message.chat.id}"]["score"]
    await bot.send_message(
        chat_id=message.chat.id, text=f"Вы набрали {score} баллов", reply_markup=markup
    )


if __name__ == "__main__":
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
