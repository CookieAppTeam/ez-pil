import asyncio
import functools
from collections.abc import Callable
from io import BytesIO

import aiohttp
import requests
from PIL import Image, UnidentifiedImageError
from PIL.GifImagePlugin import GifImageFile


async def run_in_executor(func: Callable, **kwargs):
    """Run function in executor.

    Parameters
    ----------
    func:
        Function to run
    """
    func = functools.partial(func, **kwargs)
    data = await asyncio.get_event_loop().run_in_executor(None, func)
    return data


def load_image(link: str, raw: bool = False) -> Image.Image | GifImageFile:
    """Load image from link.

    Parameters
    ----------
    link:
        Image link
    raw:
        if you want the raw image without any conversion
    """
    _bytes = BytesIO(requests.get(link).content)
    image = Image.open(_bytes)
    if not raw:
        image = image.convert("RGBA")

    return image


async def load_image_async(
    link: str,
    session: aiohttp.ClientSession | None = None,
    raw: bool = False,
    *,
    fallback_image: str | None = "https://cdn.discordapp.com/embed/avatars/0.png",
) -> Image.Image | GifImageFile:
    """Load image from link (async).

    Parameters
    ----------
    link:
        Image from the provided link (if any)
    session:
        ClientSession for making requests, defaults to None
    raw:
        if you want the raw image without any conversion
    fallback_image:
        Return a fallback image if the provided link is invalid. Defaults to a Discord avatar.
    """
    if isinstance(session, aiohttp.ClientSession):
        async with session.get(link) as response:  # type: ignore
            data = await response.read()
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                data = await response.read()

    _bytes = BytesIO(data)
    try:
        image = Image.open(_bytes)
    except UnidentifiedImageError:
        if fallback_image:
            return await load_image_async(fallback_image, None, raw, fallback_image=False)
        raise

    if not raw:
        image = image.convert("RGBA")

    return image
