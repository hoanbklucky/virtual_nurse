import streamlit as st
import csv
import io
import vertexai
import json
import os

#from text_variant import question_generator
#from virtual_nurse import generate
from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig, Retrieval, Tool, VertexRagStore
from vertexai import rag
import base64

PROJECT_ID = os.environ.get("PROJECT_ID")
#LOCATION = "us-central1"
#vertexai.init(project=PROJECT_ID, location=LOCATION)

client = genai.Client(
      vertexai=True,
      project="virtual-nurse-450613",
      location="us-central1",
  )

textsi_1 = """You are a helpful doctor and should give medical advice. You will ask patient the following questions, one question at a time: 
    1) what is the patient's name? 
    2) what is the patient's gender? 
    3) what is the patient's age? 
    4) how many day post operation? 
    5) describe patient's condition. 
    After that, you will write a summary about the patient. 
    After that, you will provide a severity classification and a triage decision written in bold."""

model = "gemini-2.0-flash-001"

tools = [
    Tool(
      retrieval=Retrieval(
        vertex_rag_store=VertexRagStore(
          rag_corpora=[
            "projects/virtual-nurse-450613/locations/us-central1/ragCorpora/6917529027641081856"
          ],
          similarity_top_k=10,
          vector_distance_threshold=0.5
        )
      )
    )
  ]

generate_content_config = GenerateContentConfig(
temperature = 1,
top_p = 0.95,
max_output_tokens = 8192,
response_modalities = ["TEXT"],
safety_settings = [types.SafetySetting(
    category="HARM_CATEGORY_HATE_SPEECH",
    threshold="BLOCK_LOW_AND_ABOVE"
),types.SafetySetting(
    category="HARM_CATEGORY_DANGEROUS_CONTENT",
    threshold="OFF"
),types.SafetySetting(
    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
    threshold="OFF"
),types.SafetySetting(
    category="HARM_CATEGORY_HARASSMENT",
    threshold="OFF"
)],
tools = tools,
system_instruction=[types.Part.from_text(text=textsi_1)],
)
    
def generate(contents):
    for chunk in client.models.generate_content_stream(
            model = model,
            contents = contents,
            config = generate_content_config,
            ):
            if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                continue
            yield chunk.text

st.title(" 🤖 Virtual Nurse")
st.header("I am a virtual nurse", divider="gray")
st.write("""To be able to assist you, I will ask you some questions related to the patient and then let you know triage decision. I can also provide you general guidance on post tonsillectomy care. Are you ready?""")

if "model" not in st.session_state:
    st.session_state["model"] = "gemini-2.0-flash-001"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "contents" not in st.session_state:
    st.session_state.contents = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.contents.append(types.Content(role="user", parts=[types.Part.from_text(text=prompt)]))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("model"):
        response = st.write_stream(generate(st.session_state.contents))

    st.session_state.messages.append({"role": "model", "content": response})
    st.session_state.contents.append(types.Content(role="model", parts=[types.Part.from_text(text=response)]))
    print(st.session_state.contents)
    
