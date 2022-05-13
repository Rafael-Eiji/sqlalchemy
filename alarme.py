from flask import Flask, request, Response
import requests
import json
import psycopg2
import psycopg2.extras
import datetime

app = Flask(__name__)

#---------------- Inicialização banco de dados ------------------------------
con = psycopg2.connect(
    database = "bd_owl_sensor_vigente",
    user = "postgres",
    password = "h3rcul3s",
    host = "192.168.21.82",
    port = "5432"
)



#----------------- Classe Alarme --------------------------------------------

class Alarme():
    def __init__(self, datainicial, datafinal):
        self.data_inicial = datainicial
        self.data_final =  datafinal

#----------------- Função que retorna a consulta -----------------------------

    def lista_periodo(self):
        cur = con.cursor()
        cur.execute("SELECT tipo_alarme.nome_alarme,\
        alarme_calculado.data_local_alarme, \
        alarme_calculado.hora_local_alarme, \
        alarme_calculado.status,\
        alarme_calculado.alarme_bruto\
        FROM alarme_calculado LEFT JOIN \
        tipo_alarme ON alarme_calculado.tipo_alarme = tipo_alarme.Id_tipo_alarme \
        WHERE data_local_alarme >= '{}' AND data_local_alarme <= '{}' \
        ORDER BY data_local_alarme, hora_local_alarme".format(self.data_inicial,self.data_final))

        retorno_sql = cur.fetchall()
        lista_empilha = []
        
        #converter lisa de tuplas para lista de lista

        ''' for converte_lista in retorno_sql:
            lista_empilha.append(list(converte_lista)) '''     

        lista_modelada = []

        #converte os valores de datetime para string
        for altera_lista in [list(x) for x in retorno_sql]:
            altera_lista[1] = altera_lista[1].strftime('%Y-%m-%d')
            altera_lista[2] = altera_lista[2].strftime('%H:%M:%S')

            #cria uma lista de dicionário
            dicionario = {
                'tipo_alarme' : altera_lista[0],
                'data': altera_lista[1],
                'hora': altera_lista[2],
                'alarme_bruto': altera_lista[4],
                'status': altera_lista[3]

            }
            lista_modelada.append(dicionario)
        
        cur.close()

        return lista_modelada


#-------------------- API -----------------------------------------

@app.route("/listaalarme")
def lista_alarme():
    args = request.args

    if "datainicial" in args:
        data_inicial = args["datainicial"]

    if "datafinal" in args:
        data_final = args["datafinal"]

    alarme = Alarme(data_inicial, data_final)
    retornojson = json.dumps(alarme.lista_periodo())

    
    return Response(retornojson, mimetype='application/json'), 200


#------------------ Inicialização da API ---------------------------

if __name__ == "__main__":
    app.run(debug=True)










