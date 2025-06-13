import streamlit as st
import math

# --- 게임 상태 초기화 ---
if 'current_room' not in st.session_state:
    st.session_state.current_room = "intro" # 시작 화면
if 'puzzle_solved' not in st.session_state:
    st.session_state.puzzle_solved = {} # 각 퍼즐 해결 여부 저장
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# --- 방탈출 게임 함수들 ---

def intro_screen():
    st.title("면목고 암호 방탈출: 미스터리 축제")
    st.write("면목고 축제 도중, 알 수 없는 힘에 이끌려 낯선 방에 갇혔습니다.")
    st.write("문은 굳게 잠겨있고, 오직 당신의 지혜만이 이 미로를 벗어날 수 있습니다.")
    st.write("각 방의 퍼즐을 풀고 다음 방으로 나아가세요! 행운을 빕니다.")

    if st.button("게임 시작"):
        st.session_state.current_room = "room1"
        st.experimental_rerun()

def room1():
    st.header("첫 번째 방: 낡은 강의실")
    st.write("당신은 낡은 책상과 의자들로 가득 찬 강의실에 갇혀 있습니다. 창문은 굳게 닫혀 있고, 희미한 먼지 냄새가 납니다.")
    st.write("책상 위에는 빛바랜 종이 한 장이 놓여있습니다. 종이에는 알 수 없는 기호들이 적혀 있네요.")

    st.markdown("---")
    st.subheader("첫 번째 암호: 단일 치환 암호")
    st.write("종이에 적힌 암호문입니다. 암호를 해독하여 **네 글자의 단어**를 찾아내세요.")

    # 암호문과 치환 규칙 (미리 정해둔 규칙)
    cipher_text = "NJSY"
    st.code(f"암호문: {cipher_text}")

    st.write("종이 아래에는 다음과 같은 글자들이 흐릿하게 보입니다:")
    st.markdown("`A=X, B=Q, C=P, D=K, E=J, F=L, G=O, H=R, I=B, J=Z, K=A, L=W, M=V, N=S, O=U, P=T, Q=M, R=Y, S=G, T=F, U=C, V=E, W=D, X=I, Y=H, Z=N`")
    st.markdown("**(힌트: 주어진 규칙에 따라 암호문의 각 글자를 원래 글자로 치환해 보세요.)**")

    user_answer = st.text_input("해독된 단어를 입력하세요:", key="room1_answer").strip().upper()

    if st.button("문 열기", key="room1_submit"):
        if user_answer == "STOP": # 정답 단어
            st.success("정답입니다! 'STOP'이라는 글자가 나타나자, 벽에 숨겨진 문이 덜커덩 소리를 내며 열립니다.")
            st.session_state.puzzle_solved["room1"] = True
            st.session_state.current_room = "room2"
            st.experimental_rerun()
        else:
            st.error("오답입니다. 다시 시도해 보세요. 힌트를 다시 한번 확인해 보세요.")

def room2():
    st.header("두 번째 방: 어두운 복도")
    st.write("당신은 낡은 문을 통해 길고 어두운 복도로 들어섰습니다. 복도 끝 저 멀리 희미한 불빛이 보입니다. 불빛이 나오는 곳으로 다가가보니 낡은 다이얼이 붙어 있는 상자입니다.")

    st.markdown("---")
    st.subheader("두 번째 암호: 시저 암호")
    st.write("다이얼 옆에는 다음과 같은 문구가 적혀 있습니다.")
    st.code("암호문: JRFUV RIWK")
    st.write("그 아래에는 작은 글씨로 '학교의 중요한 날짜를 생각해봐' 라고 쓰여 있습니다.")
    st.markdown("**힌트**: 면목고 **개교 기념일의 '월'을 숫자**로 변환하여 시저 암호의 이동 칸수로 사용하세요.")
    st.write("면목고 개교기념일: 1983년 **11**월 12일")

    # 시저 암호 해독 함수
    def decrypt_caesar(text, shift):
        result = ""
        for char in text:
            if 'A' <= char <= 'Z':
                result += chr(((ord(char) - ord('A') - shift + 26) % 26) + ord('A'))
            else:
                result += char
        return result

    cipher_text = "JRFUV RIWK"
    # 실제 정답 시프트는 11 (KOREA LIGHT)
    
    st.info("개교기념일의 '월' 값을 이동 칸수로 사용해보세요.") 

    shift_value = st.slider("시저 암호 이동 칸수 (Key)", 1, 25, 11) # 슬라이더로 키 조정
    decrypted_text = decrypt_caesar(cipher_text.replace(" ", ""), shift_value)
    
    st.markdown(f"**해독 결과 (공백 제외)**: `{decrypted_text}`")
    st.write("해독된 단어를 정확히 입력하세요. **띄어쓰기를 포함**해야 합니다.")

    user_answer = st.text_input("해독된 단어 입력:", key="room2_answer").strip().upper()

    if st.button("상자 열기", key="room2_submit"):
        if user_answer == "KOREA LIGHT":
            st.success("정답입니다! 'KOREA LIGHT'라는 단어가 나타나자, 상자가 열리고 안에서 묵직한 열쇠가 나옵니다.")
            st.session_state.puzzle_solved["room2"] = True
            st.session_state.current_room = "room3"
            st.experimental_rerun()
        else:
            st.error("오답입니다. 개교기념일의 월(Month) 값을 잘 활용해 보세요.")

def room3():
    st.header("세 번째 방: 어둠 속의 컴퓨터")
    st.write("방 안은 칠흑 같은 어둠에 잠겨 있습니다. 저 멀리 오래된 컴퓨터 한 대가 희미한 녹색 불빛을 내며 당신을 기다립니다. 화면에는 알 수 없는 숫자들과 메시지가 떠 있습니다.")

    st.markdown("---")
    st.subheader("최종 암호: RSA 소인수 분해")
    st.write("컴퓨터 화면에는 다음과 같은 내용이 보입니다.")
    st.code("암호 메시지: 이 숫자를 소인수 분해하여 두 개의 비밀스러운 소수를 찾아내세요. 두 소수를 **작은 수부터 순서대로 곱한 결과**가 최종 비밀번호입니다.")
    st.write("---")
    st.write("주어진 큰 숫자 **N**: (이 숫자를 소인수 분해해야 합니다)")
    st.code("N = 18923") # 예시 N 값 (실제 RSA는 훨씬 더 큰 수 사용)
    st.write("RSA 암호는 두 개의 큰 소수를 곱하여 공개키를 만듭니다. 당신은 그 두 소수를 찾아내야 합니다.")
    st.markdown("**(힌트: 1부터 차례대로 N을 나눌 수 있는 소수를 찾아보세요. 종이와 펜 또는 계산기를 활용해도 좋습니다.)**")

    st.write("N = 18923 의 두 소인수를 찾아 입력하세요.")
    p_input = st.number_input("첫 번째 소수 (p):", min_value=1, step=1, key="rsa_p_input")
    q_input = st.number_input("두 번째 소수 (q):", min_value=1, step=1, key="rsa_q_input")

    if st.button("탈출 시도", key="room3_submit"):
        # 실제 N=18923의 소인수는 113 * 167 입니다.
        correct_p = 113
        correct_q = 167

        # 입력받은 p, q가 유효한 소수인지, N의 소인수인지 확인
        if p_input > 1 and q_input > 1 and p_input * q_input == 18923:
            # 소수 판별 (간단한 방법)
            def is_prime(num):
                if num < 2:
                    return False
                for i in range(2, int(math.sqrt(num)) + 1):
                    if num % i == 0:
                        return False
                return True

            if is_prime(p_input) and is_prime(q_input):
                # 작은 수부터 순서대로 정렬하여 확인
                if (p_input == correct_p and q_input == correct_q) or \
                   (p_input == correct_q and q_input == correct_p):
                    st.balloons()
                    st.success("축하합니다! 모든 암호를 풀고 탈출했습니다! 컴퓨터 화면에 '탈출 성공!' 메시지가 뜹니다.")
                    st.session_state.game_over = True
                    st.experimental_rerun()
                else:
                    st.error("두 소수는 맞지만, 순서가 틀렸습니다. 작은 수부터 순서대로 입력해주세요.")
            else:
                st.error("입력한 두 숫자 중 적어도 하나는 소수가 아닙니다. 다시 확인해 보세요.")
        else:
            st.error("입력값이 올바르지 않습니다. N의 두 소인수를 정확히 찾아보세요.")

def end_screen():
    st.title("탈출 성공! 축하합니다!")
    st.write("모든 암호를 풀고 미스터리한 공간에서 벗어났습니다. 다시 면목고 축제로 돌아갈 수 있게 되었군요!")
    st.write("플레이해주셔서 감사합니다.")

    if st.button("다시 플레이하기"):
        st.session_state.clear() # 모든 상태 초기화
        st.experimental_rerun()

# --- 메인 게임 루프 ---
if st.session_state.game_over:
    end_screen()
else:
    if st.session_state.current_room == "intro":
        intro_screen()
    elif st.session_state.current_room == "room1":
        room1()
    elif st.session_state.current_room == "room2":
        room2()
    elif st.session_state.current_room == "room3":
        room3()

# --- 사이드바 (게임 정보) ---
st.sidebar.title("게임 정보")
st.sidebar.write(f"현재 방: **{st.session_state.current_room}**")
st.sidebar.markdown("---")
st.sidebar.subheader("진행 상황")
if st.session_state.puzzle_solved.get("room1"):
    st.sidebar.write("✅ 첫 번째 방 완료")
else:
    st.sidebar.write("❌ 첫 번째 방 미완료")

if st.session_state.puzzle_solved.get("room2"):
    st.sidebar.write("✅ 두 번째 방 완료")
else:
    st.sidebar.write("❌ 두 번째 방 미완료")

if st.session_state.puzzle_solved.get("room3"): # RSA는 바로 게임 종료이므로 이 부분은 거의 보이지 않을 수 있습니다.
    st.sidebar.write("✅ 세 번째 방 완료")
else:
    st.sidebar.write("❌ 세 번째 방 미완료")

st.sidebar.markdown("---")
st.sidebar.markdown("**면목고 축제로 돌아가자!**")
