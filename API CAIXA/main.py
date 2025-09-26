# pip install flask_sqlalchemy
# SQL_ALCHEMY
# PERMITE A CONEXAO DA API COM O BANCO DE DADOS

# FLASKY permite a criacao de api com python
# response e request-> requisição
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import paho.mqtt.client as mqtt
from datetime import datetime, timezone
import json

app= Flask('Caixa')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# configuraçao de conexao com o banco
# %40 -> faz o papel do @
# 1 - Usuario (root) 2 - Senha (senai%40134) 3 - localhost (127.0.0.1) 4- nome do banco
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://grupo5:senai%40134@projetointegrador-grupo-5.mysql.database.azure.com/db_analise'



server_name ='projetointegrador-grupo-5.mysql.database.azure.com'
port = '3306'
username = 'grupo5'
password = 'senai%40134'
database = 'db_analise'

certificado = 'DigiCertGlobalRootG2.crt.pem'


uri = f"mysql://{username}:{password}@{server_name}:{port}/{database}"
ssl_certificate = f"?ssl_ca={certificado}"

app.config['SQLALCHEMY_DATABASE_URI'] = uri + ssl_certificate


mybd= SQLAlchemy(app)




# ********************* CONEXÃO SENSORES *********************************

mqtt_data = {}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("projeto_integrado/SENAI134/Cienciadedados/grupo1")

def on_message(client, userdata, msg):
    global mqtt_data
 # Decodifica a mensagem recebida de bytes para string
    payload = msg.payload.decode('utf-8')
   
    # Converte a string JSON em um dicionário Python
    mqtt_data = json.loads(payload)
   
    # Imprime a mensagem recebida
    print(f"Received message: {mqtt_data}")

    # Adiciona o contexto da aplicação para a manipulação do banco de dados
    with app.app_context():
        try:
            temperatura = mqtt_data.get('temperature')
            pressao = mqtt_data.get('pressure')
            altitude = mqtt_data.get('altitude')
            umidade = mqtt_data.get('humidity')
            poeira_1 = mqtt_data.get('particula1')
            poeira_2 = mqtt_data.get('particula2')
            co2 = mqtt_data.get('co2')
            timestamp_unix = mqtt_data.get('timestamp')

            if timestamp_unix is None:
                print("Timestamp não encontrado no payload")
                return

            # Converte timestamp Unix para datetime
            try:
                timestamp = datetime.fromtimestamp(int(timestamp_unix), tz=timezone.utc)
            except (ValueError, TypeError) as e:
                print(f"Erro ao converter timestamp: {str(e)}")
                return

            # Cria o objeto Registro com os dados
            new_data = Leitura(
                temperatura=temperatura,
                pressao=pressao,
                altitude=altitude,
                umidade=umidade,
                poeira_1=poeira_1,
                poeira_2=poeira_2,
                co2=co2,
                dia_hora=timestamp
            )

            # Adiciona o novo registro ao banco de dados
            mybd.session.add(new_data)
            mybd.session.commit()
            print("Dados inseridos no banco de dados com sucesso")

        except Exception as e:
            print(f"Erro ao processar os dados do MQTT: {str(e)}")
            mybd.session.rollback()

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("test.mosquitto.org", 1883, 60)

def start_mqtt():
    mqtt_client.loop_start()









# Classe para definir o modulo dos dados que correspondem a tabela do banco de dados
class Leitura(mybd.Model):
    __tablename__= 'tb_leituras'
    id_leitura = mybd.Column(mybd.Integer,primary_key=True)
    dia_hora = mybd.Column(mybd.String(100))
    temperatura = mybd.Column(mybd.String(100))
    poeira_1 = mybd.Column(mybd.String(100))
    poeira_2 = mybd.Column(mybd.String(100))
    co2 = mybd.Column(mybd.String(100))
    umidade = mybd.Column(mybd.String(100))
    pressao = mybd.Column(mybd.String(100))
    altitude =mybd.Column(mybd.String(100))
    centro_id= 1

# Esse metodo to_json vai ser usado para converter o objeto com json
    def to_json(self):
        return {
            'id_leitura': self.id_leitura,
            'dia_hora': str(self.dia_hora),
            'temperatura':str(self.temperatura),
            'poeira_1': float(self.poeira_1),
            'poeira_2': float(self.poeira_2),
            'co2':float(self.co2),
            'umidade':float(self.umidade),
            'pressao':float(self.pressao),
            'altitude':float(self.altitude),
            'centro_id': self.centro_id,
        }
    
#---------------------------------------------------
#METODO 1- GET
@app.route('/leitura',methods=['GET'])
def seleciona_caixa():
    leitura_selecionada = Leitura.query.all()
    # Executa uma consulta no banco de dados (SELECT * FROM tb_leituras)
    leitura_json= [leitura.to_json()
                 for leitura in leitura_selecionada]
    return gera_resposta(200, 'Lista de dados coletados', leitura_json)

#-----------------------------------------------------

# metodo 2- GET (POR ID)
@app.route('/leitura/<id_leitura_pam>', methods=['GET'])
def seleciona_leitura_id(id_leitura_pam):
    leitura_selecionada = Leitura.query.filter_by(id_leitura = id_leitura_pam).first()
    #select * from tb_leituras where id_leitura = 3
    leitura_json= leitura_selecionada.to_json()

    return gera_resposta(200,leitura_json, 'leitura encontrado')


#METODO 3 - POST
@app.route('/leitura',methods=['POST'])
def criar_leitura():
    requisicao = request.get_json()

    try:
        leitura = Leitura(
            id_leitura =requisicao['id_leitura'],
            dia_hora = requisicao['dia_hora'],
            temperatura = requisicao['temperatura'],
            poeira_1 = requisicao['poeira_1'],
            poeira_2 = requisicao['poeira_2'],
            co2 = requisicao['co2'],
            umidade = requisicao ['umidade'],
            pressao = requisicao ['pressao'],
            altitude = requisicao ['altitude'],
            centro_id = requisicao['centro_id']
        )


        mybd.session.add(leitura)
        # Adiciona ao banco
        mybd.session.commit()
        #salva

        return gera_resposta(201, leitura.to_json(), 'Incluido com sucesso')
    
    except Exception as e:
        print('Erro', e)

        return gera_resposta(400,{},'Erro ao cadastrar')


#METODO 4 - DELETE

@app.route('/leitura/<id_leitura_pam>',methods=['DELETE'])
def deleta_leitura(id_leitura_pam):
    Leitura = Leitura.query.filter_by(id_carro=id_leitura_pam).first()
    
    try:
        mybd.session.delete(Leitura)
        mybd.session.commit()
        return gera_resposta(200,Leitura.to_json(),'Deletado com sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {},'Erro ao deletar')
    


# metodo 5 - put
@app.route('/leitura/<id_leitura_pam>',methods=['PUT'])
def atualiza_leitura(id_leitura_pam):
    Leitura = Leitura.query.filter_by(id_leitura = id_leitura_pam).first()
    requisicao = request.get_json()

    try:
        if ('dia_hora' in requisicao):
            Leitura.dia_hora = requisicao['dia_hora']

        if ('temperatura' in requisicao):
            Leitura.temperatura = requisicao['temperatura']    

        #if ('poeira_1' in requisicao):
            Leitura.poeira_1 = requisicao['poeira_1']

        #if ('poeira_2' in requisicao):
            Leitura.poeira_2 = requisicao['poeira_2']

        if ('co2' in requisicao):
            Leitura.co2 = requisicao['co2']

        if ('umidade' in requisicao):
            Leitura.umidade = requisicao['umidade']


        if ('pressao' in requisicao):
            Leitura.pressao = requisicao['pressao']

        
        if ('altitude' in requisicao):
            Leitura.altitude = requisicao['altitude']

        mybd.session.add(Leitura)
        mybd.session.commit()

        return gera_resposta(200,Leitura.to_json(),'Registro de Leitura Atualizado com sucesso')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {},'Erro ao atualizar')

            





#RESPOSTA PADRÃO
    #status(200,201)
    # conteudo
    # mensagem(opicional)


def gera_resposta(status,conteudo,mensagem=False):
    body={}
    body['Resultado Leitura'] = conteudo
    if(mensagem):
        body['mensagem'] = mensagem

    return Response(json.dumps(body),status=status,mimetype='application/json')

# dumps converte o dicionario criado (body) em json (json.dumps)


start_mqtt()
app.run(port=5000, host='localhost', debug=True)

