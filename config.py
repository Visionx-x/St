from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID","9333070"))
API_HASH = getenv("API_HASH","511eb11eda4af78ec8f9a0a7de9e1241")

BOT_TOKEN = getenv("BOT_TOKEN","6505771827:AAHFZVhiKg6J1hmqljnsSbCduXBVDCSRQYA")
OWNER_ID = int(getenv("OWNER_ID", "5016109398"))
MONGO_DB_URI = "mongodb+srv://atlas-sample-dataset-load-668a76c3227ccc52e298125a:Visionbot@visionbot.bhbwcls.mongodb.net/?retryWrites=true&w=majority&appName=Visionbot" #getenv("MONGO_DB_URI","mongodb+srv://Public74:Public74@public74.ulukh3x.mongodb.net/?retryWrites=true&w=majority&appName=Public74")
MUST_JOIN = ["thanos_pro", "learningbots79"]
