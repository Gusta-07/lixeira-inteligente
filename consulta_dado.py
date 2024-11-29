import time as delay
from urllib.request import urlopen
import requests

urlBase = 'https://api.thingspeak.com/channels/'
readKey = '/last?key=17KK1O7FE9H0Q8NX'
channels = '2746093'
field1 = '/fields/1/'
field2 = '/fields/2/'

def testeConexao():
    try:
        urlopen('https://unimater.edu.br/pt', timeout=1)
        return True
    except:
        return False
    
if testeConexao() == True:
    print('Conexão OK')

    while True:
        consultaDistancia = requests.get(urlBase + channels + field1 + readKey)

        print(consultaDistancia.text)
        delay.sleep(20)
else:
    print('Sem conexão com a INTERNET')
    