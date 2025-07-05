from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_core.prompts import PromptTemplate, load_prompt
import edge_tts
import asyncio




st.header('Research Tool')

llm_key = st.text_input('Your open AI api key')

paper_input = st.text_input('Enter the name of the Research Paper')

# st.write('OR')

# uploaded_file = st.file_uploader("Upload PDF file", type="pdf")

voice_style = st.selectbox("Select podcast tone", ["Guy (Probably had too much coffee)", 
                                                   "Ava (Eternal optimist energy)", 
                                                   "Christopher (Smooth operator with dad jokes)", 
                                                   "Emma (Cosmic wisdom meets cozy vibes)"])

target_length = st.selectbox("Select Explanation Length", ["Short summary of the paper", "Long detailed explanation"] )

explanation_style = st.selectbox("Select Explanation Style", ["Comprehensive - A balanced approach covering all aspects",
                                                              "Technical - Focuses on methodologies and detailed processes", 
                                                              "Mathematical - Emphasizes equations and quantitative analysis",
                                                              "Application-based - Highlights practical uses and real-world implementations",
                                                              "Conceptual - Focuses on theories and big-picture ideas",
                                                              "Story-driven - Presents findings through narratives and human impact"] )

template = load_prompt('template.json')

voice_map = {
    "Ava (Eternal optimist energy)": "en-US-AvaNeural",
    "Emma (Cosmic wisdom meets cozy vibes)": "en-US-EmmaNeural",
    "Christopher (Smooth operator with dad jokes)": "en-US-ChristopherNeural",
    "Guy (Probably had too much coffee)": "en-US-GuyNeural"
}

async def generate_audio(text, voice, file_path):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(file_path)


if st.button('Summarize'):

    if not llm_key:
        st.error('Please enter your open AI api key')

    llm = ChatOpenAI(
        model="meta-llama/llama-3.3-70b-instruct:free",
        openai_api_base="https://openrouter.ai/api/v1", 
        openai_api_key = llm_key
    )
    
    chain = template | llm
    result = chain.invoke({
        'paper_input':paper_input,
        'voice_style':voice_style,
        'target_length':target_length,
        'explanation_style':explanation_style
    })

    if "Sorry, could not find any research paper" in result.content:
        st.write(result.content)
    else:
        voice = voice_map[voice_style]
        audio_path = "summary.mp3"
        asyncio.run(generate_audio(result.content, voice, audio_path))
        st.audio(audio_path)
