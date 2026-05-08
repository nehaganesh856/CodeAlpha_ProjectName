# =========================================================
# COMPLETE WEB SCRAPING PROJECT USING BEAUTIFULSOUP
# =========================================================

# Install Required Libraries:
# pip install requests beautifulsoup4 pandas openpyxl

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# =========================================================
# STEP 1: CREATE EMPTY LISTS
# =========================================================

quotes_list = []
authors_list = []
tags_list = []

# =========================================================
# STEP 2: SCRAPE MULTIPLE PAGES
# =========================================================

for page in range(1, 6):

    # Website URL
    url = f"http://quotes.toscrape.com/page/{page}/"

    print(f"Scraping Page {page}...")

    # Send request to website
    response = requests.get(url)

    # Convert HTML into BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")

    # =====================================================
    # STEP 3: EXTRACT DATA
    # =====================================================

    quotes = soup.find_all("div", class_="quote")

    for quote in quotes:

        # Extract quote text
        text = quote.find("span", class_="text").text

        # Extract author name
        author = quote.find("small", class_="author").text

        # Extract tags
        tag_elements = quote.find_all("a", class_="tag")
        tag_text = ", ".join([tag.text for tag in tag_elements])

        # Store data in lists
        quotes_list.append(text)
        authors_list.append(author)
        tags_list.append(tag_text)

    # Delay to avoid overloading website
    time.sleep(1)

# =========================================================
# STEP 4: CREATE DATAFRAME
# =========================================================

df = pd.DataFrame({
    "Quote": quotes_list,
    "Author": authors_list,
    "Tags": tags_list
})

# =========================================================
# STEP 5: DISPLAY DATA
# =========================================================

print("\nScraping Completed Successfully!\n")

print(df.head())

# =========================================================
# STEP 6: SAVE DATASET
# =========================================================

# Save as CSV
df.to_csv("quotes_dataset.csv", index=False)

# Save as Excel
df.to_excel("quotes_dataset.xlsx", index=False)

# Save as JSON
df.to_json("quotes_dataset.json", orient="records")

# =========================================================
# STEP 7: BASIC DATA ANALYSIS
# =========================================================

print("\nTotal Quotes Collected:", len(df))

print("\nTop Authors:\n")
print(df["Author"].value_counts().head())

# =========================================================
# STEP 8: SEARCH SPECIFIC AUTHOR
# =========================================================

search_author = "Albert Einstein"

result = df[df["Author"] == search_author]

print(f"\nQuotes by {search_author}:\n")

print(result)

# =========================================================
# STEP 9: SAVE FILTERED DATA
# =========================================================

result.to_csv("einstein_quotes.csv", index=False)

print("\nAll Files Saved Successfully!")

# =========================================================
# FILES CREATED:
# 1. quotes_dataset.csv
# 2. quotes_dataset.xlsx
# 3. quotes_dataset.json
# 4. einstein_quotes.csv
# =========================================================