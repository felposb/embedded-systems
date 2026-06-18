import json
from datetime import datetime
import serial

ALUNOS = 'eren/alunos.json'
AULAS = 'eren/aulas.json'
CHAMADA = 'eren/chamada.json'
PROFESSORES = 'eren/professores.json'

def carregar(a):
    with open(a, 'r') as f:
        return json.load(f)

def salvar(a, d):
    with open(a, 'w') as f:
        json.dump(d, f, indent=4)
        
def proximo_id(lista):
    if not lista:
        return 1
    return max(item.get('id') for item in lista) + 1

def horario():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def buscar_aluno_uid(uid):
    alunos = carregar(ALUNOS)
    for aluno in alunos:
        mesmo_uid = aluno.get('uid') == uid
        if mesmo_uid:
            return aluno
    return None

def cadastrar_aluno(uid):
    alunos = carregar(ALUNOS)
    aluno = buscar_aluno_uid(uid)
    if aluno is None:
        nome = input("digite o nome do aluno para cadastrar: ")
        novo_aluno = {
            "id": proximo_id(alunos),
            "uid": uid,
            "nome": nome,
        }
        alunos.append(novo_aluno)
        salvar(ALUNOS, alunos)
        return "Cadastrado"
    return "Aluno ja esta cadastrado"

def buscar_professor_id(id):
    professores = carregar(PROFESSORES)
    for p in professores:
        mesmo_id = p.get("id") == id
        if mesmo_id:
            return p
    return None
def buscar_disciplinas_id(id):
    disciplinas = carregar(AULAS)
    for d in disciplinas:
        mesmo_id = d.get("id") == id
        if mesmo_id:
            return d
    return None
def cadastrar_chamada(uid, id_professor, id_disciplina):
    chamada = carregar(CHAMADA)
    aluno = buscar_aluno_uid(uid)
    disciplina = buscar_disciplinas_id(id_disciplina)
    professor = buscar_professor_id(id_professor)
    if aluno is None:
        return "Aluno nao cadastrado"
    if professor is None:
        return "Professor nao cadastrado"
    if disciplina is None:
        return "Disciplina nao cadastrado"
    for a in chamada:
        mesmo_uid = a.get("uid") == uid
        if mesmo_uid:
            return "Aluno ja esta na chamada"
    
    registro_chamada = {
        "uid": uid,
        "nome": aluno.get("nome"),
        "professor": professor.get("nome"),
        "disciplina": disciplina.get("nome"),
        "horario": horario()
    }
    chamada.append(registro_chamada)
    salvar(CHAMADA, chamada)
    return "Registrado"

PORTA = "COM3"
BAUD = 9600

arduino = serial.Serial(PORTA, BAUD)
print("lendo...")
while True:
    uid = arduino.readline().decode().strip()
    if uid:
        
        aluno = buscar_aluno_uid(uid)
        professor = buscar_professor_id(id)
        disciplinas = buscar_disciplinas_id(id)
        if aluno is None:
            resposta = cadastrar_aluno(uid)
            print(resposta)
        else:
            id_professor = int(input("Digite o ID do professor: "))
            id_disciplina = int(input("Digite o ID da disciplina/aula: "))
            resposta = cadastrar_chamada(uid, id_professor, id_disciplina)
            print(resposta)


        
    
