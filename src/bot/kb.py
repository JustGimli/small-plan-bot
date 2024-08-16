from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

import config


def lk() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton(text=config.gpt, callback_data=config.gpt)
    but2 = InlineKeyboardButton(
        text=config.face_swap, callback_data=config.face_swap)
    but3 = InlineKeyboardButton(
        text=config.new_img_req, callback_data=config.new_img_req)
    but4 = InlineKeyboardButton(
        text=config.settings, callback_data=config.settings)
    but4 = InlineKeyboardButton(
        text=config.settings, callback_data=config.settings)
    but5 = InlineKeyboardButton(
        text=config.channel_text, url=config.channel_url)
    kb.add(but1, but2)
    kb.add(but3, but4)
    kb.add(but5)
    return kb
