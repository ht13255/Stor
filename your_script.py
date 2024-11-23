import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
from fpdf import FPDF
import os

# Function to extract all links from a webpage
def get_all_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = [a.get("href") for a in soup.find_all("a", href=True)]
        # Filter and format links (handle relative URLs)
        full_links = []
        for link in links:
            if link.startswith("http"):
                full_links.append(link)
            elif link.startswith("/"):
                full_links.append(f"{url.rstrip('/')}{link}")
        return list(set(full_links))  # Remove duplicates
    except Exception as e:
        st.error(f"Error fetching links: {e}")
        return []

# Function to extract the content of a webpage
def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(strip=True)  # Extract text content
    except Exception as e:
        st.error(f"Error fetching page content for {url}: {e}")
        return ""

# Function to save data to JSON
def save_as_json(data, output_file):
    with open(output_file, "w", encoding="utf-8") as f:  # UTF-8 지정
        json.dump(data, f, ensure_ascii=False, indent=4)

# Function to save data to PDF
def save_as_pdf(data, output_file):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for url, content in data.items():
        pdf.multi_cell(0, 10, f"URL: {url}\nContent:\n{content}\n\n")
    pdf.output(output_file)

# Streamlit App
st.title("Webpage Link Crawler and Content Extractor")

# Input URL
url = st.text_input("Enter the URL of the webpage to crawl:")
if url and st.button("Crawl"):
    st.info("Fetching links from the webpage...")
    links = get_all_links(url)
    
    if links:
        st.success(f"Found {len(links)} links. Extracting content...")
        content_data = {}
        
        for link in links:
            st.write(f"Processing: {link}")
            content = get_page_content(link)
            content_data[link] = content
        
        # Save results
        if content_data:
            os.makedirs("output", exist_ok=True)
            json_file = "output/website_content.json"
            pdf_file = "output/website_content.pdf"

            save_as_json(content_data, json_file)
            save_as_pdf(content_data, pdf_file)

            st.success("Content extraction complete!")
            st.write(f"JSON saved at: {json_file}")
            st.write(f"PDF saved at: {pdf_file}")

            # Allow downloads
            with open(json_file, "rb") as f:
                st.download_button("Download JSON", f, file_name="website_content.json")
            with open(pdf_file, "rb") as f:
                st.download_button("Download PDF", f, file_name="website_content.pdf")
    else:
        st.warning("No links found on the provided URL.")