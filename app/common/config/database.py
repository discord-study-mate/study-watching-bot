import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get logger
logger = logging.getLogger(__name__)

# MongoDB connection string
MONGODB_URI = os.getenv("MONGODB_URI")

def get_database():
    """
    Function to get the MongoDB database connection
    """
    try:
        # Create a connection
        client = MongoClient(MONGODB_URI)
        
        # Get default database
        db = client.get_default_database()
        
        return db
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise e

def test_connection():
    """
    Test the MongoDB connection
    """
    try:
        client = MongoClient(MONGODB_URI)
        # Command to check if the server is responding
        client.admin.command('ping')
        return True
    except Exception as e:
        logger.error(f"MongoDB connection test failed: {e}")
        raise e 