import traceback
from openai import OpenAI
import pyperclip
import pyautogui
import time
import os

# Read the API key from the file
def load_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.readline().strip()

api_key = "your_api_key_here"
model = "gpt-4o-mini"  # Replace with the model you are using

class Chatbot:
    def __init__(self, api_key, model):
        """Initialize with API key and model."""
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat_completion(self, messages):
        """Centralized chat completion logic with streaming."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True  # Enable streaming
            )

            pyautogui.press('right')
            # Collect the streamed responses
            full_response = ""
            for chunk in response:
                choices = chunk.choices
                if choices and len(choices) > 0:
                    delta = choices[0].delta
                    content = getattr(delta, 'content', None)
                    if content:
                        full_response += content
                        pyautogui.typewrite(content)  # Type each chunk as it arrives

            return full_response

        except Exception as e:
            print(f"Error interacting with OpenAI API: {str(e)}")
            traceback.print_exc()
            return None
        
class Conversation:
    def __init__(self):
        self.messages = []  # No default starting message

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_conversation_format(self):
        return [{"role": message["role"], "content": message["content"]} for message in self.messages]

def get_focused_app():
    """Get the name and additional information of the currently focused application."""
    if os.name != "posix":
        return "Unknown Application", "Unknown Class"
    
    try:
        window_id = os.popen("xdotool getwindowfocus").read().strip()
        window_name = os.popen(f"xdotool getwindowname {window_id}").read().strip()
        window_class = os.popen(f"xprop -id {window_id} WM_CLASS").read().strip()
        window_class_name = window_class.split('=')[-1].strip().strip('"').split(',')[-1].strip().strip('"')
        
        useful_window_class = window_class_name.split(',')[-1].strip().strip('"')
        
        return window_name, useful_window_class
    except Exception as e:
        print(f"Error getting focused application: {str(e)}")
        return "Unknown Application", "Unknown Class"


def get_gpt_response(user_input):
    """
    Function to get GPT response for a given user input.
    """
    focused_app, focused_class = get_focused_app()
    system_message = f"""
    You are an AI designed to assist users by continuing their sentences based on the context provided. 
    Your goal is to continue the text without repeating any letters or words already present in the input. 
    Ensure that your completions are coherent and contextually relevant. Pay special attention to whether the starting character should be a space or not, as it is very important and depends on the context. If the context requires a space, make sure it is present; if not, avoid starting with a space. Specifically, if you are continuing a word, do not start with a space. If the last character is the end of a word, then start with a space.
    Do not start or end your response with quotes (' or " or `) unless it makes sense in the context.

    The user is seeking autocompletion for the currently focused application: Window name: **{focused_app}** - Process name: **{focused_class}**). 
    Your response should be based on the context of this application.

    Examples:
    - User:Tell me about the wea
        AI:ther today.
    - User:The quick brown
        AI: fox jumps over the lazy dog.
    - User:I love programming in Pyt
        AI:hon because it's versatile.
    """

    chatbot = Chatbot(api_key=api_key, model=model)
    conversation = Conversation()
    conversation.add_message("system", system_message)
    conversation.add_message("user", user_input)
    messages = conversation.get_conversation_format()
    response = chatbot.chat_completion(messages)
    
    # Ensure that if the two starting characters are space, we make it only 1
    if response.startswith("  "):
        response = response[1:]
    
    return response

def set_cursor_busy():
    if os.name == "posix":
        os.system("xsetroot -cursor_name watch")

def set_cursor_default():
    if os.name == "posix":
        os.system("xsetroot -cursor_name left_ptr")


def main():
    # Set cursor to busy
    set_cursor_busy()

    # Simulate Ctrl + A to select all text
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')

    # Wait a moment to ensure the clipboard is updated
    time.sleep(1)

    # Get the clipboard content
    clipboard_content = pyperclip.paste()

    # Pass the clipboard content to the get_gpt_response function
    get_gpt_response(clipboard_content)

    # Set cursor back to default
    set_cursor_default()

if __name__ == "__main__":
    main()