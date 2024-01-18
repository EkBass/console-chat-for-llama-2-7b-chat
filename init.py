### Constants
# Model Related
MODEL_PATH = "./model/llama-2-7b-chat.ggmlv3.q4_K_S.bin"
MODEL_TYPE = "llama"

# System and Logging
LOGGING_CONSTANTS = {
	'USER_START': "user: ",
	'AI_START': "ai: ",
	'SYSTEM_START': "system: ",
	'START_TAG': "<s>",
	'END_TAG': "</s>",
	'LOG_FILE': "log.txt",
	'ENCODING': "utf-8",
}

# Conversation
CONVERSATION_SETTINGS = {
	'SYSTEM_MSG': f"{LOGGING_CONSTANTS['START_TAG']}{LOGGING_CONSTANTS['SYSTEM_START']} 'user' is human and 'ai' is the AI assistant. 'system' provides info, such as timestamps etc.{LOGGING_CONSTANTS['END_TAG']}\n",
	'MAX_NEW_TOKENS': 4096,
	'STREAM': True,
	'HISTORY_LENGTH': 15,
	'HISTORY_START': "[HISTORY]",
	'HISTORY_END': "[/HISTORY]"
}