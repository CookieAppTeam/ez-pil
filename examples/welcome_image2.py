from ez_pil import Editor, Font, load_image


background = load_image("https://cdn.cookieapp.me/banner/space.png")

background = Editor(background).resize((800, 450))
profile = Editor("assets/pfp.png").resize((150, 150)).circle_image()

# To use users profile picture load it from url using the load_image/load_image_async function
# profile_image = load_image(ctx.user.display_avatar.url)
# profile = Editor(profile_image).resize((150, 150)).circle_image()


# Fonts
poppins = Font.poppins(size=50, variant="bold")
poppins_small = Font.poppins(size=25, variant="regular")
poppins_light = Font.poppins(size=20, variant="light")

background.paste(profile, (325, 90))
background.ellipse((325, 90), 150, 150, outline="#182330", stroke_width=4)
background.text(
    (400, 260),
    "WELCOME",
    color="white",
    font=poppins,
    align="center",
    stroke_width=2,
)
background.text(
    (400, 325),
    "tibue99",
    color="white",
    font=poppins_small,
    align="center",
)
background.text(
    (400, 360),
    "You are the 457th Member",
    color="#0BE7F5",
    font=poppins_small,
    align="center",
)

background.show()
