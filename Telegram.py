import logging
import os
import threading
from time import sleep, time

from telegram.ext import CommandHandler
from telegram.ext import Updater

from YoutubeReceiver import get_last_video


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Nice to meet you")


def last_video(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_last_video())


def init_handlers():
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    last_video_handler = CommandHandler('last_video', last_video)
    dispatcher.add_handler(last_video_handler)


def start_listening_activities():
    video = get_last_video()
    sleep_time = 300

    six_hours_sleep = 6 * 60 * 60

    while True:
        sleep(sleep_time - time() % sleep_time)
        new_video = get_last_video()

        if new_video and video != new_video:
            video = new_video
            logger.info("New video was uploaded")

            sleep_time = six_hours_sleep
        else:
            logger.info("New video was not uploaded")
            sleep_time = 15


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    logger = logging.getLogger(__name__)

    updater = Updater(token=os.environ.get('TELEGRAM_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    init_handlers()

    check_updates_thread = threading.Thread(target=start_listening_activities)
    check_updates_thread.start()

    updater.start_polling()
