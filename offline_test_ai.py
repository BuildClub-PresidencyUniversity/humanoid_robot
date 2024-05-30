from offline_ai import TextToResponseChatbot

def main():
    chatbot = TextToResponseChatbot()

    print("Enter 'exit' to stop the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting the chat. Goodbye!")
            break
        response = chatbot.get_response_from_text(user_input)
        print(f"AI: {response}")

if __name__ == "__main__":
    main()
