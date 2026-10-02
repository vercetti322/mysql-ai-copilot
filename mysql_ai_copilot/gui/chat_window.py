from mysql_ai_copilot.ai import chat
import mforms
import threading

USER = "USER"
ASSISTANT = "ASSISTANT"

AI_CHAT_PREVIEW_TEXT = 'Ask me anything...'
AI_USER_MESSAGE_COLOR = '#E8E8E8'
AI_CHAT_BACKGROUND_COLOR = "#FFFFFF"

AI_MESSAGE_INTERNAL_PADDING = 8
AI_MESSAGE_EXTERNAL_PADDING = 8

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
        response = chat(self.messages)
        self.messages.append({"role": ASSISTANT, "content": response})

        self.is_processing = False
        self.on_ai_response(response)


class ChatWindow(mforms.AppView):
    def __init__(self, chat_id):
        super(ChatWindow, self).__init__(False, "AI Chat", "ai-chat", False)
        self.set_managed()
        self.set_back_color(AI_CHAT_BACKGROUND_COLOR)
        self.set_identifier(chat_id)

        self.chat = mforms.newBox(False)
        self.chat.set_spacing(12)

        self.scroll = mforms.newScrollPanel()
        self.scroll.add(self.chat)

        self.input = mforms.newTextEntry()
        self.input.set_placeholder_text(AI_CHAT_PREVIEW_TEXT)
        self.input.set_font("Tahoma 12")
        
        self.input.add_action_callback(self.on_submit)
        self.add(self.scroll, True, True)

        self.add(self.input, False, True)
        self.conversation = Conversation(self.on_ai_response)

    def on_ai_response(self, response):
        def ai_response():
            self.add_message(ASSISTANT, response)
            return False

        # the AI response is applied to UI on MForms thread
        mforms.Utilities.add_timeout(0, ai_response)

    def add_message(self, role, content):
        row = mforms.newBox(True)
        message = mforms.newBox(False)
        
        message.set_padding(AI_MESSAGE_INTERNAL_PADDING)
        label = mforms.newLabel(content)
        
        label.set_font("Tahoma 12")
        message.add(label, False, True)

        if role == "USER":
            message.set_back_color(AI_USER_MESSAGE_COLOR)

        row.add(message, True, True)
        self.chat.add(row, False, True)

    def on_submit(self, *args):
        prompt = self.input.get_string_value().strip()
        if not prompt: 
            return

        if self.conversation.is_processing:
            return

        self.add_message(USER, prompt)
        self.input.set_value("")
        
        self.conversation.submit(prompt)