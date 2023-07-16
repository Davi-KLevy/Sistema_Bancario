import random
import string
from tkinter import *
from some_library.atm import *


# Criando um objeto para trazer a classe "Tk()" com suas funcionalidades 

root = Tk()


class Funcoes():
    """Classe para funções que interagem diretamente com a interface """    

    def limpa_tela(self, tela):
        """ Função para limpar a tela do nosso caixa eletronico """
        
        for widgets in tela.winfo_children():
            widgets.destroy()


    def gera_cod_random(self, tipo):
        """ Função que gera um código para tipo Pessoa e adiciona algumas partes para a interface """

        num = random.randint(1000, 9999)
        num2 = random.randint(10,99)
        if tipo == "Pessoa":
            self.cod_random = str(num) + ".0-" + str(num2)
        else:
            self.cod_random = str(num) + ".1-" + str(num2)

        self.l_codreal_cli = Label(self.tela_cadastra, text = self.cod_random,  foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_codreal_cli.place(relx=0.3, rely=0.7)

        self.botao_cadastra = Button(self.tela_cadastra, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Cadastrar", 
                                  font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : [self.user.cadastrar_user(self.bancoDados.clientes, self.bancoDados.historico, self.bancoDados.programado, self.tipo.get(), self.nome, self.endereco, self.telefone, self.senha_segura, self.cod_random, self.cpf_cnpj, float(self.saldo)), self.tela_usuario("")])
        self.botao_cadastra.place(relx=0.5, rely=0.93, relwidth=0.45, relheight=0.1, anchor=CENTER)

    def gera_sen_random(self):
        """ Função que gera um código aleatório para um novo usuário e adiciona algumas coisas à interface """

        carac = string.ascii_letters + string.digits + string.punctuation
        self.senha_segura = ""
        for i in range(8):
            self.senha_segura += random.choice(carac)

        self.l_senreal_cli = Label(self.tela_cadastra, text = self.senha_segura, foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_senreal_cli.place(relx=0.25, rely=0.25)


    def logar(self):
        """ Função para fazer a confirmação dos dados e permitir o programa avançar para a próxima tela """

        self.usuario = {}
        num1 = self.en_cod_part_1.get()
        num2 = self.en_cod_part_2.get()
        num3 = self.en_cod_part_3.get()
        self.cod = num1 + "." + num2 + "-" + num3
        self.senha = self.en_senha.get()

        if (self.cod in self.bancoDados.gerentes) == True:
            if (self.senha == self.bancoDados.gerentes[self.cod]["Senha"]) == True:
                nome = self.bancoDados.gerentes[self.cod]["Nome"]
                print(f"Login com Sucesso! Seja bem vindo {nome}")
                self.limpa_tela(self.frame1)
                self.usuario =  self.bancoDados.gerentes[self.cod]
                self.tela_usuario("")
            else:
                self.tela_usuario ("Falha no login! Senha incorreta!")
        elif (self.cod in self.bancoDados.clientes) == True:
            if (self.senha == self.bancoDados.clientes[self.cod]["Senha"]) == True:
                nome = self.bancoDados.clientes[self.cod]["Nome"]
                print(f"Login com Sucesso! Seja bem vindo {nome}")
                self.limpa_tela(self.frame1)
                self.usuario = self.bancoDados.clientes[self.cod]
                self.tela_usuario("")
            else:
                self.tela_usuario("Falha no login! Senha incorreta!")
        else: 
            self.tela_usuario("Falha no login! Conta inesxistente!")
        

    def select_edit(self):
        """ Função para alterar os dados dos clientes pelo gerente """
        
        selecao = self.lista_gerente.curselection()
        
        if selecao == ():
            self.mostra_aviso("AVISO: Você tem que selecionar o cliente\n para fazer a ação designada!")
        else:
            res = self.lista_gerente.get(selecao)
            self.tela_1_edita_cli(res)

    def select_del(self):
        """ Função para deletar os dados dos clientes pelo gerente """

        selecao = self.lista_gerente.curselection()

        if selecao == ():
            self.mostra_aviso("AVISO: Você tem que selecionar o cliente\n para fazer a ação designada!")
        else:
            res = self.lista_gerente.get(selecao)
            self.tela_remove_cli(res)
    
    def select_view(self):
        """ Função que mostra as propriedades do cliente selecioando pelo gerente """
        
        selecao = self.lista_gerente.curselection()
        
        if selecao == ():
            self.mostra_aviso("AVISO: Você tem que selecionar o cliente\n para fazer a ação designada!")
        else:
            res = self.lista_gerente.get(selecao)
            self.tela_visualiza_cli(res)
        
    def select_view_hist(self):
        """ Função que seleciona e visualiza o histórico de cliente pelo cliente """

        selecao = self.lista_cliente.curselection()
        
        if selecao == ():
            self.mostra_aviso("AVISO: Você tem que selecionar o histórico\n para fazer a ação designada!")
        else:
            self.tela_visualiza_hist()

    def verifica_se_pode_del(self, cod):
        """ Verifica se o saldo da conta está zerado para poder deletar """

        if self.bancoDados.clientes[cod]["Saldo"] == 0:
            self.user.remover_user(self.bancoDados.clientes, cod)
            self.tela_usuario("")
        else:
            self.tela_usuario("")
            self.mostra_aviso(f"ERROR! Usuário não pode deletar a conta {cod}\n enquanto ela não estiver ZERADA")

    def confere_pode_edit_cli(self, cod, dado, novo_dado):
        """ Função responsável por alterar os dados do cliente pelo gerente e impossibilita as alterações vazias """

        if novo_dado == "":
            self.limpa_tela(self.tela_edita)
            self.mostra_aviso("ERROR! Não pode enviar uma mudança vazia!")
        else: 
            self.user.editar_user(self.bancoDados.clientes, cod, dado, novo_dado)
            self.tela_usuario("")   

    def confere_pode_sacar(self, valor):
        """ Verifica se é possível de sacar dinheiro a partir do valor que é pedido """

        if ((self.usuario["Tipo"] == "Pessoa") and (self.bancoDados.clientes[self.cod]["Credito"] > 2000) or (self.usuario["Tipo"] == "Empresa") and (self.bancoDados.clientes[self.cod]["Credito"] > 50000)):    
            self.tela_usuario("")
            self.mostra_aviso("ERROR! Você não pode fazer essa ação até pagar\na sua dívida de cŕedito!")
        else:    
            if valor > self.usuario["Saldo"]:
                self.limpa_tela(self.tela_saca_din)
                self.mostra_aviso("ERRO! Você não pode sacar mais dinheiro do que\n você possui na conta!")
            else:
                self.user.sacar(valor, self.bancoDados.clientes, self.cod, self.usuario["Saldo"])
                self.tela_usuario("")

    def confere_pode_depo(self, valor):
        """ Verica se pode depositar dinheiro a partir do valor que é pedido """

        if valor <= 0:
            self.limpa_tela(self.tela_depo_din)
            self.mostra_aviso("ERRO! Você não pode depositar um valor nulo ou negativo!")
        else:
            self.user.depositar(valor, self.bancoDados.clientes, self.cod, self.usuario["Saldo"])
            self.tela_usuario("")
    
    def confere_pode_cred(self, valor):
        """ Verifica para empresa e pessoa física se pode solicitar crédito """

        if ((self.usuario["Tipo"] == "Pessoa") and (self.bancoDados.clientes[self.cod]["Credito"] > 2000) or (self.usuario["Tipo"] == "Empresa") and (self.bancoDados.clientes[self.cod]["Credito"] > 50000)):    
            self.tela_usuario("")
            self.mostra_aviso("ERROR! Você não pode fazer essa ação até pagar\na sua dívida de cŕedito!")
        else:    
            if self.usuario["Tipo"] == "Pessoa":
                if valor + self.bancoDados.clientes[self.cod]["Credito"] > 2000.0:
                    self.limpa_tela(self.tela_cred_din)
                    self.mostra_aviso("ERRO! Você não pode solicitar por um valor\nque supere o seu limite de R$2000.00!")
                else:
                    self.user.solicitar_credito(valor, self.bancoDados.clientes, self.cod, self.usuario["Credito"], self.usuario["Saldo"])
                    self.tela_usuario("")
            elif self.usuario["Tipo"] == "Empresa":
                if valor + self.bancoDados.clientes[self.cod]["Credito"] > 50000:
                    self.limpa_tela(self.tela_cred_din)
                    self.mostra_aviso("ERRO! Você não pode solicitar por um valor\nque supere o seu limite de R$50000.00!")
                else:
                    self.user.solicitar_credito(valor, self.bancoDados.clientes, self.cod, self.usuario["Credito"], self.usuario["Saldo"])
                    self.tela_usuario("")

    def confere_pode_pagar_cred(self):  
        """ Verifica se pode pagar crédito a partir do saldo existe na conta 
        e realiza a transação caso possa pagar crédito, alterando os valores
        no banco de dados de Clientes """

        if self.usuario["Credito"] > self.usuario["Saldo"]:
            self.limpa_tela(self.tela_visualiza)
            self.mostra_aviso("ERRO! Você não possui saldo suficiente para\n pagar a sua dívida!")
        else:
            valor = self.bancoDados.clientes[self.cod]["Credito"]
            self.bancoDados.clientes[self.cod]["Saldo"] -= self.bancoDados.clientes[self.cod]["Credito"]
            self.bancoDados.clientes[self.cod]["Credito"] = 0

            with open('Clientes.json', 'w') as clientes_file:
                json.dump(self.bancoDados.clientes, clientes_file, indent=4)

            self.user.registrar_transacao(valor, self.cod, "Pagar credito", self.bancoDados.clientes[self.cod]["Saldo"])
            self.limpa_tela(self.tela_visualiza)
            self.tela_dados_conta()

    def confere_pode_pagar_prog(self):
        """ Confere se pode realizar o pagamento programado """

        if self.usuario["Tipo"] == "Pessoa":
            limite = 2000 - self.bancoDados.clientes[self.cod]["Credito"]
        else:
            limite = 50000 - self.bancoDados.clientes[self.cod]["Credito"]

        if ((self.usuario["Tipo"] == "Pessoa") and (self.bancoDados.clientes[self.cod]["Credito"] > 2000) or (self.usuario["Tipo"] == "Empresa") and (self.bancoDados.clientes[self.cod]["Credito"] > 50000)):    
            self.tela_usuario("")
            self.mostra_aviso("ERROR! Você não pode fazer essa ação até pagar\na sua dívida de cŕedito!")
        else:    
            try:
                dia = int(self.en_data_real.get())
            except:
                return
            if (dia > 31) or (dia < 1):
                self.tela_usuario("")
                self.mostra_aviso("ERROR! Por favor, digite uma data existente\nEX: 12/5/2023")
            else:
                try:
                    mes = int(self.en_data_real2.get())
                except:
                    return
                if (mes > 12) or (mes < 1):
                    self.tela_usuario("")
                    self.mostra_aviso("ERROR! Por favor, digite uma data existente\nEX: 12/5/2023")
                else:
                    try:
                        ano = int(self.en_data_real3.get())
                    except:
                        return
                    try:
                        hora = int(self.en_hora_real.get())
                    except:
                        return
                    if (hora > 12) or (hora < 0):
                        self.tela_usuario("")
                        self.mostra_aviso("ERROR! Por favor, digite uma hora existente\nEX: 12:57:00 (Hora máxima = 12)")
                    else:
                        try:
                            min = int(self.en_hora_real2.get())
                        except:
                            return
                        if (min > 59) or (min < 0):
                            self.tela_usuario("")
                            self.mostra_aviso("ERROR! Por favor, digite uma hora existente\nEX: 12:57:00 (Hora máxima = 12)")
                        else:
                            try:
                                valor = float(self.en_valor_real.get())
        
                            except:
                                return
                            if (valor > limite) or (valor < 1):
                                self.tela_usuario("")
                                self.mostra_aviso("ERROR! O valor digitado não pode ultrapassar\no limite de crédito da conta")
                            else:
                                dic = {"Mes" : mes,
               "Dia" : dia,
               "Ano" : ano,
               "Hora" : hora,
               "Minuto" : min,
               "Valor" : valor,}
        
                                n = {}
                                for i in self.bancoDados.programado[self.cod]:
                                    n = i
                                if n == {}:
                                    num = 1
                                else:
                                    num = int(i) + 1

                                self.user.pagamento_programado(self.bancoDados.programado, dic, self.cod, num)
                                self.tela_usuario("")

    def atualiza_sistema(self):
        """ Atualiza o sistema de maneira geral """

        data_hoje = datetime.datetime.now()
        dia_atual = data_hoje.day
        mes_atual = data_hoje.month
        ano_atual = data_hoje.year
        hora_atual = data_hoje.hour
        minuto_atual = data_hoje.minute
        data_hoje_str = data_hoje.strftime("%d/%m/%Y")
        data_agora_str = data_hoje.strftime("%I:%M:%S")

        if dia_atual >= 5: 
            if mes_atual > self.bancoDados.atualizacoes["Mensal"]["Mes"]:
                tempo = mes_atual - self.bancoDados.atualizacoes["Mensal"]["Mes"]
                self.bancoDados.atualizacoes["Mensal"]["Dia"] = dia_atual
                self.bancoDados.atualizacoes["Mensal"]["Mes"] = mes_atual
                for codigo in self.bancoDados.clientes:
                    if self.bancoDados.clientes[codigo]["Tipo"] == "Pessoa":
                        self.bancoDados.clientes[codigo]["Credito"] = round(self.bancoDados.clientes[codigo]["Credito"] * (1.1**tempo), 2)
                    elif self.bancoDados.clientes[codigo]["Tipo"] == "Empresa":
                        self.bancoDados.clientes[codigo]["Credito"] = round(self.bancoDados.clientes[codigo]["Credito"] * (1.05**tempo), 2)
                with open('Clientes.json', 'w') as clifile:
                    json.dump(self.bancoDados.clientes, clifile, indent=4)

        if (minuto_atual > self.bancoDados.atualizacoes["Diaria"]["Minuto"]) or minuto_atual == 0:
            self.bancoDados.atualizacoes["Diaria"]["Minuto"] = minuto_atual
        if (mes_atual > self.bancoDados.atualizacoes["Diaria"]["Hora"]) or hora_atual == 0:
            self.bancoDados.atualizacoes["Diaria"]["Hora"] = hora_atual
        if (hora_atual > self.bancoDados.atualizacoes["Diaria"]["Dia"]) or dia_atual == 1:
            self.bancoDados.atualizacoes["Diaria"]["Dia"] = dia_atual
        if (mes_atual > self.bancoDados.atualizacoes["Diaria"]["Mes"]) or mes_atual == 1:
            self.bancoDados.atualizacoes["Diaria"]["Mes"] = mes_atual
        if (mes_atual > self.bancoDados.atualizacoes["Diaria"]["Ano"]) or ano_atual == 1:
            self.bancoDados.atualizacoes["Diaria"]["Ano"] = ano_atual
        
        with open('Atualizacoes.json', 'w') as atualiz_update:
            json.dump(self.bancoDados.atualizacoes, atualiz_update, indent=4)

        list = []
        
        for num in self.bancoDados.programado[self.cod]:
            if (ano_atual > self.bancoDados.programado[self.cod][num]["Ano"]):
                    valor = self.bancoDados.programado[self.cod][num]["Valor"]
                    if self.bancoDados.clientes[self.cod]["Saldo"] >= valor:
                        self.bancoDados.clientes[self.cod]["Saldo"] -= valor
                    else:
                        self.bancoDados.clientes[self.cod]["Credito"] += valor
                    list.append(num)
            elif (mes_atual > self.bancoDados.programado[self.cod][num]["Mes"]) or mes_atual == 1:
                if (ano_atual >= self.bancoDados.programado[self.cod][num]["Ano"]):
                    valor = self.bancoDados.programado[self.cod][num]["Valor"]
                    if self.bancoDados.clientes[self.cod]["Saldo"] >= valor:
                        self.bancoDados.clientes[self.cod]["Saldo"] -= valor
                    else:
                        self.bancoDados.clientes[self.cod]["Credito"] += valor
                    list.append(num)
            elif (dia_atual > self.bancoDados.programado[self.cod][num]["Dia"]) or dia_atual == 1:
                if (mes_atual >= self.bancoDados.programado[self.cod][num]["Mes"]) or mes_atual == 1:
                    if (ano_atual >= self.bancoDados.programado[self.cod][num]["Ano"]):
                        valor = self.bancoDados.programado[self.cod][num]["Valor"]
                        if self.bancoDados.clientes[self.cod]["Saldo"] >= valor:
                            self.bancoDados.clientes[self.cod]["Saldo"] -= valor
                        else:
                            self.bancoDados.clientes[self.cod]["Credito"] += valor
                        list.append(num)
            elif (hora_atual > self.bancoDados.programado[self.cod][num]["Hora"]) or hora_atual == 0:
                if (dia_atual >= self.bancoDados.programado[self.cod][num]["Dia"]) or dia_atual == 1:
                    if (mes_atual >= self.bancoDados.programado[self.cod][num]["Mes"]) or mes_atual == 1:
                        if (ano_atual >= self.bancoDados.programado[self.cod][num]["Ano"]):
                            valor = self.bancoDados.programado[self.cod][num]["Valor"]
                            if self.bancoDados.clientes[self.cod]["Saldo"] >= valor:
                                self.bancoDados.clientes[self.cod]["Saldo"] -= valor
                            else:
                                self.bancoDados.clientes[self.cod]["Credito"] += valor
                            list.append(num)
            elif (minuto_atual >= self.bancoDados.programado[self.cod][num]["Minuto"]) or minuto_atual == 0:
                if (hora_atual >= self.bancoDados.programado[self.cod][num]["Hora"]) or hora_atual == 0:
                    if (dia_atual >= self.bancoDados.programado[self.cod][num]["Dia"]) or dia_atual == 1:
                        if (mes_atual >= self.bancoDados.programado[self.cod][num]["Mes"]) or mes_atual == 1:
                            if (ano_atual >= self.bancoDados.programado[self.cod][num]["Ano"]):
                                valor = self.bancoDados.programado[self.cod][num]["Valor"]
                                if self.bancoDados.clientes[self.cod]["Saldo"] >= valor:
                                    self.bancoDados.clientes[self.cod]["Saldo"] -= valor
                                else:
                                    self.bancoDados.clientes[self.cod]["Credito"] += valor
                                list.append(num)              

            for num in list:
                self.bancoDados.programado[self.cod].pop(num)
                with open('Pagamento_programado.json', 'w') as pagfile:
                    json.dump(self.bancoDados.programado, pagfile, indent=4)
                with open("Clientes.json", "w") as arquivo:
                    json.dump(self.bancoDados.clientes, arquivo, indent=4)
                self.cliente.registrar_transacao(valor, self.cod, "Pagamento Programado", self.bancoDados.clientes[self.cod]["Saldo"])

    def mostra_aviso(self, aviso):
        """ Função responsável por avisos na interface """

        self.tela_aviso_select = Frame(self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.tela_aviso_select.place(relx= 0.5, rely= 0.5, relwidth= 0.8, relheight= 0.4, anchor=CENTER)

        self.botao_x = Button(self.tela_aviso_select, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="X", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_usuario(""))
        self.botao_x.place(relx=0.95, rely=0.15, relwidth=0.1, relheight=0.3, anchor=CENTER)

        self.l_aviso = Label(self.tela_aviso_select, text = aviso, foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_aviso.place(relx=0.5, rely=0.5, anchor=CENTER)    


class SistemaBancario(Funcoes):
    """ Sistema bancário responsável por intermediar as alterações do banco de dados """

    def __init__(self, master=None):
        """ Inicializando os bancos de dados e outras características"""

        self.bancoDados = BancoDeDados()
        self.hist = {}
        self.usuario = {}
        self.cod = ""
        self.senha = ""
        self.cliente = Cliente(0, "a", "b", "c", "d", "e", "f")

# Definindo estilo, tamanho e tipo de fonte padrão pra interface (não necessariamente tudo vai ser assim)
        self.tela_fonte = ("Terminal", "16", "bold")
        self.tela_fontinha = ("Terminal", "12", "bold")

# Construindo a interface inicial
        self.root = root
        self.interface_basica()

        self.frame1 = Frame(self.root, bd = 4, bg="#1C1C1C", highlightbackground= "#4D4D4D", highlightthickness=6)
        self.frame1.place(relx= 0.03, rely= 0.03, relwidth= 0.94, relheight= 0.50)

        self.tela_inicial()
        self.criando_botoes()
        root.mainloop()

    def interface_basica(self):
        """ Função para construir a interface principal do caixa eletrônico """

        self.root.title("Caixa Bancário")
        self.root.configure(background="#5E5D5D") 
        self.root.geometry("700x700")
        self.root.resizable(False, False)

    def criando_botoes(self):
        """ Função para criar todos os botões de nosso Caixa Eletrônico principal """

        self.botao1 = Button(self.root, bg="#9D9B9B", highlightbackground="#4D4D4D", highlightthickness=3, text="1", 
                             font=self.tela_fonte,  activebackground="#4D4D4D")
        self.botao1.place(relx= 0.03, rely= 0.55, relwidth= 0.22, relheight= 0.09)

        self.botao2 = Button(self.root, bg="#9D9B9B", highlightbackground="#4D4D4D", highlightthickness=3, text="2", 
                             font=self.tela_fonte,  activebackground="#4D4D4D")
        self.botao2.place(relx= 0.27, rely= 0.55, relwidth= 0.22, relheight= 0.09) 

        self.botao3 = Button(self.root, bg="#9D9B9B", highlightbackground="#4D4D4D", highlightthickness=3, text="3", 
                             font=self.tela_fonte,  activebackground="#4D4D4D")
        self.botao3.place(relx= 0.51, rely= 0.55, relwidth= 0.22, relheight= 0.09)

        self.botao4 = Button(self.root, bg="#9D9B9B", highlightbackground="#4D4D4D", highlightthickness=3, text="4", 
                             font=self.tela_fonte,  activebackground="#4D4D4D")
        self.botao4.place(relx= 0.03, rely= 0.66, relwidth= 0.22, relheight= 0.09)

        self.botao5 = Button(self.root, bg="#9D9B9B", highlightbackground="#4D4D4D", highlightthickness=3, text="5", 
                             font=self.tela_fonte,  activebackground="#4D4D4D")
        self.botao5.place(relx= 0.27, rely= 0.66, relwidth= 0.22, relheight= 0.09) 

        self.botao6 = Button(self.root, bg="#9D9B9B", highlightbackground="#4D4D4D", highlightthickness=3, text="6", 
                             font=self.tela_fonte,  activebackground="#4D4D4D")
        self.botao6.place(relx= 0.51, rely= 0.66, relwidth= 0.22, relheight= 0.09) 

        self.botao7 = Button(self.root, bg="#9D9B9B", highlightbackground="#4D4D4D", highlightthickness=3, text="7", 
                             font=self.tela_fonte,  activebackground="#4D4D4D")
        self.botao7.place(relx= 0.03, rely= 0.77, relwidth= 0.22, relheight= 0.09)

        self.botao8 = Button(self.root, bg="#9D9B9B", highlightbackground="#4D4D4D", highlightthickness=3, text="8", 
                             font=self.tela_fonte,  activebackground="#4D4D4D")
        self.botao8.place(relx= 0.27, rely= 0.77, relwidth= 0.22, relheight= 0.09) 

        self.botao9 = Button(self.root, bg="#9D9B9B", highlightbackground="#4D4D4D", highlightthickness=3, text="9", 
                             font=self.tela_fonte,  activebackground="#4D4D4D")
        self.botao9.place(relx= 0.51, rely= 0.77, relwidth= 0.22, relheight= 0.09) 

        self.botao_cancela = Button(self.root, bg="#E9441B", highlightbackground="#C10D01", highlightthickness=3, text="Cancela", 
                                    font=self.tela_fonte,  activebackground="#C10D01")
        self.botao_cancela.place(relx= 0.75, rely= 0.55, relwidth= 0.22, relheight= 0.09)

        self.botao_ponto = Button(self.root, bg="#9D9B9B", highlightbackground="#4D4D4D", highlightthickness=3, text=".", 
                                    font=self.tela_fonte,  activebackground="#C10D01")
        self.botao_ponto.place(relx= 0.03, rely= 0.88, relwidth= 0.22, relheight= 0.09)

        self.botao0 = Button(self.root, bg="#9D9B9B", highlightbackground="#4D4D4D", highlightthickness=3, text="0", 
                             font=self.tela_fonte,  activebackground="#4D4D4D")
        self.botao0.place(relx= 0.27, rely= 0.88, relwidth= 0.22, relheight= 0.09) 

        self.botaodelete = Button(self.root, bg="#9D9B9B", highlightbackground="#4D4D4D", highlightthickness=3, text="", 
                             font=self.tela_fonte,  activebackground="#4D4D4D")
        self.botaodelete.place(relx= 0.51, rely= 0.88, relwidth= 0.22, relheight= 0.09) 

        self.botao_confirma = Button(self.root, bg="#28A80F", highlightbackground="#20850D", highlightthickness=3, text="Confirma", 
                                     font=self.tela_fonte,  activebackground="#20850D")
        self.botao_confirma.place(relx= 0.75, rely= 0.77, relwidth= 0.22, relheight= 0.09) 

        self.botao_cancela = Button(self.root, bg="#cfc217", highlightbackground="#cfd217", highlightthickness=3, text="Cancela", 
                                     font=self.tela_fonte,  activebackground="#eac217")
        self.botao_cancela.place(relx= 0.75, rely= 0.66, relwidth= 0.22, relheight= 0.09)

        self.botaoseta = Button(self.root, bg="#9D9B9B", highlightbackground="#4D4D4D", highlightthickness=3, text="->", 
                             font=self.tela_fonte,  activebackground="#4D4D4D")
        self.botaoseta.place(relx= 0.75, rely= 0.88, relwidth= 0.22, relheight= 0.09) 


    def faz_titulo(self, titulo):
        """ Faz o título do caixa eletrôncio """

        self.fr_titulo_pag = Frame(self.frame1, bg="#50C649", highlightbackground= "#50C649", highlightthickness=1.5)
        self.fr_titulo_pag.place(relx= 0.5, rely= 0.04, relwidth= 0.20, relheight= 0.1, anchor=CENTER)
        self.login = Label(self.fr_titulo_pag, text = titulo, foreground="#1C1C1C", background="#50C649", font=self.tela_fonte)
        self.login.place(relx=0.5, rely=0.5, anchor=CENTER)

    def faz_cabecalho(self):
        """ Faz o cabeçalho do caixa eletrônico """

        self.bt_log_out = Button(self.frame1, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Log Out", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_inicial())
        self.bt_log_out.place(relx=0.90, rely=0.04, relwidth=0.20, relheight=0.1, anchor=CENTER)

        self.bt_log_out = Button(self.frame1, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="", 
                                  font=self.tela_fonte, activebackground="#50C649", activeforeground="#50C649")
        self.bt_log_out.place(relx=0.70, rely=0.04, relwidth=0.20, relheight=0.1, anchor=CENTER)

        self.bt_log_out = Button(self.frame1, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="", 
                                  font=self.tela_fonte, activebackground="#50C649", activeforeground="#50C649")
        self.bt_log_out.place(relx=0.30, rely=0.04, relwidth=0.20, relheight=0.1, anchor=CENTER)

        self.bt_log_out = Button(self.frame1, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", 
                                  font=self.tela_fontinha, activebackground="#50C649", activeforeground="#50C649")
        self.bt_log_out.place(relx=0.10, rely=0.04, relwidth=0.20, relheight=0.1, anchor=CENTER)

    def tela_inicial(self):
        """ Função constroi a tela inicial de quando ligamos o prgrama """

        self.limpa_tela(self.frame1)

        self.faz_titulo("MENU")

        self.botao_login = Button(self.frame1, bg="#1C1C1C", highlightbackground="#50C649", highlightthickness=1.5, foreground="#50C649", text="Login", 
                                  font=self.tela_fonte, activebackground="#50C649", activeforeground="#1C1C1C", command=lambda : self.tela_login(""))
        self.botao_login.place(relx=0.5, rely=0.42, relwidth=0.4, relheight=0.1, anchor=CENTER)

        self.botao_sair = Button(self.frame1, bg="#1C1C1C", highlightbackground="#50C649", highlightthickness=1.5, foreground="#50C649", text="Sair", 
                                 font=self.tela_fonte, activebackground="#50C649", activeforeground="#1C1C1C", command=self.root.quit)
        self.botao_sair.place(relx=0.5, rely=0.54, relwidth=0.4, relheight=0.1, anchor=CENTER)

    def tela_login(self, aviso):
        """ Função para construção da página de login """

        self.limpa_tela(self.frame1)
        self.faz_titulo("LOGIN")

        self.t_aviso = Label(self.frame1, text = aviso, foreground="#50C649", background="#1C1C1C", font=("Terminal", "10", "bold"))
        self.t_aviso.place(relx=0.5, rely=0.30, anchor=CENTER)
        
        self.t_conta = Label(self.frame1, text = "Conta:", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.t_conta.place(relx=0.12, rely=0.42, anchor=CENTER)
        self.en_cod_part_1 = Entry(self.frame1, background="#50C649", highlightbackground="#1C1C1C", font=self.tela_fonte)
        self.en_cod_part_1.place(relx=0.275, rely=0.42, relwidth=0.15, relheight=0.1, anchor=CENTER)
        self.t_ponto = Label(self.frame1, text = ".", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.t_ponto.place(relx=0.365, rely=0.44, anchor=CENTER)
        self.en_cod_part_2 = Entry(self.frame1, background="#50C649", highlightbackground="#1C1C1C", font=self.tela_fonte)
        self.en_cod_part_2.place(relx=0.4, rely=0.42, relwidth=0.04, relheight=0.1, anchor=CENTER)
        self.t_traco = Label(self.frame1, text = "-", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.t_traco.place(relx=0.435, rely=0.42, anchor=CENTER)
        self.en_cod_part_3 = Entry(self.frame1, background="#50C649", highlightbackground="#1C1C1C", font=self.tela_fonte)
        self.en_cod_part_3.place(relx=0.485, rely=0.42, relwidth=0.07, relheight=0.1, anchor=CENTER)
        self.t_senha = Label(self.frame1, text = "Senha:", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.t_senha.place(relx=0.12, rely=0.56, anchor=CENTER)
        self.en_senha = Entry(self.frame1, background="#50C649", highlightbackground="#1C1C1C", show="*", font=self.tela_fonte)
        self.en_senha.place(relx=0.55, rely=0.56, relwidth=0.7, relheight=0.1, anchor=CENTER)

        self.bt_logar = Button(self.frame1, bg="#1C1C1C", highlightbackground="#50C649", highlightthickness=1.5, foreground="#50C649", text="Logar", 
                                  font=self.tela_fonte, activebackground="#50C649", activeforeground="#1C1C1C", command=lambda : self.logar())
        self.bt_logar.place(relx=0.5, rely=0.7, relwidth=0.4, relheight=0.1, anchor=CENTER)

        self.bt_voltar = Button(self.frame1, bg="#1C1C1C", highlightbackground="#50C649", highlightthickness=1.5, foreground="#50C649", text="Voltar", 
                                  font= ("Terminal", "12", "bold"), activebackground="#50C649", activeforeground="#1C1C1C", command=lambda : self.tela_inicial())
        self.bt_voltar.place(relx=0.88, rely=0.90, relwidth=0.11, relheight=0.09)
 
# estão coerentes e gerar a pagina correspondente para o devido tipo de usuário ("Gerente" ou "Cliente")
    def tela_usuario(self, aviso):
        """ Função para construção da tela de usuário e confirmação dos dados """

        self.limpa_tela(self.frame1)
        try:
            self.atualiza_sistema()
        except:
            pass
        self.faz_cabecalho()
        self.frames_menu_de_usuário()

        if self.usuario == {}:
            self.tela_login(aviso)
        
        elif ("Saldo" in self.usuario) == True:
            if self.usuario["Tipo"] == "Empresa":
                self.user = Empresa(self.usuario["Saldo"], self.usuario["Nome"], self.usuario["Endereco"], self.usuario["Telefone"], self.usuario["Senha"], self.usuario["CPF/CNPJ"], self.usuario["Tipo"], self.cod)
                self.mostra_dados_cliente()
                self.mostra_lista_cliente()
                self.mostra_funcoes_cliente()
            else:
                self.user = PessoaFisica(self.usuario["Saldo"], self.usuario["Nome"], self.usuario["Endereco"], self.usuario["Telefone"], self.usuario["Senha"], self.usuario["CPF/CNPJ"], self.usuario["Tipo"], self.cod)
                self.mostra_dados_cliente()
                self.mostra_lista_cliente()
                self.mostra_funcoes_cliente()
            self.faz_titulo("CLIENTE") 

        elif self.usuario["Tipo"] == "Gerente":
                self.user = Gerente(self.usuario["Nome"], self.usuario["Endereco"], self.usuario["Telefone"], self.usuario["Senha"], "000100", self.usuario["Tipo"])   
                self.mostra_dados_gerente()
                self.mostra_lista_gerente()
                self.mostra_funcoes_gerente()
                self.faz_titulo("GERENTE")

    def frames_menu_de_usuário(self):
        """ Função para padronizar frames do menu de usuários """

        self.fr_info_conta = Frame (self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.fr_info_conta.place(relx= 0.01, rely= 0.12, relwidth= 0.71, relheight= 0.36)

        self.fr_acoes = Frame (self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.fr_acoes.place(relx= 0.01, rely= 0.5, relwidth= 0.71, relheight= 0.5)

        self.fr_lista = Frame (self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.fr_lista.place(relx= 0.73, rely= 0.12, relwidth= 0.27, relheight= 0.88)

    def mostra_dados_gerente(self):
        """ Interface da página gerentes """

        self.l_admin = Label(self.fr_info_conta, text = "ADMINISTRADOR", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_admin.place(relx=0.02, rely=0.01)
        
        self.l_nome_gerente = Label(self.fr_info_conta, text = self.usuario["Nome"], foreground="#50C649", background="#1C1C1C", font=("Terminal", "12", "bold"))
        self.l_nome_gerente.place(relx=0.02, rely=0.4)

        self.l_codigo_conta = Label(self.fr_info_conta, text = self.cod, foreground="#50C649", background="#1C1C1C", font=("Terminal", "12", "bold"))
        self.l_codigo_conta.place(relx=0.02, rely=0.7)
    
    def mostra_lista_gerente(self):
        """ Mostra a lista de gerentes buscando a informação no banco de dados pelo gerente """

        self.l_cliente_lista = Label(self.fr_lista, text = "Clientes", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_cliente_lista.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        self.scrollbar_lista = Scrollbar(self.fr_lista, bg="#1C1C1C", troughcolor="#50C649", activebackground="#000000")
        self.scrollbar_lista.place(relx=0.9, rely=0.2, relwidth=0.1, relheight=0.8)

        self.lista_gerente = Listbox(self.fr_lista, bg="#1C1C1C", foreground="#50C649", highlightbackground="#50C649",
                                     selectbackground="#50C649", selectforeground="#1C1C1C", font=("Terminal", "10", "bold"), yscrollcommand= self.scrollbar_lista.set)
        for cod in self.bancoDados.clientes:
            self.lista_gerente.insert(END, cod)
        self.lista_gerente.place(relx=0.0, rely= 0.2, relwidth=0.9, relheight=0.8)
        self.scrollbar_lista.config(command= self.lista_gerente.yview)
        
    def mostra_funcoes_gerente(self):
        """ Mostra as funções do gerente pelo gerente """

        self.bt_cadastra = Button(self.fr_acoes, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Cadastrar novo cliente", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_1_cadastra_cli())
        self.bt_cadastra.place(relx=0, rely=0, relwidth=1, relheight=0.25)

        self.bt_remover = Button(self.fr_acoes, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Remover cliente", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.select_del())
        self.bt_remover.place(relx=0, rely=0.25, relwidth=1, relheight=0.25)

        self.bt_editar = Button(self.fr_acoes, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Editar conta", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.select_edit())
        self.bt_editar.place(relx=0, rely=0.5, relwidth=1, relheight=0.25)

        self.bt_visualiza = Button(self.fr_acoes, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Visualizar conta", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.select_view())
        self.bt_visualiza.place(relx=0, rely=0.75, relwidth=1, relheight=0.25)


    def tela_1_cadastra_cli(self):
        """ Tela responsável pelo cadastro do cliente pelo gerente """

        self.tela_cadastra = Frame(self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.tela_cadastra.place(relx= 0.5, rely= 0.5, relwidth= 0.5, relheight= 0.9, anchor=CENTER)

        self.l_cadastro_cli = Label(self.tela_cadastra, text = "CADASTRO", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_cadastro_cli.place(relx=0.5, rely=0.08, anchor=CENTER)
        
        self.botao_x = Button(self.tela_cadastra, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="X", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_usuario(""))
        self.botao_x.place(relx=0.95, rely=0.05, relwidth=0.1, relheight=0.1, anchor=CENTER)

        self.l_nome_cli = Label(self.tela_cadastra, text = "Nome: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_nome_cli.place(relx=0.03, rely=0.15)
        self.en_nomereal_cli = Entry(self.tela_cadastra, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_nomereal_cli.place(relx=0.23, rely=0.15, relwidth=0.75)

        self.l_end_cli = Label(self.tela_cadastra, text = "End.:", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_end_cli.place(relx=0.03, rely=0.3)
        self.en_endreal_cli = Entry(self.tela_cadastra, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_endreal_cli.place(relx=0.23, rely=0.3, relwidth=0.75)

        self.l_tel_cli = Label(self.tela_cadastra, text = "Tel.:", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_tel_cli.place(relx=0.03, rely=0.45)
        self.en_telreal_cli = Entry(self.tela_cadastra, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_telreal_cli.place(relx=0.23, rely=0.45, relwidth=0.75)

        self.l_cpf_cli = Label(self.tela_cadastra, text = "CPF/CNPJ: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_cpf_cli.place(relx=0.03, rely=0.60)
        self.en_cpfreal_cli = Entry(self.tela_cadastra, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_cpfreal_cli.place(relx=0.35, rely=0.60, relwidth=0.63)

        self.l_sal_cli = Label(self.tela_cadastra, text = "Saldo: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_sal_cli.place(relx=0.03, rely=0.75)
        self.en_salreal_cli = Entry(self.tela_cadastra, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_salreal_cli.place(relx=0.25, rely=0.75, relwidth=0.73)

        self.botao_continua = Button(self.tela_cadastra, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Continuar", 
                                  font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_2_cadastra_cliente())
        self.botao_continua.place(relx=0.5, rely=0.93, relwidth=0.45, relheight=0.1, anchor=CENTER)

    def tela_2_cadastra_cliente(self):
        """ Segunda tela responsável pelo cadastro do cliente pelo gerente """

        self.nome = self.en_nomereal_cli.get()
        if self.nome == "":
            return
        else:
            self.endereco = self.en_endreal_cli.get()
            if self.endereco == "":
                return
            else:
                self.telefone = self.en_telreal_cli.get()
                if self.telefone == "":
                    return
                else:
                    self.cpf_cnpj = self.en_cpfreal_cli.get()
                    if self.cpf_cnpj == "":
                        return
                    else:
                        self.saldo = self.en_salreal_cli.get()
                        try:
                            self.saldo = float(self.saldo)
                        except:
                            return
                        if self.saldo < 0:
                            return
                        else:
                            self.limpa_tela(self.tela_cadastra)

                            self.l_cadastro_cli = Label(self.tela_cadastra, text = "CADASTRO", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
                            self.l_cadastro_cli.place(relx=0.5, rely=0.08, anchor=CENTER)
                            
                            self.botao_x = Button(self.tela_cadastra, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="X", 
                                                    font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_usuario(""))
                            self.botao_x.place(relx=0.95, rely=0.05, relwidth=0.1, relheight=0.1, anchor=CENTER)

                            self.l_sen_cli = Label(self.tela_cadastra, text = "Senha:", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
                            self.l_sen_cli.place(relx=0.03, rely=0.25)

                            self.gera_sen_random()
                                                
                            self.l_tip_cli = Label(self.tela_cadastra, text = "Tipo:", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
                            self.l_tip_cli.place(relx=0.03, rely=0.4)
                            self.tipo = StringVar()
                            self.rb_pessoa = Radiobutton(self.tela_cadastra, text="Pessoa Física", variable= self.tipo, value="Pessoa", command=lambda : self.gera_cod_random(self.tipo.get()), 
                                                        bg="#1C1C1C", foreground="#50C649", highlightcolor="#1C1C1C", highlightbackground="#50C649", activebackground="#1C1C1C", activeforeground="#50C649", selectcolor="#1c1c1c", font=self.tela_fontinha)
                            self.rb_pessoa.place (relx=0.3, rely=0.4)
                            self.rb_empresa = Radiobutton(self.tela_cadastra, text="Empresa", variable= self.tipo, value="Empresa", command=lambda : self.gera_cod_random(self.tipo.get()), 
                                                        bg="#1C1C1C", foreground="#50C649", highlightcolor="#1C1C1C", highlightbackground="#50C649", activebackground="#1C1C1C", activeforeground="#50C649", selectcolor="#1c1c1c", font=self.tela_fontinha)
                            self.rb_empresa.place (relx=0.3, rely=0.55)

        self.l_cod_cli = Label(self.tela_cadastra, text = "Cód. : ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_cod_cli.place(relx=0.03, rely=0.7)

        self.botao_volta = Button(self.tela_cadastra, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Voltar", 
                                font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_1_cadastra_cli())
        self.botao_volta.place(relx=0.5, rely=0.93, relwidth=0.45, relheight=0.1, anchor=CENTER)

    def tela_remove_cli(self, cod):
        """ Tela responsável pela remossão de um certo usuário pelo gerente """

        self.tela_deleta = Frame(self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.tela_deleta.place(relx= 0.5, rely= 0.5, relwidth= 0.6, relheight= 0.8, anchor=CENTER)

        self.l_confirma_del = Label(self.tela_deleta, text = "Você tem certeza que quer deletar\n essa conta?", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_confirma_del.place(relx=0.5, rely=0.1, anchor=CENTER)
    
        self.l_nome_cli = Label(self.tela_deleta, text = "Nome :", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_nome_cli.place(relx=0.03, rely=0.25)
        self.l_nomereal_cli = Label(self.tela_deleta, text = self.bancoDados.clientes[cod]["Nome"], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_nomereal_cli.place(relx=0.25, rely=0.25)

        self.l_cod_cli = Label(self.tela_deleta, text = "Cód. :", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_cod_cli.place(relx=0.03, rely=0.4)
        self.l_codreal_cli = Label(self.tela_deleta, text = cod, foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_codreal_cli.place(relx=0.25, rely=0.40)

        self.l_sal_cli = Label(self.tela_deleta, text = "Saldo:", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_sal_cli.place(relx=0.03, rely=0.55)
        self.l_salreal_cli = Label(self.tela_deleta, text = "R$" + str(self.bancoDados.clientes[cod]["Saldo"]), foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_salreal_cli.place(relx=0.25, rely=0.55)
        
        self.botao_cancela = Button(self.tela_deleta, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Cancelar", 
                                  font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_usuario(""))
        self.botao_cancela.place(relx=0.3, rely=0.85, relwidth=0.3, relheight=0.1, anchor=CENTER)

        self.botao_confirma = Button(self.tela_deleta, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Confirmar", 
                                  font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.verifica_se_pode_del(cod))
        self.botao_confirma.place(relx=0.7, rely=0.85, relwidth=0.3, relheight=0.1, anchor=CENTER)
        
    def tela_1_edita_cli(self, cod = ""):
        """ Tela responsável pela edição dos dadso do cliente pelo gerente """
        
        self.tela_edita = Frame(self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.tela_edita.place(relx= 0.5, rely= 0.5, relwidth= 0.5, relheight= 0.8, anchor=CENTER)

        self.l_edicao_cli = Label(self.tela_edita, text = "EDIÇÃO", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_edicao_cli.place(relx=0.5, rely=0.08, anchor=CENTER)

        self.botao_x = Button(self.tela_edita, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="X", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_usuario(""))
        self.botao_x.place(relx=0.95, rely=0.05, relwidth=0.1, relheight=0.1, anchor=CENTER)

        self.l_nome_cli = Label(self.tela_edita, text = "Nome :", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_nome_cli.place(relx=0.03, rely=0.17)
        self.l_nomereal_cli = Label(self.tela_edita, text = self.bancoDados.clientes[cod]["Nome"], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_nomereal_cli.place(relx=0.27, rely=0.17)
        self.bt_edita_nome = Button(self.tela_edita, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Editar", 
                                  font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_2_edita_cli("Nome", cod))
        self.bt_edita_nome.place(relx=0.5, rely=0.32, relwidth=0.3, relheight=0.09, anchor=CENTER)

        self.l_end_cli = Label(self.tela_edita, text = "End. :", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_end_cli.place(relx=0.03, rely=0.37)
        self.l_endreal_cli = Label(self.tela_edita, text = self.bancoDados.clientes[cod]["Endereco"], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_endreal_cli.place(relx=0.27, rely=0.37)
        self.bt_edita_end = Button(self.tela_edita, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Editar", 
                                  font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_2_edita_cli("Endereco", cod))
        self.bt_edita_end.place(relx=0.5, rely=0.52, relwidth=0.3, relheight=0.09, anchor=CENTER)

        self.l_tel_cli = Label(self.tela_edita, text = "Tel. :", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_tel_cli.place(relx=0.03, rely=0.57)
        self.l_telreal_cli = Label(self.tela_edita, text = self.bancoDados.clientes[cod]["Telefone"], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_telreal_cli.place(relx=0.27, rely=0.57)
        self.bt_edita_tel = Button(self.tela_edita, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Editar", 
                                  font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_2_edita_cli("Telefone", cod))
        self.bt_edita_tel.place(relx=0.5, rely=0.72, relwidth=0.3, relheight=0.09, anchor=CENTER)

        self.l_sen_cli = Label(self.tela_edita, text = "Senha:", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_sen_cli.place(relx=0.03, rely=0.77)
        self.l_senreal_cli = Label(self.tela_edita, text = self.bancoDados.clientes[cod]["Senha"], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_senreal_cli.place(relx=0.27, rely=0.77)
        self.bt_edita_sen = Button(self.tela_edita, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Editar", 
                                  font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_2_edita_cli("Senha", cod))
        self.bt_edita_sen.place(relx=0.5, rely=0.92, relwidth=0.3, relheight=0.09, anchor=CENTER)
    
    def tela_2_edita_cli(self, escolha, cod):
        """ Segunda tela responsável pela edição dos dados do cliente pelo gerente """

        self.tela_edita = Frame(self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.tela_edita.place(relx= 0.5, rely= 0.5, relwidth= 0.5, relheight= 0.8, anchor=CENTER)

        self.l_edicao_cli = Label(self.tela_edita, text = "EDIÇÃO", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_edicao_cli.place(relx=0.5, rely=0.08, anchor=CENTER)

        self.botao_x = Button(self.tela_edita, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="X", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_usuario(""))
        self.botao_x.place(relx=0.95, rely=0.05, relwidth=0.1, relheight=0.1, anchor=CENTER)

        self.l_escolha_cli = Label(self.tela_edita, text = escolha + ":", foreground="#50C649", background="#1C1C1C", font=("Terminal", "13", "bold"))
        self.l_escolha_cli.place(relx=0.03, rely=0.19)
        self.l_escolhareal_cli = Label(self.tela_edita, text = self.bancoDados.clientes[cod][escolha], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_escolhareal_cli.place(relx=0.5, rely=0.35, anchor=CENTER)

        self.l_nova_esc_cli = Label(self.tela_edita, text = "Novo " + escolha + ":", foreground="#50C649", background="#1C1C1C", font=("Terminal", "13", "bold"))
        self.l_nova_esc_cli.place(relx=0.03, rely=0.46)
        self.en_nova_esc_cli = Entry(self.tela_edita, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_nova_esc_cli.place(relx=0.125, rely=0.60, relwidth=0.75)

        self.bt_confirmar = Button(self.tela_edita, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Confirmar", 
                                  font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.confere_pode_edit_cli(cod, escolha, self.en_nova_esc_cli.get()))
        self.bt_confirmar.place(relx=0.5, rely=0.9, relwidth=0.45, relheight=0.15, anchor=CENTER)

    def tela_visualiza_cli(self, cod = ""):
        """ Tela responsável por visualizar os dados do cliente selecioando pelo gerente """

        self.tela_visualiza = Frame(self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.tela_visualiza.place(relx= 0.5, rely= 0.5, relwidth= 0.5, relheight= 0.8, anchor=CENTER)

        self.botao_x = Button(self.tela_visualiza, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="X", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_usuario(""))
        self.botao_x.place(relx=0.95, rely=0.05, relwidth=0.1, relheight=0.1, anchor=CENTER)

        self.l_nome_cli = Label(self.tela_visualiza, text = "Nome: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_nome_cli.place(relx=0.03, rely=0.05)
        self.l_nomereal_cli = Label(self.tela_visualiza, text = self.bancoDados.clientes[cod]["Nome"], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_nomereal_cli.place(relx=0.23, rely=0.05)

        self.l_end_cli = Label(self.tela_visualiza, text = "End: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_end_cli.place(relx=0.03, rely=0.17)
        self.l_endreal_cli = Label(self.tela_visualiza, text = self.bancoDados.clientes[cod]["Endereco"], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_endreal_cli.place(relx=0.23, rely=0.17)

        self.l_tel_cli = Label(self.tela_visualiza, text = "Tel: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_tel_cli.place(relx=0.03, rely=0.29)
        self.l_telreal_cli = Label(self.tela_visualiza, text = self.bancoDados.clientes[cod]["Telefone"], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_telreal_cli.place(relx=0.23, rely=0.29)

        self.l_cpf_cli = Label(self.tela_visualiza, text = "CPF: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_cpf_cli.place(relx=0.03, rely=0.41)
        self.l_cpfreal_cli = Label(self.tela_visualiza, text = self.bancoDados.clientes[cod]["CPF/CNPJ"], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_cpfreal_cli.place(relx=0.23, rely=0.41)

        self.l_sal_cli = Label(self.tela_visualiza, text = "Saldo: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_sal_cli.place(relx=0.03, rely=0.53)
        self.l_salreal_cli = Label(self.tela_visualiza, text = "R$ " + str(self.bancoDados.clientes[cod]["Saldo"]), foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_salreal_cli.place(relx=0.03, rely=0.70)

    def mostra_dados_cliente(self):
        """ Inicio da interface da classe clientes """

        self.l_nome_cliente = Label(self.fr_info_conta, text = self.usuario["Nome"], foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_nome_cliente.place(relx=0.02, rely=0.01)
        
        self.l_id_cliente = Label(self.fr_info_conta, text = self.usuario["Endereco"], foreground="#50C649", background="#1C1C1C", font=("Terminal", "12", "bold"))
        self.l_id_cliente.place(relx=0.02, rely=0.4)

        self.l_codigo_conta = Label(self.fr_info_conta, text = self.cod, foreground="#50C649", background="#1C1C1C", font=("Terminal", "12", "bold"))
        self.l_codigo_conta.place(relx=0.02, rely=0.7)

        self.l_saldo_conta = Label(self.fr_info_conta, text = "Saldo:", foreground="#50C649", background="#1C1C1C", font=("Terminal", "12", "bold"))
        self.l_saldo_conta.place(relx=0.4, rely=0.7)

        self.l_saldoreal_conta = Label(self.fr_info_conta, text = "R$ " + str(self.usuario["Saldo"]), foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_saldoreal_conta.place(relx=0.55, rely=0.65)

        self.botao_ver_conta = Button(self.fr_info_conta, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Conta", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_dados_conta())
        self.botao_ver_conta.place(relx=0.9, rely=0.15, relwidth=0.2, relheight=0.3, anchor=CENTER)
    
    def mostra_lista_cliente(self):
        """ Mostra a lista de clientes para os clientes além de outras funcionalidades """

        self.l_hist_lista = Label(self.fr_lista, text = "Histórico", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_hist_lista.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        self.scrollbar_lista = Scrollbar(self.fr_lista, bg="#1C1C1C", troughcolor="#50C649", activebackground="#000000")
        self.scrollbar_lista.place(relx=0.9, rely=0.2, relwidth=0.1, relheight=0.8)

        self.lista_cliente = Listbox(self.fr_lista, bg="#1C1C1C", foreground="#50C649", highlightbackground="#50C649",
                                     selectbackground="#50C649", selectforeground="#1C1C1C", font=("Terminal", "8", "bold"), yscrollcommand= self.scrollbar_lista.set)
        
        with open("Historico.json") as HistFile:
            self.bancoDados.historico = json.load(HistFile)

        self.tempos = []
        
        for self.dia in self.bancoDados.historico[self.cod]:
            for self.seg in self.bancoDados.historico[self.cod][self.dia]:
                self.lista_cliente.insert(0, self.dia + " R$" + str(self.bancoDados.historico[self.cod][self.dia][self.seg]["Valor"]))
                self.tempos.insert(0,[self.dia, self.seg])
                if (self.bancoDados.historico[self.cod][self.dia][self.seg]["Tipo"] == "Saque") or (self.bancoDados.historico[self.cod][self.dia][self.seg]["Tipo"] == "Pagar credito") or (self.bancoDados.historico[self.cod][self.dia][self.seg]["Tipo"] == "Pagamento Programado"):
                    self.lista_cliente.itemconfig(0, {'fg' : '#E9441B'})
                elif self.bancoDados.historico[self.cod][self.dia][self.seg]["Tipo"] == "Credito":
                    self.lista_cliente.itemconfig(0, {'fg' : '#cd4fe6'})
        self.lista_cliente.place(relx=0.0, rely= 0.2, relwidth=0.9, relheight=0.8)
        self.scrollbar_lista.config(command= self.lista_cliente.yview)

    def mostra_funcoes_cliente(self):
        """ Mostra as funções de clientes para os clientes """

        self.bt_sacar = Button(self.fr_acoes, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Sacar", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_sacar())
        self.bt_sacar.place(relx=0, rely=0, relwidth=1, relheight=0.2)

        self.bt_depositar = Button(self.fr_acoes, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Depositar", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_depositar())
        self.bt_depositar.place(relx=0, rely=0.2, relwidth=1, relheight=0.2)

        self.bt_pagar_programado = Button(self.fr_acoes, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Pagamento Programado", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_pagar_programado())
        self.bt_pagar_programado.place(relx=0, rely=0.4, relwidth=1, relheight=0.2)

        self.bt_visualiza = Button(self.fr_acoes, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Visualiza Histórico", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.select_view_hist())
        self.bt_visualiza.place(relx=0, rely=0.6, relwidth=1, relheight=0.2)

        self.bt_solicita_cred = Button(self.fr_acoes, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Solicita Crédito", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_solicita_crédito())
        self.bt_solicita_cred.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)

    
    def tela_dados_conta(self):
        """ Mostra a tela de dados dos clientes para os clientes """
        
        self.tela_visualiza = Frame(self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.tela_visualiza.place(relx= 0.5, rely= 0.5, relwidth= 0.5, relheight= 0.8, anchor=CENTER)

        self.botao_x = Button(self.tela_visualiza, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="X", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_usuario(""))
        self.botao_x.place(relx=0.95, rely=0.05, relwidth=0.1, relheight=0.1, anchor=CENTER)

        self.l_nome_cli = Label(self.tela_visualiza, text = "Nome: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_nome_cli.place(relx=0.03, rely=0.05)
        self.l_nomereal_cli = Label(self.tela_visualiza, text = self.usuario["Nome"], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_nomereal_cli.place(relx=0.23, rely=0.05)

        self.l_end_cli = Label(self.tela_visualiza, text = "End: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_end_cli.place(relx=0.03, rely=0.17)
        self.l_endreal_cli = Label(self.tela_visualiza, text = self.usuario["Endereco"], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_endreal_cli.place(relx=0.23, rely=0.17)

        self.l_tel_cli = Label(self.tela_visualiza, text = "Tel: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_tel_cli.place(relx=0.03, rely=0.29)
        self.l_telreal_cli = Label(self.tela_visualiza, text = self.usuario["Telefone"], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_telreal_cli.place(relx=0.23, rely=0.29)

        if self.usuario["Tipo"] == "Pessoa":
            self.l_cpf_cli = Label(self.tela_visualiza, text = "CPF: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        else:
            self.l_cpf_cli = Label(self.tela_visualiza, text = "CNPJ: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_cpf_cli.place(relx=0.03, rely=0.41)
        self.l_cpfreal_cli = Label(self.tela_visualiza, text = self.usuario["CPF/CNPJ"], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_cpfreal_cli.place(relx=0.23, rely=0.41)

        self.l_sal_cli = Label(self.tela_visualiza, text = "Crédito à Pagar: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_sal_cli.place(relx=0.03, rely=0.53)
        self.l_salreal_cli = Label(self.tela_visualiza, text = "R$ " + str(self.usuario["Credito"]), foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_salreal_cli.place(relx=0.03, rely=0.70)

        self.bt_pagar = Button(self.tela_visualiza, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Pagar Crédito", 
                                  font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.confere_pode_pagar_cred())
        self.bt_pagar.place(relx=0.5, rely=0.9, relwidth=0.5, relheight=0.1)
    
    def tela_sacar(self):
        """ Tela de saque para os clientes """
        
        self.tela_saca_din = Frame(self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.tela_saca_din.place(relx= 0.5, rely= 0.5, relwidth= 0.5, relheight= 0.8, anchor=CENTER)

        self.l_sacar = Label(self.tela_saca_din, text = "SACAR", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_sacar.place(relx=0.5, rely=0.08, anchor=CENTER)

        self.botao_x = Button(self.tela_saca_din, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="X", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_usuario(""))
        self.botao_x.place(relx=0.95, rely=0.05, relwidth=0.1, relheight=0.1, anchor=CENTER)

        self.l_valor_atual = Label(self.tela_saca_din, text = "Saldo atual:", foreground="#50C649", background="#1C1C1C", font=("Terminal", "13", "bold"))
        self.l_valor_atual.place(relx=0.03, rely=0.19)
        self.l_valor_real = Label(self.tela_saca_din, text = "R$ " + str(self.usuario["Saldo"]), foreground="#50C649", background="#1C1C1C", font=("Terminal", "15", "bold"))
        self.l_valor_real.place(relx=0.5, rely=0.35, anchor=CENTER)

        self.l_quanto_sacar = Label(self.tela_saca_din, text = "Quanto você quer sacar:", foreground="#50C649", background="#1C1C1C", font=("Terminal", "13", "bold"))
        self.l_quanto_sacar.place(relx=0.03, rely=0.46)
        self.en_quanto_sacar = Entry(self.tela_saca_din, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_quanto_sacar.place(relx=0.125, rely=0.60, relwidth=0.75)

        self.bt_confirmar = Button(self.tela_saca_din, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Confirmar", 
                                  font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.confere_pode_sacar(float(self.en_quanto_sacar.get())))
        self.bt_confirmar.place(relx=0.5, rely=0.9, relwidth=0.45, relheight=0.15, anchor=CENTER)

    def tela_depositar(self):
        """ Tela de depósito para os clientes """

        self.tela_dep_din = Frame(self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.tela_dep_din.place(relx= 0.5, rely= 0.5, relwidth= 0.5, relheight= 0.8, anchor=CENTER)

        self.l_depositar = Label(self.tela_dep_din, text = "DEPOSITAR", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_depositar.place(relx=0.5, rely=0.08, anchor=CENTER)

        self.botao_x = Button(self.tela_dep_din, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="X", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_usuario(""))
        self.botao_x.place(relx=0.95, rely=0.05, relwidth=0.1, relheight=0.1, anchor=CENTER)

        self.l_valor_atual = Label(self.tela_dep_din, text = "Saldo atual:", foreground="#50C649", background="#1C1C1C", font=("Terminal", "13", "bold"))
        self.l_valor_atual.place(relx=0.03, rely=0.19)
        self.l_valor_real = Label(self.tela_dep_din, text = "R$ " + str(self.usuario["Saldo"]), foreground="#50C649", background="#1C1C1C", font=("Terminal", "15", "bold"))
        self.l_valor_real.place(relx=0.5, rely=0.35, anchor=CENTER)

        self.l_quanto_depo = Label(self.tela_dep_din, text = "Quanto você quer depositar:", foreground="#50C649", background="#1C1C1C", font=("Terminal", "13", "bold"))
        self.l_quanto_depo.place(relx=0.03, rely=0.46)
        self.en_quanto_depo = Entry(self.tela_dep_din, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_quanto_depo.place(relx=0.125, rely=0.60, relwidth=0.75)

        self.bt_confirmar = Button(self.tela_dep_din, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Confirmar", 
                                  font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.confere_pode_depo(float(self.en_quanto_depo.get())))
        self.bt_confirmar.place(relx=0.5, rely=0.9, relwidth=0.45, relheight=0.15, anchor=CENTER)

    def tela_pagar_programado(self):
        """ Tela de pagamento programado para o cliente """
        
        self.tela_pag_prog = Frame(self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.tela_pag_prog.place(relx= 0.5, rely= 0.5, relwidth= 0.5, relheight= 0.8, anchor=CENTER)

        self.botao_x = Button(self.tela_pag_prog, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="X", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_usuario(""))
        self.botao_x.place(relx=0.95, rely=0.05, relwidth=0.1, relheight=0.1, anchor=CENTER)

        self.l_pag_prog = Label(self.tela_pag_prog, text = "Pag. Programado", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_pag_prog.place(relx=0.5, rely=0.08, anchor=CENTER)

        self.l_text_pag = Label(self.tela_pag_prog, text = "Digite a data, a hora e o valor que você\nquer que seja pago.", foreground="#50C649", background="#1C1C1C", font=("Terminal", "9", "bold"))
        self.l_text_pag.place(relx=0.5, rely=0.25, anchor=CENTER) 

        self.l_data = Label(self.tela_pag_prog, text = "Data:", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_data.place(relx=0.03, rely=0.35)
        self.en_data_real = Entry(self.tela_pag_prog, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_data_real.place(relx=0.25, rely=0.35, relwidth=0.1)
        self.l_barra = Label(self.tela_pag_prog, text = "/", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_barra.place(relx=0.35, rely=0.35)
        self.en_data_real2 = Entry(self.tela_pag_prog, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_data_real2.place(relx=0.4, rely=0.35, relwidth=0.1)
        self.l_barra2 = Label(self.tela_pag_prog, text = "/", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_barra2.place(relx=0.5, rely=0.35)
        self.en_data_real3 = Entry(self.tela_pag_prog, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_data_real3.place(relx=0.55, rely=0.35, relwidth=0.2)

        self.l_hora = Label(self.tela_pag_prog, text = "Hora:", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_hora.place(relx=0.03, rely=0.50)
        self.en_hora_real = Entry(self.tela_pag_prog, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_hora_real.place(relx=0.25, rely=0.50, relwidth=0.1)
        self.l_barra3 = Label(self.tela_pag_prog, text = ":", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_barra3.place(relx=0.35, rely=0.5)
        self.en_hora_real2 = Entry(self.tela_pag_prog, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_hora_real2.place(relx=0.4, rely=0.5, relwidth=0.1)
        self.l_barra4 = Label(self.tela_pag_prog, text = ":", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_barra4.place(relx=0.5, rely=0.5)
        self.en_hora_real3 = Entry(self.tela_pag_prog, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_hora_real3.place(relx=0.55, rely=0.5, relwidth=0.1)

        self.l_valor = Label(self.tela_pag_prog, text = "Valor:", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_valor.place(relx=0.03, rely=0.65)
        self.en_valor_real = Entry(self.tela_pag_prog, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_valor_real.place(relx=0.25, rely=0.65, relwidth=0.73)

        self.bt_confirmar = Button(self.tela_pag_prog, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Confirmar", 
                                  font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.confere_pode_pagar_prog())
        self.bt_confirmar.place(relx=0.5, rely=0.9, relwidth=0.5, relheight=0.1, anchor=CENTER)

    def tela_visualiza_hist(self):
        """ Tela responsável por visualizar o histórico do cliente pelo cliente """

        item = self.lista_cliente.curselection()
        tempo = self.tempos[item[0]]

        self.tela_visualiza = Frame(self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.tela_visualiza.place(relx= 0.5, rely= 0.5, relwidth= 0.5, relheight= 0.8, anchor=CENTER)

        self.botao_x = Button(self.tela_visualiza, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="X", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_usuario(""))
        self.botao_x.place(relx=0.95, rely=0.05, relwidth=0.1, relheight=0.1, anchor=CENTER)

        self.l_historico = Label(self.tela_visualiza, text = "HISTÓRICO", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_historico.place(relx=0.5, rely=0.08, anchor=CENTER)

        self.l_tipo = Label(self.tela_visualiza, text = "Tipo: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_tipo.place(relx=0.03, rely=0.17)
        self.l_tipo_real = Label(self.tela_visualiza, text = self.bancoDados.historico[self.cod][tempo[0]][tempo[1]]["Tipo"], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_tipo_real.place(relx=0.23, rely=0.17)

        self.l_data = Label(self.tela_visualiza, text = "Data: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_data.place(relx=0.03, rely=0.29)
        self.l_data_real = Label(self.tela_visualiza, text = tempo[0], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_data_real.place(relx=0.23, rely=0.29)
        self.l_hora_real = Label(self.tela_visualiza, text = tempo[1], foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_hora_real.place(relx=0.65, rely=0.29)

        self.l_valor = Label(self.tela_visualiza, text = "Valor: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_valor.place(relx=0.03, rely=0.41)
        self.l_valor_real = Label(self.tela_visualiza, text = str(self.bancoDados.historico[self.cod][tempo[0]][tempo[1]]["Valor"]), foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_valor_real.place(relx=0.27, rely=0.41)

        self.l_sal = Label(self.tela_visualiza, text = "Saldo Final: ", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.l_sal.place(relx=0.03, rely=0.53)
        self.l_salreal = Label(self.tela_visualiza, text = "R$ " + str(self.bancoDados.historico[self.cod][tempo[0]][tempo[1]]["Saldo final"]), foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_salreal.place(relx=0.03, rely=0.70)
        

    def tela_solicita_crédito(self):
        """ Tela responsável por visualizar o crédito do cliente pelo cliente """

        self.tela_cred_din = Frame(self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.tela_cred_din.place(relx= 0.5, rely= 0.5, relwidth= 0.5, relheight= 0.8, anchor=CENTER)

        self.l_credito = Label(self.tela_cred_din, text = "CRÉDITO", foreground="#50C649", background="#1C1C1C", font=self.tela_fonte)
        self.l_credito.place(relx=0.5, rely=0.08, anchor=CENTER)

        self.botao_x = Button(self.tela_cred_din, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="X", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_usuario(""))
        self.botao_x.place(relx=0.95, rely=0.05, relwidth=0.1, relheight=0.1, anchor=CENTER)

        self.l_valor_atual = Label(self.tela_cred_din, text = "Saldo atual de crédito:", foreground="#50C649", background="#1C1C1C", font=("Terminal", "13", "bold"))
        self.l_valor_atual.place(relx=0.03, rely=0.19)
        self.l_valor_real = Label(self.tela_cred_din, text = "R$ " + str(self.usuario["Credito"]), foreground="#50C649", background="#1C1C1C", font=("Terminal", "15", "bold"))
        self.l_valor_real.place(relx=0.5, rely=0.35, anchor=CENTER)

        self.l_quanto_cred = Label(self.tela_cred_din, text = "Quanto você quer solicitar:", foreground="#50C649", background="#1C1C1C", font=("Terminal", "13", "bold"))
        self.l_quanto_cred.place(relx=0.03, rely=0.46)
        self.en_quanto_cred = Entry(self.tela_cred_din, foreground="#1C1C1C", background="#50C649", highlightbackground="#50C649", font=self.tela_fontinha)
        self.en_quanto_cred.place(relx=0.125, rely=0.60, relwidth=0.75)

        if self.usuario["Tipo"] == "Pessoa":
            self.l_limite = Label(self.tela_cred_din, text = "limite: R$ 2000.00", foreground="#50C649", background="#1C1C1C", font=("Terminal", "9", "bold"))
            self.l_limite.place(relx=0.5, rely=0.75, anchor=CENTER)
        elif self.usuario["Tipo"] == "Empresa":
            self.l_limite = Label(self.tela_cred_din, text = "limite: R$ 50000.00", foreground="#50C649", background="#1C1C1C", font=("Terminal", "9", "bold"))
            self.l_limite.place(relx=0.5, rely=0.75, anchor=CENTER) 

        self.bt_confirmar = Button(self.tela_cred_din, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Confirmar", 
                                  font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.confere_pode_cred(float(self.en_quanto_cred.get())))
        self.bt_confirmar.place(relx=0.5, rely=0.9, relwidth=0.45, relheight=0.15, anchor=CENTER)
    
    def tela_confirma_senha(self, cod):
        """ FUNÇÃO NÃO ESTÁ SENDO UTILIZADA """

        self.tela_aviso_select = Frame(self.frame1, bd = 4, bg="#1C1C1C", highlightbackground= "#50C649", highlightthickness=3)
        self.tela_aviso_select.place(relx= 0.5, rely= 0.3, relwidth= 0.5, relheight= 0.5, anchor=CENTER)

        self.botao_x = Button(self.tela_aviso_select, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="X", 
                                  font=self.tela_fonte, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.tela_usuario(""))
        self.botao_x.place(relx=0.95, rely=0.15, relwidth=0.1, relheight=0.3, anchor=CENTER)

        self.en_confirma_senha = Entry(self.tela_aviso_select, text = "Senha", foreground="#50C649", background="#1C1C1C", font=self.tela_fontinha)
        self.en_confirma_senha.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.botao_confirma = Button(self.tela_deleta, bg="#50C649", highlightbackground="#50C649", highlightthickness=1.5, foreground="#1C1C1C", text="Confirmar", 
                                  font=self.tela_fontinha, activebackground="#1C1C1C", activeforeground="#50C649", command=lambda : self.verifica_se_pode_del(cod))
        self.botao_confirma.place(relx=0.5, rely=0.85, relwidth=0.5, relheight=0.1, anchor=CENTER)







