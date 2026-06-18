import json
from datetime import datetime
import serial

TEMP = 'dados/temperatura.json'

PORT = "COM3"
BAUD = 9600

arduino = serial.Serial(PORT, BAUD)
def carregar(a):
  with open(a, 'r') as f:
    return json.load(f)
def salvar(a, d):
  with open(a, 'w') as f:
    return json.dump(d, f, indent=4)
def hora():
  return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
def registrar_temp(temperatura):
  temperaturas = carregar(TEMP)
  
  nova_temp = {
    'temperatura': temperatura,
    'horario': hora()
  }
  temperaturas.append(nova_temp)
  salvar(TEMP, temperaturas)
print("Começando...")
while True:
  leitura = arduino.readline().decode().strip()
  if leitura:
    try:
      temperatura = float(leitura)
      print(f"Temperatura recebida: {temperatura:.2f}" )
      registrar_temp(temperatura)
    except ValueError:
      print("Temperatura não recebe esse valor")
      