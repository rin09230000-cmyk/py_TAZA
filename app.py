import streamlit as st
from streamlit_ace import st_ace
import time
import random

st.set_page_config(
    page_title="Python 타자 연습",
    page_icon="⌨️",
    layout="centered"
)

# 난이도별 Python 코드
sentences = {
    "초급": [
        "print('Hello World')",
        "name = input()",
        "x = 10",
        "for i in range(5):\n    print(i)",
        "if x > 0:\n    print('positive')"
    ],

    "중급": [
        "def hello(name):\n    return name.upper()",

        "numbers = [1, 2, 3, 4]\nfor n in numbers:\n    print(n)",

        "try:\n    print(x)\nexcept Exception as e:\n    print(e)",

        "with open('test.txt') as file:\n    data = file.read()"
    ],

    "고급": [
        "result = [x for x in range(100) if x % 2 == 0]",

        "class Student:\n    def __init__(self, name):\n        self.name = name",

        "data = sorted(users, key=lambda x: x['age'])",

        "async def fetch_data():\n    await asyncio.sleep(1)\n    return True"
    ]
}

# 제목
st.title("⌨️ Python 타자 연습")

# 이름 입력
username = st.text_input(
    "이름을 입력하세요",
    placeholder="예: 규린"
)

# 이름 입력 전 안내
if not username:
    st.warning("이름을 입력해주세요!")
    st.stop()

# 환영 메시지
st.success(f"{username}님 환영합니다 👋")

# 난이도 선택
difficulty = st.selectbox(
    "난이도 선택",
    ["초급", "중급", "고급"]
)

# 세션 상태
if "sentence" not in st.session_state:
    st.session_state.sentence = random.choice(sentences[difficulty])

if "previous_difficulty" not in st.session_state:
    st.session_state.previous_difficulty = difficulty

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "finished" not in st.session_state:
    st.session_state.finished = False

# 난이도 변경 시 새 문제
if difficulty != st.session_state.previous_difficulty:
    st.session_state.sentence = random.choice(sentences[difficulty])
    st.session_state.previous_difficulty = difficulty
    st.session_state.start_time = None
    st.session_state.finished = False

sentence = st.session_state.sentence

# 문제 표시
st.subheader("아래 Python 코드를 그대로 입력하세요")

st.code(sentence, language="python")

st.divider()

# 코드 입력창
user_input = st_ace(
    placeholder="여기에 Python 코드를 입력하세요...",
    language="python",
    theme="monokai",
    keybinding="vscode",
    font_size=16,
    tab_size=4,
    show_gutter=True,
    wrap=True,
    auto_update=True,
    height=250
)

# 시작 시간
if user_input and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# 정확도 계산
def calculate_accuracy(input_text, target_text):

    correct = 0

    for a, b in zip(input_text, target_text):
        if a == b:
            correct += 1

    return (correct / len(target_text)) * 100

# 정답 체크
if user_input == sentence and not st.session_state.finished:

    end_time = time.time()
    elapsed = end_time - st.session_state.start_time

    chars = len(sentence)
    cpm = (chars / elapsed) * 60

    accuracy = calculate_accuracy(user_input, sentence)

    st.success(f"🎉 {username}님 성공!")

    st.metric("⏱️ 시간", f"{elapsed:.2f}초")
    st.metric("⚡ 속도", f"{cpm:.0f} CPM")
    st.metric("🎯 정확도", f"{accuracy:.1f}%")

    st.balloons()

    st.session_state.finished = True

# 실시간 정확도
elif user_input:

    accuracy = calculate_accuracy(user_input, sentence)

    st.info(f"현재 정확도: {accuracy:.1f}%")

# 버튼
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 새 문제"):
        st.session_state.sentence = random.choice(sentences[difficulty])
        st.session_state.start_time = None
        st.session_state.finished = False
        st.rerun()

with col2:
    if st.button("🧹 초기화"):
        st.session_state.start_time = None
        st.session_state.finished = False
        st.rerun()
