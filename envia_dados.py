import RPi.GPIO as gpio
import time as delay
from urllib.request import urlopen
import requests

gpio.setmode(gpio.BOARD)

ledVermelho, ledVerde = 11, 12
pin_e = 16
pin_t = 15

gpio.setup(ledVermelho, gpio.OUT)
gpio.setup(ledVerde, gpio.OUT)
gpio.setup(pin_t, gpio.OUT)
gpio.setup(pin_e, gpio.IN)

gpio.output(ledVermelho, False)
gpio.output(ledVerde, False)

urlBase = 'https://api.thingspeak.com/update?api_key='
keyWrite = '3VI1TQIPX172RJ9I'
sensorDistancia = '&field1='

def testaConexao():
    try:
        urlopen('https://www.materdei.edu.br/pt', timeout=1)
        return True
    except:
        return False

def distancia():
    gpio.output(pin_t, True)
    delay.sleep(0.000001)
    gpio.output(pin_t, False)
    tempo_i = delay.time()
    tempo_f = delay.time()
    while gpio.input(pin_e) == False:
        tempo_i = delay.time()
    while gpio.input(pin_e) == True:
        tempo_f = delay.time()
        temp_d = tempo_f - tempo_i
        distancia = (temp_d*34300) / 2
        
    return distancia


if testaConexao() == True:
    i = 0
    while i < 3:
        gpio.output(ledVerde, True)
        delay.sleep(0.2)
        gpio.output(ledVerde, False)
        delay.sleep(0.2)
        i = i + 1

    while True:
        urlDados = (urlBase + keyWrite + sensorDistancia + str(distancia()))
        retorno = requests.post(urlDados)

        if retorno.status_code == 200:
            print('Dados envidados com sucesso')
        else:
            print('Erro ao enviar dados: '+ retorno.status_code)

        delay.sleep(20)

else:
    i = 0
    while i < 3:
        gpio.output(ledVermelho, True)
        delay.sleep(0.2)
        gpio.output(ledVermelho, False)
        delay.sleep(0.2)
        i = i + 1