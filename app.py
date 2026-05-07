import streamlit as st
import time
import random

# 연습 문장 목록
sentences = [
    "Python is very fun to learn.",
    "Streamlit makes web apps easy.",
    "Typing fast takes practice.",
    "GitHub is useful for developers.",
    "Artificial intelligence is amazing."
]

st.set_page_config(page_title="타자 연습", page_icon="⌨️")

st.title("⌨️ 타자 연습 웹앱")

# 세션 상태 초기화
if "sentence" not in st.session_state:
    st.session_state.sentence = random.choice(sentences)

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "finished" not in st.session_state:
    st.session_state.finished = False

sentence = st.session_state.sentence

st.subheader("다음 문장을 입력하세요:")
st.code(sentence)

user_input = st.text_input("여기에 입력:")

# 입력 시작 시간 기록
if user_input and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# 완료 체크
if user_input == sentence and not st.session_state.finished:
    end_time = time.time()
    elapsed_time = end_time - st.session_state.start_time

    words = len(sentence.split())
    wpm = (words / elapsed_time) * 60

    correct_chars = sum(
        1 for a, b in zip(user_input, sentence) if a == b
    )
    accuracy = (correct_chars / len(sentence)) * 100

    st.success("완료!")

    st.write(f"⏱️ 시간: {elapsed_time:.2f}초")
    st.write(f"⚡ 속도: {wpm:.2f} WPM")
    st.write(f"🎯 정확도: {accuracy:.2f}%")

    st.session_state.finished = True

# 재시작 버튼
if st.button("다시 시작"):
    st.session_state.sentence = random.choice(sentences)
    st.session_state.start_time = None
    st.session_state.finished = False
    st.rerun()
