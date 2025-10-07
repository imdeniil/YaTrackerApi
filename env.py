import os
from dotenv import load_dotenv

load_dotenv()

TRACKER_API_KEY = os.environ.get("TRACKER_API_KEY")
TRACKER_ORG_ID = os.environ.get("TRACKER_ORG_ID")