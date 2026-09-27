# MySQL Copilot Chat Plugin
# Written for MySQL 8.0.46
from wb import *
import grt
import mforms

ModuleInfo = DefineModule(
    "AiCopilotModule", 
    author="Jatin Jindal", 
    version="1.0.0", 
    description="Chat with Local AI models in MySQL Workbench"
)

@ModuleInfo.plugin(
    plugin_name="vercetti322.AiCopilotChat.Chat",
    caption="Chat with AI",
    pluginMenu="Utilities",
    input=[wbinputs.currentSQLEditor()]
)
@ModuleInfo.export(grt.INT, grt.classes.db_query_Editor)
def chat_window(editor):
    from mysql_ai_copilot import window
    window(editor).run()
    return 0