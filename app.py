from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Replace with your actual bot token
bot_token = "6140888607:AAElQv1wgxZVUh7VWNNNLw9Nh6Shid_hhcw"
offset = None

@app.route(f"/{bot_token}", methods=['POST'])
def webhook():
    global offset
    data = request.get_json()

    if "message" in data:
        user_id = data["message"]["chat"]["id"]
        message_text = data["message"]["text"]
        username = data["message"]["from"].get("username", "N/A")

        if message_text == "/start":
            url = f"http://iotapiserver.ap-south-1.elasticbeanstalk.com/api/add_user_id/{username}"
            payload = {
                "user_id": user_id
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.put(url, json=payload, headers=headers)
            print(response.text)

        elif message_text == "/checkstatus":
            url = f"http://iotapiserver.ap-south-1.elasticbeanstalk.com/api/user_data/{username}"
            headers = {'Content-Type': 'application/json'}
            data = requests.get(url, headers=headers).json()
            formatted_message = json.dumps(data, indent=5)

            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            payload = {
                'chat_id': user_id,
                'text': formatted_message,
            }
            response = requests.post(url, json=payload)

        elif message_text == "/turnonmachine":
            url = f"http://iotapiserver.ap-south-1.elasticbeanstalk.com/api/change_motor_status/{username}"
            payload = {"motor_status": 1}
            headers = {'Content-Type': 'application/json'}
            response = requests.put(url, json=payload, headers=headers)
            
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            payload = {
                'chat_id': user_id,
                'text': "Motor turned on",
            }
            response = requests.post(url, json=payload)

        elif message_text == "/turnoffmachine":
            url = f"http://iotapiserver.ap-south-1.elasticbeanstalk.com/api/change_motor_status/{username}"
            payload = {"motor_status": 0}
            headers = {'Content-Type': 'application/json'}
            response = requests.put(url, json=payload, headers=headers)
            
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            payload = {
                'chat_id': user_id,
                'text': "Motor turned off",
            }
            response = requests.post(url, json=payload)

        else:
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            payload = {
                'chat_id': user_id,
                'text': "Enter a valid command. Please check the menu for the set of commands.",
            }
            response = requests.post(url, json=payload)

        offset = data["update_id"] + 1

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=5000)
