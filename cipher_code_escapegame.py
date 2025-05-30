import streamlit as st

# --- 설정 ---
story = [
    {"stage": 1,
     "title": "수상한 쪽지",
     "cipher_type": "caesar",
     "ciphertext": "Lipps asvph!",
     "hint": "알파벳이 규칙적으로 밀려 있는 것 같습니다. 쪽지 상단에 'SHIFT=4'라고 적혀 있습니다.",
     "answer": "Hello world!",
     "shift": 4,
     "message": "낡은 책상 밑에서 발견한 쪽지. 누군가 급하게 쓴 듯 합니다."},
    {"stage": 2,
     "title": "고대 문양",
     "cipher_type": "substitution",
     "ciphertext": "uryyb jbeyq",
     "hint": "벽에 새겨진 문양 아래, 깨진 타일에 다음과 같은 글자들이 보입니다: 'u=h, r=e, y=l, b=o, j=w, e=r, q=d'.",
     "answer": "hello world",
     "mapping": {'u': 'h', 'r': 'e', 'y': 'l', 'b': 'o', ' ': ' ', 'j': 'w', 'e': 'r', 'q': 'd'},
     "message": "기이한 문양들이 가득한 방. 벽 한쪽에는 알아볼 수 없는 글자들이 나열되어 있습니다."},
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

def next_stage_button():
    st.session_state['stage'] += 1
    st.rerun()

def reset_stage():
    st.session_state['stage'] = 1
    st.rerun()

st.title("고전 암호 방탈출")
if 'stage' not in st.session_state:
    st.session_state['stage'] = 1

current_stage = None
for s in story:
    if s['stage'] == st.session_state['stage']:
        current_stage = s
        break

if current_stage:
    st.header(f"스테이지 {current_stage['stage']}: {current_stage['title']}")
    st.write(current_stage['message'])
    st.write(f"힌트: {current_stage['hint']}")
    st.markdown(f"**암호문:** `{current_stage['ciphertext']}`")
    user_answer = st.text_input("해독된 평문:", "")

    if st.button("해독 완료"):
        if user_answer.strip() == current_stage['answer'].strip():
            st.success("정답입니다!")
            if st.session_state['stage'] < len(story):
                st.button("다음 스테이지로 이동", on_click=next_stage_button)
            else:
                st.balloons()
                st.write("탈출 성공!")
        else:
            st.error("틀렸습니다. 다시 시도해보세요.")
else:
    st.write("모든 스테이지를 완료했습니다!")

if st.sidebar.button("처음으로 돌아가기", on_click=reset_stage):
    pass
