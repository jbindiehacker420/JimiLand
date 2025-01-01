from notion_client import Client
from dotenv import load_dotenv
import os

def test_notion_connection():
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    notion_token = os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    print(f"Testing Notion API connection...")
    print(f"Database ID: {database_id}")
    
    try:
        # Initialize the Notion client
        notion = Client(auth=notion_token)
        
        # Try to retrieve the database
        database = notion.databases.retrieve(database_id=database_id)
        
        print("\n✅ Successfully connected to Notion API!")
        print("\nDatabase Information:")
        print(f"Title: {database.get('title', [{}])[0].get('plain_text', 'No title')}")
        print(f"Description: {database.get('description', 'No description')}")
        
        # List the first few pages in the database
        print("\nFetching first few pages...")
        pages = notion.databases.query(
            database_id=database_id,
            page_size=3
        )
        
        if pages["results"]:
            print("\nFound the following pages:")
            for page in pages["results"]:
                # Try to get the title from properties
                title_prop = next(iter(page.get("properties", {}).values()))
                if title_prop.get("title"):
                    title = title_prop["title"][0]["plain_text"] if title_prop["title"] else "Untitled"
                else:
                    title = "Untitled"
                print(f"- {title}")
                
                print("\nPage properties:")
                for prop_name, prop_value in page.get("properties", {}).items():
                    print(f"{prop_name}: {prop_value}")
                print("\nPage content:")
                blocks = notion.blocks.children.list(block_id=page["id"])
                for block in blocks.get("results", []):
                    print(f"Block type: {block.get('type')}")
                    print(f"Block content: {block}")
        else:
            print("No pages found in the database.")
            
    except Exception as e:
        print("\n❌ Error connecting to Notion:")
        print(f"Error details: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check if your NOTION_API_KEY is correct")
        print("2. Verify that the database ID is correct")
        print("3. Ensure the integration has access to the database")
        print("4. Check if the database ID is in the correct format")

if __name__ == "__main__":
    test_notion_connection()
