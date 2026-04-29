from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Literal

from PIL import Image as PilImage
from PIL import ImageDraw, ImageFilter, ImageFont
from PIL.Image import Image

from .canvas import Canvas
from .font import Font
from .text import Text
from .types.common import Color


class Editor:
    """Editor class. It does all the editing operations.

    Parameters
    ----------
    _image : Union[Image, str, Editor, Canvas]
        Image or Canvas to edit.
    """

    def __init__(self, _image: Image | str | BytesIO | Editor | Canvas | Path) -> None:
        self.image: Image
        if isinstance(_image, (str, BytesIO, Path)):
            self.image = PilImage.open(_image)
        elif isinstance(_image, (Canvas, Editor)):
            self.image = _image.image
        elif isinstance(_image, Image):
            self.image = _image
        else:
            raise ValueError("Editor requires an Image, Path, Editor or Canvas to start with")

        self.image = self.image.convert("RGBA")

    @property
    def image_bytes(self) -> BytesIO:
        """Return image bytes."""
        _bytes = BytesIO()
        self.image.save(_bytes, "png")

        _bytes.seek(0)
        return _bytes

    def close(self):
        self.image.close()

    def resize(self, size: tuple[int, int], crop: bool = False) -> Editor:
        """Resize image.

        Parameters
        ----------
        size:
            New Size of image
        crop:
            Crop the image to bypass distortion, by default False
        """
        if not crop:
            self.image = self.image.resize(size, PilImage.LANCZOS)

        else:
            width, height = self.image.size
            ideal_width, ideal_height = size

            aspect = width / height
            ideal_aspect = ideal_width / ideal_height

            if aspect > ideal_aspect:
                new_width = ideal_aspect * height
                offset = int((width - new_width) / 2)
                resize = (offset, 0, width - offset, height)
            else:
                new_height = width / ideal_aspect
                offset = int((height - new_height) / 2)
                resize = (0, offset, width, height - offset)

            self.image = self.image.crop(resize).resize(
                (ideal_width, ideal_height), PilImage.LANCZOS
            )

        return self

    def rounded_corners(self, radius: int = 10, offset: int = 2) -> Editor:
        """Make image rounded corners.

        Parameters
        ----------
        radius:
            Radius of roundness, by default 10
        offset:
            Offset pixel while making rounded, by default 2
        """
        background = PilImage.new("RGBA", size=self.image.size, color=(255, 255, 255, 0))
        holder = PilImage.new("RGBA", size=self.image.size, color=(255, 255, 255, 0))
        mask = PilImage.new("RGBA", size=self.image.size, color=(255, 255, 255, 0))
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle(
            (offset, offset) + (self.image.size[0] - offset, self.image.size[1] - offset),
            radius=radius,
            fill="black",
        )
        holder.paste(self.image, (0, 0))
        self.image = PilImage.composite(holder, background, mask)

        background.close()
        holder.close()
        mask.close()

        return self

    def circle_image(self) -> Editor:
        """Make image circle."""
        background = PilImage.new("RGBA", size=self.image.size, color=(255, 255, 255, 0))
        holder = PilImage.new("RGBA", size=self.image.size, color=(255, 255, 255, 0))
        mask = PilImage.new("RGBA", size=self.image.size, color=(255, 255, 255, 0))
        mask_draw = ImageDraw.Draw(mask)
        ellipse_size = tuple(i - 1 for i in self.image.size)
        mask_draw.ellipse((0, 0) + ellipse_size, fill="black")
        holder.paste(self.image, (0, 0))
        self.image = PilImage.composite(holder, background, mask)

        background.close()
        holder.close()
        mask.close()

        return self

    def rotate(self, deg: float = 0, expand: bool = False) -> Editor:
        """Rotate image.

        Parameters
        ----------
        deg:
            Degrees to rotate, by default 0
        expand:
            Expand while rotating, by default False
        """
        self.image = self.image.rotate(deg, expand=expand)
        return self

    def blur(self, mode: Literal["box", "gaussian"] = "gaussian", amount: float = 1) -> Editor:
        """Blur image.

        Parameters
        ----------
        mode:
            Blur mode, by default "gaussian"
        amount:
            Amount of blur, by default 1
        """
        if mode == "box":
            self.image = self.image.filter(ImageFilter.BoxBlur(radius=amount))
        if mode == "gaussian":
            self.image = self.image.filter(ImageFilter.GaussianBlur(radius=amount))

        return self

    def blend(
        self,
        image: Image | Editor | Canvas,
        alpha: float = 0.0,
        on_top: bool = False,
    ) -> Editor:
        """Blend image into editor image.

        Parameters
        ----------
        image:
            Image to blend
        alpha:
            Alpha amount, by default 0.0
        on_top:
            Places image on top, by default False
        """
        if isinstance(image, Editor) or isinstance(image, Canvas):
            image = image.image

        if image.size != self.image.size:
            image = Editor(image).resize(self.image.size, crop=True).image

        if on_top:
            self.image = PilImage.blend(self.image, image, alpha=alpha)
        else:
            self.image = PilImage.blend(image, self.image, alpha=alpha)

        return self

    def paste(
        self,
        image: Image | Editor | Canvas,
        position: tuple[int, int],
    ) -> Editor:
        """Paste image into editor.

        Parameters
        ----------
        image:
            Image to paste
        position:
            Position to paste
        """
        blank = PilImage.new("RGBA", size=self.image.size, color=(255, 255, 255, 0))

        if isinstance(image, Editor) or isinstance(image, Canvas):
            image = image.image

        blank.paste(image, position)
        self.image = PilImage.alpha_composite(self.image, blank)

        blank.close()

        return self

    def text(
        self,
        position: tuple[float, float],
        text: str,
        font: ImageFont.FreeTypeFont | Font | None = None,
        color: Color = "black",
        align: Literal["left", "center", "right"] = "left",
        stroke_width: int | None = None,
        stroke_fill: Color = "black",
    ) -> Editor:
        """Draw text into image.

        Parameters
        ----------
        position:
            Position to draw text.
        text:
            Text to draw
        font:
            Font used for text, by default None
        color:
            Color of the font, by default "black"
        align:
            Align text, by default "left"
        stroke_width:
            Whether there should be any stroke. Defaults to
            None. It represents the width of the said stroke.
        stroke_fill:
            Color of the stroke, if any stroke is applied to the
            text. Defaults to "black"
        """
        if isinstance(font, Font):
            font = font.font

        anchors = {"left": "lt", "center": "mt", "right": "rt"}

        draw = ImageDraw.Draw(self.image)

        if stroke_width:
            draw.text(
                position,
                text,
                color,
                font=font,
                anchor=anchors[align],
                stroke_width=stroke_width,
                stroke_fill=stroke_fill,
            )
        else:
            draw.text(position, text, color, font=font, anchor=anchors[align])

        return self

    def multi_text(
        self,
        position: tuple[float, float],
        texts: list[Text],
        space_separated: bool = True,
        align: Literal["left", "center", "right"] = "left",
    ) -> Editor:
        """Draw multicolor text.

        Parameters
        ----------
        position:
            Position to draw text
        texts:
            List of texts
        space_separated:
            Separate texts with space, by default True
        align:
            Align texts, by default "left"
        """
        draw = ImageDraw.Draw(self.image)

        if align == "left":
            position = position

        if align == "right":
            total_width = 0

            for t in texts:
                total_width += t.font.getlength(t.text)

            position = (int(position[0] - total_width), int(position[1]))

        if align == "center":
            total_width = 0

            for t in texts:
                total_width += t.font.getlength(t.text)

            position = (int(position[0] - (total_width / 2)), int(position[1]))

        for text in texts:
            sentence = text.text
            font = text.font
            color = text.color

            if space_separated:
                width = font.getlength(sentence + " ")
            else:
                width = font.getlength(sentence)

            draw.text(position, sentence, color, font=font, anchor="lm")
            position = (int(position[0] + width), int(position[1]))

        return self

    def rectangle(
        self,
        position: tuple[float, float],
        width: float,
        height: float,
        fill: Color | None = None,
        color: Color | None = None,
        outline: Color | None = None,
        stroke_width: float = 1,
        radius: int = 0,
    ) -> Editor:
        """Draw rectangle into image.

        Parameters
        ----------
        position:
            Position to draw rectangle
        width:
            Width of rectangle
        height:
            Height of rectangle
        fill:
            Fill color, by default None
        color:
            Alias of fill, by default None
        outline:
            Outline color, by default None
        stroke_width:
            Stroke width, by default 1
        radius:
            Radius of rectangle, by default 0
        """
        draw = ImageDraw.Draw(self.image)

        to_width = width + position[0]
        to_height = height + position[1]

        if color:
            fill = color

        if radius <= 0:
            draw.rectangle(
                position + (to_width, to_height),
                fill=fill,
                outline=outline,
                width=stroke_width,
            )
        else:
            draw.rounded_rectangle(
                position + (to_width, to_height),
                radius=radius,
                fill=fill,
                outline=outline,
                width=stroke_width,
            )

        return self

    def bar(
        self,
        position: tuple[int, int],
        max_width: int | float,
        height: int | float,
        percentage: int = 1,
        fill: Color | None = None,
        color: Color | None = None,
        outline: Color | None = None,
        stroke_width: float = 1,
        radius: int = 0,
    ) -> Editor:
        """Draw a progress bar.

        Parameters
        ----------
        position:
            Position to draw bar
        max_width:
            Max width of the bar
        height:
            Height of the bar
        percentage:
            Percentage to fill of the bar, by default 1
        fill:
            Fill color, by default None
        color:
            Alias of fill, by default None
        outline:
            Outline color, by default None
        stroke_width:
            Stroke width, by default 1
        radius:
            Radius of the bar, by default 0
        """
        if percentage == 0:
            return self

        if color:
            fill = color

        bg = PilImage.new("RGBA", (int(max_width), int(height)), (0, 0, 0, 0))
        main = PilImage.new("RGBA", (int(max_width), int(height)), (0, 0, 0, 0))
        mask = PilImage.new("L", (int(max_width), int(height)), 0)
        main_draw = ImageDraw.Draw(main)

        if percentage > 100 or percentage < 0:
            raise ValueError("Percentage must be between 1 and 100")

        bar_width = int((max_width / 100) * percentage)

        if radius <= 0:
            main_draw.rectangle(
                (0, 0) + (bar_width, height),
                fill=fill,
                outline=outline,
                width=stroke_width,
            )
        else:
            main_draw.rounded_rectangle(
                (0, 0) + (bar_width, height),
                radius=radius,
                fill=fill,
                outline=outline,
                width=stroke_width,
            )

        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle(
            (0, 0) + (max_width, height),
            radius=radius,
            fill=255,
            outline=255,
            width=stroke_width,
        )

        final = PilImage.composite(main, bg, mask)
        self.paste(final, position)

        main.close()
        final.close()
        bg.close()
        mask.close()

        return self

    def rounded_bar(
        self,
        position: tuple[float, float],
        width: int | float,
        height: int | float,
        percentage: float,
        fill: Color | None = None,
        color: Color | None = None,
        stroke_width: float = 1,
    ) -> Editor:
        """Draw a rounded bar.

        Parameters
        ----------
        position:
            Position to draw rounded bar
        width:
            Width of the bar
        height:
            Height of the bar
        percentage:
            Percentage to fill.
        fill:
            Fill color, by default None
        color:
            Alias of color, by default None
        stroke_width:
            Stroke width, by default 1
        """
        draw = ImageDraw.Draw(self.image)

        if color:
            fill = color

        start = -90
        end = (percentage * 3.6) - 90

        draw.arc(
            position + (position[0] + width, position[1] + height),
            start,
            end,
            fill,
            width=stroke_width,
        )

        return self

    def ellipse(
        self,
        position: tuple[float, float],
        width: float,
        height: float,
        fill: Color | None = None,
        color: Color | None = None,
        outline: Color | None = None,
        stroke_width: float = 1,
    ) -> Editor:
        """Draw an ellipse.

        Parameters
        ----------
        position:
            Position to draw ellipse
        width:
            Width of ellipse
        height:
            Height of ellipse
        fill:
            Fill color, by default None
        color:
            Alias of fill, by default None
        outline:
            Outline color, by default None
        stroke_width:
            Stroke width, by default 1
        """
        draw = ImageDraw.Draw(self.image)
        to_width = width + position[0]
        to_height = height + position[1]

        if color:
            fill = color

        draw.ellipse(
            position + (to_width, to_height),
            outline=outline,
            fill=fill,
            width=stroke_width,
        )

        return self

    def polygon(
        self,
        coordinates: list,
        fill: Color | None = None,
        color: Color | None = None,
        outline: Color | None = None,
    ) -> Editor:
        """Draw a polygon.

        Parameters
        ----------
        coordinates:
            Coordinates to draw
        fill:
            Fill color, by default None
        color:
            Alias of fill, by default None
        outline:
            Outline color, by default None
        """
        if color:
            fill = color

        draw = ImageDraw.Draw(self.image)
        draw.polygon(coordinates, fill=fill, outline=outline)

        return self

    def arc(
        self,
        position: tuple[float, float],
        width: float,
        height: float,
        start: float,
        rotation: float,
        fill: Color | None = None,
        color: Color | None = None,
        stroke_width: float = 1,
    ) -> Editor:
        """Draw arc.

        Parameters
        ----------
        position:
            Position to draw arc
        width:
            Width or arc
        height:
            Height of arch
        start:
            Start position of arch
        rotation:
            Rotation in degree
        fill:
            Fill color, by default None
        color:
            Alias of fill, by default None
        stroke_width:
            Stroke width, by default 1
        """
        draw = ImageDraw.Draw(self.image)

        start = start - 90
        end = rotation - 90

        if color:
            fill = color

        draw.arc(
            position + (position[0] + width, position[1] + height),
            start,
            end,
            fill,
            width=stroke_width,
        )

        return self

    def show(self):
        """Show the image."""
        self.image.show()

    def save(self, fp: str, file_format: str | None = None, **params):
        """Save the image.

        Parameters
        ----------
        fp:
            File path
        file_format:
            File format, by default None
        """
        self.image.save(fp, file_format, **params)
