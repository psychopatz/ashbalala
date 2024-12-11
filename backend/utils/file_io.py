import aiofiles

async def save_audio_file(audio_content: bytes, file_path: str):
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(audio_content)
