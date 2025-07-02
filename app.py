import streamlit as st
import os
import random
from PIL import Image

# 이미지 폴더 경로
IMAGE_FOLDER = 'images'

# 세션 상태 초기화 함수
def init_state():
    if 'image_list' not in st.session_state:
        # images 폴더 내 png 파일 목록 (확장자 제외한 파일명: 정답)
        st.session_state.image_list = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith('.png')]
        random.shuffle(st.session_state.image_list)
        st.session_state.current_idx = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.user_answer = ''
        st.session_state.finished = False

# 상태 초기화
init_state()

st.title('캐릭터 이름 맞추기 게임')

# 이미지가 없을 때 예외 처리
if not st.session_state.image_list:
    st.error('images 폴더에 png 파일이 없습니다. 이미지를 추가해 주세요.')
    st.stop()

# 인덱스 범위 초과 방지
if st.session_state.current_idx >= len(st.session_state.image_list):
    st.session_state.finished = True

# 게임 종료 시
if st.session_state.finished:
    st.success(f'게임 종료! 맞춘 개수: {st.session_state.score} / {len(st.session_state.image_list)}')
    if st.button('다시하기'):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    # 현재 이미지 파일명
    current_file = st.session_state.image_list[st.session_state.current_idx]
    answer = os.path.splitext(current_file)[0]  # 확장자 제거
    image_path = os.path.join(IMAGE_FOLDER, current_file)
    image = Image.open(image_path)

    st.image(image, use_container_width=True)
    st.write(f'문제 {st.session_state.current_idx + 1} / {len(st.session_state.image_list)}')

    # 정답 입력 폼
    with st.form(key='answer_form', clear_on_submit=True):
        user_input = st.text_input('캐릭터 이름을 입력하세요 (정확히 입력!)', value=st.session_state.user_answer)
        submitted = st.form_submit_button('제출')

    # 정답 판별
    if submitted and not st.session_state.answered:
        st.session_state.user_answer = user_input.strip()
        if st.session_state.user_answer == answer:
            st.session_state.score += 1
            st.session_state.answered = True
            st.success('정답입니다!')
        else:
            st.session_state.answered = True
            st.error(f'오답입니다! 정답: {answer}')

    # 다음 문제로
    if st.session_state.answered:
        if st.session_state.current_idx < len(st.session_state.image_list) - 1:
            if st.button('다음 문제'):
                st.session_state.current_idx += 1
                st.session_state.answered = False
                st.session_state.user_answer = ''
                st.rerun()
        else:
            st.session_state.finished = True
            st.rerun() 
