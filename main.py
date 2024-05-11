import streamlit as st 

from utils import (is_valid_url, 
                   classify_news, 
                   set_style,
                   extract_artcle_from_url,
                   highlight_common_fake_words,
)

st.set_page_config(layout="wide")
set_style()

description = 'Це інструмент, що допомагає автоматично виявляти фейки в українськомовних новинах. Він створений на основі нейронної мережі, натренованої на 8237 текстах. Оригінальний код для тренування можна знайти <a href="https://github.com/soph-ma/fake_news_ua/blob/main/lstm.ipynb">тут</a>.'

st.markdown('<h1 class="title">Детектор фейкових новин 🗞️</h1>', unsafe_allow_html=True)
st.markdown(f"""
<div style="display: flex; justify-content: center; align-items: center;">
    <p style="color: grey; font-style: italic;">{description}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 2])

result = None

with col1:
    st.header("1. Вкажіть новину:")
    choice = st.radio(label="", options=["У мене є посилання на новину", "У мене є текст новини"], index=None)
    if choice == "У мене є посилання на новину": 
        pasted_link = st.text_input("Посилання:")
        predict_button = st.button(label="Показати результат")
        if predict_button: 
            if is_valid_url(pasted_link): 
                try:
                    if not "t.me" in pasted_link:
                        text, title = extract_artcle_from_url(url=pasted_link)
                        result = classify_news(text=text, title=title)
                        st.session_state.pasted_text_and_title = title + " " + text
                    else: st.error('На жаль, наш сервіс не має доступу до цього джерела 😞 Вставте текст вручну, обравши "У мене є текст новини"')
                except: st.error('На жаль, наш сервіс не має доступу до цього джерела 😞 Вставте текст вручну, обравши "У мене є текст новини"')
            else: st.error("Недійсне посилання 😞")
    elif choice == "У мене є текст новини": 
        pasted_title = st.text_input("Заголовок (опціонально):")
        pasted_text = st.text_area("Текст:", height=300)
        predict_button = st.button(label="Показати результат")
        if predict_button: 
            if not pasted_text: 
                st.error("Вставте текст  👀")
            else: 
                result = classify_news(text=pasted_text, title=pasted_title)
                st.session_state.pasted_text_and_title = pasted_title + " " + pasted_text

with col2: 
    st.markdown("""<div class = "vertical"></div>""", unsafe_allow_html=True)


def get_result(result=result): 
    if result == "Fake": 
        return "<span style='color:red'>імовірно, фейк</span>"
    elif result == "Real": 
        return "<span style='color:green'>імовірно, не фейк</span>"

with col3:
    if result: 
        st.markdown(f"<h2>2. Ваш результат: {get_result()}</h2>", unsafe_allow_html=True)
        if result == "Fake":
                highlight_common_fake_words(st.session_state.pasted_text_and_title)
                interpretation = "Жовтим виділено слова, котрі часто зустрічаються в ненадійних медіа."
                st.markdown(f"""
                    <div style="display: flex;">
                        <p style="color: grey; font-style: italic;">{interpretation}</p>
                    </div>
                    """, unsafe_allow_html=True)
    else: 
        st.header("2. Ваш результат:")
