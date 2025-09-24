# pip install flask_sqlalchemy
# SQL_ALCHEMY
# PERMITE A CONEXAO DA API COM O BANCO DE DADOS

# FLASKY permite a criacao de api com python
# response e request-> requisição
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app= Flask('Caixa')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# configuraçao de conexao com o banco
# %40 -> faz o papel do @
# 1 - Usuario (root) 2 - Senha (senai%40134) 3 - localhost (127.0.0.1) 4- nome do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Senai%40134@127.0.0.1/db_analise'

mybd= SQLAlchemy(app)

# Classe para definir o modulo dos dados que correspondem a tabela do banco de dados
class Leitura(mybd.Model):
    __tablename__= 'tb_leituras'
    id_leitura = mybd.Column(mybd.Integer,primary_key=True)
    dia_hora = mybd.Column(mybd.String(100))
    poeira= mybd.Column(mybd.String(100))
    poeira_2= mybd.Column(mybd.String(100))
    co2= mybd.Column(mybd.String(100))
    umidade= mybd.Column(mybd.String(100))
    centro_id= mybd.Column(mybd.Integer,mybd.ForeignKey('tb_centros.centro_id'), nullable=False)

# Esse metodo to_json vai ser usado para converter o objeto com json
    def to_json(self):
        return {
            'id_leitura': self.id_leitura,
            'dia_hora': str(self.dia_hora),
            'poeira': float(self.poeira),
            'poeira_2': float(self.poeira),
            'co2':float(self.co2),
            'umidade':float(self.umidade),
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
@app.route('/letiura/<id_leitura_pam>', methods=['GET'])
def seleciona_leitura_id(id_leitura_pam):
    leitura_selecionada = Leitura.query.filter_by(id_leitura = id_leitura_pam).first()
    #select * from tb_carro where id_leitura = 3
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
            poeira = requisicao['poeira'],
            poeira_2 = requisicao['poeira_2'],
            co2 = requisicao['co2'],
            umidade = requisicao ['umidade'],
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

        if ('poeira' in requisicao):
            Leitura.poeira = requisicao['poeira']

        if ('poeira2' in requisicao):
            Leitura.poeira2 = requisicao['poeira2']

        if ('co2' in requisicao):
            Leitura.co2 = requisicao['co2']

        if ('umidade' in requisicao):
            Leitura.umidade = requisicao['umidade']

        if ('centro_id' in requisicao):
            Leitura.centro_id = requisicao['centro_id']

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



app.run(port=5000, host='localhost', debug=True)

