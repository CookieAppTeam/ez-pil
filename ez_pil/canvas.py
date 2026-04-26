from PIL import Image

from .types.common import Color


class Canvas:
    """Canvas class.

    Parameters
    ----------
    size:
        Size of image, by default None.
    width:
        Width of image, by default None.
    height:
        Height of image, by default None.
    color:
        Color of image, by default None.

    Raises
    ------
    ValueError
        When either ``size`` or ``width and height`` is not a provided
    """

    def __init__(
        self,
        size: tuple[int, int] | None = None,
        width: int = 0,
        height: int = 0,
        color: Color = 0,
    ) -> None:
        if not (size or (width and height)):
            raise ValueError("size, width, and height cannot all be None")

        elif not size:
            size = (width, height)

        self.size = size
        self.color = color

        self.image = Image.new("RGBA", size, color=color)
