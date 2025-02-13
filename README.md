# Virtual Nurse
This Gen AI app collect patient information by asking questions and provide a summary and a triage decision.
The app was build using Streamlit, following two tutorials with modification so that it works for Vertex AI.
- Streamlit tutorial on how to create a chat app: https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps
- Medium tutorial on how to integrate Vertex AI into Streamlit: https://swethag04.medium.com/build-and-deploy-a-gen-ai-app-using-vertexai-gemini-and-streamlit-df3e52e1d2f2
- Set up virtual environment as instructed in the Medium tutorial
- In the virtual environment, pip install -r requirements.txt (from the Medium tutorial git repo https://github.com/swethag04/question_variant_gemini/)
- Authenticate to google cloud (gcloud init & gcloud auth application-default login, may need to install Google Cloud CLI so that gcloud can be recognized)
- Set Google cloud Project_ID as an environment variable (export/set PROJECT_ID = 'your_project_id')
- Create Vertex AI: Chat AI -> add instruction for AI -> test -> get code
- Insert the code into the Streamlit tutorial
- Modify the Streamlit tutorial.
- Streamlit app rerun script after each event. Therefore, make sure to store chat contents/messages in st.session_state.contents and st.session_state.messages which will be preserved between the script reruns https://docs.streamlit.io/get-started/fundamentals/advanced-concepts
- Contents for Vertex AI has to be saved in a certain format, e.g. st.session_state.contents.append(types.Content(role="user", parts=[types.Part.from_text(text=prompt)])) and st.session_state.contents.append(types.Content(role="model", parts=[types.Part.from_text(text=response)]))
- To deploy on Cloud Run, follow this https://www.cloudskillsboost.google/course_templates/978/labs/488167. May need to authenticate gcloud auth application-default login as instructed in the Medium tutorial.
