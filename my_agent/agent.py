from json import tool

from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
import os

def open_window_settings():
    os.system('start ms-settings:')

def open_notepad():
    os.system('start notepad')

def folder_exists(folder_name):
    return os.path.exists(folder_name)

def create_folder(folder_name):
    os.mkdir(folder_name)
    return f"Folder '{folder_name}' created successfully"

def delete_folder(folder_name):
    os.rmdir(folder_name)
    return f"Folder '{folder_name}' deleted successfully"

def rename_folder(old_name, new_name):
    os.rename(old_name, new_name)
    return "Folder renamed successfully"

def create_file(folder_name, file_name, content):
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, "w") as file:
     file.write(content)
    return "File created successfully"


def delete_file(folder_name, file_name):
    file_path = os.path.join(folder_name, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    return "File deleted successful"

def update_file_content(folder_name, file_name, content):
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, "w") as file:
        file.write(content)
    return "File content updated successfully"

def rename_file(folder_name, old_file_name, new_file_name):
    old_path = os.path.join(folder_name, old_file_name)
    new_path = os.path.join(folder_name, new_file_name)
    os.rename(old_path, new_path)
    return "File renamed successfully"


folder_agent = Agent(
    model='gemini-2.5-flash',
    name='folder_agent',
    instruction="when user ask to create folder extract folder name and call create_folder tool"
                "when user ask to delete folder extract folder name and call delete_folder tool"
                "when user ask to rename folder extract folder name and call rename_folder tool",
    tools=[create_folder, delete_folder, rename_folder],
)

file_agent = Agent(
    model='gemini-2.5-flash',
    name='file_agent',
    instruction="""
    when user ask to create file:
    - extract folder name
    - extract file name
    - extract content
    - call create_file tool

    when user ask to delete file:
    - extract folder name
    - extract file name
    - call delete_file tool

    when user ask to update file contents:
    - extract folder name
    - extract file name
    - extract content
    - call update_file_content tool

    when user ask to rename file:
    - extract folder name
    - extract old file name
    - extract new file name
    - call rename_file tool
    """,
    tools=[create_file, delete_file, update_file_content, rename_file],

)
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    instruction="""
    - Use folder_agent for folder tasks
    - Use file_agent for file tasks

    If user asks to create file:
    1. Check folder exists using folder_exists
    2. If folder missing invoke folder_agent
    3. Then invoke file_agent
    """,
    tools=[folder_exists],
    sub_agents=[folder_agent, file_agent]
)

agents = root_agent