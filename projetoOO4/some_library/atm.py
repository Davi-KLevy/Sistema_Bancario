import json
import datetime


class BancoDeDados:
    """ Classe responsável por inicializar todos os bancos de dados """

    def __init__(self):
        """ Inicializando os bancos de dados """

        with open("Gerentes.json") as GeFile:
            self.gerentes = json.load(GeFile)
        with open("Clientes.json") as CliFile:
            self.clientes = json.load(CliFile)
        with open("Historico.json") as HistFile:
            self.historico = json.load(HistFile)
        with open("Pagamento_programado.json") as Pagfile:
            self.programado = json.load(Pagfile)
        with open("Atualizacoes.json") as Atufile:
            self.atualizacoes = json.load(Atufile)


class Usuario:
    """ Classe responsável por definir o usuário """
    
    def __init__(self, nome, endereco, telefone, senha, codigo, tipo):
        """ Inicializando os atributos do usuário """

        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.senha = senha
        self.codigo = codigo
        self.tipo = tipo


class Gerente(Usuario):
    """ Classe responsável pelas características de gerente herdando o usuário"""
    
    def __init__(self, nome, endereco, telefone, senha, codigo, tipo):
        """ Inicializando os atributos """

        super().__init__(nome, endereco, telefone, senha, codigo, tipo)
    
    def cadastrar_user(self, clientes, historico, programado, tipo, nome, endereco, telefone, senha, codigo, cpf_cnpj, saldo):
        """ Cadastramento do cliente pelo gerente e adicionado no banco de dados Clientes, Historico e Pagamento_programdo """
  
        novo_cliente = {"Tipo" : tipo,
                        "Nome" : nome,
                        "Endereco" : endereco,
                        "Telefone" : telefone,
                        "Senha" : senha,
                        "CPF/CNPJ" : cpf_cnpj,
                        "Saldo" : saldo,
                        "Credito" : 0.0,}
        clientes.update({codigo : novo_cliente})
        historico.update({codigo : {}})
        programado.update({codigo : {}})

        with open("Clientes.json", "w") as arquivo:
            json.dump(clientes, arquivo, indent=4)
        with open("Historico.json", "w") as arquivo:
            json.dump(historico, arquivo, indent=4)
        with open("Pagamento_programado.json", "w") as arquivo:
            json.dump(programado, arquivo, indent=4)
    
    def remover_user(self, clientes, codigo):
        """ Remossão do cliente pelo gerente e adicionado ao banco de dados Clientes """

        clientes.pop(codigo, "Cliente não existe")

        with open("Clientes.json", "w") as arquivo:
            json.dump(clientes, arquivo, indent=4)
    
    def editar_user(self, clientes, codigo, dado, novo_dado):
        """ Edição de usuários pelo cliente e adicionado ao banco de dados Clientes """

        clientes[codigo][dado] = novo_dado

        with open("Clientes.json", "w") as arquivo:
            json.dump(clientes, arquivo, indent=4)
        
    def visualiza_user(self, clientes):
        """ Visualização do cliente pelo gerente """

        for conta in clientes:
            print (f"[{conta}]\n\n")
            for item in clientes[conta]:
                print (f"{item}: {clientes[conta][item]}")
            print ("\n\n")


class Cliente(Usuario):
    """ Classe responsável pelo cliente herdando as características de usuário """

    def __init__(self, saldo, nome, endereco, telefone, senha, codigo, tipo):
        """ Inicializando a classe com as características de usuário mais o saldo """

        super().__init__(nome, endereco, telefone, senha, codigo, tipo)
        self.saldo = saldo

    def sacar(self, valor, clientes, codigo, saldo):
        """ Saque feito pelo cliente e adicioando ao banco de dados Clientes e registrado pela função registrar_transacao"""

        saldo -= valor
        clientes[codigo]["Saldo"] = saldo
        
        with open('Clientes.json', 'w') as clientes_file:
            json.dump(clientes, clientes_file, indent=4)
        
        self.registrar_transacao(valor, codigo, 'Saque', saldo)
    
    def depositar(self, valor, clientes, codigo, saldo):
        """ Deposito feito pelo cliente e adicionado ao banco de dados Clientes e registrado pela função registrar_transacao """

        clientes[codigo]['Saldo'] += valor
        saldo += valor
        
        with open('Clientes.json', 'w') as clientes_file:
            json.dump(clientes, clientes_file, indent=4)
        
        self.registrar_transacao(valor, codigo, 'Deposito', saldo)
        
    def pagamento_programado(self, programado, dic, codigo, num):
        """ Pagamento programdo pelo cliente e adicioando ao banco de dados Pagamento_programado """
    
        programado[codigo].update({num : dic})
        
        with open('Pagamento_programado.json', 'w') as pagfile:
            json.dump(programado, pagfile, indent=4)
    
    def visualizar_historico(self):
        """ Visualização do histórico pelo cliente """

        with open('Historico.json') as historico_file:
            historico_lista = json.load(historico_file)

        for item in historico_lista:
            for key, value in item.items():
                print(f'{key}:\t {value}')
            print('--------------------')

    def registrar_transacao(self, valor, codigo, tipo_transacao, saldo):
        """ Registro da transação e adicioando ao banco de dados Historico """

        data_hoje = datetime.datetime.now()
        data_hoje_str = data_hoje.strftime("%d/%m/%Y")
        data_agora_str = data_hoje.strftime("%I:%M:%S")

        with open('Historico.json') as historico_file:
            historico_dic = json.load(historico_file)

        transacao = {data_agora_str : {'Tipo' : tipo_transacao,
                                        'Valor' : valor,
                                        'Saldo final' : saldo}}
        
        transacao2 = {'Tipo' : tipo_transacao,
                    'Valor' : valor,
                    'Saldo final' : saldo}
        
        if (data_hoje_str in historico_dic[codigo]) == True:
            historico_dic[codigo][data_hoje_str].update({data_agora_str : transacao2})
        else:
            historico_dic[codigo].update({data_hoje_str : transacao})

        with open('Historico.json', 'w') as historico_update:
            json.dump(historico_dic, historico_update, indent=4)
        
    
class Empresa(Cliente):
    """ Classe responsável pelas características da empresa herdando o cliente """
    
    def __init__(self, saldo, nome, endereco, telefone, senha, cnpj, tipo, codigo):
        """ Inicializando as características da empresa """

        super().__init__(saldo, nome, endereco, telefone, senha, tipo, codigo)
        self.cnpj = cnpj

    def solicitar_credito(self, valor, clientes, codigo, credito, saldo):
        """ Soliciatação de crédito pela empresa e adicionado ao banco de dados Clientes e registando transação """

        credito += valor
        saldo += valor
        clientes[codigo]["Saldo"] = saldo
        clientes[codigo]["Credito"] = credito
        
        with open('Clientes.json', 'w') as clientes_file:
            json.dump(clientes, clientes_file, indent=4)
        
        self.registrar_transacao(valor, codigo, 'Credito', saldo)
    

class PessoaFisica(Cliente):
    """Classe responsável pela Pessoa física e herdando as características de cliente """

    def __init__(self, saldo, nome, endereco, telefone, senha, cpf, tipo, codigo):
        """ Inicializando as características de pessoa física """

        super().__init__(saldo, nome, endereco, telefone, senha, tipo, codigo)
        self.cpf = cpf

    def solicitar_credito(self, valor, clientes, codigo, credito, saldo):
        """ Solicitando crédito pela pessoa física e adicionando ao banco de dados Clientes e registrando transação """

        credito += valor
        saldo += valor
        clientes[codigo]["Saldo"] = saldo
        clientes[codigo]["Credito"] = credito

        with open('Clientes.json', 'w') as clientes_file:
            json.dump(clientes, clientes_file, indent=4)

        self.registrar_transacao(valor, codigo, 'Credito', saldo)
