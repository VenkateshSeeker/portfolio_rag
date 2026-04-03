from langchain_core.chat_history import InMemoryChatMessageHistory

# Initialize the global store dictionary here
store = {}

def get_session_history(session_id: str):
    """
    Retrieves or creates chat history for a given session ID.
    """
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
        
    return store[session_id]