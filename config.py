import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise Exception(".env not found")

TOKEN = os.environ.get("API_TOKEN")
WEBHOOK_HOST = os.environ.get("WEBHOOK_HOST")
WEBHOOK_PORT = os.environ.get("WEBHOOK_PORT")
WEBHOOK_URL_BASE = "https://%s" % (WEBHOOK_HOST,)
WEBHOOK_URL_PATH = "/%s/" % (TOKEN)
FLASK_PORT = int(os.environ.get('FLASK_PORT', 5000))