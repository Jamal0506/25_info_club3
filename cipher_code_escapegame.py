import streamlit as st

# --- 설정 ---
story = [
    {"stage": 1,
     "title": "수상한 쪽지",
     "cipher_type": "caesar",
     "ciphertext": "Lipps asvph!",
     "hint": "알파벳이 규칙적으로 밀려 있는 것 같습니다.",
     "answer": "Hello world!",
     "shift": 4,
     "message": "낡은 책상 밑에서 발견한 쪽지. 누군가 급하게 쓴 듯 합니다."},
    {"stage": 2,
     "title": "이상한 암호문",
     "cipher_type": "substitution",
     "ciphertext": "uryyb jbeyq",
     "hint": "각 알파벳이 다른 알파벳으로 치환된 것 같습니다.",
     "answer": "hello world",
     "mapping": {'u': 'h', 'r': 'e', 'y': 'l', 'b': 'o', ' ': ' ', 'j': 'w', 'e': 'r', 'q': 'd'},
     "message": "벽에 적힌 알 수 없는 글자들. 어떤 규칙이 숨어 있는 걸까요?"}
]

def caesar_decrypt(ciphertext, shift):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            shifted_char = chr((ord(char) - start - shift) % 26 + start)
        elif char.isdigit():
            shifted_char = str((int(char) - shift) % 10)
        else:
            shifted_char = char
        plaintext += shifted_char
    return plaintext

def simple_substitution_decrypt(ciphertext, mapping):
    plaintext = ""
    reverse_mapping = {v: k for k, v in mapping.items()}
    for char in ciphertext:
        plaintext += reverse_mapping.get(char, char)
    return plaintext

st.title("고전 암호 방탈출")
stage_number = st.session_state.get('stage', 1)
current_stage = None
for s in story:
    if s['stage'] == stage_number:
        current_stage = s
        break

if current_stage:
    st.header(f"스테이지 {current_stage['stage']}: {current_stage['title']}")
    st.write(current_stage['message'])
    st.write(f"힌트: {current_stage['hint']}")
    ciphertext = st.text_area("암호문을 해독하세요:", current_stage['ciphertext'])
    user_answer = st.text_input("해독된 평문:", "")

    if st.button("해독 완료"):
        if user_answer.strip() == current_stage['answer'].strip():
            st.success("정답입니다!")
            if stage_number < len(story):
                next_stage = stage_number + 1
                if st.button("다음 스테이지로 이동"):
                    st.session_state['stage'] = next_stage
                    st.rerun()
            else:
                st.balloons()
                st.write("탈출 성공!")
        else:
            st.error("틀렸습니다. 다시 시도해보세요.")
else:
    st.write("모든 스테이지를 완료했습니다!")

if st.sidebar.button("처음으로 돌아가기"):
    st.session_state['stage'] = 1
    st.rerun()
