import os
import sys
import streamlit as st

#add_page_title() 
# add_indentation()

# show_pages(
#     [
#         Page("main.py", "Definitive AI"),
#         Section("Generators", "🧙‍♂️"),
#         Page("interview.py", "Chat Interview", "🛠️", in_section=True),        
#         Page("process.py", "Process Documentation", "🛠️", in_section=True),
#         Page("form.py", "Form", "🛠️", in_section=True),
#         Page("brainstorm.py", "Brainstorm", "🛠️", in_section=True),     
#         Page("video.py", "Video Interview", "🛠️", in_section=True),
#         Section("Aider", "🧙‍♂️"),
#         Page("aider_gui.py", "Aider",  icon="🛠️", in_section=True),
#         Section("Agents", "💾"),
#         Page("management.py", "Management", "🛠️", in_section=True),
#         Page("registration.py", "Signup",  icon="📩", in_section=False ),
#         Page("blog.py", "Blog",  icon="📩", in_section=False ),        
#     ]
# )

st.set_page_config(layout="centered")

st.html("""
<style>
[data-testid=stSidebar] {
        background-color: #212750;
        h1 {
            color: white;
        }
        header {
            color: white;
        }
    }
[data-testid="stSidebarContent"] {
    color: white;
    span {
        color: white;
    }
}
</style>
""")

st.markdown("""<p align="center"">
<img src="https://raw.githubusercontent.com/Definitive-AI-Testing/agents-streamlit/master/.streamlit/Logo.png" height="150" />
</p>""", unsafe_allow_html=True) 

st.markdown("---")

st.markdown("""<p align="center" style="font-size: 23px;" markdown="1"><b>Join our Private Beta</b></p>
<p align="center">
<a href="https://definitive-ai.streamlit.app/Signup"><img src="https://raw.githubusercontent.com/Definitive-AI-Testing/agents-streamlit/master/.streamlit/sign-up.jpg" height="50" /></a>
</p>""", unsafe_allow_html=True)

st.markdown("""
### 📓 User Guide

## Introduction
[Definitive AI](https://definitive-ai.com/) is a groundbreaking developer tool that leverages the power of GPT to revolutionize the creation and deployment of AI agents. By simply providing process documentation or participating in a structured interview with an AI, developers can automatically generate comprehensive code for sophisticated AI agents, complete with all necessary components and configurations.

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
            
#### [Multi-Agent Systems](https://github.com/Definitive-AI/Agent-Examples)

These examples demonstrate how multiple AI agents types can work together:

1. **Content Writing Agents**: A system of agents that collectively gather, analyze, and synthesize research data.
2. **Email Agents**: Multiple agents managing an email account and documenting expiring emails.
3. **LinkedIn Agents**: A system of agents that follow and write comments for a specific target.
    
#### [Solution Design Documents](https://github.com/Definitive-AI/Agent-Examples/blob/main/CreativeWritingAgents/documentation/Content%20Workflow%20Agents%20Solution%20Design%20Document.docx)
            
The Agent Generator automatically builds a comprehensive Solution Design Document (SDD) based on the requirements extracted from your process documentation or interview. The SDD includes:

1. System Architecture: Detailed breakdown of the AI agent's components and their interactions.
2. Data Flow Diagrams: Visual representations of how information moves through the system.
3. Tooling Specifications: Clearly defined interfaces for integrating the AI agent with existing systems.

The SDD serves as a blueprint for implementing the AI agents, ensuring all stakeholders have a clear understanding of the system's design and functionality.

#### [Compliance Reviews](https://github.com/Definitive-AI/Agent-Examples/blob/main/CreativeWritingAgents/documentation/Content%20Workflow%20Agents%20Compliance%20Review.docx)

As part of the AI agent generation process, Definitive AI conducts an automated Compliance Review to ensure the proposed solution adheres to relevant regulations and industry standards. This review includes:

1. Regulatory Checklist: Verification of compliance with applicable laws and regulations (e.g., GDPR, HIPAA).
3. Data Privacy Analysis: Review of data handling practices to ensure user privacy protection.
4. Audit Trail Capabilities: Confirmation that the system can provide necessary logging for compliance audits.
5. Recommendations: Suggested modifications or additional safeguards to enhance compliance.   

## Generators
Definitive AI provides five generators for creating AI agents.
Each generation session has a unique Generator SessionID for tracking and reference.
The average Anthropic cost per Interview-based Agent generation is $5-30, and the typical processing time is 10-40 minutes, depending on the complexity of the process, number of agents, and number of tools needed.
You can monitor the agent generation process in the management section. 
            
### Interview

1. Go to the Interview generator. 
2. Enter your Anthropic Key and Defintive AI key to start the interview with Eva, Definitive AI's interview agent. Eva will ask a series of questions to understand your process in detail.
3. You may choose a screenshot to upload that provides context for the interview at any time.            
4. After the interview, Eva will generate process documentation and AI agent designs based on the information gathered. You will receive an email notification when the generation is complete, and the outputs will be available in the Storage area.
    
### Form

1. Go to the Form generator. 
2. Enter your Anthropic Key and Defintive AI key
3. Answer the questions on the form, and click submit 
            
### Process Documentation 
Using existing process documentation like the example below, you can upload the document, and AI Agents will be created from it.
            
[Process Documentation Example](http://officeautomata.blob.core.windows.net/officeautomata-documents/PDD%20Example.docx)
            
1. Navigate to the Process Documentation generator.
2. Enter your Anthropic Key and Defintive AI key, and Select the process documentation file(s) you want to upload. You can drag and drop files or browse to select them. The limit is 200MB per file.
3. Definitive AI will analyze the provided documentation and generate optimized AI agents based on the extracted requirements. 

### Brainstorming

1. Go to the Brainstorming generator. 
2. Enter your Anthropic Key and Defintive AI key
3. Work with Eva to define the process you want to generate agents for
            
### Video

1. Go to the Video generator. 
2. Enter your Anthropic Key and Defintive AI key
3. Setup an call with Eva

## Storage
The Storage section allows you to access, download, and manage the AI agents and documentation generated using the Process Documentation or Interview tools. Simply navigate to Storage, input the Session ID of the generator, and click Download.

## Support
If you need any assistance or have questions about using Definitive AI, the best way to get support is through the Definitive AI Discord. Join the #definitive-ai channel to discuss with the community. 

To make Discord discussions more organized:
- Follow these recommendations when asking for help
- Read the Definitive AI community guidelines

By leveraging Definitive AI's powerful GPT-based system, you can rapidly design and deploy optimized AI agents to automate and enhance your organization's processes. The intuitive generators streamline the development workflow, while the Storage area provides easy access to your created assets.
            
Sign up through the above link to receive a Definitive AI API Key.            
    
### ❔ Asking for help in Discord

The best way to get support is to use Definitive AI Discord. Join the [`#DefinitiveAI`](https://discord.gg/4zsxZKkv) channel.     

### Privacy and Data Policy

At Definitive AI, we take your privacy and data security seriously. Please review the following information regarding our data practices during the beta phase:

Data Usage and Retention
- During the beta phase, data submitted to Definitive AI will be used to improve our product and services.
- This includes process documentation, interview responses, and generated AI agent designs.
- We anonymize and aggregate data to protect individual privacy while allowing us to enhance our systems.
- You can delete your data at any time through the Management panel

API Key Security
- Anthropic API keys are not stored or retained by Definitive AI.
- Your API key is used only for the duration of your session to generate the AI Agents.
- Always keep your API key confidential and do not share it with others.
- It is recommended to setup and use temporary Anthropic keys, and disable/delete them after the Agents are created.

Third-Party Services
- Definitive AI may use third-party services for data processing and storage.
- All third-party services are vetted to ensure they meet our security and privacy standards.

Updates to Privacy Practices
- As we transition from beta to full release, our privacy practices may be updated.
- We will notify all users of any significant changes to our data handling procedures.

By using Definitive AI during the beta phase, you acknowledge and agree to these data practices. If you have any concerns or questions about our privacy and data policies, please contact our support team through the Definitive AI Discord channel.
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""<p align="center" style="font-size: 23px;" markdown="1"><b>Join our Private Beta</b></p>
<p align="center">
<a href="https://definitive-ai.streamlit.app/Signup"><img src="https://raw.githubusercontent.com/Definitive-AI-Testing/agents-streamlit/master/.streamlit/sign-up.jpg" height="50" /></a>
</p>""", unsafe_allow_html=True)


hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 



# To make discussions in Discord more organized:

# * Follow [these recommendations](asking-questions.md) when asking for help
# * Read the [Definitive AI community guidelines](https://datatalks.club/slack/guidelines.html)