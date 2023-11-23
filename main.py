import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def extract_metadata_spans(url):
    # Initialize the WebDriver
    driver = webdriver.Chrome()  # or use any other browser/driver
    driver.get(url)

    # Wait for the metadata elements to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'metadata')))

    # Locate the 'metadata' divs
    metadata_divs = driver.find_elements(By.ID, 'metadata')

    # Find all span elements within the 'metadata-inline' div and extract text from each element
    list_spans = []
    for metadata_div in metadata_divs:
        try:
            spans = metadata_div.find_elements(By.TAG_NAME, 'span')[::2]
            for span in spans:
                span = span.text[5:]
                list_spans.append(span[:-7])
        except NoSuchElementException:
            pass
    print(f"list_spans: {list_spans}")
    # Close the driver
    driver.quit()
    return list_spans


def str_to_int(view_str):
    # Regular expression to match the number and the unit (k or mill)
    match = re.search(r'(\d+(?:,\d+)?(?:\.\d+)?)(\s*)(k|mill\.)?', view_str, re.IGNORECASE)

    if not match:
        return None

    # Extract the number and the unit
    number_str = match.group(1).replace(',', '.')
    number = float(number_str)
    unit = match.group(3) if match.group(3) else ''

    # Convert the number based on the unit
    if unit:
        if unit.lower() == 'k':
            number *= 1000
        elif unit.lower() == 'mill.':
            number *= 1000000
    return number

# Test the function with some examples

url = "https://youtube.com/"

converted_values = [str_to_int(s) for s in extract_metadata_spans(url=url)]
print(converted_values)