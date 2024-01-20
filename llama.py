### Imports
from ctransformers import AutoModelForCausalLM, AutoConfig

from datetime import datetime
from init import MODEL_PATH, MODEL_TYPE, LOGGING_CONSTANTS, CONVERSATION_SETTINGS


### Functions
def update_history(history, new_message, max_length=CONVERSATION_SETTINGS['HISTORY_LENGTH']):
    """
    Updates the conversation history with a new message. Removes the oldest messages 
    if the combined length of the history exceeds max_length.
    """
    history.append(new_message)  # Add the new message to history

    # Calculate the combined length of the messages in history
    combined_length = sum(len(message) for message in history)

    # Remove the oldest messages until the combined length is less than max_length
    while combined_length > max_length and history:
        removed_message = history.pop(0)  # Remove the oldest message
        combined_length -= len(removed_message)  # Update the combined length

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
	return f"{LOGGING_CONSTANTS['SYSTEM_START']}<timestamp='{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'/>{LOGGING_CONSTANTS['SYSTEM_END']}\n"


### Initialize
llm_model 	= AutoModelForCausalLM.from_pretrained(MODEL_PATH, model_type=MODEL_TYPE,  stream=CONVERSATION_SETTINGS['STREAM'], context_length=4096)
history 	= [CONVERSATION_SETTINGS['SYSTEM_MSG']]
write_to_log("[NEW-CONVERSATION/]\n")
write_to_log(CONVERSATION_SETTINGS['SYSTEM_MSG'])


### Conversation Loop
while True:
	user_input = input(LOGGING_CONSTANTS['USER_START'])
	user_input = user_input.strip()
	if user_input == "---exit":
		break
	elif user_input == "---history":
		# Print each item in the history list
		print(CONVERSATION_SETTINGS['HISTORY_START'])
		for item in history:
			print(item)

		print(CONVERSATION_SETTINGS["HISTORY_END"])
		continue  # Skip the rest of the loop and wait for next user input

	history = update_history(history, LOGGING_CONSTANTS['START_TAG'] + LOGGING_CONSTANTS['INST_START'] + system_timestamp())

	formatted_input = f"{LOGGING_CONSTANTS['USER_START']} {user_input}\n{LOGGING_CONSTANTS['INST_END']}\n"
	history = update_history(history, formatted_input)

	ai_response = LOGGING_CONSTANTS['AI_START']
	prompt = "".join(history) + ai_response

	# Model interaction and response handling...
	for word in llm_model(prompt):
		ai_response += word


	# remove tags incase AI likes to put them and also strip the string
	formatted_response = ai_response.replace(LOGGING_CONSTANTS['END_TAG'], '')
	formatted_response = formatted_response.strip() + LOGGING_CONSTANTS['END_TAG'] + "\n"

	# print and log
	print(formatted_response)  # Print without the END_TAG
	update_history(history, formatted_response)
