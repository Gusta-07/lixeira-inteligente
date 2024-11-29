import RPi.GPIO as gpio
import time as delay
from app import app
from flask import render_template
from datetime import datetime
from urllib.request import urlopen
import requests


ledVermelho, ledVerde = 11, 12
statusVermelho =""
statusVerde =""
ocupacao = 0
pin_t = 15
pin_e = 16
lixeira_v = 20
lista_registro = []
urlBase = 'https://api.thingspeak.com/channels/'
readKey = '/last?key=17KK1O7FE9H0Q8NX'
channels = '2746093'
field1 = '/fields/1/'
field2 = '/fields/2/'
keyWrite = '3VI1TQIPX172RJ9I'
sensorDistancia = '&field1='


gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

gpio.setup(ledVermelho, gpio.OUT)
gpio.setup(ledVerde, gpio.OUT)

gpio.output(ledVermelho, gpio.LOW)
gpio.output(ledVerde, gpio.LOW)

#lixeira em baixo
gpio.setup(pin_t, gpio.OUT)
gpio.setup(pin_e, gpio.IN)

def abrir_tampa():
    i = 0
    while i <= 3:
        gpio.output(ledVerde, gpio.HIGH)
        delay.sleep(3)
        gpio.output(ledVerde, gpio.LOW)
        delay.sleep(3)
        i += 1

def fechar_tampa():
    i = 0
    while i <= 3:
        gpio.output(ledVermelho, gpio.HIGH)
        delay.sleep(3)
        gpio.output(ledVermelho, gpio.LOW)
        delay.sleep(3)
        i += 1

def status_lixeira():
    disponivel = True
    while True:
        if ocupacao < 100:
            gpio.output(ledVerde, gpio.HIGH)
            disponivel = True
        else:
            gpio.output(ledVermelho, gpio.HIGH)
            disponivel = False
        return disponivel

def resgitro_tampa():
    now = datetime.now()
    time = now.strftime("%d/%m/%Y %H:%M")
    lista_registro.append(time)
    return lista_registro

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

    ocupacao_l = (distancia/lixeira_v)*100
    ocupacao_f = 100-ocupacao_l

    ocupacao_lixeira = 0

    if ocupacao_f < 0:
        ocupacao_lixeira = 0
    elif ocupacao_f > 100:
        ocupacao_lixeira = 100
    else:
        ocupacao_lixeira = ocupacao_f
    
    return ocupacao_lixeira

def envia_dados():
    if testarConexao() == True:
        while True:
            urlDados = (urlBase + keyWrite + sensorDistancia + str(distancia()))
            retorno = requests.post(urlDados)

            if retorno.status_code == 200:
                print('Dados envidados com sucesso')
            else:
                print('Erro ao enviar dados: '+ retorno.status_code)

            delay.sleep(20)

    else:
        print('Sem conexão')
        
def consulta_dados():
    if testarConexao() == True:
        print('Conexão OK')

        while True:
            consultaDistancia = requests.get(urlBase + channels + field1 + readKey)

            print(consultaDistancia.text)
            delay.sleep(20)
    else:
        print('Sem conexão com a INTERNET')

def status_Led_vermelho():
    if gpio.input(ledVermelho) ==1:
        statusVermelho ="Led Vermelho ON"
    else: 
        statusVermelho ="Led Vermelho OFF"
    return statusVermelho

def status_Led_verde():
    if gpio.input(ledVerde) ==1:
        statusVerde ="Led Verde ON"
    else: 
        statusVerde ="Led Verde OFF"
    return statusVerde

def testarConexao():
    try:
        urlopen('https://www.materdei.edu.br/pt', timeout=1)
        return True
    except:
        return False
    
@app.route("/")
def index():
    templateData = {
        'ledred': status_Led_vermelho(),
        'ledverde':status_Led_verde(),
        'ocupacao_lixeira': distancia(),
        'registro_tampa': resgitro_tampa(),
        'status_lixeira': status_lixeira(),
        'abrir_tampa': abrir_tampa(),
        'fechar_tampa': fechar_tampa()
    }
    return render_template('index.html', **templateData)

@app.route("/led_vermelho/<action>")
def led_vermelho(action):
      if action =='on':
          gpio.output(ledVermelho, gpio.HIGH)
      if action =='off':
          gpio.output(ledVermelho, gpio.LOW)

      templateData = {
        'ledred': status_Led_vermelho(),
        'ledverde':status_Led_verde()
    } 
      return render_template('index.html', **templateData)


@app.route("/led_verde/<action>")
def led_verde(action):
      if action =='on':
          gpio.output(ledVerde, gpio.HIGH)
      if action =='off':
          gpio.output(ledVerde, gpio.LOW)

      templateData = {
        'ledred': status_Led_vermelho(),
        'ledverde':status_Led_verde()
    } 
      return render_template('index.html', **templateData)

@app.route('/abrir-tampa')
def index_abrir():
   abrir_tampa()
   templateData = {
        'registro_tampa': resgitro_tampa()
    }
   return render_template('index.html', **templateData)

@app.route('/fechar-tampa')
def index_fechar():
    fechar_tampa()
    templateData = {
        'registro_tampa': resgitro_tampa()
    }
    return render_template('index.html', **templateData)