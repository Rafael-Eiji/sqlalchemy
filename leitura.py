import pyrebase
from model import Read, Write, Senha, Status

#----------------Inicialização firebase------------------------------
firebaseConfig = {
  'apiKey': "AIzaSyBn0tVT9Rah7X-y-Juncvk8Cm7cSsS7DtI",
  'databaseURL': 'https://owl-control-light-73a4e-default-rtdb.firebaseio.com/',
  'authDomain': "owl-control-light-73a4e.firebaseapp.com",
  'projectId': "owl-control-light-73a4e",
  'storageBucket': "owl-control-light-73a4e.appspot.com",
  'messagingSenderId': "18934294278",
  'appId': "1:18934294278:web:7546871fd4a483acf12087"
};

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
#----------------------------------------------------------------------

#--------------------Adiciona o id novo nas outras tabelas-------------
def add_data(id):
    data_read = {"comando_front": 0,
            "running_fw": 0,
            "update_to": 0,
            "vibra_sensivity": 0}
    db.child('read').child(id).child('leitura').set(data_read)

    data_senha = {'senha_1' : ""}
    db.child('senha').child(id).set(data_senha)

    data_status = {'status': 0}
    db.child('status').child(id).set(data_status)
#-----------------------------------------------------------------

#--------------------Adiciona as informações do novo id no BD---------------------------
def add_data_bd(id, value):
    read = Read(id_firebase = id, comando_front = 0, running_fw = 0, update_to = 0, vibra_sensivity = 0)
    read.save()

    senha = Senha(id_firebase = id, senha_1 = "")
    senha.save()

    stat = Status(id_firebase = id, status = 0)
    stat.save()

    write = Write(id_firebase = id, value = value)
    write.save()

#-----------------------------------------------------------------------------------------

#ler as gravações do firebase
owl_read = db.child('read').get()
owl_write = db.child('write').get()

lista_read = []
lista_write = []

#lista os id do banco de 'write' e 'read'
for task in owl_read.each():
    lista_read.append(task.key())

for task in owl_write.each():
    lista_write.append({'id': task.key(), 'value' : task.val()['senha_1']['value']})

#verifica se tem uma nova gravação no 'write' e replicao id para as outras tabelas
for i in lista_write:
    if i['id'] not in lista_read:
        add_data(i['id'])
        add_data_bd(i['id'], i['value'])
        