from datetime import datetime, timezone
from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json
import paho.mqtt.client as mqtt

# ********************* CONEXÃO BANCO DE DADOS *********************************

app = Flask('registro')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configura o SQLAlchemy para rastrear modificações dos objetos, o que não é recomendado para produção.
# O SQLAlchemy cria e modifica todos os dados da nossa tabela de forma automatica 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Senai%40134@127.0.0.1/db_analise'
# Configura a URI de conexão com o banco de dados MySQL.
# Senha -> senai@134, porém aqui a senha passa a ser -> senai%40134
app.config['SQLALCHEMY_ECHO'] = True  # Habilita o log de SQLAlchemy

mybd = SQLAlchemy(app)
# Cria uma instância do SQLAlchemy, passando a aplicação Flask como parâmetro.

# ********************* CONEXÃO SENSORES *********************************

mqtt_data = {}

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))
    client.subscribe("projeto_integrado/SENAI134/Cienciadedados/grupo1")

def on_message(client, userdata, msg):
    global mqtt_data
    payload = msg.payload.decode('utf-8')
    mqtt_data = json.loads(payload)
    print(f"Received message: {mqtt_data}")

    # Adiciona o contexto da aplicação para a manipulação do banco de dados
    with app.app_context():
        try:
            temperatura = mqtt_data.get('temperature')
            pressao = mqtt_data.get('pressure')
            altitude = mqtt_data.get('altitude')
            umidade = mqtt_data.get('humidity')
            co2 = mqtt_data.get('CO2')
            timestamp_unix = mqtt_data.get('timestamp')
            centro_id = 1

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
            new_data = Registro(
                temperatura=temperatura,
                pressao=pressao,
                altitude=altitude,
                umidade=umidade,
                co2=co2,
                dia_hora=timestamp,
                centro_id=centro_id
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

# ********************************************************************************************************

# Cadastrar
@app.route('/data', methods=['POST'])
def post_data():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Nenhum dado fornecido"}), 400

        # Adiciona logs para depuração
        print(f"Dados recebidos: {data}")

        temperatura = data.get('temperatura')
        pressao = data.get('pressao')
        altitude = data.get('altitude')
        umidade = data.get('umidade')
        co2 = data.get('co2')
        timestamp_unix = data.get('dia_hora')
        centroid=data.get("centro_id")

        # Converte timestamp Unix para datetime
        try:
            timestamp = datetime.fromtimestamp(int(timestamp_unix), tz=timezone.utc)
        except ValueError as e:
            print(f"Erro no timestamp: {str(e)}")
            return jsonify({"error": "Timestamp inválido"}), 400

        # Cria o objeto Registro com os dados
        new_data = Registro(
            temperatura=temperatura,
            pressao=pressao,
            altitude=altitude,
            umidade=umidade,
            co2=co2,
            dia_hora=timestamp
        )

        # Adiciona o novo registro ao banco de dados
        mybd.session.add(new_data)
        print("Adicionando o novo registro")

        # Tenta confirmar a transação
        mybd.session.commit()
        print("Dados inseridos no banco de dados com sucesso")

        return jsonify({"message": "Data received successfully"}), 201

    except Exception as e:
        print(f"Erro ao processar a solicitação: {str(e)}")
        mybd.session.rollback()  # Reverte qualquer alteração em caso de erro
        return jsonify({"error": "Falha ao processar os dados"}), 500

# *************************************************************************************

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(mqtt_data)

class Registro(mybd.Model):
    __tablename__ = 'tb_leituras'
    id_leitura = mybd.Column(mybd.Integer, primary_key=True, autoincrement=True)
    temperatura = mybd.Column(mybd.Numeric(10, 2))
    pressao = mybd.Column(mybd.Numeric(10, 2))
    altitude = mybd.Column(mybd.Numeric(10, 2))
    umidade = mybd.Column(mybd.Numeric(10, 2))
    co2 = mybd.Column(mybd.Numeric(10, 2))
    dia_hora = mybd.Column(mybd.DateTime)

    def to_json(self):
        return {
            "id_leitura": self.id_leitura,
            "temperatura": float(self.temperatura),
            "pressao": float(self.pressao),
            "altitude": float(self.altitude),
            "umidade": float(self.umidade),
            "co2": float(self.co2),
            "dia_hora": self.dia_hora.strftime('%Y-%m-%d %H:%M:%S') if self.dia_hora else None
        }

# *************************************************************************************

@app.route("/registro", methods=["GET"])
def seleciona_registro():
    registro_objetos = Registro.query.all()
    registro_json = [registro.to_json() for registro in registro_objetos]
    return gera_response(200, "registro", registro_json)

@app.route("/registro/<id>", methods=["GET"])
def seleciona_registro_id(id):
    registro_objetos = Registro.query.filter_by(id=id).first()
    if registro_objetos:
        registro_json = registro_objetos.to_json()
        return gera_response(200, "registro", registro_json)
    else:
        return gera_response(404, "registro", {}, "Registro não encontrado")

# *************************************************************************************

@app.route("/registro/<id>", methods=["DELETE"])
def deleta_registro(id):
    registro_objetos = Registro.query.filter_by(id=id).first()
    if registro_objetos:
        try:
            mybd.session.delete(registro_objetos)
            mybd.session.commit()
            return gera_response(200, "registro", registro_objetos.to_json(), "Deletado com sucesso")
        except Exception as e:
            print('Erro', e)
            mybd.session.rollback()
            return gera_response(400, "registro", {}, "Erro ao deletar")
    else:
        return gera_response(404, "registro", {}, "Registro não encontrado")

def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo
    if mensagem:
        body["mensagem"] = mensagem
    return Response(json.dumps(body), status=status, mimetype="application/json")

if __name__ == '__main__':
    with app.app_context():
        mybd.create_all()  # Cria as tabelas no banco de dados
    
    start_mqtt()
    app.run(port=5000, host='localhost', debug=True)