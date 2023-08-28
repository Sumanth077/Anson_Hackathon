import os
import streamlit as st
from streamlit_chat import message
from clarifai.auth.helper import ClarifaiAuthHelper
from clarifai.modules.css import ClarifaiStreamlitCSS
from clarifai.client import create_stub
from clarifai_grpc.grpc.api import resources_pb2, service_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
from streamlit_chat import message  # Assuming this library exists for the purpose of the example
import langchain
from langchain.llms import Clarifai
from clarifai_utils.modules.css import ClarifaiStreamlitCSS
from clarifai.client.workflow import Workflow

auth = ClarifaiAuthHelper.from_streamlit(st)
stub = create_stub(auth)
userDataObject = auth.get_user_app_id_proto()
# Workflow Predict
workflow = Workflow("https://clarifai.com/anson/Idea/workflows/NeuroHarbor") 
workflow_prediction = workflow.predict_by_url(url="https://clarifai.com/anson/Idea/workflows/NeuroHarbor", input_type="text") # Supports image, text, audio, video

# Customizing Workflow Inference Output
workflow = Workflow(user_id="anson", app_id="NeuroHarbor", workflow_id="NeuroHarbor",
                  output_config={"min_value": 0.98}) # Return predictions having prediction confidence > 0.98
workflow_prediction = workflow.predict_by_filepath(filepath="local_filepath", input_type="text") # Supports image, text, audio, video

def clear_chat():
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to NeuroHarbor, Navigate your mind, Find your Harbor. How may I help you today?"}]


st.title("NeuroHarbor")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello I am NeuroHarbor"}]


with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])

    user_prompt = a.text_input(
        label="Your message:",
        placeholder="Type something...",
        label_visibility="collapsed",
    )

    b.form_submit_button("Send", use_container_width=True)


for msg in st.session_state.messages:
    message(msg["content"], is_user=msg["role"] == "user")


if user_prompt:

    print('user_prompt: ', user_prompt)

    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    message(user_prompt, is_user=True)


    response = workflow.get_response(user_prompt)  # get response from llama2 API (in our case from Workflow we created before)

    msg = {"role": "assistant", "content": response}

    print('st.session_state.messages: ', st.session_state.messages)

    st.session_state.messages.append(msg)

    print('msg.content: ', msg["content"])

    message(msg["content"])


if len(st.session_state.messages) > 1:
    st.button('Clear Chat', on_click=clear_chat)
