# Notion-Powered Static Site Generator

A modern static site generator that uses Notion as a CMS, allowing you to write and manage content in Notion while generating a beautiful static website. Perfect for personal blogs, documentation sites, and portfolios.

## Features

### Content Management
- **Notion Integration**
  - Write and manage content in Notion
  - Support for rich text formatting
  - Images and media embedding
  - Code blocks with syntax highlighting
  - Lists and tables
  - Bookmarks and link previews
  - YouTube video embeds

### Site Features
- **Modern Design**
  - Responsive layout
  - Dark/light theme toggle
  - Clean typography
  - Tag-based navigation
  - Archive page with yearly grouping
  - Progress bar while reading
  - Back to top button
  - Image lazy loading
  - Smooth scrolling
  - Estimated reading times

- **Gigs Page**
  - List and calendar views of concert history
  - Integration with Notion database
  - Stats dashboard showing total gigs, venues, and artists
  - Optional setlist links and notes
  - Interactive calendar with year/month navigation
  - Responsive design for all devices
  - Yearly grouping in list view

- **Development**
  - Hot reload during development
  - File watching for instant updates
  - Local development server
  - Template customization
  - Asset management

- **Performance**
  - Fast static HTML generation
  - Optimized asset loading
  - Lazy image loading
  - SEO-friendly output
  - Minimal JavaScript

## Quick Start

1. **Prerequisites**
   - Python 3.8 or higher
   - A Notion account
   - A Notion integration token

2. **Installation**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd your-site-directory

   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Running the Site**
   ```bash
   # Generate the site
   python3 -m src.generator.site_generator
   
   # View the generated site
   # The site will be generated in the 'output' directory
   # You can serve it using any static file server
   ```

4. **Configuration**
   Create a `.env` file in the project root:
   ```
   NOTION_API_KEY=your_integration_token
   NOTION_DATABASE_ID=your_database_id
   NOTION_GIGS_DATABASE_ID=your_gigs_database_id
   ```

## Notion Setup

### Database Structure
The site generator expects specific Notion database structures:

1. **Main Database**
   - This is your content index/registry
   - Set `NOTION_DATABASE_ID` to this database's ID

2. **Gigs Database** (Optional)
   - Set `NOTION_GIGS_DATABASE_ID` to this database's ID
   - Required Properties:
     - `Gig` (title): Unique identifier for each gig
     - `Date` (date): When the gig took place
     - `Artist` (rich_text): Name of the artist/band
     - `Venue` (rich_text): Name of the venue
   - Optional Properties:
     - `location` (rich_text): Location of the venue (defaults to venue name)
     - `Notes` (rich_text): Additional notes about the gig
     - `Setlist` (url): Link to the setlist (e.g., from setlist.fm)

3. **Content Pages**
   - Each database entry points to a separate Notion page via the `Content` property
   - The actual article content lives in these linked pages
   - The site generator fetches content from these pages, not the database entries

### Important Notes
- Content must be in separate pages linked via the `Content` property
- The database entries act as a registry/index
- Do not put content directly in database entries
- Always link to full content pages

This two-level structure (database → content pages) allows for better content organization and richer formatting options.

## Project Structure

```
.
├── src/
│   ├── generator/        # Site generation logic
│   │   └── site_generator.py
│   ├── notion/          # Notion API integration
│   │   └── processor.py
│   ├── static/          # Static assets
│   │   ├── css/         # Stylesheets
│   │   └── js/          # JavaScript files
│   └── templates/       # Jinja2 templates
│       ├── base.html    # Base template with common elements
│       ├── index.html   # Home page template
│       ├── post.html    # Article template
│       ├── archive.html # Archive page template
│       └── gigs.html    # Gigs page template
├── .env                # Environment variables
├── .gitignore         # Git ignore rules
└── README.md          # Documentation
```

## Templates

The site uses Jinja2 templates with a modular structure:

### base.html
- Common elements and layout
- Dark/light theme toggle
- Reading progress bar
- Back to top button
- Navigation menu
- Meta tags and SEO
- Asset loading

### index.html
- Article previews
- Tag filtering
- Clean card layout
- Pagination support

### post.html
- Article content
- Meta information
  - Publication date
  - Reading time estimate
  - Tags
- Lazy image loading
- Code syntax highlighting

### archive.html
- Yearly grouping of articles
- Chronological listing
- Interactive hover effects
- Reading time estimates
- Responsive layout
- Tag display and filtering

### gigs.html
- Dual-view layout:
  - List view with yearly grouping
  - Full calendar view using FullCalendar
- Stats dashboard showing:
  - Total number of gigs
  - Number of unique venues
  - Number of unique artists
- Interactive features:
  - View switching between list and calendar
  - Calendar navigation
  - Setlist links when available
  - Responsive design for all screen sizes

## Interactive Features

### Theme Toggle
- Dark/light theme support
- Theme preference saved in localStorage
- Smooth transition between themes
- Accessible toggle button

### Reading Progress
- Progress bar at top of page
- Shows reading progress while scrolling
- Smooth updates
- Minimal and unobtrusive

### Back to Top
- Fixed position button
- Appears after scrolling
- Smooth scroll to top
- Responsive design

### Image Loading
- Lazy loading for images
- Loading on scroll
- Prevents unnecessary bandwidth usage
- Improved page load times

### Smooth Scrolling
- Smooth scroll for internal links
- Enhanced navigation experience
- Configurable scroll behavior
- Cross-browser support

## Customization

1. **Styling**
   - Edit CSS variables in `base.html` for theme colors
   - Modify typography and spacing
   - Customize responsive breakpoints
   - Add new animations and transitions

2. **Templates**
   - Customize existing templates
   - Add new template files
   - Modify layouts and components
   - Add new interactive features

3. **Configuration**
   - Update site settings in `site_generator.py`
   - Customize Notion processing in `processor.py`
   - Configure build options
   - Add new functionality

## Development

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints
   - Add comprehensive docstrings
   - Keep functions focused and modular

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Notion API](https://developers.notion.com/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [Python Static Site Generator Community](https://www.staticgen.com/)
