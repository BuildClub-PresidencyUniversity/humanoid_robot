import requests
import json
from offline_ai import TextToResponseChatbot

def ask_question(question):
    url = "http://localhost:5000/chat"
    headers = {"Content-Type": "application/json"}
    payload = {"input_text": question}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            data = response.json()
            # Concatenate the response chunks into a single paragraph
            concatenated_response = ' '.join(data.get('response', []))
            return concatenated_response
    except requests.exceptions.ConnectionError:
        return "Sorry, can't connect to the internet. Please check your connection."
    return None

def main():
    chatbot = TextToResponseChatbot()

    print("Enter 'exit' to stop the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting the chat. Goodbye!")
            break

        # Try to get response from Gemini chatbot
        gemini_response = ask_question(user_input)
        if gemini_response is not None:
            if(gemini_response=="Sorry, can't connect to the internet. Please check your connection."):
                #print(f"Gemini: {gemini_response}")
                offline_response = chatbot.get_response_from_text(user_input)
                print(f"Offline Robot: {offline_response}")
                continue
            print(f"Gemini: {gemini_response}")
        else:
            # If Gemini fails, fallback to offline robot
            offline_response = chatbot.get_response_from_text(user_input)
            print(f"Offline Robot: {offline_response}")

if __name__ == "__main__":
    main()
