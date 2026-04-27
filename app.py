import json
from pathlib import Path

import streamlit as st


QUIZ_DATA_PATH = Path(__file__).with_name("quiz_data.json")
DEFAULT_USERS = {"demo": "professor123"}


@st.cache_data(show_spinner=True)
def load_quiz_data():
    with QUIZ_DATA_PATH.open(encoding="utf-8") as quiz_file:
        return json.load(quiz_file)


def initialize_session_state():
    if "users" not in st.session_state:
        st.session_state.users = DEFAULT_USERS.copy()
    if "authenticated_user" not in st.session_state:
        st.session_state.authenticated_user = None


def render_header():
    st.title("All About Professor::Kyu Dong Park")
    st.subheader("학번: 2025404045")
    st.subheader("이름: 이효원")


def render_auth_panel():
    with st.sidebar:
        st.header("계정")
        if st.session_state.authenticated_user:
            st.success(f"{st.session_state.authenticated_user}님 로그인 중")
            if st.button("로그아웃", use_container_width=True):
                st.session_state.authenticated_user = None
                st.rerun()
            return True

        auth_tab, signup_tab = st.tabs(["로그인", "회원가입"])

        with auth_tab:
            with st.form("login_form"):
                username = st.text_input("아이디", key="login_username")
                password = st.text_input(
                    "비밀번호",
                    type="password",
                    key="login_password",
                )
                submitted = st.form_submit_button(
                    "로그인", use_container_width=True)

            if submitted:
                saved_password = st.session_state.users.get(username)
                if saved_password == password:
                    st.session_state.authenticated_user = username
                    st.success("로그인에 성공했습니다.")
                    st.rerun()
                else:
                    st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

            st.caption("테스트 계정: `demo / professor123`")

        with signup_tab:
            with st.form("signup_form"):
                new_username = st.text_input("새 아이디", key="signup_username")
                new_password = st.text_input(
                    "새 비밀번호",
                    type="password",
                    key="signup_password",
                )
                confirm_password = st.text_input(
                    "비밀번호 확인",
                    type="password",
                    key="signup_confirm_password",
                )
                signup_submitted = st.form_submit_button(
                    "회원가입",
                    use_container_width=True,
                )

            if signup_submitted:
                if not new_username or not new_password:
                    st.error("아이디와 비밀번호를 모두 입력하세요.")
                elif new_username in st.session_state.users:
                    st.error("이미 존재하는 아이디입니다.")
                elif new_password != confirm_password:
                    st.error("비밀번호 확인이 일치하지 않습니다.")
                else:
                    st.session_state.users[new_username] = new_password
                    st.success("회원가입이 완료되었습니다. 새 계정으로 로그인하세요.")

        return False


def render_quiz(quiz_data):
    st.divider()
    st.header("퀴즈")

    with st.form("quiz_form"):
        answers = {}
        for quiz in quiz_data:
            quiz_id = int(quiz["id"])
            st.markdown(f"**문제 {quiz_id}. {quiz['question']}**")
            answers[quiz_id] = st.radio(
                "정답을 선택하세요.",
                quiz["options"],
                key=f"quiz_{quiz_id}",
                label_visibility="collapsed",
            )

        submitted = st.form_submit_button("제출", use_container_width=True)

    if not submitted:
        return

    correct_count = 0
    st.subheader("채점 결과")

    for quiz in quiz_data:
        quiz_id = int(quiz["id"])
        selected_answer = answers[quiz_id]
        correct_answer = quiz["answer"]
        is_correct = selected_answer == correct_answer
        if is_correct:
            correct_count += 1

        result_icon = "정답" if is_correct else "오답"
        st.write(
            f"문제 {quiz_id}: {result_icon} "
            f"(선택: {selected_answer}, 정답: {correct_answer})"
        )

    st.success(f"최종 점수: {correct_count} / {len(quiz_data)}")


def main():
    st.set_page_config(
        page_title="All About Professor::Kyu Dong Park",
        page_icon="🎓",
        layout="centered",
    )
    initialize_session_state()
    render_header()
    is_authenticated = render_auth_panel()

    quiz_data = load_quiz_data()
    st.info(
        f"퀴즈 데이터 {len(quiz_data)}개를 로딩했습니다. "
        "`@st.cache_data`로 파일 읽기를 캐싱합니다."
    )

    if not is_authenticated:
        st.warning("퀴즈를 풀려면 먼저 로그인하세요.")
        st.stop()

    st.success("로그인 완료. 퀴즈를 시작할 수 있습니다.")
    render_quiz(quiz_data)


if __name__ == "__main__":
    main()
