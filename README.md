# Ez PIL
[![](https://img.shields.io/pypi/v/ez-pil.svg?style=for-the-badge&logo=pypi&color=yellow&logoColor=white)](https://pypi.org/project/ez-pil/)
[![](https://img.shields.io/pypi/l/ez-pil?style=for-the-badge)](https://github.com/CookieAppTeam/ez-pil/blob/master/LICENSE)

An easy-to-use extension for [PIL](https://github.com/python-pillow/Pillow) to edit and modify images.

## Installation
Python 3.12 or higher is required.
```bash
pip install ez-pil
```

## Examples
Example for Discord Bot integration. For further information, see the [Documentation](https://ez-pil.readthedocs.io/).

```python
import discord
import ezcord
from ez_pil import Editor, load_image_async

bot = ezcord.Bot()

@bot.slash_command()
async def circle(ctx):
    # Load the image using `load_image_async` method
    image = await load_image_async(ctx.author.display_avatar.url)

    # Initialize the editor and pass image as a parameter
    editor = Editor(image).circle_image()

    # Creating File object from image_bytes from editor
    file = discord.File(fp=editor.image_bytes, filename='circle.png')

    await ctx.respond(file=file)

bot.run("TOKEN")
```

## Credits
This repository is a fork of [easy-pil](https://github.com/shahriyardx/easy-pil), because the original repository is no longer maintained 👻
