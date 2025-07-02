import streamlit as st
import random
import os
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="캐릭터 이름 맞추기 게임",
    page_icon="🎮",
    layout="centered"
)

# 스타일링
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #FF6B6B;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    
    .score-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 1rem 0;
    }
    
    .correct-answer {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #c3e6cb;
    }
    
    .wrong-answer {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #f5c6cb;
    }
    
    .game-over {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

def get_character_name_from_filename(filename):
    """파일명에서 캐릭터 이름을 추출 (확장자 제거)"""
    return Path(filename).stem

def load_images():
    """images 폴더에서 이미지 파일들을 로드"""
    image_folder = "images"
    if not os.path.exists(image_folder):
        st.error("images 폴더가 없습니다. images 폴더를 생성하고 캐릭터 이미지들을 넣어주세요.")
        st.stop()
    
    image_files = []
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']:
        image_files.extend(Path(image_folder).glob(ext))
    
    if len(image_files) == 0:
        st.error("images 폴더에 이미지 파일이 없습니다.")
        st.stop()
    
    return [str(img) for img in image_files]

def initialize_game():
    """게임 초기화"""
    images = load_images()
    random.shuffle(images)
    
    st.session_state.images = images
    st.session_state.current_index = 0
    st.session_state.correct_count = 0
    st.session_state.answered_questions = []
    st.session_state.game_over = False
    st.session_state.show_result = False
    st.session_state.user_answer = ""

def check_answer(user_answer, correct_answer):
    """답안 체크 (대소문자, 공백 무시)"""
    return user_answer.strip().lower() == correct_answer.strip().lower()

def next_question():
    """다음 문제로 이동"""
    st.session_state.current_index += 1
    st.session_state.show_result = False
    st.session_state.user_answer = ""
    
    if st.session_state.current_index >= len(st.session_state.images):
        st.session_state.game_over = True

# 세션 상태 초기화
if 'images' not in st.session_state:
    initialize_game()

# 메인 타이틀
st.markdown('<div class="main-title">🎮 캐릭터 이름 맞추기 게임</div>', unsafe_allow_html=True)

# 게임 오버 체크
if st.session_state.game_over:
    total_questions = len(st.session_state.images)
    score_percentage = (st.session_state.correct_count / total_questions) * 100
    
    st.markdown(f"""
    <div class="game-over">
        <h2>🎉 게임 완료! 🎉</h2>
        <h3>총 {total_questions}문제 중 {st.session_state.correct_count}문제 정답!</h3>
        <h3>정답률: {score_percentage:.1f}%</h3>
        <p>수고하셨습니다! 다시 도전해보세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 다시하기", key="restart_game", use_container_width=True):
        initialize_game()
        st.rerun()

else:
    # 현재 진행상황 표시
    current_num = st.session_state.current_index + 1
    total_num = len(st.session_state.images)
    
    st.markdown(f"""
    <div class="score-container">
        <h3>문제 {current_num} / {total_num}</h3>
        <h3>정답: {st.session_state.correct_count}개</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 현재 이미지 표시
    current_image = st.session_state.images[st.session_state.current_index]
    correct_answer = get_character_name_from_filename(os.path.basename(current_image))
    
    # 이미지 표시
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(current_image, caption="이 캐릭터의 이름은?", use_container_width=True)
    
    # 결과 표시
    if st.session_state.show_result:
        last_answer = st.session_state.answered_questions[-1]
        if last_answer['correct']:
            st.markdown(f'<div class="correct-answer">✅ 정답입니다! "{correct_answer}"</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="wrong-answer">❌ 틀렸습니다. 정답은 "{correct_answer}"입니다.</div>', unsafe_allow_html=True)
        
        st.button("➡️ 다음 문제", on_click=next_question, key="next_question", use_container_width=True)
    
    else:
        # 답안 입력
        with st.form(key="answer_form"):
            user_answer = st.text_input("캐릭터 이름을 입력하세요:", key="answer_input", placeholder="정답을 입력하고 Enter를 누르세요")
            submit_button = st.form_submit_button("제출", use_container_width=True)
            
            if submit_button and user_answer:
                is_correct = check_answer(user_answer, correct_answer)
                
                # 답안 기록
                st.session_state.answered_questions.append({
                    'question': current_image,
                    'user_answer': user_answer,
                    'correct_answer': correct_answer,
                    'correct': is_correct
                })
                
                if is_correct:
                    st.session_state.correct_count += 1
                
                st.session_state.show_result = True
                st.rerun()

# 사이드바에 게임 정보
with st.sidebar:
    st.header("📋 게임 정보")
    st.write("- 총 50개의 캐릭터 이미지")
    st.write("- 랜덤 순서로 출제")
    st.write("- 대소문자 구분 없음")
    st.write("- 공백 무시")
    
    st.header("📁 설정 방법")
    st.write("1. `images` 폴더 생성")
    st.write("2. 캐릭터 이미지 파일을 넣기")
    st.write("3. 파일명이 정답이 됩니다")
    st.write("   (예: `피카츄.png` → 정답: 피카츄)")
    
    if st.button("🔄 게임 초기화"):
        initialize_game()
        st.rerun()
