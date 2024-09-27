# GPT Autocomplete

## Description

This repository contains a Python script that uses OpenAI's GPT model to autocomplete text from the clipboard. The script simulates `Ctrl + A` and `Ctrl + C` to copy the current text, processes it with GPT to generate an autocomplete continuation, and then pastes the combined text back using `Ctrl + V`.

## Features

- Simulates `Ctrl + A` and `Ctrl + C` to copy the current text.
- Uses OpenAI's GPT model to generate an autocomplete continuation of the copied text.
- Combines the original text with the GPT-generated continuation.
- Updates the clipboard with the combined text.
- Simulates `Ctrl + V` to paste the combined text.

## Requirements

- Python 3.x
- `pyperclip` library
- `pyautogui` library
- OpenAI API key

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/gpt-autocomplete.git
   cd gpt-autocomplete
   ```

2. Install the required libraries:
   ```sh
   pip install pyperclip pyautogui
   ```

3. Ensure you have an OpenAI API key and save it in a file named `gpt_api_key.txt`.

## Usage

1. Run the script:
   ```sh
   python main.py
   ```

2. The script will:
   - Simulate `Ctrl + A` and `Ctrl + C` to copy the current text.
   - Retrieve the clipboard content.
   - Pass the clipboard content to the GPT model to generate an autocomplete continuation.
   - Combine the original text with the GPT-generated continuation.
   - Update the clipboard with the combined text.
   - Simulate `Ctrl + V` to paste the combined text.

## License

This project is licensed under the MIT License.
