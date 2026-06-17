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
while True:
  temperatura = arduino.readline().decode().strip()
  if temperatura:
    registrar_temp(temperatura)