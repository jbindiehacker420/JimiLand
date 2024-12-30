"""
Configuration settings for the static site generator.
This module centralizes all configuration variables used throughout the application.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory paths
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATE_DIR = BASE_DIR / "src" / "templates"
OUTPUT_DIR = BASE_DIR / "output"
STATIC_DIR = BASE_DIR / "static"

# Notion settings
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

if not NOTION_API_KEY or not NOTION_DATABASE_ID:
    raise ValueError(
        "Missing required environment variables. "
        "Please ensure NOTION_API_KEY and NOTION_DATABASE_ID are set in your .env file."
    )

# Site settings
SITE_TITLE = "Jimi Land"  # Your blog title
SITE_DESCRIPTION = "Personal blog powered by Notion"
SITE_AUTHOR = "Josh Brown"
SITE_URL = "http://localhost:8000"  # Change this to your actual domain in production

# Blog settings
POSTS_PER_PAGE = 10  # Number of posts to display per page
DATE_FORMAT = "%B %d, %Y"  # Format for displaying dates

# Required Notion database properties
# These must match exactly with your Notion database property names
NOTION_PROPERTIES = {
    'title': 'title',
    'slug': 'slug',
    'date': 'date',
    'tags': 'tag',
    'description': 'description',
    'published': 'published',
    'content': 'content'
}
