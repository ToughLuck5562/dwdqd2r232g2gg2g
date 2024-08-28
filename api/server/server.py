
from flask import Flask, render_template, request, jsonify
import base64 as O000OO00000OO0
from pymongo import MongoClient
import requests

app = Flask(__name__, template_folder='../client/templates', static_folder='../client/static')

URI = "mongodb+srv://admin1:vKq1jh7KBWdsttWM@cluster0.nswpj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(URI)
database = client["ChattingSite"]
collectionMessages = database["Messages"]

VERIFICATION_CODE = b'c2VjdXJlYml0bWVzc2FnaW5nbWV0aG9kWlc1amIyUmxaSEJoY25ReTA='

# WEBHOOKS = 

SITETRAFFICWEBHOOK = "https://discord.com/api/webhooks/1278105774257868916/sWng4vrXdrC0ZlfWXeUSEGpPZyu8c1epciPKe0ba9Y6GEI7oHCNXgpBxJUJ9znV-62qB"
LOGINFAILSWEBHOOK = "https://discord.com/api/webhooks/1278105923088420989/FQRfBm7JFPpN4D3HWoRp669WpL9yfNh_wZH2hq3ykAKV1Rn9P_n0ROqd-0DWNhbIeo4t"
MESSAGEWEBHOOK = "https://discord.com/api/webhooks/1278105963806855272/LUV1ih4StJznr0k1ndwyZyP1vt8T3KgZIncZ49W12UF1AvvSV_V6ro5uqsY7T0Jx9xUu"
LOGINWEBHOOK = "https://discord.com/api/webhooks/1278106012922023999/i52qhOMEAEge8SyKWhljde1GqOMDUYx8NZh9FyGm9ecB-BroikOYKtQzfGjazKtefS1a"

SITETRAFFICPAYLOAD = {
    'content': f'`New site request!`'
}
LOGINFAILSPAYLOAD = {
    'content': f'`Failed to login!'
}
LOGINPAYLOAD = {
    'content': f'`Someone logged in!`'
}
MESSAGEPAYLOAD = {
    'content': f'`Someone sent a message!`'
}
BLOCKEDPAYLOAD = {
    'content': f'`Someone has been blocked!`'
}

encryption_method = {
    "A": "m", "B": "x", "C": "r", "D": "p",
    "E": "s", "F": "v", "G": "w", "H": "q",
    "I": "f", "J": "n", "K": "d", "L": "c",
    "M": "j", "N": "t", "O": "y", "P": "k",
    "Q": "z", "R": "a", "S": "l", "T": "o",
    "U": "b", "V": "g", "W": "e", "X": "i",
    "Y": "h", "Z": "u", "1": "4", "2": "7",
    "3": "5", "4": "9", "5": "2", "6": "3",
    "7": "8", "8": "1", "9": "6", "=": "0",
    "0": "!", "'": "_", "!": "%",
    "a": "M", "b": "U", "c": "L", "d": "K",
    "e": "W", "f": "I", "g": "V", "h": "Y",
    "i": "X", "j": "M", "k": "P", "l": "S",
    "m": "A", "n": "J", "o": "T", "p": "D",
    "q": "H", "r": "C", "s": "E", "t": "N",
    "u": "Z", "v": "F", "w": "G", "x": "B",
    "y": "O", "z": "Q", "|": " "
}

def create_decryption_method(encryption_method):
    return {v: k for k, v in encryption_method.items()}

def decrypt(text:str, decryption_method):
    text = O000OO00000OO0.b64decode(text.encode()).decode()
    return ''.join(decryption_method.get(char, char) for char in text)

decryption_method = create_decryption_method(encryption_method)

def GetAllMessages():
    try:
        messages = collectionMessages.find({}, {'_id': 0})
        messagelist = list(messages)
        for message in messagelist:
            message['Username'] = decrypt(message.get('Username', ''), decryption_method)
            message['Message'] = decrypt(message.get('Message', ''), decryption_method)
        messagelist.reverse()
        return messagelist
    except Exception as e:
        print(f"An error occurred while fetching messages: {e}")
        return []

def ClearAllMessages():
    collectionMessages.delete_many({})
    
@app.route('/')
def fail():
    requests.post(url=SITETRAFFICWEBHOOK, data=SITETRAFFICPAYLOAD)
    return jsonify('This is an invalid page. Please try again later!')

@app.route('/Yml0', methods=['GET', 'POST'])
def main():
    requests.post(url=SITETRAFFICWEBHOOK, data=SITETRAFFICPAYLOAD)
    if request.method == 'POST':
        if request.form.get('code'):
            code = request.form['code']
            if code == O000OO00000OO0.b64decode(VERIFICATION_CODE).decode():
                requests.post(url=LOGINWEBHOOK, data=LOGINPAYLOAD)
                return render_template('Y2hhdG1ldGhvZA==.html', messages=GetAllMessages())
            else:
                requests.post(url=LOGINFAILSWEBHOOK, data=LOGINFAILSPAYLOAD)
                return jsonify(f'fail')
        if 'message' in request.form:
            requests.post(url=MESSAGEWEBHOOK, data=MESSAGEPAYLOAD)
            message = request.form[r'message']
            username = request.form[r'username']
            encodedusername = ''
            encodedmessage = ''
            for chracter in username:
                if chracter in encryption_method:
                    encodedusername = encodedusername + encryption_method[chracter]
                else:
                    encodedusername = encodedusername + chracter
            for chracter in message:
                if chracter in encryption_method:
                    encodedmessage = encodedmessage + encryption_method[chracter]
                else:
                    encodedmessage = encodedmessage + chracter       
            newdata = {
                'Username': O000OO00000OO0.b64encode(encodedusername.encode()).decode(),
                'Message': O000OO00000OO0.b64encode(encodedmessage.encode()).decode()
            }
            collectionMessages.insert_one(newdata)
            return render_template('Y2hhdG1ldGhvZA==.html', messages=GetAllMessages())
        if 'delete' in request.form:
            ClearAllMessages()
            return render_template('Y2hhdG1ldGhvZA==.html', messages=GetAllMessages())
        if 'refresh' in request.form:
            return render_template('Y2hhdG1ldGhvZA==.html', messages=GetAllMessages())
        else:
            requests.post(url=LOGINFAILSWEBHOOK, data=BLOCKEDPAYLOAD)
            return jsonify('You have been blocked from this request!')
    elif request.method == 'GET':
        return render_template('verification.html')
    else:
        requests.post(url=LOGINFAILSWEBHOOK, data=BLOCKEDPAYLOAD)
        return jsonify('You have been blocked from this request!')

if __name__ == "__main__":
    
    app.run()