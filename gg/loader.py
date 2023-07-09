# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.input_file import InputFile

from utils.config import Config
from database.database import Database
from keyboards.keyboards import Keyboards


cfg = Config()
db = Database()
db.create_tables()
kb = Keyboards(cfg)

bot = Bot(token=cfg.get_bot_token(), parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)