# MySQL Copilot Chat Plugin
from wb import *
import mforms, grt, uuid

_chat_window = None
_chat_dock = None
CHAT_ID = "ai-chat-" + str(uuid.uuid4())

ModuleInfo = DefineModule(
    "AiCopilotModule", 
    author="Jatin Jindal", 
    version="1.0.0", 
    description="Chat with Local AI models in MySQL Workbench"
)

@ModuleInfo.plugin(
    "vercetti322.AiCopilotChat.Chat",
    caption="Chat with AI",
    pluginMenu="SQL/Utilities",
    input=[wbinputs.currentSQLEditor()]
)
@ModuleInfo.export(grt.INT, grt.classes.db_query_Editor)
def chat_window(editor):
    global _chat_window, _chat_dock
    import os, sys

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from mysql_ai_copilot import ChatWindow

    # get the docing point reference for the current editor
    d_point = mforms.fromgrt(editor.dockingPoint)
    chat_view_exists = False

    # iterate over tabs in editor to find the "ai-chat" window
    for i in range(d_point.view_count()):
        view = d_point.view_at_index(i)

        if view.identifier() == CHAT_ID:
            d_point.select_view(view)
            chat_view_exists = True
            break
            
    # "ai-chat" not in editor, create a window
    if not chat_view_exists:
        chat_window_view = ChatWindow(chat_id=CHAT_ID)
        d_point.dock_view(chat_window_view, "", 0)

        chat_window_view.set_title("AI Chat")
        d_point.select_view(chat_window_view)
        return 0