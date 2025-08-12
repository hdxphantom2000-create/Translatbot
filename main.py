import discord
from googletrans import Translator
import os
from dotenv import load_dotenv

# .env laden
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents setzen
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = discord.Client(intents=intents)
translator = Translator()

# Mapping von Flagge -> Sprachcode
FLAG_LANG_MAP = {
    "🇩🇪": "de",
    "🇬🇧": "en",
    "🇫🇷": "fr",
    "🇪🇸": "es",
    "🇮🇹": "it",
    "🇯🇵": "ja",
    "🇷🇺": "ru",
    "🇨🇳": "zh-cn",
}

# Funktion zum Senden langer Nachrichten
async def send_long_message(destination, text):
    for i in range(0, len(text), 2000):
        await destination.send(text[i:i+2000])

@bot.event
async def on_ready():
    print(f"✅ Bot eingeloggt als {bot.user}")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    emoji = str(reaction.emoji)

    if emoji in FLAG_LANG_MAP:
        lang_code = FLAG_LANG_MAP[emoji]
        try:
            original_text = reaction.message.content

            if not original_text.strip():
                await user.send("❌ Die Nachricht enthält keinen Text zum Übersetzen.")
                return

            translated = translator.translate(original_text, dest=lang_code)

            # Privat senden (DM)
            await send_long_message(user, f"**Original:** {original_text}\n**Übersetzt ({lang_code}):** {translated.text}")

            # Bestätigung im Kanal
            await reaction.message.channel.send(f"{user.mention} ✅ Übersetzung per DM gesendet!")

        except Exception as e:
            await user.send(f"⚠️ Fehler beim Übersetzen: {str(e)}")

bot.run(TOKEN)

