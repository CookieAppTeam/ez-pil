import asyncio
import functools
from collections.abc import Callable
from io import BytesIO

import aiohttp
import requests
from PIL import Image
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
    """
    if isinstance(session, aiohttp.ClientSession):
        async with session.get(link) as response:  # type: ignore
            data = await response.read()
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                data = await response.read()

    _bytes = BytesIO(data)
    image = Image.open(_bytes)
    if not raw:
        image = image.convert("RGBA")

    return image
