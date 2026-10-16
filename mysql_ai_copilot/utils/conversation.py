from mysql_ai_copilot.ai import chat
import threading

USER = "USER"
ASSISTANT = "ASSISTANT"

class Conversation:
    def __init__(self, on_ai_response):
        self.messages = []
        self.on_ai_response = on_ai_response
        self.is_processing = False

    def submit(self, prompt):
        if self.is_processing: return
        self.is_processing = True
        
        self.messages.append({"role": USER, "content": prompt})
        # assigns the task to call ai on a separate thread to not block UI
        threading.Thread(target=self.call_ai, daemon=True).start()
    
    def call_ai(self):
        try:
            response = chat(self.messages)
        except Exception as e:
            response = f"AI request failed: {type(e).__name__}: {e}"

        self.messages.append({
            "role": ASSISTANT,
            "content": response
        })

        self.is_processing = False
        self.on_ai_response(response)
