### Imports
from ctransformers import AutoModelForCausalLM
from datetime import datetime
from init import MODEL_PATH, MODEL_TYPE, LOGGING_CONSTANTS, CONVERSATION_SETTINGS


### Functions
def update_history(history, new_message, max_length=CONVERSATION_SETTINGS['HISTORY_LENGTH']):
	"""
	Updates the conversation history with a new message and keeps the length within max_length.
	Also, ensures SYSTEM_MSG is always at the beginning of the history.
	"""
	if not history or history[0] != CONVERSATION_SETTINGS["SYSTEM_MSG"]:
		history.insert(0, LOGGING_CONSTANTS['SYSTEM_MSG'])

	history.append(new_message)
	history = history[-(max_length+1):]

	write_to_log(new_message)
	return history

def write_to_log(message):
	"""
	Writes a message to the log file.
	"""
	try:
		with open(LOGGING_CONSTANTS['LOG_FILE'], 'a', encoding=LOGGING_CONSTANTS['ENCODING']) as file:
			file.write(message)
	except IOError as e:
		print(f"Error writing to log: {e}")

def system_timestamp():
	"""
	Returns the current timestamp in 'YYYY-MM-DD HH:MM:SS' format.
	"""
	return f"{LOGGING_CONSTANTS['START_TAG']}{LOGGING_CONSTANTS['SYSTEM_START']} <time='{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'/>{LOGGING_CONSTANTS['END_TAG']}\n"


### Initialize
llm_model 	= AutoModelForCausalLM.from_pretrained(MODEL_PATH, model_type=MODEL_TYPE)
history 	= [CONVERSATION_SETTINGS['SYSTEM_MSG']]
write_to_log(CONVERSATION_SETTINGS['SYSTEM_MSG'])


### Conversation Loop
while True:
	user_input = input(LOGGING_CONSTANTS['USER_START'])
	if user_input == "---exit":
		break
	elif user_input == "---history":
		# Print each item in the history list
		print(CONVERSATION_SETTINGS['HISTORY_START'])
		for item in history:
			print(item)

		print(CONVERSATION_SETTINGS["HISTORY_END"])
		continue  # Skip the rest of the loop and wait for next user input

	history = update_history(history, system_timestamp())

	formatted_input = f"{LOGGING_CONSTANTS['START_TAG']}{LOGGING_CONSTANTS['USER_START']} {user_input}{LOGGING_CONSTANTS['END_TAG']}\n"
	history = update_history(history, formatted_input)

	prompt = "".join(history) + LOGGING_CONSTANTS['START_TAG'] + LOGGING_CONSTANTS['AI_START']
	ai_response = LOGGING_CONSTANTS['AI_START']

    # Model interaction and response handling...
	for word in llm_model(prompt, stream=CONVERSATION_SETTINGS['STREAM'], max_new_tokens=CONVERSATION_SETTINGS['MAX_NEW_TOKENS']):
		ai_response += word
		if LOGGING_CONSTANTS['END_TAG'] in ai_response:
		# Trim the END_TAG from the response and break
			ai_response = ai_response.split(LOGGING_CONSTANTS['END_TAG'])[0]
			break

	# Check if AI response is valid
	if ai_response.strip() != LOGGING_CONSTANTS['AI_START']:
		print(ai_response)  # Print without the END_TAG
		formatted_response = f"{LOGGING_CONSTANTS['START_TAG']}{ai_response}{LOGGING_CONSTANTS['END_TAG']}\n"  # Add END_TAG only once for the log
		update_history(history, formatted_response)
	else:
		# Handle cases where AI response is empty or malformed
		print("Error: Invalid response from AI.")
