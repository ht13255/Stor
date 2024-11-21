# 파일 경로: app.py

import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from PyPDF2 import PdfMerger
from io import BytesIO
import os

# 링크 크롤링 함수
def get_all_links(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag['href']
            full_url = urljoin(base_url, href)
            if urlparse(full_url).netloc == urlparse(base_url).netloc:  # 같은 도메인만
                links.add(full_url)
        return links
    except Exception as e:
        st.error(f"링크를 가져오는 중 오류가 발생했습니다: {e}")
        return set()

# Selenium으로 PDF 저장 함수
def save_page_as_pdf(url, output_dir):
    try:
        # Chrome 옵션 설정
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 브라우저 창을 표시하지 않음
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # PDF 저장 설정
        chrome_prefs = {
            "printing.print_preview_sticky_settings.appState": '{"recentDestinations":[{"id":"Save as PDF","origin":"local","account":""}],"selectedDestinationId":"Save as PDF","version":2}',
            "savefile.default_directory": output_dir,
        }
        chrome_options.add_experimental_option("prefs", chrome_prefs)
        chrome_options.add_argument("--kiosk-printing")

        # WebDriver 시작
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        pdf_file_path = os.path.join(output_dir, f"{urlparse(url).path.replace('/', '_')}.pdf")
        driver.execute_script("window.print();")  # PDF 저장 실행
        driver.quit()
        return pdf_file_path
    except Exception as e:
        st.warning(f"PDF로 저장하는 중 오류 발생 ({url}): {e}")
        return None

# PDF 통합 함수
def merge_pdfs(pdf_paths, output_path):
    merger = PdfMerger()
    for pdf_path in pdf_paths:
        merger.append(pdf_path)
    merger.write(output_path)
    merger.close()
    return output_path

# Streamlit 앱
def main():
    st.title("사이트의 모든 링크를 크롤링 후 PDF로 변환")
    st.write("사이트의 모든 링크 페이지를 크롬의 인쇄 기능을 이용하여 PDF로 저장하고, 이를 통합합니다.")

    url = st.text_input("사이트 URL 입력")
    if st.button("PDF 생성"):
        if url:
            # 임시 폴더 생성
            output_dir = "pdf_output"
            os.makedirs(output_dir, exist_ok=True)

            st.info("사이트 링크를 수집 중입니다...")
            links = get_all_links(url)

            if not links:
                st.warning("수집된 링크가 없습니다. URL을 확인해주세요.")
                return

            pdf_paths = []
            st.info("페이지를 PDF로 저장 중입니다...")
            for link in links:
                pdf_path = save_page_as_pdf(link, output_dir)
                if pdf_path:
                    pdf_paths.append(pdf_path)

            if pdf_paths:
                st.info("PDF 통합 중입니다...")
                final_pdf_path = os.path.join(output_dir, "merged_output.pdf")
                merge_pdfs(pdf_paths, final_pdf_path)

                st.success("PDF 생성 완료!")
                with open(final_pdf_path, "rb") as f:
                    st.download_button(
                        label="통합 PDF 다운로드",
                        data=f,
                        file_name="merged_output.pdf",
                        mime="application/pdf",
                    )
            else:
                st.warning("PDF로 저장된 파일이 없습니다.")
        else:
            st.warning("URL을 입력하세요.")

if __name__ == "__main__":
    main()