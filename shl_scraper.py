import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time
import re

BASE_URL = "https://www.shl.com"
START_PAGE = 0
STEP = 12

# Test Type Legend
TEST_TYPE_LEGEND = {
    "A": "Ability & Aptitude",
    "B": "Biodata & Situational Judgement",
    "C": "Competencies",
    "D": "Development & 360",
    "E": "Assessment Exercises",
    "K": "Knowledge & Skills",
    "P": "Personality & Behavior",
    "S": "Simulations"
}

def get_duration_from_page(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for p in soup.find_all("p"):
        if "Approximate Completion Time" in p.text:
            match = re.search(r"(\d+)", p.text)
            if match:
                return f"{match.group(1)} minutes"

    return "Not available"

def get_page_data(start):
    url = f"{BASE_URL}/solutions/products/product-catalog/?start={start}&type=1&type=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table_rows = soup.select('table tr[data-entity-id]')
    data = []

    for row in table_rows:
        name_tag = row.select_one('td a')
        name = name_tag.text.strip()
        link = urljoin(BASE_URL, name_tag['href'])

        cells = row.select('td')
        remote = 'Yes' if cells[1].find('span', class_='-yes') else 'No'
        adaptive = 'Yes' if cells[2].find('span', class_='-yes') else 'No'

        test_type_spans = cells[3].select('.product-catalogue__key')
        test_types = [TEST_TYPE_LEGEND.get(span.text.strip(), span.text.strip()) for span in test_type_spans]

        # 👇 New duration logic here
        duration = get_duration_from_page(link)

        data.append({
            "name": name,
            "url": link,
            "remote_testing": remote,
            "adaptive_irt": adaptive,
            "test_types": test_types,
            "Duration": duration
        })

    return data

def scrape_all(max_pages=32):  # 32 pages * 12 = 384 items max
    results = []
    start = START_PAGE
    page_count = 0

    while page_count < max_pages:
        print(f"Scraping page starting at: {start}")
        page_data = get_page_data(start)

        if not page_data:
            print("⚠️ Empty page detected. Might be last page.")
            break

        results.extend(page_data)
        start += STEP
        page_count += 1
        time.sleep(1)

    print(f"Scraped {len(results)} total assessments.")
    return results


if __name__ == "__main__":
    assessments = scrape_all()

    with open("individual_test_solutions.json", "a", encoding="utf-8") as f:
        json.dump(assessments, f, indent=2, ensure_ascii=False)

    print(f"✅ Scraped and saved {len(assessments)} assessments to individual_test_solutions.json")
