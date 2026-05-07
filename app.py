import streamlit as st
from streamlit_ace import st_ace
import time
import random

st.set_page_config(
    page_title="Python 타자 연습",
    page_icon="⌨️",
    layout="centered"
)

# 난이도별 문제
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

# 상단 설정 영역
col1, col2 = st.columns(2)

with col1:
    username = st.text_input(
        "이름",
        placeholder="이름 입력"
    )

with col2:
    difficulty = st.selectbox(
        "난이도",
        ["초급", "중급", "고급"]
    )

# 세션 상태 초기화
if "sentence" not in st.session_state:
    st.session_state.sentence = random.choice(sentences[difficulty])

if "previous_difficulty" not in st.session_state:
    st.session_state.previous_difficulty = difficulty

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "editor_key" not in st.session_state:
    st.session_state.editor_key = 0

# 난이도 변경 시 문제 변경
if difficulty != st.session_state.previous_difficulty:

    st.session_state.sentence = random.choice(sentences[difficulty])
    st.session_state.previous_difficulty = difficulty
    st.session_state.start_time = None
    st.session_state.editor_key += 1

sentence = st.session_state.sentence

st.divider()

# 이름 안내
if username:
    st.success(f"{username}님 화이팅! 🚀")
else:
    st.info("이름을 입력하면 기록에 표시돼요!")

# 제시 코드
st.subheader("📌 제시 코드")

st.code(sentence, language="python")

# 입력창
st.subheader("⌨️ 코드 입력")

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
    height=250,
    key=f"editor_{st.session_state.editor_key}"
)

# 시작 시간
if user_input and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# 정확도 계산 함수
def calculate_accuracy(input_text, target_text):

    correct = 0

    for a, b in zip(input_text, target_text):
        if a == b:
            correct += 1

    return (correct / len(target_text)) * 100

# 정답 체크
if user_input == sentence:

    end_time = time.time()
    elapsed = end_time - st.session_state.start_time

    chars = len(sentence)
    cpm = (chars / elapsed) * 60

    accuracy = calculate_accuracy(user_input, sentence)

    st.success(
        f"🎉 완료! "
        f"⏱️ {elapsed:.2f}초 | "
        f"⚡ {cpm:.0f} CPM | "
        f"🎯 {accuracy:.1f}%"
    )

    # 다음 문제 자동 생성
    st.session_state.sentence = random.choice(sentences[difficulty])

    # 입력창 초기화
    st.session_state.editor_key += 1

    # 시간 초기화
    st.session_state.start_time = None

    st.rerun()

# 실시간 정확도
elif user_input:

    accuracy = calculate_accuracy(user_input, sentence)

    st.info(f"현재 정확도: {accuracy:.1f}%")

st.divider()

# 버튼
col3, col4 = st.columns(2)

with col3:
    if st.button("🔄 문제 변경"):

        st.session_state.sentence = random.choice(sentences[difficulty])
        st.session_state.start_time = None
        st.session_state.editor_key += 1

        st.rerun()

with col4:
    if st.button("🧹 입력 초기화"):

        st.session_state.start_time = None
        st.session_state.editor_key += 1

        st.rerun()
