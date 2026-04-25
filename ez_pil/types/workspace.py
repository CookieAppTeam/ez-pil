from io import BytesIO
from pathlib import Path

try:
    from typing import Literal, NotRequired, TypedDict
except ImportError:
    from typing import Literal, NotRequired

    from typing_extensions import TypedDict

from PIL.Image import Image
from PIL.ImageFont import FreeTypeFont

from ..canvas import Canvas
from ..editor import Editor
from ..font import Font
from ..text import Text


class ComponentKwargs(TypedDict):
    size: NotRequired[tuple[float, float]]
    position: NotRequired[tuple[float, float]]
    crop: NotRequired[bool]
    radius: NotRequired[int]
    offset: NotRequired[int]
    deg: NotRequired[float]
    expand: NotRequired[bool]
    mode: NotRequired[Literal["box", "gaussian"]]
    amount: NotRequired[float]
    image: NotRequired[Image | Editor | Canvas | BytesIO | Path | bytes]
    alpha: NotRequired[float]
    on_top: NotRequired[bool]
    text: NotRequired[str]
    font: NotRequired[FreeTypeFont | Font]
    align: NotRequired[Literal["left", "center", "right"]]
    color: NotRequired[int | str | tuple[int, int, int] | tuple[int, int, int, int]]
    fill: NotRequired[int | str | tuple[int, int, int] | tuple[int, int, int, int]]
    space_separated: NotRequired[bool]
    texts: NotRequired[list[Text]]
    width: NotRequired[float]
    height: NotRequired[float]
    stoke_width: NotRequired[float]
    outline: NotRequired[float]
    max_width: NotRequired[float]
    percent: NotRequired[int]
    start: NotRequired[float]
    rotation: NotRequired[int]
