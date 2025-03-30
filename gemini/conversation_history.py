import json

# Global variable to store the conversation history.
conversation_history = []

# Optional path for persisting the conversation history.
persist_file = None

def init_history(persist_file_path: str = None):
    """
    Initialize the conversation history. If a persist_file_path is provided, load
    history from that file.
    
    :param persist_file_path: Path to the file for persisting conversation history.
    """
    global persist_file, conversation_history
    persist_file = persist_file_path
    if persist_file:
        try:
            with open(persist_file, 'r') as f:
                conversation_history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            conversation_history = []

def add_message(role: str, text: str):
    """
    Add a message to the conversation history.
    
    :param role: 'user' or 'assistant'
    :param text: The message text.
    """
    global conversation_history
    message = {
        "role": role,
        "parts": [{"text": text}]
    }
    conversation_history.append(message)
    if persist_file:
        save_history()

def get_history():
    """
    Retrieve the entire conversation history.
    
    :return: List of message dictionaries.
    """
    return conversation_history

def clear_history():
    """
    Clear the conversation history and update persisted file if applicable.
    """
    global conversation_history
    conversation_history = []
    if persist_file:
        save_history()

def save_history():
    """
    Save the conversation history to the persist_file if specified.
    """
    if persist_file:
        with open(persist_file, 'w') as f:
            json.dump(conversation_history, f, indent=2)

def load_history():
    """
    Load the conversation history from the persist_file if specified.
    """
    global conversation_history
    if persist_file:
        try:
            with open(persist_file, 'r') as f:
                conversation_history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            conversation_history = []