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
def generate_story(style_prompt, mood_prompt, user_input,
