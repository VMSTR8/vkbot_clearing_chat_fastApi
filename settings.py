import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

CONFIRMATION_TOKEN = os.environ.get('CONFIRMATION_TOKEN')

OPEN_GROUP_TOKEN = os.environ.get('OPEN_GROUP_TOKEN')
CLOSED_GROUP_TOKEN = os.environ.get('CLOSED_GROUP_TOKEN')

SERVICE_TOKEN = os.environ.get('SERVICE_TOKEN')

ADMIN_ID = os.environ.get('ADMIN_ID')
GROUP_ID = os.environ.get('GROUP_ID')
