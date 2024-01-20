### Constants
# Model Related
MODEL_PATH = "./model/llama-2-7b-chat.ggmlv3.q4_K_S.bin"
MODEL_TYPE = "llama"


# System and Logging
LOGGING_CONSTANTS = {
	'USER_START': "user: ",
	'AI_START': "ai: ",
	'SYSTEM_START': "<<SYS>>",
	'SYSTEM_END': "<</SYS>>",
	'START_TAG': "<s>",
	'END_TAG': "</s>",
	'LOG_FILE': "log.txt",
	'ENCODING': "utf-8",
	'INST_START': "[INST]",
	'INST_END': "[/INST]",
}

# Conversation
CONVERSATION_SETTINGS = {
	'SYSTEM_MSG': f"{LOGGING_CONSTANTS['START_TAG']}{LOGGING_CONSTANTS['INST_START']}{LOGGING_CONSTANTS['SYSTEM_START']}'ai' is helpfull and friendly assistant.{LOGGING_CONSTANTS['SYSTEM_END']}\nuser: connecting...{LOGGING_CONSTANTS['INST_END']}\nai: connected{LOGGING_CONSTANTS['END_TAG']}",
	'MAX_NEW_TOKENS': 8192,
	'STREAM': True,
	'HISTORY_LENGTH': 2048,
	'HISTORY_START': "[HISTORY]",
	'HISTORY_END': "[/HISTORY]"
}
