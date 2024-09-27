import json
import traceback
from openai import OpenAI
import pyperclip
import pyautogui
import time


# Read the API key from the file
def load_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.readline().strip()

api_key = load_api_key('gpt_api_key.txt')
model = "gpt-4o-mini"  # Replace with the model you are using

class Chatbot:
    def __init__(self, api_key, model):
        """Initialize with API key and model."""
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat_completion(self, messages):
        """Centralized chat completion logic."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )

            # Get the message content from the first choice
            message = response.choices[0].message.content
            return message

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

def get_gpt_response(user_input):
    """
    Function to get GPT response for a given user input.
    """
    system_message = """
    You are an AI designed to assist users by continuing their sentences based on the context provided. 
    Your goal is to continue the text without repeating any letters or words already present in the input. 
    Ensure that your completions are coherent and contextually relevant.

    Examples:
    - User: 'Tell me about the wea'
      AI: 'ther today.'
    - User: 'The quick brown'
      AI: 'fox jumps over the lazy dog.'
    - User: 'I love programming in Pyt'
      AI: 'hon because it's versatile.'
    """


    chatbot = Chatbot(api_key=api_key, model=model)
    conversation = Conversation()
    conversation.add_message("system", system_message)
    conversation.add_message("user", user_input)
    messages = conversation.get_conversation_format()
    return chatbot.chat_completion(messages)



def main():
    # Simulate Ctrl + A and Ctrl + C
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')

    # Wait a moment to ensure the clipboard is updated
    time.sleep(1)

    # Get the clipboard content
    clipboard_content = pyperclip.paste()

    # Pass the clipboard content to the get_gpt_response function
    response = get_gpt_response(clipboard_content)

    # Combine the initial clipboard content with the GPT response
    combined_content = clipboard_content + response

    # Update the clipboard with the combined content
    pyperclip.copy(combined_content)

    # Simulate Ctrl + V to paste the combined content
    pyautogui.hotkey('ctrl', 'v')

time.sleep(3)

if __name__ == "__main__":
    main()
