import streamlit as st
from st_pages import Page, show_pages, add_page_title, Section, add_indentation

#add_page_title() 
add_indentation()

show_pages(
    [
        Page("main.py", "Definitive AI"),
        Section("Generators", "🧙‍♂️"),
        Page("process.py", "Process Documentation", "🛠️", in_section=True),
        Page("interview.py", "Interview", "🛠️", in_section=True),
        Section("Storage", "💾"),
        Page("file.py", "Download", "🛠️", in_section=True),
        Page("form.py", "Signup",  icon="📩", in_section=False ),
    ]
)

st.html("""
<style>
[data-testid=stSidebar] {
        background-color: #212750;
    }
[data-testid="stSidebarContent"] {
    color: white;
    span {
        color: white;
    }
}
</style>
""")

st.markdown("""<img src="https://raw.githubusercontent.com/Definitive-AI-Testing/agents-streamlit/master/.streamlit/Logo.png" height="150" />""", unsafe_allow_html=True) 


st.markdown("---")

with st.expander("Sign up here"):
    st.markdown("""
    
    <a href="https://definitive-ai.com/"><img src="https://raw.githubusercontent.com/Definitive-AI-Testing/agents-streamlit/master/.streamlit/sign-up.jpg" height="50" /></a>

""", unsafe_allow_html=True)

st.markdown("""
### 📓 User Guide
 
## Introduction
Definitive AI is a cutting-edge solution that harnesses the power of GPT to enable organizations to seamlessly develop and deploy AI agents. By simply providing process documentation or user interviews, Definitive AI can automatically extract requirements, design optimized agent architectures, and implement the agents within your existing systems and workflows.

### Why Definitive AI?
Traditionally, developing AI agents has been a complex and time-consuming process, requiring significant expertise in AI design and implementation. Even with advanced toolkits and frameworks, translating real-world requirements into optimized agent architectures remains a major challenge. 

Definitive AI breaks through these limitations by leveraging GPT's advanced natural language processing capabilities. It can understand and extract key information from unstructured data sources like process documents and user interviews. This eliminates the need for manual requirements gathering and design, dramatically accelerating the AI agent development lifecycle.

With Definitive AI, organizations can:
- Rapidly prototype and deploy AI agents with minimal effort
- Ensure agents are optimized for their specific use case and environment
- Seamlessly integrate agents into existing systems and workflows
- Scale AI initiatives without needing to expand their in-house AI expertise

## Getting Started
1. Sign up for a Definitive AI account at the signup page. Enter your first name, last name, email, language preference, use case, and register.

2. After signing up, you will receive a Definitive API Key. This key is unique to your account and is required to authenticate and access Definitive AI's features. Keep this key secure and do not share it with others. You can manage your key in the account settings.

3. To use Definitive AI's generators, you will also need an Anthropic API Key. This key allows Definitive AI to access Anthropic's GPT models which power the agent generation. You can sign up for an Anthropic API key at [https://www.anthropic.com](https://www.anthropic.com). See the Anthropic API Key Guide for more details on obtaining and using your key.

## Generators
Definitive AI provides two main generators for creating AI agents:

### Process Documentation 
1. Navigate to the Process Documentation generator.
2. Select the process documentation file(s) you want to upload. You can drag and drop files or browse to select them. The limit is 200MB per file.
3. Definitive AI will analyze the provided documentation and generate optimized AI agents based on the extracted requirements. 
4. Each Process Documentation generation session is assigned a unique Generator SessionID. You can use this ID to track and reference the specific generation task.
5. The average cost per Process Documentation generation is $5-10, and the typical processing time is 15-30 minutes, depending on the complexity and size of the provided documentation.
6. Once the agent generation is complete, you will receive an email notification. The generated agents can then be accessed in the Storage section.

### Interview
1. Go to the Interview generator. 
2. Choose a screenshot to upload that provides context for the interview. You can drag and drop the file or browse to select it.
3. Enter your message to start the interview with Eva, Definitive AI's interview agent. Eva will ask a series of questions to understand your process in detail.
4. Like Process Documentation generation, each Interview session has a unique Generator SessionID for tracking and reference.
5. The average cost per Interview-based generation is $5-10, and the typical interview duration is 15-30 minutes.
6. After the interview, Eva will generate process documentation and AI agent designs based on the information gathered. You will receive an email notification when the generation is complete, and the outputs will be available in the Storage area.

## Storage
The Storage section allows you to access, download, and manage the AI agents and documentation generated using the Process Documentation or Interview tools. Simply navigate to Storage and select the desired file.

## Support
If you need any assistance or have questions about using Definitive AI, the best way to get support is through the Definitive AI Discord. Join the #definitive-ai channel to discuss with the community. 

To make Discord discussions more organized:
- Follow these recommendations when asking for help
- Read the Definitive AI community guidelines

By leveraging Definitive AI's powerful GPT-based system, you can rapidly design and deploy optimized AI agents to automate and enhance your organization's processes. The intuitive generators streamline the development workflow, while the Storage area provides easy access to your created assets.
            
Sign up through the above link to receive a Definitive AI API Key.            

[Anthropic API Key Guide](https://docs.anthropic.com/en/docs/getting-access-to-claude)
            
[Process Documentation Example](http://officeautomata.blob.core.windows.net/officeautomata-documents/PDD%20Example.docx)
            

### ❔ Asking for help in Discord

The best way to get support is to use [Definitive AI Discord](https://datatalks.club/slack.html). Join the [`#Definitive AI`](https://app.slack.com/client/T01ATQK62F8/C01FABYF2RG) channel.

To make discussions in Discord more organized:

* Follow [these recommendations](asking-questions.md) when asking for help
* Read the [Definitive AI community guidelines](https://datatalks.club/slack/guidelines.html)

""", unsafe_allow_html=True)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
