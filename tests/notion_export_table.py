from notion_client import Client
from dotenv import load_dotenv
import os
import json
from datetime import datetime

def export_notion_table():
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    notion_token = os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    print(f"Connecting to Notion database...")
    
    try:
        # Initialize the Notion client
        notion = Client(auth=notion_token)
        
        # Get database schema first
        database = notion.databases.retrieve(database_id=database_id)
        properties = database.get('properties', {})
        
        print("\nDatabase Properties:")
        for prop_name, prop_details in properties.items():
            print(f"- {prop_name} ({prop_details.get('type', 'unknown type')})")
        
        # Query all pages in the database
        print("\nFetching all pages...")
        pages = notion.databases.query(
            database_id=database_id,
            page_size=100  # Adjust if you have more pages
        )
        
        # Process and store the results
        table_data = []
        
        for page in pages["results"]:
            page_data = {}
            page_data["page_id"] = page["id"]
            page_data["url"] = page["url"]
            
            # Extract all properties
            for prop_name, prop_details in page["properties"].items():
                prop_type = prop_details["type"]
                
                if prop_type == "title":
                    value = prop_details["title"][0]["plain_text"] if prop_details["title"] else ""
                elif prop_type == "rich_text":
                    value = prop_details["rich_text"][0]["plain_text"] if prop_details["rich_text"] else ""
                elif prop_type == "date":
                    value = prop_details["date"]["start"] if prop_details["date"] else None
                elif prop_type == "multi_select":
                    value = [item["name"] for item in prop_details["multi_select"]]
                elif prop_type == "select":
                    value = prop_details["select"]["name"] if prop_details["select"] else None
                elif prop_type == "checkbox":
                    value = prop_details["checkbox"]
                elif prop_type == "url":
                    value = prop_details["url"]
                else:
                    value = str(prop_details.get(prop_type, ""))
                
                page_data[prop_name] = value
            
            table_data.append(page_data)
        
        # Save to a JSON file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"notion_table_export_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(table_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Successfully exported {len(table_data)} pages!")
        print(f"Data saved to: {output_file}")
        
        # Print a preview of the data
        print("\nPreview of exported data:")
        for page in table_data[:3]:  # Show first 3 entries
            print("\nPage:")
            for key, value in page.items():
                print(f"  {key}: {value}")
            
    except Exception as e:
        print("\n❌ Error during export:")
        print(f"Error details: {str(e)}")

if __name__ == "__main__":
    export_notion_table()
