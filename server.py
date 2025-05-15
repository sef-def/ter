# Импортируем необходимые классы.
import asyncio
import logging
import random
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardRemove
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.media_group import MediaGroupBuilder
from ui import cats
import datetime


# Запускаем логгирование



logger = logging.getLogger(__name__)
reply_keyboard = [['/address', '/phone', '/date', '/time'],
                      ['/Start_Game', '/work_time', '/close', '/cats']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def cats(update, context):
    await update.message.reply_text('\nкотики t.me/wdwrbot')


async def echo(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    await update.message.reply_text(update.message.text)


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


async def date_command(update, context):
    await update.message.reply_text(f"{datetime.date.today()}")


async def time_command(update, context):
    await update.message.reply_text(f"{datetime.datetime.now().time()}")


async def start(update, context):
    await update.message.reply_text(
        "Я бот крестики-нолики начнём?",
        reply_markup=markup
    )

async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... ")


async def help(update, context):
    await update.message.reply_text(
        "Я бот крестики-нолики")


async def address(update, context):
    await update.message.reply_text(
        "Адрес: г. Хута, ул. Льва Толстого, 16")


async def phone(update, context):
    await update.message.reply_text("Телефон: 8-800-535-35-35")




def print_board(board):
    po = ''
    for row in board:
        po += " | ".join(row)
        po += '\n'
        po += "-" * 9
        po += '\n'
    return po


def check_winner(board):
    # Проверка строк
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return row[0]

    # Проверка столбцов
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]

    # Проверка диагоналей
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]

    return None


def is_board_full(board):
    for row in board:
        if " " in row:
            return False
    return True


def get_empty_cells(board):
    return [(row, col) for row in range(3) for col in range(3) if board[row][col] == " "]


def computer_move_easy(board):
    """Случайный ход (лёгкий уровень)."""
    return random.choice(get_empty_cells(board))


def computer_move_medium(board):
    """Блокировка игрока и попытка выиграть (средний уровень)."""
    # Проверка победы компьютера
    for row, col in get_empty_cells(board):
        board[row][col] = "O"
        if check_winner(board) == "O":
            board[row][col] = " "
            return (row, col)
        board[row][col] = " "

    # Блокировка игрока
    for row, col in get_empty_cells(board):
        board[row][col] = "X"
        if check_winner(board) == "X":
            board[row][col] = " "
            return (row, col)
        board[row][col] = " "

    # Случайный ход
    return computer_move_easy(board)


def minimax(board, depth, is_maximizing):
    """Алгоритм Minimax для сложного уровня."""
    winner = check_winner(board)
    if winner == "O":
        return 1
    if winner == "X":
        return -1
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for row, col in get_empty_cells(board):
            board[row][col] = "O"
            score = minimax(board, depth + 1, False)
            board[row][col] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row, col in get_empty_cells(board):
            board[row][col] = "X"
            score = minimax(board, depth + 1, True)
            board[row][col] = " "
            best_score = min(score, best_score)
        return best_score


def computer_move_hard(board):
    """Непобедимый ИИ (сложный уровень)."""
    best_move = None
    best_score = -float("inf")
    for row, col in get_empty_cells(board):
        board[row][col] = "O"
        score = minimax(board, 0, False)
        board[row][col] = " "
        if score > best_score:
            best_score = score
            best_move = (row, col)
    return best_move


async def tic_tac_toe(update, context):
    await update.message.reply_text("Выберите уровень сложности:\n1 - Лёгкий (компьютер ходит случайно)\n"
                                      "2 - Средний (компьютер блокирует победу)\n3 - Сложный (компьютер непобедим)"
                                      "\nВведите число (1-3): ", reply_markup=ReplyKeyboardRemove())
    return 1


board = [[" " for _ in range(3)] for _ in range(3)]
current_player = "X"
difficulty = 0
rent = 0


async def t(update, context):
    global board
    if update.message.text in ["1", "2", "3"]:
        global difficulty
        difficulty = int(update.message.text)
    else:
        await update.message.reply_text("Некорректный ввод!")
        return 2
    global current_player  # Игрок начинает первым
    current_player = "X"

    await update.message.reply_text("\nДобро пожаловать в Крестики-нолики! \n"
                                    "Вводите координаты в формате 'строка столбец' (от 0 до 2).")
    await update.message.reply_text(print_board(board))
    return 3

async def r(update, context):
    global difficulty
    global current_player
    global rent
    try:
        row, col = map(int, update.message.text.split())
        if (row, col) not in get_empty_cells(board):
            await update.message.reply_text("Некорректный ход! Попробуйте ещё.")
            return 3
    except ValueError:
        await update.message.reply_text("Введите два числа через пробел (например: 1 1).")
        return 3
    board[row][col] = current_player
    winner = check_winner(board)
    if winner:
        await update.message.reply_text(print_board(board))
        await update.message.reply_text("Вы победили!" if winner == "X" else "Компьютер победил!")
        rent = 1
        return ConversationHandler.END

    if is_board_full(board):
        await update.message.reply_text(print_board(board))
        await update.message.reply_text("Ничья!")
        rent = 1
        return ConversationHandler.END
    await update.message.reply_text(print_board(board))
    current_player = "O" if current_player == "X" else "X"
    await update.message.reply_text("Ход компьютера...")
    if difficulty == 1:
        row, col = computer_move_easy(board)
    elif difficulty == 2:
        row, col = computer_move_medium(board)
    else:
        row, col = computer_move_hard(board)
    board[row][col] = current_player
    await update.message.reply_text(print_board(board))
    current_player = "O" if current_player == "X" else "X"
    return 3


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def work_time(update, context):
    await update.message.reply_text(
        "Время работы: круглосуточно.")


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token('8167570443:AAGtJONr4kGGXVX-ODN-BkshE8Y41BMLVTw').build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help1", help_command))
    application.add_handler(CommandHandler("date", date_command))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("address", address))
    application.add_handler(CommandHandler("phone", phone))
    application.add_handler(CommandHandler("work_time", work_time))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(CommandHandler("cats", cats))
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('Start_Game', tic_tac_toe)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, t)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, tic_tac_toe)],

            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, r)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    # Запускаем приложение.
    application.run_polling()







# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
