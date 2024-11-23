import streamlit as st
from googletrans import Translator, LANGCODES, LANGUAGES
from gtts import gTTS
import tempfile
import os

def clean_input(text:str) -> str | None:

    if not text or not text.strip() or not isinstance(text, str) or '\x00' in text: return None

    return text.strip().lower()


def translate_text(text:str, dest:str, src:str=None) -> str | None:

    translator = Translator()

    dest = clean_input(dest)
    if not dest:
        print("Invalid Destination Format")
        return None

    if not src: src = translator.detect(text=text).lang
    else:
        src = clean_input(src)
        if not src:
            print("Invalid Source Language")
            update_translated_text("Invalid Source Language")
            return None

    try:
        result = translator.translate(
            text=text,
            dest=LANGCODES[dest],
            src=src
        )

    except KeyError:
        print("Destination Not Found !")
        return None

    return result.text

def text_to_speech(text:str, lang:str) -> str | None:

    lang = clean_input(lang)

    if not lang:
        print("Invalid Language Format")
        return None

    try:
        tts = gTTS(
            text=text,
            lang=LANGCODES[lang],
            slow=False,
            lang_check=False
        )

        with tempfile.NamedTemporaryFile(
            mode='w+b',
            suffix='.mp3',
            delete=False
        ) as temporaryFile:

            tts.save(temporaryFile.name)
            return temporaryFile.name

    except Exception as error:
        print(f"TTS Error: {error}")
        return None

def update_translated_text(text:str='Translate'):

    with placeHolder:
        st.text_area(
            label='Translated Content',
            height=200,
            key=f'translatedText_{text}',
            help='Displays the translated text',
            value=text,
            disabled=True,
            label_visibility='visible'
        )

st.set_page_config(
    page_title='Cultural Connect',
    page_icon='images\\page_icon.png',
    layout='wide'
)


titleCol, imageCol = st.columns(spec=[1, 7], gap='small', vertical_alignment='top')
with titleCol:st.title("Translate")
with imageCol: st.image('images\\title_icon.png', width=64)

col1, col2 = st.columns(spec=2, gap='medium', vertical_alignment='top')

with col1:
    sourceLang = st.selectbox(
        label='Source',
        options=LANGCODES.keys(),
        index=list(LANGCODES.keys()).index('english'),
        key='source',
        help='Select the source of the input text',
        placeholder='Choose the Source Language',
        disabled=False,
        label_visibility='visible'
    )

with col2:
    destinationLang = st.selectbox(
        label='Destination',
        options=LANGUAGES.values(),
        index=list(LANGUAGES.values()).index('tamil'),
        key='destination',
        help='Select the Destination of the input text',
        placeholder='Choose the Destination Language',
        disabled=False,
        label_visibility='visible'
    )

inputText = st.text_area(
    label='Enter Text',
    height=200,
    key='inputText',
    help='Enter the text to translate',
    placeholder='Type something !',
    disabled=False,
    label_visibility='visible'
)

placeHolder = st.empty()
update_translated_text()

if inputText:
    translatedText = translate_text(text=inputText, dest=destinationLang, src=sourceLang)

    if translatedText: update_translated_text(text=translatedText)

st.markdown(
    """
    ---
    <div style="text-align: center;  margin-top: 50px;">
        Built with ❤️ by <a href="https://github.com/Hariesh28" target="_blank">Hariesh</a>
    </div>
    """,
    unsafe_allow_html=True
)