# 파일 경로: app.py

import streamlit as st
from fpdf import FPDF
import requests
from bs4 import BeautifulSoup

# PDF 생성 함수
def create_pdf_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 웹페이지의 텍스트 추출
        text_content = soup.get_text()
        
        # PDF 생성
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # 긴 텍스트를 줄바꿈 처리하여 PDF에 추가
        for line in text_content.split("\n"):
            if line.strip():  # 공백 라인 제거
                pdf.multi_cell(0, 10, line.strip())
        
        return pdf
    except Exception as e:
        st.error(f"페이지를 PDF로 변환하는 중 오류가 발생했습니다: {e}")
        return None

# Streamlit 앱
def main():
    st.title("URL 페이지를 PDF로 변환")
    st.write("URL을 입력하면 해당 페이지를 PDF 파일로 변환합니다.")

    url = st.text_input("URL 입력")
    if st.button("PDF 생성"):
        if url:
            pdf = create_pdf_from_url(url)
            if pdf:
                # PDF를 바이트 형태로 저장 후 다운로드 제공
                pdf_output = f"{url.replace('https://', '').replace('http://', '').replace('/', '_')}.pdf"
                pdf_output_bytes = pdf.output(dest="S").encode("latin1")
                
                st.download_button(
                    label="PDF 다운로드",
                    data=pdf_output_bytes,
                    file_name=pdf_output,
                    mime="application/pdf",
                )
        else:
            st.warning("URL을 입력하세요.")

if __name__ == "__main__":
    main()