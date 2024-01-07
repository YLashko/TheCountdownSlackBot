import os
import slack
from pathlib import Path
from dotenv import load_dotenv
from sender import Sender
from datetime import datetime
from track_calendar import Calendar
from images_config import *
from image_adjust import place_text_on_image
import asyncio

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

async def main():
    client = slack.WebClient(token=os.environ['SLACK_TOKEN'], run_async=True)
    target_channel = os.environ['CHANNEL_NAME']
    send_time = os.environ['SEND_TIME']
    timespan = int(os.environ['TIMESPAN_MINUTES'])
    country = os.environ['HOLIDAYS_COUNTRY']

    sender = Sender(send_time, timespan, Calendar(country, False))
    while True:
        now = datetime.now()
        if sender.is_to_send(datetime_now=now):
            remaining_days = str(sender.get_remaining_days(now))

            place_text_on_image(
                IMAGE_IN_PATH,
                IMAGE_OUT_PATH,
                FONT_PATH,
                POSITION,
                remaining_days
            )

            await client.files_upload(
                channels=target_channel,
                filename='countdown.jpg',
                file=IMAGE_OUT_PATH
            )
            sender.set_today_sent(now)
        await asyncio.sleep(30)

if __name__ == '__main__':
    asyncio.run(main())
