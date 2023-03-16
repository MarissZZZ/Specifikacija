import base64 #Importē base64 moduli, lai pēc tam varētu izmantot bāzes 64 kodēšanu
import json #Importē json moduli, lai varētu apstrādāt JSON datu struktūras
from lib2to3.pgen2 import token #Importē token
from dotenv import load_dotenv #Importē load_dotenv funkciju no dotenv moduļa, lai varētu ielādēt .env failu
import os #Importē os, lai varētu piekļūt operētājsistēmas darbībām
from requests import post #Importē post funkciju no requests moduļa, lai varētu veikt POST pieprasījumus

load_dotenv() #Ielādē mainīgos no .env faila

client_id = os.getenv("CLIENT_ID") #Iegūstam "CLIENT_ID" no .env faila
client_secret = os.getenv("CLIENT_SECRET") #Iegūstam "CLIENT_SECRET" no .env faila

def get_token(): #Definējam funkciju "get_token"
    auth_string = client_id + ":" + client_secret #Apvienojam "client_id" un "client_secret" paroles un saglabājam tos mainīgajā "auth_string"
    auth_bytes = auth_string.encode("utf-8") #Pārvēršam "auth_string" par baitiem, izmantojot UTF-8 kodējumu, un saglabājam tos mainīgajā "auth_bytes"
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8") #Kodējam "auth_bytes" ar bāzes 64 kodu un saglabājam tos mainīgajā "auth_base64"

    url = "https://accounts.spotify.com/api/token" #Definējam URL, uz kuru veiksim POST pieprasījumu

    headers = { #Definējam HTTP galvenes
        "Authorization" : "Basic " + auth_base64, #autorizācijas galvene
        "Content_Type": "application/x-www-form-urlencoded" #Tiek iestatīts saturs
    }
    data = {"grant_type": "client_credentials"} #Definē pieprasījuma datus
    result = post(url, headers=headers, data=data) #POST pieprasījums un rezultāts saglabāts mainīgajā "result"
    json_result = json.loads(result.content) #Ielādē atbildi JSON formātā un saglabā to mainīgajā "json_result"
    token = json_result["access_token"] #Saglabā pieejas kodu mainīgajā "token"
    return token #Atgriež tokenu

token = get_token()
print(token) #izprintē tokenu