import asyncio
import logging

from bot_instance import bot, dp
from handlers import client_handlers


async def main():
    dp.include_router(client_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
