from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_main = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add")
    ],
    [
        InlineKeyboardButton(text="➖ Kanal uzish", callback_data="remove")
    ],
    [
        InlineKeyboardButton(text="👨‍💻 Adminlar", callback_data="admins")
    ],
    [
        InlineKeyboardButton(text="📡 Barcha kanallar", callback_data="channels")
    ],
    [
        InlineKeyboardButton(text="✏️ Menyularni boshqarish", callback_data="manage_menus")
    ],
        [
        InlineKeyboardButton(text="✏️ Yangiliklarni boshqarish", callback_data="manage_news")
    ],
    [
        InlineKeyboardButton(text=" ⚙️ Boshqa sozlamalar", callback_data="settings")

    ],
    [
        InlineKeyboardButton("❌ Panelni yopish", callback_data="hide")
    ]
])

admin_second = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✏️ Matn o'zgartirish", callback_data="add_text")
    ],
    [
        InlineKeyboardButton(text="🕹 Tugma nomi", callback_data="button")
    ],
    [
        InlineKeyboardButton("🔝 Asosiy menyu", callback_data="main")
    ]
])

cancel = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="⛔️ Bekor qilish", callback_data="main"),
    ]
])

yes_no = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✅", callback_data="yes"),
        InlineKeyboardButton(text="❌", callback_data="no")
    ]
])


def generate_inline_keyboard(btn_list):
    inline_keyboard = InlineKeyboardMarkup()
    for btn in btn_list:
        if btn.startswith("🔙 Ortga qaytish"):
            inline_keyboard.add(InlineKeyboardButton(text=btn, callback_data="main"))
        else:
            inline_keyboard.add(InlineKeyboardButton(text=btn, callback_data=btn))

    return inline_keyboard


back_manage_menus = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⛔️ Bekor qilish", callback_data="manage_menus")]
])


def generate_inline_keyboard_menus(btn_list):
    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(InlineKeyboardButton(text="➕ Qo'shish", callback_data="add-sub-menu"))
    for btn in btn_list:
        inline_keyboard.add(InlineKeyboardButton(text=btn, callback_data=btn))
    inline_keyboard.add(InlineKeyboardButton(text="🔙 Ortga qaytish", callback_data="manage_menus"))
    return inline_keyboard


def create_channels_button(names):
    channels_button = InlineKeyboardMarkup()
    back = InlineKeyboardButton(text="🔝 Asosiy menyu", callback_data="main")
    for text, callback_data in names.items():
        button = InlineKeyboardButton(text=text, callback_data=callback_data)
        channels_button.add(button)
    channels_button.add(back)
    return channels_button


def create_admins_button(names):
    list = InlineKeyboardMarkup()
    add = InlineKeyboardButton(text="➕ Admin qo'shish", callback_data="add_admin")
    back = InlineKeyboardButton(text="🔝 Asosiy menyu", callback_data="main")
    list.add(add)
    for text, callback_data in names.items():
        button = InlineKeyboardButton(text=text, callback_data=callback_data)
        list.add(button)
    list.add(back)
    return list
