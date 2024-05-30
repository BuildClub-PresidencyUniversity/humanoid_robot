import requests
import json

def ask_question(question):
    url = "http://localhost:5000/chat"
    headers = {"Content-Type": "application/json"}
    payload = {"input_text": question}
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        data = response.json()
        # Concatenate the response chunks into a single paragraph
        concatenated_response = ' '.join(data.get('response', []))
        return {'response': concatenated_response}
    else:
        return {"error": "Failed to get response from the server"}

if __name__ == "__main__":
    question = "Do You know about lord Sri Krishna"
    response = ask_question(question)
    print(response)
