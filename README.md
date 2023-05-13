## Overview

The app creates an action plan to complete the user's tasks and searches Google for information to keep itself up to date.
This is a BabyAGI + Google Search API tool that uses Langchain's framework hosted on Streamlit.

---
Access app here: https://dheerajinampudi-ai-architect-streamlit-app-r3ui99.streamlit.app/

<img width="1728" alt="image" src="src/assets/example-screenshot/running_assistant_screenshot.png">

# Sample results GIF
<img width="1328" alt="image" src="src/assets/example-screenshot/AUTOGPT_results.gif">

## To run

Then run the following commands:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py

```
If streamlit is not working, checkout their [installation page](https://docs.streamlit.io/library/get-started/installation)

---

### Develop

1. BabyAGI + Google Search API App

2. UI inputs types
   - AI Role
   - User Roles
   - Task type

---

### TODO

- [ ] Need toimprove prompt inputs 
- [ ] Need to format the output into code formats
- [ ] Need to add AI Role dropdown
- [ ] Need to add User Role dropdown
- [ ] Need to add Task Type dropdown

---
### Inspired by

- https://discuss.streamlit.io/t/free-autogpt-a-powerful-ai-agent-without-paid-apis-with-streamlit/41576