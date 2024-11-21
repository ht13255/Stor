# 파일 경로: app.py

import streamlit as st
from fpdf import FPDF
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from io import BytesIO
from PyPDF2 import PdfMerger

# PDF 생성 함수 (단일 페이지)
def create_pdf_from_text(title, text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # 제목 추가
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(10)

    # 내용 추가
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        if line.strip():  # 공백 라인 제거
            pdf.multi_cell(0, 10, line.strip())
    return pdf

# 사이트에서 모든 링크를 크롤링
def get_all_links(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag['href']
            full_url = urljoin(base_url, href)
            # 동일한 도메인 내 링크만 수집
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                links.add(full_url)
        return links
    except Exception as e:
        st.error(f"링크를 가져오는 중 오류가 발생했습니다: {e}")
        return set()

# 페이지 내용을 텍스트로 추출
def get_page_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "제목 없음"
        text = soup.get_text()
        return title, text
    except Exception as e:
        st.warning(f"페이지를 가져오는 중 오류가 발생했습니다 ({url}): {e}")
        return "오류 발생", f"페이지를 불러오지 못했습니다: {e}"

# PDF 통합 함수
def merge_pdfs(pdf_list):
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(BytesIO(pdf.output(dest="S").encode("latin1")))
    output_pdf = BytesIO()
    merger.write(output_pdf)
    merger.close()
    output_pdf.seek(0)
    return output_pdf

# Streamlit 앱
def main():
    st.title("사이트 링크 크롤링 및 PDF 통합 생성")
    st.write("사이트의 모든 링크를 크롤링하여 각 페이지를 PDF로 변환하고, 이를 통합합니다.")

    url = st.text_input("사이트 URL 입력")
    if st.button("PDF 생성"):
        if url:
            st.info("사이트 링크를 수집 중입니다...")
            links = get_all_links(url)

            if not links:
                st.warning("수집된 링크가 없습니다. URL을 확인해주세요.")
                return

            pdf_list = []
            st.info("페이지 내용을 PDF로 변환 중입니다...")
            for link in links:
                title, text = get_page_text(link)
                if text:
                    pdf = create_pdf_from_text(title, text)
                    pdf_list.append(pdf)

            if pdf_list:
                st.info("PDF 통합 중입니다...")
                final_pdf = merge_pdfs(pdf_list)
                st.success("PDF 생성 완료!")

                st.download_button(
                    label="통합 PDF 다운로드",
                    data=final_pdf,
                    file_name="merged_output.pdf",
                    mime="application/pdf",
                )
            else:
                st.warning("PDF로 변환할 데이터가 없습니다.")
        else:
            st.warning("URL을 입력하세요.")

if __name__ == "__main__":
    main()