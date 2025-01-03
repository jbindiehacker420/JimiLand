#!/usr/bin/env python3
"""
Build script for generating and serving the static site.
Supports both one-time builds and development mode with auto-rebuild.
"""

import os
import sys
import time
import http.server
import socketserver
import argparse
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.generator.site_generator import SiteGenerator
from src.spotify.spotify import get_current_track

class RebuildHandler(FileSystemEventHandler):
    """Handles file system events to trigger site rebuilds."""
    
    def __init__(self, generator):
        self.generator = generator
        self.last_build = 0
        self.build_delay = 1  # Minimum seconds between builds
        
    def on_any_event(self, event):
        """Rebuild site on any file change, with rate limiting."""
        if event.is_directory:
            return
            
        # Skip temporary files
        if event.src_path.endswith('.tmp'):
            return
            
        # Implement rate limiting
        current_time = time.time()
        if current_time - self.last_build > self.build_delay:
            print(f"\nRebuilding site due to changes in {event.src_path}")
            self.generator.generate_site()
            self.last_build = current_time

def serve_site(directory, port=8000):
    """
    Serve the static site using Python's built-in HTTP server.
    
    Args:
        directory: Directory containing the static site
        port: Port number to serve on
    """
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)
    
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving site at http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server...")
            httpd.shutdown()

def main():
    """Main entry point for the build script."""
    parser = argparse.ArgumentParser(description="Build and serve the static site")
    parser.add_argument("--serve", action="store_true", help="Start development server")
    parser.add_argument("--port", type=int, default=8000, help="Port for development server")
    parser.add_argument("--watch", action="store_true", help="Watch for changes and rebuild")
    args = parser.parse_args()
    
    # Set up paths
    base_dir = Path(__file__).parent
    template_dir = base_dir / "src" / "templates"
    output_dir = base_dir / "output"
    
    # Initialize site generator
    generator = SiteGenerator(str(output_dir), str(template_dir))
    
    # Generate site
    print("Generating site...")
    generator.generate_site()
    print("Site generation complete!")
    
    if args.watch or args.serve:
        # Set up file watcher
        observer = Observer()
        handler = RebuildHandler(generator)
        
        # Watch template and content directories
        for watch_dir in [template_dir, base_dir / "content"]:
            observer.schedule(handler, str(watch_dir), recursive=True)
        
        observer.start()
        print("Watching for changes...")
        
        if args.serve:
            # Start development server
            serve_site(str(output_dir), args.port)
            observer.stop()
        else:
            # Watch mode only
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                print("\nStopping file watcher...")
        
        observer.join()

class SiteGenerator:
    def __init__(self, output_dir, template_dir):
        self.output_dir = output_dir
        self.template_dir = template_dir

    def generate_site(self):
        # Get Spotify data
        current_track = get_current_track()
        
        # Add to your template context
        context = {
            'current_track': current_track
        }
        # Your existing build code...

if __name__ == "__main__":
    main()
