import aiml
import presidencyRelatedAi as pai

class TextToResponseChatbot:
    def __init__(self, aiml_startup_file="std-startup.xml", aiml_load_command="LOAD AIML B"):
        """
        Initialize the AIML chatbot.

        Parameters:
        - aiml_startup_file (str): The AIML startup file to load.
        - aiml_load_command (str): The command to load AIML files.
        """
        print("""Hi! This is Sukarna Jana, the creator of this code.
It's an offline Mode which was trained long back.
Thank you!
================= Happy Chatting =================""")
        
        self.kernel = aiml.Kernel()
        self.kernel.learn(aiml_startup_file)
        self.kernel.respond(aiml_load_command)

    def update_expression_ai(self, new_expression):
        """
        Update the expression AI.

        Parameters:
        - new_expression (str): The new expression to update.
        """
        try:
            with open('expression.txt', 'w') as file:
                file.write(new_expression)
            #print("Expression updated successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_response_from_text(self, input_text):
        """
        Get response based on the input text.

        Parameters:
        - input_text (str): The input text.

        Returns:
        - str: The response from the chatbot.
        """
        # Get AI response from presidencyRelatedAi
        ai_response = pai.presiAnswer(input_text)
        if ai_response == "sorry":
            # Fall back to AIML chatbot if presidencyRelatedAi does not have a response
            ai_response = self.kernel.respond(input_text)
        
        # Update expression AI to indicate talking
        #self.update_expression_ai("talking")
        #print(f"AI: {ai_response}")
        # Update expression AI to indicate neutral
        #self.update_expression_ai("neutral")
        
        return ai_response
