import ollama

def ask_ollama(prompt):
    response = ollama.chat(
        model="llama3",  # can also be mistral, gemma, etc.
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

# Example:
reply = ask_ollama("Hello, how are you?")
print("Jarvis:", reply)

# def aiProcess(command):
#     try:
#         response = ollama.chat(
#             model="llama3",
#             messages=[
#                 {"role": "system", "content": "You are a virtual assistant named Jarvis. Your role is to provide concise, direct, and conversational responses, like Alexa or Google Assistant. Keep your answers brief and to the point. "},
#                 {"role": "user", "content": "What is coding?"}
#             ]
#         )
#         return response['message']['content']
#     except Exception as e:
#         # A more helpful error message for the user.
#         return f"Error: Could not get a response from Ollama. Please check if Ollama is running and the model is pulled. Details: {str(e)}"
#     # --- Simple Test to Verify Ollama is Working ---
# if __name__ == "__main__":
#     test_command = "What is the capital of France?"
#     print(f"Testing aiProcess with command: '{test_command}'")
#     response = aiProcess(test_command)
#     print("Ollama response:", response)

#     # You can test with another command to be sure
#     test_command_2 = "What is the square root of 64?"
#     print(f"\nTesting aiProcess with command: '{test_command_2}'")
#     response_2 = aiProcess(test_command_2)
#     print("Ollama response:", response_2)

