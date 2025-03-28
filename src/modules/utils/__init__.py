#  Copyright (c) 2025 AshokShau.
#  TgMusicBot is an open-source Telegram music bot licensed under AGPL-3.0.
#  All rights reserved where applicable.
#

__all__ = [
    "sec_to_min",
    "get_audio_duration",
    "play_button",
    "PauseButton",
    "ResumeButton",
    "SupportButton",
]

import asyncio
import json

from src.logger import LOGGER
from .buttons import play_button, PauseButton, ResumeButton, SupportButton


def sec_to_min(seconds):
    """Convert seconds to minutes:seconds format."""
    try:
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes}:{remaining_seconds:02}"
    except Exception as e:
        LOGGER.warning(f"Failed to convert seconds to minutes:seconds format: {e}")
        return None


async def get_audio_duration(file_path):
    try:
        proc = await asyncio.create_subprocess_exec(
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            file_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        data = json.loads(stdout)
        duration = float(data['format']['duration'])
        return int(duration)
    except Exception as e:
        LOGGER.warning(f"Failed to get audio duration using ffprobe: {e}")
        return 0
