import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import streamlit as st

# Hugging Face에서 LLaMA 모델 다운로드 및 로드
@st.cache_resource  # Streamlit에서 캐시 처리하여 모델 로드 시간을 단축
def load_model():
    model_name = "meta-llama/Llama-2-7b-hf"
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

# 모델과 토크나이저 로드
model, tokenizer = load_model()

# GPU 사용 여부 확인
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# 소설 스타일과 분위기 설정
STYLES = {
    "에리히 마리아 레마르크 스타일": "Write in the style of Erich Maria Remarque, with a focus on the tragedy of war, loss, and the human cost of conflict.",
    "프란츠 카프카 스타일": "Write in the style of Franz Kafka, exploring the themes of alienation, existential dread, and bureaucratic absurdity.",
    "도스토옙스키 스타일": "Write in the style of Fyodor Dostoevsky, delving into psychological conflict, moral dilemmas, and the nature of sin and redemption.",
    "헤밍웨이 스타일": "Write in the style of Ernest Hemingway, with concise and direct sentences.",
}

MOODS = {
    "어두운 분위기": "The story is set in a dark, ominous atmosphere where the protagonist is surrounded by conflict and despair.",
    "비극적인 분위기": "The story is tragic and somber, where characters face inevitable sorrow or loss.",
    "코믹한 분위기": "The story is humorous and lighthearted, filled with funny situations and witty dialogue.",
    "로맨틱한 분위기": "The story is lighthearted and focuses on love and relationships, with romantic settings and hopeful themes.",
    "모험적인 분위기": "The story is adventurous, filled with excitement and exploration, with the protagonist embarking on a daring journey.",
}

# 텍스트 생성 함수
def generate_story(style_prompt, mood_prompt, user_input, length=100, temperature=0.7):
    """LLaMA 모델을 사용하여 소설 생성"""
    full_prompt = f"{style_prompt}\n{mood_prompt}\n{user_input}"
    
    # 입력 텍스트를 토크나이즈
    inputs = tokenizer(full_prompt, return_tensors="pt").input_ids.to(device)
    
    # LLaMA 모델로 텍스트 생성
    outputs = model.generate(inputs, max_length=length, temperature=temperature, num_return_sequences=1)
    
    # 생성된 텍스트를 디코딩
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

def main():
    st.title("LLaMA 소설 작성기 - 다양한 작가 스타일과 분위기 선택")

    # 사용자 입력
    user_input = st.text_area("소설의 대략적인 내용을 입력하세요:", height=200)

    # 소설 스타일 선택
    style = st.selectbox("소설 스타일 선택", list(STYLES.keys()))
    style_prompt = STYLES[style]

    # 소설 분위기 선택
    mood = st.selectbox("소설 분위기 선택", list(MOODS.keys()))
    mood_prompt = MOODS[mood]

    # 소설 길이 선택
    length = st.slider("소설의 글자 수 선택", min_value=50, max_value=1000, value=200)

    # 창의성(Temperature) 조절
    temperature = st.slider("창의성 조절 (낮을수록 고증에 충실, 높을수록 창의적)", 0.0, 1.0, 0.7)

    # 소설 생성 버튼
    if st.button("소설 생성"):
        if user_input:
            with st.spinner("소설을 생성 중입니다..."):
                story = generate_story(style_prompt, mood_prompt, user_input, length=length, temperature=temperature)
            st.subheader(f"{style}와 {mood}로 작성된 소설:")
            st.write(story)

            # 결과를 파일로 저장할 수 있는 옵션 제공
            st.download_button("소설을 TXT 파일로 저장", data=story, file_name="generated_story.txt")
        else:
            st.warning("소설 내용을 입력해주세요.")

if __name__ == "__main__":
    main()
