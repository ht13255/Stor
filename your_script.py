import openai
import streamlit as st
from config import OPENAI_API_KEY  # config.py에서 API 키 불러오기

# OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY

# 소설 스타일과 분위기 설정
STYLES = {
    "에리히 마리아 레마르크 스타일": "Write in the style of Erich Maria Remarque, with a focus on the tragedy of war, loss, and the human cost of conflict.",
    "프란츠 카프카 스타일": "Write in the style of Franz Kafka, exploring the themes of alienation, existential dread, and bureaucratic absurdity.",
    "도스토옙스키 스타일": "Write in the style of Fyodor Dostoevsky, delving into psychological conflict, moral dilemmas, and the nature of sin and redemption.",
    "헤밍웨이 스타일": "Write in the style of Ernest Hemingway, with concise and direct sentences.",
    "제인 오스틴 스타일": "Write in the style of Jane Austen, focusing on social commentary and wit.",
    "톨스토이 스타일": "Write in the style of Leo Tolstoy, with deep philosophical insights and complex character development.",
    "마거릿 애트우드 스타일": "Write in the style of Margaret Atwood, with dystopian themes and deep character introspection.",
    "조지 오웰 스타일": "Write in the style of George Orwell, focusing on political allegory and social commentary."
}

MOODS = {
    "어두운 분위기": "The story is set in a dark, ominous atmosphere where the protagonist is surrounded by conflict and despair.",
    "비극적인 분위기": "The story is tragic and somber, where characters face inevitable sorrow or loss.",
    "코믹한 분위기": "The story is humorous and lighthearted, filled with funny situations and witty dialogue.",
    "긴장감 넘치는 분위기": "The story is thrilling and filled with tension, where suspense keeps the reader on edge.",
    "로맨틱한 분위기": "The story is lighthearted and focuses on love and relationships, with romantic settings and hopeful themes.",
    "모험적인 분위기": "The story is adventurous, filled with excitement and exploration, with the protagonist embarking on a daring journey.",
    "서사적 분위기": "The story is grand and epic, following the journey of a hero through significant trials and achievements.",
    "미래지향적 분위기": "The story is set in a futuristic or sci-fi setting, exploring advanced technology or alien worlds."
}

def generate_story(style_prompt, mood_prompt, user_input, ending_input, length, temperature=0.7):
    """GPT 모델을 사용하여 소설 생성"""
    full_prompt = f"{style_prompt}\n{mood_prompt}\n소설 내용:\n{user_input}\n결말:\n{ending_input}\n"
    response = openai.Completion.create(
        engine="text-davinci-003",  # GPT 모델 (GPT-4로 변경 가능)
        prompt=full_prompt,
        max_tokens=length,
        temperature=temperature,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

def main():
    st.title("비극적이고 어두운 소설 작성기 - 다양한 작가 스타일과 분위기 선택")

    # 사용자 입력
    user_input = st.text_area("소설의 대략적인 내용을 입력하세요:", height=200)

    # 엔딩 분위기 입력
    ending_input = st.text_area("소설의 결말을 어떤 분위기로 만들지 직접 작성하세요:", height=100)

    # 소설 스타일 선택
    style = st.selectbox("소설 스타일 선택", list(STYLES.keys()))
    style_prompt = STYLES[style]

    # 소설 분위기 선택
    mood = st.selectbox("소설 분위기 선택", list(MOODS.keys()))
    mood_prompt = MOODS[mood]

    # 소설 길이와 스타일 선택
    length_type = st.radio("글 길이 선택", ("문장 수", "글자 수"))
    if length_type == "문장 수":
        sentence_count = st.slider("문장 수 선택", 1, 100, 10)
        length = sentence_count * 15  # 한 문장을 약 15개의 토큰으로 가정
    else:
        length = st.slider("글자 수 선택", 100, 3000, 500)

    temperature = st.slider("창의성 (낮을수록 고증에 충실, 높을수록 창의적)", 0.0, 1.0, 0.7)

    # 버튼 클릭 시 소설 생성
    if st.button("소설 생성"):
        if user_input and ending_input:
            # 소설 생성
            with st.spinner("소설을 생성 중입니다..."):
                story = generate_story(style_prompt, mood_prompt, user_input, ending_input, length, temperature)
            st.subheader(f"{style}와 {mood}로 작성된 소설:")
            st.write(story)

            # 결과를 파일로 저장할 옵션 제공
            st.download_button("소설을 TXT 파일로 저장", data=story, file_name="generated_story.txt")
        else:
            st.warning("소설 내용과 결말 분위기를 입력해주세요.")

if __name__ == "__main__":
    main()
