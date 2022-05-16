import requests, json
import os

def post_discord_webhook(text):
    main_content = {'content': text}
    headers = {'Content-Type': 'application/json'}
    requests.post(os.environ["DISCORD_WEBHOOK_URL"], json.dumps(main_content), headers=headers)