from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image as PilImage
from PIL import ImageSequence
from PIL.GifImagePlugin import GifImageFile

from .editor import Editor


class GifEditor:
    def __init__(self, image: str | BytesIO | Path | GifImageFile):
        if isinstance(image, (str, BytesIO, Path)):
            self.image = PilImage.open(image)
        if isinstance(image, GifImageFile):
            self.image = image

        self.original_frames = ImageSequence.Iterator(self.image)
        self.frames: list[Editor] = [Editor(x) for x in self.original_frames]
        self.size: tuple[int, int] = self.image.size

    def __getattr__(self, name: str):
        def wrapper(*args, **kwargs):
            for frame in self.frames:
                getattr(frame, name)(*args, **kwargs)

        return wrapper

    @property
    def image_bytes(self) -> BytesIO:
        """Return image bytes.

        Returns
        -------
        BytesIO
            Bytes from the image of Editor
        """
        _bytes = BytesIO()
        images = [e.image for e in self.frames]
        images[0].save(_bytes, "GIF", save_all=True, append_images=images[1:])

        _bytes.seek(0)
        return _bytes

    def save(self, fp: str, **kwargs):
        """Save the image.

        Parameters
        ----------
        fp : str
            File path
        """
        images = [e.image for e in self.frames]
        images[0].save(fp, "GIF", save_all=True, append_images=images[1:], **kwargs)
