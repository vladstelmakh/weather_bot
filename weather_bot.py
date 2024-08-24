import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext


TELEGRAM_API_TOKEN = '7406506174:AAEQrmtxsXRAw0p320oCjZ72SqzB9lrqAPk'

# Visual Crossing API Key
WEATHER_API_KEY = 'UU86W6H9ALAQGDGVHJW8VFCNA'


# Function to get the weather with API Visual Crossing
def get_weather(location: str) -> str:
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?key={WEATHER_API_KEY}&unitGroup=metric'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        current_conditions = data['currentConditions']
        temperature = current_conditions['temp']
        conditions = current_conditions['conditions']
        weather_info = f"The current temperature in {location} is {temperature}°C with {conditions}."
        return weather_info
    else:
        return "Sorry, I couldn't retrieve the weather data."


# Function for the command /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'Hello! I can provide you with the current weather information. Just send me the name of the city!')


# Function for processing messages with the name of the city
async def weather(update: Update, context: CallbackContext) -> None:
    location = update.message.text
    weather_info = get_weather(location)
    await update.message.reply_text(weather_info)


def main() -> None:
    # Creating a bot
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    #  /start
    application.add_handler(CommandHandler("start", start))

    # Processing of user messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, weather))

    # Running a bot
    application.run_polling()


if __name__ == '__main__':
    main()
