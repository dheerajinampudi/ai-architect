import os
import streamlit as st
from PIL import Image
from constants import (
    EMBEDDING_MODEL_NAME,
    EMBEDDING_SIZE, 
    TODO_CHAIN_MODEL_NAME,
    BABY_AGI_MODEL_NAME
)
from src.agent import run_agent

im = Image.open("src/assets/favicon.png")
st.set_page_config(page_title='AI-Architect', page_icon=im, initial_sidebar_state="auto", menu_items=None)
st.title("AWS AutoGPT+Google Search Assistant")
st.caption('This AI tool use Langchain, OpenAI, Google search API and AutoGPT to develop an action plan with AWS Cloudformation/SAM Templates')

# if you just want to use the .env file, uncomment the following lines
# from decouple import config
# if config('OPENAI_API_KEY', default=None) is not None and config('GOOGLE_API_KEY', default=None) is not None:
#     os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')
#     os.environ["GOOGLE_API_KEY"] = config('GOOGLE_API_KEY')
#     os.environ["google_cse_id"] = config('google_cse_id')

st.sidebar.title("Configuration")
st.sidebar.subheader("Enter Your API Keys 🗝️")
#OPEN API KEY
open_api_key = st.sidebar.text_input(
    "Open API Key", 
    value=st.session_state.get('open_api_key', ''),
    help="Get your API key from https://platform.openai.com/account/api-keys",
    type='password'
)
os.environ["OPENAI_API_KEY"] = open_api_key
#GOOGLE API KEY
google_api_key = st.sidebar.text_input(
    "Google Search API Key", 
    value=st.session_state.get('google_api_key', ''),
    help="Get your API key from https://developers.google.com/custom-search/v1/overview/",
    type='password'
)
os.environ["GOOGLE_API_KEY"] = google_api_key
#GOOGLE CSE ID
google_cse_id = st.sidebar.text_input(
    "Google CSE ID", 
    value=st.session_state.get('google_cse_id', ''),
    help="Get your CSE ID from https://cse.google.com/cse/create/new/",
    type='password'
)
os.environ["GOOGLE_CSE_ID"] = google_cse_id

#Setting the sessions
st.session_state['open_api_key'] = open_api_key
st.session_state['google_api_key'] = google_api_key
st.session_state['google_cse_id'] = google_cse_id

#st.sidebar.divider()  # 👈 Draws a horizontal rule

#selecting the intensity of the results #### NEW CHANGES (NOT YET USED in the model)
st.sidebar.subheader("Set your temperature (Experimental)")
st.sidebar.markdown("For transformation tasks (extraction, standardization, format conversion, grammar fixes) prefer a temperature of 0 - 0.3.")
st.sidebar.markdown("For writing tasks, you should use the temperature higher, closer to 0.5. ")
st.sidebar.markdown("If you want GPT to be highly creative, consider values between 0.7 - 1.")
temperature = st.sidebar.slider('What is the model temperature?', min_value =0.0, max_value=1.0, value= 0.1,step=0.1)

#st.sidebar.divider()  # 👈 Draws a horizontal rule
#Advanced Settings
with st.sidebar.expander('Advanced Settings ⚙️', expanded=False):
    st.subheader('Advanced Settings ⚙️')
    num_iterations = st.number_input(
        label='Max Iterations',
        value=5,
        min_value=2,
        max_value=20,
        step=1
    )
    baby_agi_model = st.text_input('OpenAI Baby AGI Model', BABY_AGI_MODEL_NAME, help='See model options here: https://platform.openai.com/docs/models/overview')
    todo_chaining_model = st.text_input('OpenAI TODO Model', TODO_CHAIN_MODEL_NAME, help='See model options here: https://platform.openai.com/docs/models/overview')   
    embedding_model = st.text_input('OpenAI Embedding Model', EMBEDDING_MODEL_NAME, help='See model options here: https://platform.openai.com/docs/guides/embeddings/what-are-embeddings')
    # embedding_size = st.text_input('Embedding Model Size', EMBEDDING_SIZE, help='See model options here: https://platform.openai.com/docs/guides/embeddings/what-are-embeddings')


# user_input = st.text_input(
#     "How can I be of service?", 
#     key="input"
# )
col1, col2 = st.columns(2)
## Assistant ROLE types
assistant_role_name = col1.selectbox('What is the AI Assistant Role Name?',
    ('Solutions Architect', 'Python Developer', 'DynamoDB Expert'))
#st.write('You selected:', assistant_role_name)

## User ROLE
user_role_name = col2.selectbox('What is the User Role Name?',
    ('CTO', 'Product Manager', 'Engineering Manager'))

## Question area with sample
task = st.text_area("Task", "Develop a SAM template to deploy an Amazon API Gateway HTTP API with a Lambda integration.")
word_limit = st.number_input("Word Limit", 10, 1500, 100)
task_specifier_prompt = f"""Here is a task that {assistant_role_name} will help {user_role_name} to complete: {task}.
    Please make it more specific. Make sure you give code examples to every response.
    Please reply with the specified task in {word_limit} words or less."""
user_input = task_specifier_prompt ## Temp for testing

if st.button('Start Autonomus AI Architect'):
    if user_input != "" and (open_api_key == '' or google_api_key == '' or google_cse_id == ''):
        st.error("Please enter your API keys in the sidebar")
    elif user_input != "":
        run_agent(
            user_input=user_input,
            num_iterations=num_iterations,
            baby_agi_model=baby_agi_model,
            todo_chaining_model=todo_chaining_model,
            embedding_model=embedding_model,
            # embedding_size=embedding_size
        )
    
        # Download the file using Streamlit's download_button() function
        st.download_button(
            label='Download Results',
            data=open('output.txt', 'rb').read(),
            file_name='output.txt',
            mime='text/plain'
        )