import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from lxml import html  # Import lxml for parsing




def scrape_website(website):
    """Connects to a website using a headless browser and retrieves the HTML content."""
    print("Connecting to Scraping Browser...")

    
    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--disable-css')
    options.add_argument('--disable-javascript')

    
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    try:
        driver.get(website)  # Load the specified website
        print("Page Loaded...")
        html = driver.page_source  # Get the HTML source of the page
        # time.sleep(10)  # Wait for additional content to load (if necessary)
        
        return html  # Return the HTML content
    finally:
        driver.quit()  # Ensure the browser is closed after scraping



def extract_body_content(html_content):
    """Extracts the body content from the provided HTML using lxml."""
    tree = html.fromstring(html_content)  # Parse the HTML content
    body_content = tree.xpath('//body')  # Use XPath to get the body element
    if body_content:
        return html.tostring(body_content[0], encoding='unicode')  # Return the body content as a string
    return ""  # Return an empty string if no body content is found



def clean_body_content(body_content):
    """Cleans the body content by removing scripts, styles, and unnecessary whitespace using lxml."""
    tree = html.fromstring(body_content)  # Parse the body content

    # Remove script and style elements
    for element in tree.xpath('//script | //style'):
        element.getparent().remove(element)

    cleaned_content = ''.join(tree.xpath('//text()'))  # Get all text content
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )  # Strip whitespace from each line and remove empty lines
    
    return cleaned_content  # Return the cleaned text content



def remove_unwanted_sections(html_content):
    """Removes headers, footers, reviews, and other unwanted sections from the HTML content using lxml."""
    tree = html.fromstring(html_content)  # Parse the HTML content
    
    # Common XPath expressions for headers, footers, and reviews
    unwanted_selectors = [
        '//header', '//footer',  # Standard HTML5 tags
        '//*[contains(@class, "header")]', '//*[contains(@class, "footer")]',  # Classes containing these words
        '//*[contains(@id, "header")]', '//*[contains(@id, "footer")]',
        '//*[contains(@class, "nav")]', '//*[contains(@id, "nav")]',  # Navigation elements
        '//*[contains(@class, "menu")]', '//*[contains(@id, "menu")]',
        '//*[contains(@class, "review")]', '//*[contains(@id, "review")]',  # Review sections
        '//*[contains(@class, "comment")]', '//*[contains(@id, "comment")]',
        '//*[contains(@class, "rating")]', '//*[contains(@id, "rating")]'
    ]
    
    # Remove elements matching the selectors
    for selector in unwanted_selectors:
        for element in tree.xpath(selector):
            element.getparent().remove(element)  # Remove the selected elements from the tree
    
    return html.tostring(tree, encoding='unicode')  # Return the modified HTML as a string


# LLM can process maximum 8000 character in one batch

def split_dom_content(dom_content, max_length=6000):
    """Splits the DOM content into chunks of a specified maximum length."""
    # Use list comprehension instead of set for faster sequential access
    # Pre-calculate length once for better performance
    content_length = len(dom_content)
    return [
        dom_content[i:i + max_length] 
        for i in range(0, content_length, max_length)
    ]  # Return a list of content chunks