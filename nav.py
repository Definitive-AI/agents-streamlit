import os
import sys
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

definitive_ai = st.Page("main.py", title="Definitive AI")
chat_interview = st.Page("interview.py", title="Chat Interview", icon="🛠️")
process_documentation = st.Page("process.py", title="Process Documentation", icon="🛠️")
form = st.Page("form.py", title="Form", icon="🛠️")
brainstorm = st.Page("brainstorm.py", title="Brainstorm", icon="🛠️")
video_interview = st.Page("video.py", title="Video Interview", icon="🛠️")

aider_gui = st.Page("aider_gui.py", title="Aider", icon="🛠️")

management = st.Page("management.py", title="Management", icon="🛠️")

signup = st.Page("registration.py", title="Signup", icon="📩")
blog = st.Page("blog.py", title="Blog", icon="📩")

# Create the navigation structure
pg = st.navigation({
    "Home": [definitive_ai],
    "Generators": [chat_interview, process_documentation, form, brainstorm, video_interview],
    "Aider": [aider_gui],
    "Agents": [management],
    "Other": [signup, blog]
})

pg.run()

# try:
#     pg.run()
# except Exception as e:
#    st.error(f"Something went wrong: {str(e)}", icon=":material/error:")


# @st.fragment(run_every="4s")
# def this_is_a_fragment():
#     st.write("This is inside of a fragment!")


# st.rerun(scope="fragment") # This will only rerun the fragment it is inside
# st.rerun() # This will rerun the entire a
if __name__ == '__main__':
    args = sys.argv[1:]
    print("Start")
    print(args)
    os.environ["Def_API_KEY"] = args[0]
    os.environ["ANTHROPIC_API_KEY"] = args[1]
    os.environ["SERVER"] = args[2]