
import streamlit as st
import os
import time
import re

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from dotenv import load_dotenv


"""
README.MD
1. 코드 편집 프로그램 다운로드 및 설치
    https://theia-ide.org/
    - Get Theia IDE for desktop 클릭
    - Download 버튼 클릭
    - Windows(latest) 클릭하면 다운로드됨
    - 설치

2. MistralAI API KEY 받기
    https://mistral.ai/
    - 로그인 후
    - 중간 화면에 'Build on la Plateforme' 클릭(https://console.mistral.ai/)
    - Set up your workspace 부분에 Workspace team 선택하는 곳에 'I'm a solo creator' 선택 후 아래 약관 동의 체크박스 누르고 Create workspace 버튼 클릭
    - 파란 상자 부분에 Activate my trial 버튼을 누르고 핸드폰 인증
    - 인증 후 API를 5달러 내에서 일정 기간 사용 가능합니다.
    - 왼쪽 메뉴에서 API Keys 클릭
    - Create API Key 버튼 클릭
    - 나오는 API Key를 잘 저장해놓습니다(창을 닫으면 다시는 나타나지 않아서 다음에 또 만들어야 함)
    - 내가 작업하고자 하는 폴더에 .env 라는 파일(파일명 앞에 꼭 점(.) 붙일 것)을 만들고 아래와 같이 적습니다.
    
    MISTRALAI_API_KEY=여러분들이 받은 API KEY 입력

    - 그리고 저장합니다.

3. Python 설치(https://www.python.org/)

4. 가상환경 만들기(Windows 기준)
 - VScode나 Theia IDE에서 위 메뉴에 Terminal 클릭
 - python -m venv venv 또는 python3 -m venv venv 입력
 - venv\Scripts\activate
 - 터미널 앞에 (venv) 표시 있는지 확인

5. 라이브러리 설치
 - pip install -r requirements.txt 터미널 입력

6. 스트림릿(Streamlit 실행)
 - streamlit run app.py 터미널 입력

질문은 imhyuk@huno.kr로 연락주세요.

"""

load_dotenv()


api_key = os.environ["MISTRALAI_API_KEY"]


# 다른 모델들
# Openai gpt-4-o-mini
# claude-3.5-sonnet
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

st.title("Simple Chat")

system_message = "Since the person you are addressing is Korean, please use only Korean. You are a highly skilled and professional journalist, so you respond to everything in an article format."


if "messages" not in st.session_state:
    st.session_state.messages = [ChatMessage(role="system", content=system_message)]

def response_generator():
    stream_response = client.chat_stream(model=model, messages=st.session_state.messages)
    if stream_response is not None:
        for word in stream_response:
            if word.choices:
                response = re.sub(r"\s{2,}", "", word.choices[0].delta.content)
                yield response



for message in st.session_state.messages:
    if message.role != "system":
        with st.chat_message(message.role):
            st.markdown(message.content)


if prompt := st.chat_input("What's up"):
    with st.chat_message("user"):
        st.markdown(prompt)

    
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))

    with st.chat_message("assistant"):
        response_container = st.empty()
        response_text = ""

        for response in response_generator():
            response_text += response
            response_container.markdown(f"<div style='display: flex; flex-wrap: wrap;'>{response_text}</div>", unsafe_allow_html=True)

            time.sleep(0.05)

        st.session_state.messages.append(ChatMessage(role="assistant", content=response_text))