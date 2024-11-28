import argparse
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def extract_links(url, classname):
    # Start Playwright and launch the browser
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Navigate to the YouTube URL
        page.goto(url, timeout=60000)
        # Wait for network to be idle (no activity for at least 500ms)
        page.wait_for_load_state("networkidle")
        
        # Additional wait to ensure dynamic content is loaded
        page.wait_for_load_state("domcontentloaded")
        
        # Get the page content
        content = page.content()

        # Close the browser
        browser.close()
    
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    # Try finding elements with a more specific selector
    elements = soup.select(f'a[class*="{classname}"]')
    if not elements:
        # Fallback to searching for any link containing the class substring
        elements = soup.find_all(lambda tag: tag.name == 'a' and classname in str(tag.get('class', [])))
    
    # Extract the href attributes
    links = [el.get('href') for el in elements if el.get('href')]
    return links

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Extract href attributes from a YouTube page.")
    parser.add_argument('url', type=str, help="YouTube link to extract hrefs from.")
    parser.add_argument('--thumb', action='store_true', help="Use thumbnail classname.")
    args = parser.parse_args()
    
    # Determine the classname based on the flag
    classname = "yt-video-attribute-view-model__link-container" if args.thumb else "yt-core-attributed-string__link"
    # Extract links

    try:
        links = extract_links(args.url, classname)

        if not links:
            print("No links found with the specified class.")
            return

        links = [link for link in links if link.startswith("/watch")]
        links = [f"https://www.youtube.com{link}" for link in links]

        import os
        from datetime import datetime
        
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = args.url.split('/')[-1]  # Get the last part of the URL
        filename = f'extracted_links_{current_time}.txt'
        
        # Create folder if it doesn't exist
        destination_folder = os.path.join('downloads', folder_name)
        os.makedirs(destination_folder, exist_ok=True)
        
        # Create file path inside the folder
        file_path = os.path.join(destination_folder, filename)
        
        # Write links to file
        
        with open(file_path, 'w') as file:
            for link in links:
                file.write(link + '\n')

        print(f"--- Links saved to {file_path} ---")
        
        # Download each link as mp3 using yt-dlp
        for link in links:
            import subprocess
            subprocess.run([
                'yt-dlp',
                '-x',  # Extract audio
                '--audio-format', 'mp3',  # Convert to mp3
                '--audio-quality', '0',  # Best quality
                '-o', f'{folder_name}/%(title)s.%(ext)s',  # Save in folder
                link
            ])

        if links:
            print("Extracted Links:")
            for link in links:
                print(link)
        else:
            print("No links found with the specified class.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()