from ez_pil import Canvas, Editor, Font

user_data = {  # Most likely coming from database or calculation
    "name": "tibue99",
    "xp": 420,
    "next_level_xp": 6900,
    "level": 42,
    "percentage": 23,
}

background = Editor(Canvas((900, 300), color="#23272A"))
profile = Editor("assets/pfp.png").resize((150, 150)).circle_image()

# To use users profile picture load it from url using the load_image/load_image_async function
# profile_image = load_image(ctx.user.display_avatar.url)
# profile = Editor(profile_image).resize((200, 200)).circle_image()

poppins = Font.poppins(size=40)
poppins_small = Font.poppins(size=30)

card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

background.polygon(card_right_shape, "#2C2F33")
background.paste(profile, (30, 30))

background.rectangle((30, 220), width=650, height=40, fill="#494b4f", radius=20)
background.bar(
    (30, 220),
    max_width=650,
    height=40,
    percentage=user_data["percentage"],
    fill="#3db374",
    radius=20,
    stroke_width=0,
)
background.text((200, 40), user_data["name"], font=poppins, color="white")

background.rectangle((200, 100), width=350, height=2, fill="#17F3F6")
background.text(
    (200, 130),
    f"Level : {user_data['level']}  XP : {user_data['xp']} / {user_data['next_level_xp']}",
    font=poppins_small,
    color="white",
)


background.show()
