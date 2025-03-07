from flask import Flask
import requests
import time
import random

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Facebook Auto Comment Script Running!"

@app.route('/start')
def start_commenting():
    try:
        # 📂 Files Read करना
        with open("Token.txt", "r") as f:
            tokens = f.read().splitlines()

        with open("Comments.txt", "r") as f:
            comments = f.read().splitlines()

        with open("PostURL.txt", "r") as f:
            post_urls = f.read().splitlines()
        
        with open("Time.txt", "r") as f:
            interval = int(f.read().strip())  # ⏳ Time Interval Read करो

        # 🔄 Auto Commenting System
        for post_url in post_urls:
            try:
                post_id = post_url.split("posts/")[1].split("/")[0]
            except IndexError:
                return "❌ Invalid Post URL!"

            url = f"https://graph.facebook.com/{post_id}/comments"
            for token in tokens:
                for comment in comments:
                    emoji_comment = comment + " " + random.choice(["😂", "🤣", "😍", "🔥", "💯", "❤️"])
                    payload = {'message': emoji_comment, 'access_token': token}
                    response = requests.post(url, data=payload)

                    if response.status_code == 200:
                        print(f"✅ Commented: {emoji_comment}")
                    else:
                        print(f"❌ Failed for Token: {token}")

                    time.sleep(interval)  # ⏳ Time Interval from Time.txt
        
        return "✅ All Comments Posted!"
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
