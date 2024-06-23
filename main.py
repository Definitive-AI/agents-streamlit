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

st.markdown("""<p align="center">
<img src="https://raw.githubusercontent.com/Definitive-AI-Testing/agents-streamlit/master/.streamlit/Logo.png" height="150" />
</p>""", unsafe_allow_html=True) 

st.markdown("---")

st.markdown("""<p align="center">
<a href="https://definitive-ai.streamlit.app/Signup"><img src="https://raw.githubusercontent.com/Definitive-AI-Testing/agents-streamlit/master/.streamlit/sign-up.jpg" height="50" /></a>
</p>""", unsafe_allow_html=True)

st.markdown("""
### 📓 User Guide
 
## Introduction
[Definitive AI](hhttps://definitive-ai.com/) is a groundbreaking developer tool that leverages the power of GPT to revolutionize the creation and deployment of AI agents. By simply providing process documentation or participating in a structured interview, developers can automatically generate comprehensive code for sophisticated AI agents, complete with all necessary components and configurations.

### Why Definitive AI?
As a developer, creating robust AI agents involves numerous complex tasks: defining agent types, implementing tools, managing context and memory, configuring inputs and outputs, crafting system prompts, setting up triggers and decision-making processes, and integrating human input. Definitive AI streamlines this entire process, allowing you to focus on high-level design and integration rather than low-level implementation details.

With Definitive AI, developers can:

- **Automate Agent Code Generation**: Rapidly produce code for AI agents based on interviews or process documentation.
- **Define Complex Agent Architectures**: Automatically configure various agent types, tools, and decision-making processes.
- **Optimize Context and Memory Management**: Generate code for efficient handling of agent context and memory systems.
- **Streamline I/O and Prompt Engineering**: Automatically create optimized system prompts and I/O configurations.
- **Implement Triggers and Human-in-the-Loop**: Automatically generate event triggers and human input integration points.
- **Accelerate Development Cycles**: Significantly reduce time spent on boilerplate code and common AI agent patterns.
- **Enhance Code Quality and Consistency**: Leverage best practices and optimized patterns in generated agent code.

By automating the intricate details of AI agent implementation, Definitive AI empowers developers to rapidly prototype, iterate, and deploy sophisticated AI systems with minimal manual coding. This tool bridges the gap between high-level agent design and low-level implementation, enabling you to bring your AI agent concepts to life more quickly and efficiently than ever before.
   

## Getting Started
1. Sign up for a Definitive AI account at the signup page. Enter your first name, last name, email, use case, and register.

2. After signing up, you will receive a Definitive API Key. This key is unique to your account and is required to authenticate and access Definitive AI's features. Keep this key secure and do not share it with others. You can manage your key in the account settings.

3. To use Definitive AI's generators, you will also need an Anthropic API Key. This key allows Definitive AI to access Anthropic's GPT models which power the agent generation. You can sign up for an Anthropic API key at [Anthropic API Key Guide](https://docs.anthropic.com/en/docs/getting-access-to-claude).

## Example Outputs:
            
### [Multi-Agent Systems](https://github.com/Definitive-AI/Agent-Examples)

These examples demonstrate how multiple AI agents can work together:

1. **Content Writing Agents**: A system of agents that collectively gather, analyze, and synthesize research data.
2. **Email Agents**: Multiple agents managing an email account and saving short term data.
3. **LinkedIn Agents**: A system of agents that follow and write comments for a specific target.

           

## Generators
Definitive AI provides two main generators for creating AI agents:

### Process Documentation 
Using existing process documentation like the example below, you can upload the document, and AI Agents will be created from it.
            
[Process Documentation Example](http://officeautomata.blob.core.windows.net/officeautomata-documents/PDD%20Example.docx)
            
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
     

""", unsafe_allow_html=True)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# ### ❔ Asking for help in Discord

# The best way to get support is to use [Definitive AI Discord](https://datatalks.club/slack.html). Join the [`#Definitive AI`](https://app.slack.com/client/T01ATQK62F8/C01FABYF2RG) channel.

# To make discussions in Discord more organized:

# * Follow [these recommendations](asking-questions.md) when asking for help
# * Read the [Definitive AI community guidelines](https://datatalks.club/slack/guidelines.html)