import requests, json
import os

def send(text):
    main_content = {'content': text}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(os.environ["DISCORD_WEBHOOK_URL"], json.dumps(main_content), headers=headers)