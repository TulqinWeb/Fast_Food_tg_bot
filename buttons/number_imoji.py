def number_to_emoji(number):
    # Har bir raqamni emoji shakliga o'tkazish
    digit_to_emoji = {
        "0": "0️⃣",
        "1": "1️⃣",
        "2": "2️⃣",
        "3": "3️⃣",
        "4": "4️⃣",
        "5": "5️⃣",
        "6": "6️⃣",
        "7": "7️⃣",
        "8": "8️⃣",
        "9": "9️⃣",
    }
    return ''.join(digit_to_emoji[digit] for digit in str(number))
