from notion_client import Client
from dotenv import load_dotenv
import os
import json
from datetime import datetime

def extract_page_id(url):
    """Extract the page ID from a Notion URL."""
    # Remove any query parameters
    url = url.split('?')[0]
    # Get the last part of the URL
    return url.split('-')[-1]

def get_text_content(rich_text_list):
    """Extract full text content from rich_text list."""
    return ''.join([text.get('plain_text', '') for text in rich_text_list])

def fetch_block_content(notion, block_id, level=0):
    """Recursively fetch block content."""
    content = []
    try:
        blocks = notion.blocks.children.list(block_id=block_id)
        
        for block in blocks.get('results', []):
            block_type = block.get('type')
            block_content = {}
            
            if block_type == 'paragraph':
                text_content = get_text_content(block[block_type].get('rich_text', []))
                block_content = {
                    'type': 'paragraph',
                    'content': text_content,
                    'annotations': block[block_type].get('rich_text', [{}])[0].get('annotations', {}) if block[block_type].get('rich_text') else {}
                }
            
            elif block_type in ['heading_1', 'heading_2', 'heading_3']:
                text = get_text_content(block[block_type].get('rich_text', []))
                block_content = {'type': block_type, 'content': text}
            
            elif block_type in ['bulleted_list_item', 'numbered_list_item']:
                text = get_text_content(block[block_type].get('rich_text', []))
                block_content = {
                    'type': 'bullet' if block_type == 'bulleted_list_item' else 'number',
                    'content': text.strip()
                }
            
            elif block_type == 'image':
                url = block[block_type].get('file', {}).get('url', '')
                caption = get_text_content(block[block_type].get('caption', []))
                block_content = {'type': 'image', 'url': url, 'caption': caption}
            
            elif block_type == 'code':
                code = get_text_content(block[block_type].get('rich_text', []))
                language = block[block_type].get('language', 'plain text')
                block_content = {'type': 'code', 'content': code, 'language': language}
            
            elif block_type == 'quote':
                text = get_text_content(block[block_type].get('rich_text', []))
                block_content = {'type': 'quote', 'content': text}
            
            elif block_type == 'divider':
                block_content = {'type': 'divider'}
            
            if block_content:
                content.append(block_content)
            
            # Check if block has children
            if block.get('has_children', False):
                child_content = fetch_block_content(notion, block['id'], level + 1)
                content.extend(child_content)
    
    except Exception as e:
        print(f"Error fetching content: {str(e)}")
    
    return content

def fetch_notion_content():
    # Load environment variables
    load_dotenv()
    
    notion_token = os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    print("Connecting to Notion database...")
    
    try:
        notion = Client(auth=notion_token)
        
        # Query the database
        pages = notion.databases.query(
            database_id=database_id,
            page_size=100
        )
        
        articles = []
        
        for page in pages["results"]:
            article = {
                'title': get_text_content(page['properties']['Title']['title']),
                'description': get_text_content(page['properties']['Description']['rich_text']),
                'date': page['properties']['Date']['date']['start'] if page['properties']['Date']['date'] else None,
                'tag': get_text_content(page['properties']['tag']['rich_text']),
                'slug': get_text_content(page['properties']['slug']['rich_text']),
                'published': page['properties']['Published']['checkbox'],
                'content_url': get_text_content(page['properties']['Content']['rich_text'])
            }
            
            if article['content_url']:
                print(f"\nFetching content for: {article['title']}")
                content_page_id = extract_page_id(article['content_url'])
                article['content'] = fetch_block_content(notion, content_page_id)
            
            articles.append(article)
        
        # Save to a JSON file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"notion_content_export_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Successfully exported {len(articles)} articles with content!")
        print(f"Data saved to: {output_file}")
        
        # Print a preview of the first article
        if articles:
            print("\nPreview of first article:")
            article = articles[0]
            print(f"Title: {article['title']}")
            print(f"Description: {article['description']}")
            print(f"Date: {article['date']}")
            print(f"Tag: {article['tag']}")
            print("\nContent Preview:")
            
            current_section = None
            for block in article['content']:
                if block['type'].startswith('heading'):
                    current_section = block['content']
                    print(f"\n{block['content']}")
                elif block['type'] == 'bullet' and current_section == 'Set 1:' or current_section == 'Set 2:':
                    print(f"  • {block['content']}")
                elif block['type'] == 'paragraph':
                    print(f"{block['content'][:100]}...")
        
    except Exception as e:
        print(f"\n❌ Error during export:")
        print(f"Error details: {str(e)}")

if __name__ == "__main__":
    fetch_notion_content()
