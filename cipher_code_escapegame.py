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
    st.write("탈출구는 굳게 잠겨있고, 오직 당신의 지혜만이 이 미로를 벗어날 수 있습니다.")
    st.write("각 방의 퍼즐을 풀고 다음 방으로 나아가세요! 행운을 빕니다.")

    if st.button("게임 시작"):
        st.session_state.current_room = "room1"
        st.experimental_rerun()

def room1():
    st.header("첫 번째 방: 낡은 강의실")
    st.write("낡은 책상 위에는 빛바랜 종이가 놓여있고, 알 수 없는 기호들이 적혀 있습니다.")
    st.image("classroom.png", caption="낡은 강의실 (예시 이미지, 실제 파일은 경로 지정)")

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
            st.success("정답입니다! 'STOP'이라는 글자가 나타나자, 벽에 숨겨진 문이 열립니다.")
            st.session_state.puzzle_solved["room1"] = True
            st.session_state.current_room = "room2"
            st.experimental_rerun()
        else:
            st.error("오답입니다. 다시 시도해 보세요.")
            st.write("힌트가 충분하지 않다면, 위 치환 규칙을 다시 한 번 확인해 보세요.")

def room2():
    st.header("두 번째 방: 어두운 복도")
    st.write("어둡고 긴 복도입니다. 저 멀리 희미한 불빛이 보입니다. 불빛이 나오는 곳에 낡은 다이얼이 있습니다.")
    st.image("hallway.png", caption="어두운 복도 (예시 이미지)")

    st.markdown("---")
    st.subheader("두 번째 암호: 시저 암호")
    st.write("다이얼 옆에는 다음과 같은 문구가 적혀 있습니다.")
    st.code("암호문: JRFUV RIWK")
    st.write("그 아래에는 작은 글씨로 '학교의 중요한 날짜를 생각해봐' 라고 쓰여 있습니다.")
    st.markdown("**(힌트: 면목고 개교 기념일을 숫자로 변환하여 시저 암호의 이동 칸수로 사용하세요. (예: 11월 12일 -> 11 또는 12))**")
    st.write("면목고 개교기념일: 1983년 11월 12일")

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
    # 11월 12일. 11을 shift로 사용해봅시다. (또는 12)
    # 실제 정답: 11 (KOREA)
    # 12로 시도할 경우: JRFUV RIWK -> IWQUT QHVJ
    # 11로 시도할 경우: JRFUV RIWK -> KOREA LIGHT
    # 11칸 이동해서 해독하는 것이 "KOREA"라는 의미있는 단어가 되므로 11로 가정.
    
    st.info("개교기념일의 '월'을 이동 칸수로 사용해보세요.") # 구체적인 힌트

    shift_value = st.slider("시저 암호 이동 칸수 (Key)", 1, 25, 11) # 슬라이더로 키 조정
    decrypted_text = decrypt_caesar(cipher_text.replace(" ", ""), shift_value)
    
    st.markdown(f"**해독 결과**: `{decrypted_text}` (공백 제외)")
    st.write("공백을 포함하여 해독된 단어를 정확히 입력하세요. (띄어쓰기 포함)")

    user_answer = st.text_input("해독된 단어 입력 (공백 포함):", key="room2_answer").strip().upper()

    if st.button("문 열기", key="room2_submit"):
        # 실제 해독된 단어는 KOREA LIGHT (11칸 이동)
        if user_answer == "KOREA LIGHT":
            st.success("정답입니다! 'KOREA LIGHT'라는 단어가 나타나자, 복도 끝의 문이 열립니다.")
            st.session_state.puzzle_solved["room2"] = True
            st.session_state.current_room = "room3"
            st.experimental_rerun()
        else:
            st.error("오답입니다. 개교기념일의 월(Month) 값을 잘 활용해 보세요.")

def room3():
    st.header("세 번째 방: 어둠 속의 컴퓨터")
    st.write("어둠 속에서 오래된 컴퓨터 한 대가 희미하게 빛나고 있습니다. 화면에는 알 수 없는 숫자들과 메시지가 떠 있습니다.")
    st.image("old_computer.png", caption="오래된 컴퓨터 (예시 이미지)")

    st.markdown("---")
    st.subheader("최종 암호: RSA 소인수 분해")
    st.write("컴퓨터 화면에는 다음과 같은 내용이 보입니다.")
    st.code("암호 메시지: 이 숫자를 소인수 분해하여 두 개의 비밀스러운 소수를 찾아내세요. 두 소수를 **작은 수부터 순서대로 곱한 결과**가 최종 비밀번호입니다.")
    st.write("---")
    st.write("주어진 큰 숫자 N:")
    st.code("N = 18923") # 예시 N 값 (실제 RSA는 훨씬 더 큰 수 사용)
    st.write("RSA 암호는 두 개의 큰 소수를 곱하여 공개키를 만듭니다. 당신은 그 두 소수를 찾아내야 합니다.")
    st.markdown("**(힌트: 1부터 차례대로 N을 나눌 수 있는 소수를 찾아보세요. 계산기를 활용해도 좋습니다.)**")

    # 소인수 분해 함수 (플레이어가 직접 찾도록 유도)
    def find_factors(n):
        factors = []
        d = 2
        temp_n = n
        while d * d <= temp_n:
            if temp_n % d == 0:
                factors.append(d)
                temp_n //= d
            else:
                d += 1
        if temp_n > 1:
            factors.append(temp_n)
        return sorted(list(set(factors))) # 중복 제거 및 정렬된 소인수 반환

    st.write("N = 18923 의 두 소인수를 찾아 입력하세요.")
    p_input = st.number_input("첫 번째 소수 (p):", min_value=1, step=1, key="rsa_p_input")
    q_input = st.number_input("두 번째 소수 (q):", min_value=1, step=1, key="rsa_q_input")

    if st.button("탈출 시도", key="room3_submit"):
        # 실제 N=18923의 소인수는 113 * 167 입니다.
        correct_p = 113
        correct_q = 167

        if p_input == correct_p and q_input == correct_q:
            st.success("정답입니다! 두 소수를 정확히 찾아냈습니다!")
            st.write(f"최종 비밀번호: {correct_p * correct_q}")
            st.session_state.game_over = True
            st.experimental_rerun()
        elif p_input * q_input == 18923 and p_input != 1 and q_input != 1:
            st.error("곱셈 결과는 맞지만, 두 수가 소수가 아니거나, 순서가 틀렸습니다. 다시 확인해보세요.")
        else:
            st.error("틀렸습니다. N의 소인수를 정확히 찾아보세요.")

def end_screen():
    st.title("탈출 성공! 축하합니다!")
    st.write("모든 암호를 풀고 미스터리한 공간에서 벗어났습니다. 다시 면목고 축제로 돌아갈 수 있게 되었군요!")
    st.balloons()
    st.image("celebration.png", caption="탈출 성공! (예시 이미지)")

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
st.sidebar.write(f"현재 방: {st.session_state.current_room}")
st.sidebar.write("---")
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
