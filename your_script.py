# app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup

# Streamlit 앱 구성
st.title("사이트 링크 수집기")
st.write("사이트의 모든 글 링크를 가져옵니다. URL을 입력하세요.")

# URL 입력 받기
url = st.text_input("URL을 입력하세요", "https://example.com")

# 링크 수집 함수
def get_links(url):
    try:
        # 웹 페이지 요청
        response = requests.get(url)
        response.raise_for_status()
        
        # BeautifulSoup로 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 모든 <a> 태그에서 링크 추출
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        
        # 중복 제거 후 리스트 반환
        unique_links = list(set(links))
        return unique_links
    except requests.exceptions.RequestException as e:
        st.error(f"에러가 발생했습니다: {e}")
        return []

# 버튼 클릭 시 링크 가져오기 실행
if st.button("링크 가져오기"):
    if url:
        with st.spinner("링크를 수집 중입니다..."):
            links = get_links(url)
            if links:
                st.success(f"{len(links)}개의 링크를 찾았습니다!")
                # 링크 리스트 출력
                for link in links:
                    st.write(link)
            else:
                st.warning("링크를 찾을 수 없습니다.")
    else:
        st.warning("URL을 입력하세요.")
