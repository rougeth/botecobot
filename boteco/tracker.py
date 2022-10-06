from datetime import datetime, timedelta

import discord
from loguru import logger


class VoiceChannelTracker:
    def __init__(self):
        self.status = {}

    def __len__(self):
        return len(self.status)

    def track(self, channel):
        self.status[channel.id] = {
            "empty_at": datetime.now(),
            "channel": channel,
        }

    def stop_tracking(self, channel):
        if channel.id in self.status:
            logger.info(f"Stop tracking channel. channel={channel.name!r}")
            del self.status[channel.id]

    async def delete_empty_channels(self):
        delete_before = datetime.now() - timedelta(minutes=5)

        to_remove_now = [
            channel["channel"]
            for channel in self.status.values()
            if delete_before > channel["empty_at"]
        ]
        for channel in to_remove_now:
            logger.info(f"Deleting voice channel. channel={channel.name}")
            try:
                await channel.delete()
            except discord.errors.NotFound:
                logger.info(
                    f"Voice channel doesn't exist anymore. channel={channel.name}"
                )
            self.stop_tracking(channel)
