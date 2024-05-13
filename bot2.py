from telegram.ext import Application, MessageHandler, filters,\
    CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
import sqlite3


async def start(update, context):
    con = sqlite3.connect('./bot_data.db')
    cur = con.cursor()
    context.user_data['game'] = cur.execute("""SELECT * FROM game""").fetchall()
    context.user_data['questions'] = []
    context.user_data['result'] = 0
    await update.message.reply_text('👋《-❲Приветствую, мою друг!❳ -》👋 \n'
                                    'Я бот Бариновой Рощи могу:\n'
                                    '• Сыграть с тобой в игру и узнать,'
                                    ' на сколько хорошо ты знаешь трассу Бариновой Рощи\n'
                                    '• Могу проанализировать твою тренировку и дать советы\n'
                                    '• Показать даты предстоящих соревнований\n '
                                    '• Рассказать о победителях в этом сезоне\n'
                                    '〔Команды:〕\n'
                                    '/game - начать игру со мной 🎲\n'
                                    '/sports_training - тренировался? Расскажи про свою'
                                    ' тренировку 🤸‍♂️\n'
                                    '/competition_dates - даты соревнований в Бариновой рощи 📃 \n'
                                    '/result_sorev - победители предыдущих соревнований 🏆 ',
                                    reply_markup=ReplyKeyboardRemove())
    return 0


async def empty_function(update, context):
    await update.message.reply_text('Я не понимаю...')


async def game(update, context):
    req = update.message.text.strip().lower()
    if req == '/game':
        context.user_data['right_answers'] = ['Поздравляем!', 'Высший класс!', 'Отличная работа!',
                                              'Вы мастер!', 'Потрясающе!', 'Идеально!', 'Браво!',
                                              'Великолепно!', 'Превосходно!',
                                              'Исключительная наблюдательность!',
                                              'Невероятная сообразительность!',
                                              'Великолепное дедуктивное мышление!',
                                              'Ум как бритва!',
                                              'Ген анализа работает!', 'Мастер головоломок!',
                                              'Легенда дедукции!']
        context.user_data['wrong_answers'] = ['Нам жаль, но это неправильный ответ!',
                                              'К сожалению это неправильный ответ!',
                                              'Эхх... мимо, это неправильный ответ!',
                                              'Нет, это неправильный ответ!',
                                              'Так близко, но так далеко, это неправильный ответ!',
                                              'Почти так, но есть вариант лучше!',
                                              'Промах, это неправильный ответ!',
                                              'Это неправильный ответ!',
                                              'Никого тильта, только полный тильт!', 'Почти было!',
                                              'Следовало подумать ещё, это нерпавильный ответ!']
        await update.message.reply_text(f'ПРАВИЛА ИГРЫ ❗️\n'
                                        f'Бот отправляет вам фотографию, на которой изображена'
                                        f' часть трассы или момент из соревнований Бариновы Рощи, '
                                        f'Вам нужно угадать, как называется этот участок трассы'
                                        f' или соревнование, на выбор будет 4 варианта ответа,'
                                        f' выберите один из них.\n'
                                        f'В конце игры бот напишет вам результат, удачи 🍀')
    if req == '/game' or req == 'Следующий вопрос'.lower():
        chat_id = update.effective_message.chat_id
        past_questions = context.user_data['questions']
        now_question = random.choice(context.user_data['game'])
        while now_question in past_questions:
            now_question = random.choice(context.user_data['game'])
        context.user_data['questions'].append(now_question)
        context.user_data['now_question'] = now_question
        photo = now_question[-1]
        arr = [1, 2, 3, 4]
        random.shuffle(arr)
        reply_keyboard = [[now_question[arr[0]], now_question[arr[1]]],
                          [now_question[arr[2]], now_question[arr[3]]]]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
        await context.bot.sendPhoto(chat_id, photo=photo, reply_markup=markup)
        return 2
    elif req == 'Показать результат'.lower():
        await update.message.reply_text(f'Ваш результат: {context.user_data["result"]}👍\n'
                                        f'Неплохая попытка!\n'
                                        f'Но ты не прошёл тест до конца,'
                                        f' пройди тест заново и получи медаль 🟢',
                                        reply_markup=ReplyKeyboardRemove())
        context.user_data['questions'] = []
        context.user_data['result'] = 0
        return 0
    await update.message.reply_text(f'Я вас не понимаю(')


async def answer(update, context):
    req = update.message.text.strip().lower()
    right_answer = context.user_data['now_question'][4]
    reply_keyboard = [['Показать результат', 'Следующий вопрос']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    if req == right_answer.lower():
        answer = context.user_data['right_answers'].pop(random.randint(0,
                                                                       len(context.user_data['right'
                                                                                             '_answ'
                                                                                             'ers'])
                                                                       - 1))
        context.user_data['result'] += 1
        await update.message.reply_text(f'✅ {answer} Это правильный ответ!\n'
                                        f'{context.user_data["now_question"][5]}',
                                        reply_markup=markup)
    else:
        answer = context.user_data['wrong_answers'].pop(random.randint(0,
                                                                       len(context.user_data['wrong'
                                                                                             '_answ'
                                                                                             'ers'])
                                                                       - 1))
        await update.message.reply_text(f'❌ {answer}\n'
                                        f'{context.user_data["now_question"][5]}',
                                        reply_markup=markup)
    if len(context.user_data['questions']) == len(context.user_data['game']):
        k = context.user_data["result"]
        if 9 <= k <= 11:
            result = 'Отличный результат!\nТвои знания о Роще впечатляют! 🥇'
        elif 4 <= k <= 8:
            result = 'Умница!\nТы явно бывал у нас на трассе! 🥈'
        else:
            result = 'Неплохая попытка!\nНадеюсь ты узнал много нового! 🥉'
        await update.message.reply_text(f'Ваш результат: {context.user_data["result"]}👍\n'
                                        f'{result}',
                                        reply_markup=ReplyKeyboardRemove())
        context.user_data['questions'] = []
        context.user_data['result'] = 0
        return 0
    return 3


async def competition_dates(update, context):
    con = sqlite3.connect('./bot_data.db')
    cur = con.cursor()
    dates = cur.execute("""SELECT date, competition FROM dates""").fetchall()
    answer = ''
    for d in dates:
        answer += f'{d[0]} - {d[1]}\n'
    await update.message.reply_text(f'{answer}\nСоревнование может быть перенесено на другую дату,'
                                    f' чтобы не упустить этого '
                                    f'советую подписаться на наше сообщество:'
                                    f' https://vk.com/scbarro, спасибо 🥰',
                                    reply_markup=ReplyKeyboardRemove())
    return 0


async def result_sorev(update, context):
    reply_keyboard = [['ЧЛМД ⛷'], ['Зимний триатлон ⛷'], ['Ночная гонка ⛷'],
                      ['Назад ⬅️']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    await update.message.reply_text('Выберете соревнование для вывода результата',
                                    reply_markup=markup)
    return 4


async def print_results(update, context):
    req = update.message.text
    if req == 'Зимний триатлон ⛷':
        with open("results/triathlon.txt", 'r', encoding='utf-8') as file:
            data = [a for a in file.readlines()]
        s = ''
        for a in data:
            s += a
        await update.message.reply_text(s)
    elif req == 'ЧЛМД ⛷':
        with open("results/CHLMD.txt", 'r', encoding='utf-8') as file:
            data = [a for a in file.readlines()]
        s = ''
        for a in data:
            s += a
        await update.message.reply_text(s)
    elif req == 'Ночная гонка ⛷':
        with open("results/night.txt", 'r', encoding='utf-8') as file:
            data = [a for a in file.readlines()]
        s = ''
        for a in data:
            s += a
        await update.message.reply_text(s)
    elif req == 'Назад ⬅️':
        await update.message.reply_text(f'Возвращаемся назад', reply_markup=ReplyKeyboardRemove())
        return 0


async def sports_training(update, context):
    reply_keyboard = [['Бег 🏃', 'Лыжи ⛷️'], ['Езда на велосипеде 🚴', 'Плаванье 🏊'],
                      ['Назад ⬅️']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    await update.message.reply_text('Каким видом спорта занимались?',
                                    reply_markup=markup)
    return 1


async def talking_function(update, context):
    req = update.message.text.strip()
    reply_keyboard = [['Назад ⬅️']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    context.user_data['questions'] = ['Какое расстояние ты преодолел за тренировку? В ответ запиши '
                                      'число',
                                      'Какая средняя скорость у тебя была на тренировке? В ответ '
                                      'запиши число',
                                      'А какой максимальный пульс? '
                                      'В ответ запиши число',
                                      'Какой средний пульс у тебя был на тренировке? '
                                      'В ответ запиши число']
    if req == 'Назад ⬅️':
        await update.message.reply_text('Вы не прошли опрос до конца, пройдите опрос до конца,'
                                        ' и бот даст вам совет по тренировке 🌹',
                                        reply_markup=ReplyKeyboardRemove())
        return 0
    elif req == 'Бег 🏃':
        context.user_data['training'] = 'running'
        context.user_data['now_question'] = 'average_heart_rate'
        context.user_data['points'] = 0
        ques = context.user_data['questions'].pop()
        await update.message.reply_text(ques, reply_markup=markup)
        return 5
    elif req == 'Лыжи ⛷️':
        context.user_data['training'] = 'ski'
        context.user_data['now_question'] = 'average_heart_rate'
        context.user_data['points'] = 0
        ques = context.user_data['questions'].pop()
        await update.message.reply_text(ques, reply_markup=markup)
        return 5
    elif req == 'Езда на велосипеде 🚴':
        context.user_data['training'] = 'bicycle'
        context.user_data['now_question'] = 'average_heart_rate'
        context.user_data['points'] = 0
        ques = context.user_data['questions'].pop()
        await update.message.reply_text(ques, reply_markup=markup)
        return 5
    elif req == 'Плаванье 🏊':
        context.user_data['training'] = 'swimming'
        context.user_data['now_question'] = 'average_heart_rate'
        context.user_data['points'] = 0
        ques = context.user_data['questions'].pop()
        await update.message.reply_text(ques, reply_markup=markup)
        return 5
    else:
        await update.message.reply_text('Я не понимаю...')


async def training(update, context):
    reply_keyboard = [['Назад ⬅️']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    req = update.message.text.strip()
    if req == 'Назад ⬅️':
        await update.message.reply_text('Вы не прошли опрос до конца, пройдите опрос до конца,'
                                        ' и бот даст вам совет по тренировке 🌹',
                                        reply_markup=ReplyKeyboardRemove())
        return 0
    quest = context.user_data['now_question']
    now_training = context.user_data['training']
    con = sqlite3.connect('./bot_data.db')
    cur = con.cursor()
    s = f"""SELECT {quest} FROM training WHERE name = '{now_training}'"""
    info = cur.execute(s).fetchall()[0][0].split(', ')
    try:
        x = float(req)
        if context.user_data['now_question'] in ('average_heart_rate', 'maximum_heart_rate') and \
                x > float(info[0].split('-')[-1]):
            await update.message.reply_text(f'Вау, ваш пульс слишком высокий, как Бурдж-Халифа,'
                                            f' может он был ниже?',
                                            reply_markup=markup)
            return 5
        if context.user_data['now_question'] == 'distance' and \
                x > float(info[0].split('-')[-1]):
            await update.message.reply_text(f'Я уверен, вы потратили на эти много времени…',
                                            reply_markup=markup)
            context.user_data['points'] += 3
        if context.user_data['now_question'] == 'speed' and \
                x > float(info[0].split('-')[-1]):
            await update.message.reply_text(f'Бари, это ты? Может ваша скорость была ниже?',
                                            reply_markup=markup)
            return 5
        if context.user_data['now_question'] in ('average_heart_rate', 'maximum_heart_rate') and \
                x < 50:
            await update.message.reply_text(f'Слишком низкий пульс',
                                            reply_markup=markup)
            return 5
        point = 3
        for span in info:
            m1, m2 = [float(i) for i in span.split('-')]
            if m1 <= x <= m2:
                context.user_data['points'] += point
                break
            point -= 1
        if len(context.user_data['questions']) == 0:
            point = context.user_data["points"]
            if 8 <= point <= 12:
                ans = 'Высокая интенсивность! 💪\n' \
                      'Восстановите силы легкой силовой тренировкой ✅'
            elif 4 <= point <= 8:
                ans = 'Вы большой молодец! 💪\n' \
                      'Продолжайте в том же духе и не снижайте интенсивность ✅'
            else:
                ans = 'Неплохо, но вы можете лучше!\n' \
                      'Советую повысить интенсивность ✅'
            await update.message.reply_text(f'{ans}',
                                            reply_markup=ReplyKeyboardRemove())
            return 0
        ques = context.user_data['questions'].pop()
        if len(context.user_data['questions']) == 2:
            context.user_data['now_question'] = 'maximum_heart_rate'
        elif len(context.user_data['questions']) == 1:
            context.user_data['now_question'] = 'speed'
        elif len(context.user_data['questions']) == 0:
            context.user_data['now_question'] = 'distance'
        await update.message.reply_text(ques, reply_markup=markup)
    except Exception:
        await update.message.reply_text('Вводятся только числа')


def main():
    TOKEN = '6713892324:AAFjnC6ziUNQdZMLdeTnTPCWMQk1j89rmJ8'
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, empty_function)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, talking_function)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, game)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, print_results)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, training)]
        },
        fallbacks=[CommandHandler("game", game),
                   CommandHandler("sports_training", sports_training),
                   CommandHandler("competition_dates", competition_dates),
                   CommandHandler("result_sorev", result_sorev)])
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
