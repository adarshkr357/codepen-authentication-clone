from pymongo import MongoClient
from requests import post
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import hashes
import base64

client = MongoClient("mongodb+srv://pranavkandpal05:OneaNTBR8XqnROSr@cluster0.wupcbdl.mongodb.net/Cluster0")
db= client.Codepen
collection = db.Users

def insert_user():
    login_data= {

        "username": "pranva",
        "email": "knakns",
        "password": "ds122",
        "last_log": "1/05/2024T1713094382"
    }

    result = collection.insert_one(login_data)
    print(f"inserted document ID {result.inserted_id}")

def search(query):


    results= collection.find_one(query)
    
    if results == None:
        return None
    
    return results


def check_captcha(captcha_response,ip):

    url= "https://www.google.com/recaptcha/api/siteverify"

    payload= {
        "secret": "6LfIn7opAAAAAHSbjXa8UqDAgw7Ezb1QvKssWDNZ",
        "response": captcha_response,
        "remoteip": ip
    }
    req = post(url,payload).json()

    if req.success:
        return True
    else:
        return False
    


def decryptWithPrivateKey(privateKeyPath, encryptedMessage):
    with open(privateKeyPath, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    original_message = private_key.decrypt(
        base64.b64decode(encryptedMessage),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return original_message.decode('utf-8')

print(decryptWithPrivateKey('./private_key.pem', '...')) 
