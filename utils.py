import validators
import requests
import os
import json
import pymorphy2
from nltk import sent_tokenize
from typing import Optional
from dotenv import load_dotenv
from newspaper import Article
from telethon import TelegramClient
import streamlit as st

import nltk
nltk.download("punkt")
morph = pymorphy2.MorphAnalyzer(lang='uk')
with open("common_lemmas.txt", "r", encoding="utf-8") as f: 
    common_fake_lemmas = f.read().split("\n")[:1000]

load_dotenv()

def set_style() -> None:
    """sets css""" 
    st.markdown("""
    <style>
        .vertical {
        border-left: 1px solid lightgrey;
        height: 70vh;
        position:absolute;
        left: 50%;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .title {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

def classify_news(text: str, title: Optional[str] = None) -> str: 
    """classifies news"""
    url = os.getenv("CLASSIFIER_URL")
    headers = {'Content-Type': 'application/json'}
    data = {
        "text": text, 
        "title": title if title else extract_title_if_none(text),
    }
    response = requests.post(url=url, json=data, headers=headers)
    if response.status_code == 200: 
        return json.loads(response.content)["label"]
    print(response)

def extract_title_if_none(text: str) -> str: 
    """extracts the title of the news"""
    sentences = sent_tokenize(text)
    title = sentences[0]
    return title

def is_valid_url(url) -> bool:
    """checks if url is valid"""
    return validators.url(url)

def extract_artcle_from_url(url) -> tuple[str, str]:  
    """extracts article text and title based on article url"""
    article = Article(url)
    article.download()
    article.parse()
    title = article.title
    text = article.text
    return (text, title)


def lemmatize_word(word):
    """lemmatisation"""
    return morph.parse(word)[0].normal_form

def is_common_fake_word(word: str) -> bool: 
    """checks if the word is commonly encountered  in fake news"""
    lemma = lemmatize_word(word)
    if lemma in common_fake_lemmas: 
        return True
    return False

def highlight_common_fake_words(text: str) -> None:
    """highlights common fake news"""
    words = text.split()
    highlighted_text = []
    for word in words:
        
        if is_common_fake_word(word):
            highlighted_text.append(f'<span style="background-color: yellow;">{word}</span>')
        else:
            highlighted_text.append(word)
    st.markdown(' '.join(highlighted_text), unsafe_allow_html=True)
