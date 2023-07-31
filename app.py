import nest_asyncio
nest_asyncio.apply()

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import load_config
import logging


config = load_config('.env')
logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.MARKDOWN_V2)
logger.info('INIT BOT CLASS')



if __name__ == '__main__':
    logger.info("STARTING BOT")
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    from handlers._loader import HandlerLoader
    HandlerLoader(dp)
    logger.info("SETUP HANDLERS")

    executor.start_polling(dp, skip_updates=True)
