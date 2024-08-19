#!/usr/bin/env python

import os
import random
import sys
import git
import requests
import asyncio
import socketio
import threading
import time
import socketio
from git import Repo
from pathlib import Path

import streamlit as st
from streamlit.runtime import get_instance
from streamlit.runtime.scriptrunner import get_script_run_ctx

from aider import urls
from aider.coders import Coder
from aider.dump import dump  # noqa: F401
from aider.io import InputOutput
from aider.main import main as cli_main
from aider.scrape import Scraper
from aider.models import Model
from aider.repo import GitRepo
from aider.io import InputOutput

import streamlit as st

from dotenv import load_dotenv
load_dotenv()

Def_API_KEY = os.environ['Def_API_KEY']
ANTHROPIC_API_KEY = os.environ['ANTHROPIC_API_KEY']
SERVER = os.environ['Def_Server'] # 'http://localhost:5000'    

st.set_page_config(layout="wide")

# st.set_page_config(
#     layout="wide",
# )

st.html("""
<style>
[data-testid=stSidebar] {
    background-color: #212750;
    header {
        color: white;
    }
    h1 {
        color: white;
    }
    p {
        color: white;
    }
}
[data-testid="stSidebarNavViewButton"]{
    h1 {
        color: white;
    }
    p {
        color: white;
    }
}
[data-testid="stSidebarContent"] {
    color: white;
    span {
        color: white;
    }
}
[data-testid=stMarkdownContainer] {
        p {
            color: gray;
        }
}        
</style>
""")

def _get_session():
    runtime = get_instance()
    session_id = get_script_run_ctx().session_id
    session_info = runtime._session_mgr.get_session_info(session_id)
    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    return session_info.session.id

session_id = _get_session()

class CaptureIO(InputOutput):
    lines = []

    def tool_output(self, msg, log_only=False):
        if not log_only:
            self.lines.append(msg)
        super().tool_output(msg, log_only=log_only)

    def tool_error(self, msg):
        self.lines.append(msg)
        super().tool_error(msg)

    def get_captured_lines(self):
        lines = self.lines
        self.lines = []
        return lines


def search(text=None):
    results = []
    for root, _, files in os.walk("aider"):
        for file in files:
            path = os.path.join(root, file)
            if not text or text in path:
                results.append(path)
    # dump(results)

    return results


# Keep state as a resource, which survives browser reloads (since Coder does too)
class State:
    keys = set()

    def init(self, key, val=None):
        if key in self.keys:
            return

        self.keys.add(key)
        setattr(self, key, val)
        return True
    
def get_git_root():
    """Try and guess the git repo, since the conf.yml can be at the repo root"""
    try:
        repo = git.Repo(search_parent_directories=True)
        return repo.working_tree_dir
    except git.InvalidGitRepositoryError:
        return None

def list_all_files(directory):
    """
    List all files in a directory and its subdirectories.
    
    :param directory: Path to the directory to scan.
    :return: A list of file paths.
    """
    file_list = []
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Join the root path and the file name to get the full file path
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    return file_list

@st.cache_resource
def get_state():
    return State()

from aider_main import main
@st.cache_resource
def get_coder(dir):
    current_directory = os.getcwd()
    new_repo_path = os.path.join(os.path.dirname(current_directory), "agents")
    #files = list_all_files(new_repo_path)
    
    argv = []

    coder = main(argv=argv,return_coder=True,force_git_root=new_repo_path,dir=dir) # argv={"git": ,force_git_root=base_dir)
    if not isinstance(coder, Coder):
        raise ValueError(coder)
    if not coder.repo:
        raise ValueError("GUI can currently only be used inside a git repo")

    io = CaptureIO(
        pretty=False,
        yes=True,
        dry_run=coder.io.dry_run,
        encoding=coder.io.encoding,
    )
    # coder.io = io # this breaks the input_history
    coder.commands.io = io

    for line in coder.get_announcements():
        coder.io.tool_output(line)

    return coder

@st.cache_resource
def reset_repo(dir):
    all_files = list_all_files(dir)
    fnames = [str(Path(fn).resolve()) for fn in all_files]
    if len(all_files) > 1:
        good = True
        for fname in all_files:
            if Path(fname).is_dir():
                good = False
        if not good:
            return 1
    git_dname = None
    if len(all_files) == 1:
        if Path(all_files[0]).is_dir():
            git_dname = str(Path(all_files[0]).resolve())
            fnames = []
    io = InputOutput()
    print(git_dname)
    repo = GitRepo(
                io,
                fnames,
                git_dname,
                False,
                # models=main_model.commit_message_models(),
                # attribute_author=args.attribute_author,
                # attribute_committer=args.attribute_committer,
                # attribute_commit_message=args.attribute_commit_message,
                # commit_prompt=args.commit_prompt,
                # subtree_only=args.subtree_only,
            )
    return repo


class Server():
    def __init__(self): # SERVER, Def_API_KEY
        print("__Server_init__")
        # self.sio = _sio
        self.SERVER = SERVER
        self.Def_API_KEY = Def_API_KEY
        self.sio = socketio.AsyncClient() # logger=True, engineio_logger=True
        
    def start(self):
        thread = threading.Thread(target=self.run_asyncio_in_thread)
        thread.start()    

    async def start_server(self):
        try:
            await self.sio.connect(self.SERVER, auth=self.Def_API_KEY) #{'token': 'my-token'}
            print('my sid is', self.sio.sid)
            await self.sio.emit('join', {'room': Def_API_KEY})
            await self.sio.wait()
        except Exception as exn:
            print(exn)


    def run_asyncio_in_thread(self):
        try:
            loop = asyncio.get_running_loop()
            task = loop.create_task(self.start_server())
        except:
            asyncio.run(self.start_server())

# @st.fragment(run_every=None)
class GUI:
    prompt = None
    prompt_as = "user"
    last_undo_empty = None
    recent_msgs_empty = None
    web_content_empty = None

    def __init__(self):
        current_directory = os.getcwd()
        new_repo_path = os.path.join(os.path.dirname(current_directory), "agents")
        # llm_model = Model(model="claude-3-5-sonnet-20240620")
        # coder:Coder = Coder.create(main_model=llm_model)
        print("__init__")
        getCurrDir = os.getcwd()
        print(getCurrDir)
        print(Def_API_KEY)
        print(ANTHROPIC_API_KEY)
        print(SERVER)
        self.coder = get_coder(new_repo_path)
        self.state = get_state()

        # print(new_repo_path)
        # self.git_repo = reset_repo(new_repo_path)
        # self.coder.repo = self.git_repo
        # print("Git Path: " + str(self.coder.repo.normalized_path))

        # self.repo_map = self.coder.get_repo_map()
        self.server = self.server() #self.callbacks,SERVER,Def_API_KEY)
        self.sio = self.server.sio
        self.callbacks()
        self.server.start()
        
        # thread = threading.Thread(target=self.run_asyncio_in_thread)
        # thread.start()    

        # Force the coder to cooperate, regardless of cmd line args
        self.coder.yield_stream = True
        self.coder.stream = True
        self.coder.pretty = False
        self.msgs = ""

        self.initialize_state()

        self.do_messages_container()
        self.do_sidebar()

        user_inp = st.chat_input("Say something")
        print("prompt:")
        print(user_inp)
        if user_inp:
            print("user_inp")
            self.prompt = user_inp
            self.process_chat(user_inp)

        # if self.prompt_pending():
        #     self.process_chat()

        # print(self.prompt_pending())
        if not self.prompt:
            return

        self.state.prompt = self.prompt

        print(self.prompt_as)

        if self.prompt_as == "user":
            self.coder.io.add_to_input_history(self.prompt)

        self.state.input_history.append(self.prompt)

        if self.prompt_as:
            self.write_msg({"role": self.prompt_as, "content": self.prompt})
        if self.prompt_as == "user":
            with self.messages.chat_message("user"):
                st.write(self.prompt)
        elif self.prompt_as == "text":
            line = self.prompt.splitlines()[0]
            line += "??"
            with self.messages.expander(line):
                st.text(self.prompt)

        # re-render the UI for the prompt_pending state
        st.rerun()    

    @st.cache_resource
    def server(_self):
        return Server() 

    def announce(self):
        lines = self.coder.get_announcements()
        lines = "  \n".join(lines)
        return lines

    def show_edit_info(self, edit):
        commit_hash = edit.get("commit_hash")
        commit_message = edit.get("commit_message")
        diff = edit.get("diff")
        fnames = edit.get("fnames")
        if fnames:
            fnames = sorted(fnames)

        if not commit_hash and not fnames:
            return

        show_undo = False
        res = ""
        if commit_hash:
            res += f"Commit `{commit_hash}`: {commit_message}  \n"
            if commit_hash == self.coder.last_aider_commit_hash:
                show_undo = True

        if fnames:
            fnames = [f"`{fname}`" for fname in fnames]
            fnames = ", ".join(fnames)
            res += f"Applied edits to {fnames}."

        if diff:
            with st.expander(res):
                st.code(diff, language="diff")
                if show_undo:
                    self.add_undo(commit_hash)
        else:
            with st.container(border=True):
                st.write(res)
                if show_undo:
                    self.add_undo(commit_hash)

    def add_undo(self, commit_hash):
        if self.last_undo_empty:
            self.last_undo_empty.empty()

        self.last_undo_empty = st.empty()
        undone = self.state.last_undone_commit_hash == commit_hash
        if not undone:
            with self.last_undo_empty:
                if self.button(f"Undo commit `{commit_hash}`", key=f"undo_{commit_hash}"):
                    self.do_undo(commit_hash)

    def do_sidebar(self):
        with st.sidebar:
            st.title("Aider")
            # self.cmds_tab, self.settings_tab = st.tabs(["Commands", "Settings"])

            # self.do_recommended_actions()
            self.do_add_to_chat()
            self.do_recent_msgs()
            self.do_clear_chat_history()
            # st.container(height=150, border=False)
            # st.write("### Experimental")

    def do_settings_tab(self):
        pass

    def do_recommended_actions(self):
        text = "Aider works best when your code is stored in a git repo.  \n"
        text += f"[See the FAQ for more info]({urls.git})"

        with st.expander("Recommended actions", expanded=True):
            with st.popover("Create a git repo to track changes"):
                st.write(text)
                self.button("Create git repo", key=random.random(), help="?")

            with st.popover("Update your `.gitignore` file"):
                st.write("It's best to keep aider's internal files out of your git repo.")
                self.button("Add `.aider*` to `.gitignore`", key=random.random(), help="?")

    def do_add_to_chat(self):
        # with st.expander("Add to the chat", expanded=True):
        self.do_add_files()
        self.do_add_web_page()

    def do_add_files(self):
        fnames = st.multiselect(
            "Add files to the chat",
            self.coder.get_all_relative_files(),
            default=self.state.initial_inchat_files,
            placeholder="Files to edit",
            disabled=self.prompt_pending(),
            help=(
                "Only add the files that need to be *edited* for the task you are working"
                " on. Aider will pull in other relevant code to provide context to the LLM."
            ),
        )

        for fname in fnames:
            if fname not in self.coder.get_inchat_relative_files():
                self.coder.add_rel_fname(fname)
                self.info(f"Added {fname} to the chat")

        for fname in self.coder.get_inchat_relative_files():
            if fname not in fnames:
                self.coder.drop_rel_fname(fname)
                self.info(f"Removed {fname} from the chat")

    def do_add_web_page(self):
        st.markdown("Hello World 👋")
        with st.popover("Add a web page to the chat"):
            self.do_web()

    def do_add_image(self):
        with st.popover("Add image"):
            st.markdown("Hello World 👋")
            st.file_uploader("Image file", disabled=self.prompt_pending())

    def do_run_shell(self):
        with st.popover("Run shell commands, tests, etc"):
            st.markdown(
                "Run a shell command and optionally share the output with the LLM. This is"
                " a great way to run your program or run tests and have the LLM fix bugs."
            )
            st.text_input("Command:")
            st.radio(
                "Share the command output with the LLM?",
                [
                    "Review the output and decide whether to share",
                    "Automatically share the output on non-zero exit code (ie, if any tests fail)",
                ],
            )
            st.selectbox(
                "Recent commands",
                [
                    "my_app.py --doit",
                    "my_app.py --cleanup",
                ],
                disabled=self.prompt_pending(),
            )

    def do_tokens_and_cost(self):
        with st.expander("Tokens and costs", expanded=True):
            pass

    def do_show_token_usage(self):
        with st.popover("Show token usage"):
            st.write("hi")

    def do_clear_chat_history(self):
        text = "Saves tokens, reduces confusion"
        if self.button("Clear chat history", help=text):
            self.coder.done_messages = []
            self.coder.cur_messages = []
            self.info("Cleared chat history. Now the LLM can't see anything before this line.")

    def do_show_metrics(self):
        st.metric("Cost of last message send & reply", "$0.0019", help="foo")
        st.metric("Cost to send next message", "$0.0013", help="foo")
        st.metric("Total cost this session", "$0.22")

    def do_git(self):
        with st.expander("Git", expanded=False):
            # st.button("Show last diff")
            # st.button("Undo last commit")
            self.button("Commit any pending changes")
            with st.popover("Run git command"):
                st.markdown("## Run git command")
                st.text_input("git", value="git ")
                self.button("Run")
                st.selectbox(
                    "Recent git commands",
                    [
                        "git checkout -b experiment",
                        "git stash",
                    ],
                    disabled=self.prompt_pending(),
                )

    def do_recent_msgs(self):
        if not self.recent_msgs_empty:
            self.recent_msgs_empty = st.empty()

        if self.prompt_pending():
            self.recent_msgs_empty.empty()
            self.state.recent_msgs_num += 1

        with self.recent_msgs_empty:
            self.old_prompt = st.selectbox(
                "Resend a recent chat message",
                self.state.input_history,
                placeholder="Choose a recent chat message",
                # label_visibility="collapsed",
                index=None,
                key=f"recent_msgs_{self.state.recent_msgs_num}",
                disabled=self.prompt_pending(),
            )
            if self.old_prompt:
                self.prompt = self.old_prompt

    def do_messages_container(self):
        self.messages = st.container()

        # stuff a bunch of vertical whitespace at the top
        # to get all the chat text to the bottom
        # self.messages.container(height=300, border=False)

        with self.messages:
            for msg in self.state.messages:
                role = msg["role"]

                if role == "edit":
                    self.show_edit_info(msg)
                elif role == "info":
                    st.info(msg["content"])
                elif role == "text":
                    text = msg["content"]
                    line = text.splitlines()[0]
                    with self.messages.expander(line):
                        st.text(text)
                elif role in ("user", "assistant"):
                    with st.chat_message(role):
                        st.write(msg["content"])
                        # self.cost()
                else:
                    st.dict(msg)

    def initialize_state(self):
        messages = [
            dict(role="info", content=self.announce()),
            dict(role="assistant", content="How can I help you?"),
        ]

        self.state.init("messages", messages)
        self.state.init("last_aider_commit_hash", self.coder.last_aider_commit_hash)
        self.state.init("last_undone_commit_hash")
        self.state.init("recent_msgs_num", 0)
        self.state.init("web_content_num", 0)
        self.state.init("prompt")
        self.state.init("scraper")

        self.state.init("initial_inchat_files", self.coder.get_inchat_relative_files())

        if "input_history" not in self.state.keys:
            input_history = list(self.coder.io.get_input_history())
            seen = set()
            input_history = [x for x in input_history if not (x in seen or seen.add(x))]
            self.state.input_history = input_history
            self.state.keys.add("input_history")

    def button(self, args, **kwargs):
        "Create a button, disabled if prompt pending"

        # Force everything to be disabled if there is a prompt pending
        if self.prompt_pending():
            kwargs["disabled"] = True

        return st.button(args, **kwargs)

    def callbacks(self):
        @self.sio.on(Def_API_KEY)
        async def on_message(data):
            print('Received msg ' + Def_API_KEY + " : ", data['data'])  
            input = data['data']  
            self.agent_run(input)

        @self.sio.event
        def connect():
            print("I'm connected!")

        # @sio.event
        # def connect_error(data):
        #     print("The connection failed!")

        @self.sio.event
        def disconnect():
            print("I'm disconnected!")    

    async def send_event(self,data):
        await self.sio.send(data)


    def send_data(self,data):
        try:
            loop = asyncio.get_running_loop()
            task = loop.create_task(self.send_event(data))
        except:
            asyncio.run(self.send_event(data))

    def agent_run(self, prompt):
        self.msgs = ""
        while prompt:
            with self.messages.chat_message("assistant"):
                res = st.write_stream(self.coder.run_stream(prompt))
                self.write_msg({"role": "assistant", "content": res})
                # self.cost()

            prompt = None
            if self.coder.reflected_message:
                if self.num_reflections < self.max_reflections:
                    self.num_reflections += 1
                    self.info(self.coder.reflected_message)
                    prompt = self.coder.reflected_message

        with self.messages:
            edit = dict(
                role="edit",
                fnames=self.coder.aider_edited_files,
            )
            if self.state.last_aider_commit_hash != self.coder.last_aider_commit_hash:
                edit["commit_hash"] = self.coder.last_aider_commit_hash
                edit["commit_message"] = self.coder.last_aider_commit_message
                commits = f"{self.coder.last_aider_commit_hash}~1"
                diff = self.coder.repo.diff_commits(
                    self.coder.pretty,
                    commits,
                    self.coder.last_aider_commit_hash,
                )
                edit["diff"] = diff
                self.state.last_aider_commit_hash = self.coder.last_aider_commit_hash

            self.write_msg(edit)
            self.show_edit_info(edit)

        print("complete")
        try:
            data = {"Authorization": f"{Def_API_KEY}", "sessionid": session_id, "type":"tool", "prompt": self.msgs}  
            self.send_data(data)
        except:
            ()
        # re-render the UI for the non-prompt_pending state
        #st.rerun()

    def prompt_pending(self):
        return self.state.prompt is not None

    def cost(self):
        cost = random.random() * 0.003 + 0.001
        st.caption(f"${cost:0.4f}")

    def write_msg(self, input):
        self.state.messages.append(input)   
        if "content" in input:
            res = input["content"]
            self.msgs = self.msgs + "\n" + res
        # else:
        #     res = str(input)       

    def agent(self, prompt):
        try:
            #self.msgs
            repo_map = self.coder.get_repo_map()
            input = "User request: " + prompt + "\n\nGit Repository Map:\n" + repo_map
            headers = {"Authorization": f"{Def_API_KEY}", "sessionid": session_id, "anthapikey": ANTHROPIC_API_KEY}   
            chat_response = requests.post(url=SERVER + "/api/aider", headers=headers, json={"type":"user", "prompt": input,})
            assistant_response = chat_response.json()["response"]    
            self.msgs = ""
            return assistant_response
        except Exception as exn:
            print(exn)
            return prompt
        
    def agent_post(self,prompt):
        try:
            self.msgs
            headers = {"Authorization": f"{Def_API_KEY}", "sessionid": session_id, "anthapikey": ANTHROPIC_API_KEY}   
            chat_response = requests.post(url=SERVER + "/api/aider", headers=headers, json={"type":"user", "prompt": prompt,})
        except Exception as exn:
            print(exn)    

    def process_chat(self, prompt):
        res = self.agent_post(prompt)
        self.prompt = None


    def process_chat2(self):
        print("process_chat")
        prompt = self.state.prompt
        self.state.prompt = None

        # This duplicates logic from within Coder
        self.num_reflections = 0
        self.max_reflections = 3
        print("process_chat")

        # res = self.agent(prompt)
        # print("Agent: " + str(res))
        while prompt:
            with self.messages.chat_message("assistant"):
                res = st.write_stream(self.coder.run_stream(prompt))
                self.write_msg({"role": "assistant", "content": res})
                # self.cost()

            prompt = None
            if self.coder.reflected_message:
                if self.num_reflections < self.max_reflections:
                    self.num_reflections += 1
                    self.info(self.coder.reflected_message)
                    prompt = self.coder.reflected_message

        with self.messages:
            edit = dict(
                role="edit",
                fnames=self.coder.aider_edited_files,
            )
            if self.state.last_aider_commit_hash != self.coder.last_aider_commit_hash:
                edit["commit_hash"] = self.coder.last_aider_commit_hash
                edit["commit_message"] = self.coder.last_aider_commit_message
                commits = f"{self.coder.last_aider_commit_hash}~1"
                diff = self.coder.repo.diff_commits(
                    self.coder.pretty,
                    commits,
                    self.coder.last_aider_commit_hash,
                )
                edit["diff"] = diff
                self.state.last_aider_commit_hash = self.coder.last_aider_commit_hash

            self.write_msg(edit)
            self.show_edit_info(edit)

        print("complete")
        # try:
        #     data = {"Authorization": f"{Def_API_KEY}", "sessionid": session_id, "type":"tool", "prompt": self.msgs}  
        #     self.send_data(data)
        # except:
        #     ()
        # re-render the UI for the non-prompt_pending state
        #st.rerun()

    def info(self, message, echo=True):
        info = dict(role="info", content=message)
        self.write_msg(info)

        # We will render the tail of the messages array after this call
        if echo:
            self.messages.info(message)

    def do_web(self):
        st.markdown("Add the text content of a web page to the chat")

        if not self.web_content_empty:
            self.web_content_empty = st.empty()

        if self.prompt_pending():
            self.web_content_empty.empty()
            self.state.web_content_num += 1

        with self.web_content_empty:
            self.web_content = st.text_input(
                "URL",
                placeholder="https://...",
                key=f"web_content_{self.state.web_content_num}",
            )

        if not self.web_content:
            return

        url = self.web_content

        if not self.state.scraper:
            self.scraper = Scraper(print_error=self.info)

        content = self.scraper.scrape(url) or ""
        if content.strip():
            content = f"{url}\n\n" + content
            self.prompt = content
            self.prompt_as = "text"
        else:
            self.info(f"No web content found for `{url}`.")
            self.web_content = None

    def do_undo(self, commit_hash):
        self.last_undo_empty.empty()

        if (
            self.state.last_aider_commit_hash != commit_hash
            or self.coder.last_aider_commit_hash != commit_hash
        ):
            self.info(f"Commit `{commit_hash}` is not the latest commit.")
            return

        self.coder.commands.io.get_captured_lines()
        reply = self.coder.commands.cmd_undo(None)
        lines = self.coder.commands.io.get_captured_lines()

        lines = "\n".join(lines)
        lines = lines.splitlines()
        lines = "  \n".join(lines)
        self.info(lines, echo=False)

        self.state.last_undone_commit_hash = commit_hash

        if reply:
            self.prompt_as = None
            self.prompt = reply

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# if "aider" not in st.session_state:
#     st.session_state.aider = GUI()
    


# if __name__ == "__main__":
#     status = gui_main()
#     sys.exit(status)

def gui_main():
    GUI()


if __name__ == "__main__":
    args = sys.argv[1:]
    print("Start")
    print(args)
    os.environ["Def_API_KEY"] = args[0]
    os.environ["ANTHROPIC_API_KEY"] = args[1]
    os.environ["SERVER"] = args[2]
    status = gui_main()
    sys.exit(status)