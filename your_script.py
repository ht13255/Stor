# app.py

import streamlit as st
import json
import pandas as pd

def main():
    st.title("JSON 파일 병합 도구")
    st.write("여러 JSON 파일을 업로드하고 병합합니다.")

    # JSON 파일 업로드
    uploaded_files = st.file_uploader("JSON 파일을 업로드하세요", type="json", accept_multiple_files=True)

    if uploaded_files:
        st.write(f"업로드된 파일 수: {len(uploaded_files)}")

        # JSON 데이터를 저장할 리스트
        json_data = []

        # 업로드된 파일 읽기
        for file in uploaded_files:
            try:
                data = json.load(file)
                json_data.append(data)
            except Exception as e:
                st.error(f"{file.name} 파일을 읽는 중 오류 발생: {e}")

        # 병합 옵션 선택
        merge_option = st.selectbox("병합 방법을 선택하세요", ["단순 병합", "공통 키로 병합"])

        # 병합 처리
        if merge_option == "단순 병합":
            merged_data = merge_simple(json_data)
        elif merge_option == "공통 키로 병합":
            key = st.text_input("공통 키를 입력하세요:")
            if key:
                merged_data = merge_by_key(json_data, key)
            else:
                st.warning("공통 키를 입력하세요.")
                return
        else:
            st.error("올바른 병합 옵션을 선택하세요.")
            return

        # 병합 결과 출력
        st.subheader("병합 결과")
        st.write(merged_data)

        # 병합된 JSON 파일 다운로드
        st.download_button(
            label="병합된 JSON 파일 다운로드",
            data=json.dumps(merged_data, ensure_ascii=False, indent=4),
            file_name="merged_data.json",
            mime="application/json"
        )

# 단순 병합
def merge_simple(json_list):
    merged = []
    for data in json_list:
        if isinstance(data, list):
            merged.extend(data)
        elif isinstance(data, dict):
            merged.append(data)
    return merged

# 공통 키로 병합
def merge_by_key(json_list, key):
    df_list = []
    for data in json_list:
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            continue

        if key in df.columns:
            df_list.append(df)
        else:
            st.warning(f"공통 키 '{key}'가 없는 데이터가 포함되어 있습니다.")

    if not df_list:
        st.error("공통 키를 가진 데이터가 없습니다.")
        return {}

    merged_df = pd.concat(df_list, ignore_index=True)
    return merged_df.to_dict(orient="records")

if __name__ == "__main__":
    main()