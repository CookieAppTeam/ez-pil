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

    # Creating nextcord.File object from image_bytes from editor
    file = discord.File(fp=editor.image_bytes, filename='circle.png')

    await ctx.respond(file=file)

bot.run("TOKEN")
