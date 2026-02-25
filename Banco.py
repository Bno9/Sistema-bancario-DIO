from abc import ABC, abstractproperty, abstractclassmethod
from datetime import datetime

def log(func, nome_operacao):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{func.__name__} realizada as {datetime.now().strftime("%d/%m/%Y %H:%M")}")
        return resultado

    return envelope

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("Você excedeu o numero de transações permitidas para hoje")
            return
        
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, nome, cpf, data_nascimento):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Saldo insuficiente na sua conta")
            return False
        
        elif valor > 0 :
            self._saldo -= valor
            print("Saque realizado com sucesso")
            return True

        else:
            print("Operação falhou")

        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Deposito realizado com sucesso")
        else:
            print("Operação falhou")
            return False
        

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques

        if excedeu_limite:
            print("Você excedeu o valor limite de saque")
        
        elif excedeu_saques:
            print("Você atingiu o limite de saques diarios, tente novamente amanhã")

        else:
            return super().sacar(valor)
            
        return False
    
    def __str__(self):
        return  f"""
        Agência:\t{self.agencia}
        C/C:\t\t{self.numero}
        Titular:\t{self.cliente.nome}"""

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
         })
        
    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []

        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao  = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao  = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    print( """

    [u] Criar Cliente
    [c] Criar Conta
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [l] Listar contas
    [q] Sair

    => """)

def filtrar_cliente(cpf, clientes):
    cliente_filtrado = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_filtrado[0] if cliente_filtrado else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta")
        return

    return cliente.contas[0]

@log
def depositar(clientes):
    cpf = input("Digite o cpf do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente nao encontrado")
        return

    valor = float(input("Informe o valor do deposito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

@log
def sacar(clientes):
    cpf = input("Digite o cpf do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente nao encontrado")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

@log
def exibir_extrato(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente nao encontrado")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("Extrato")
    transacoes = conta.historico.transacoes

    extrato = ""

    if not transacoes:
        extrato = "Não foram encontradas movimentações"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f"Saldo R$ {conta.saldo:.2f}")

@log
def criar_clientes(clientes):
    nome = input("Digite o nome: ")
    data_nascimento = input("Digite a data de nascimento: ")
    CPF = input("Digite o CPF: ")
    endereço = input("Digite o endereço nesse formato -> logradouro, numero - bairro - cidade/sigla estado\n")

    cliente = filtrar_cliente(CPF, clientes)

    if cliente:
        print("Já existe um cliente com esse cpf")
        return

    cliente = PessoaFisica(nome=nome, cpf=CPF, data_nascimento=data_nascimento, endereco=endereço)
    clientes.append(cliente)

@log
def criar_conta(clientes, numero_conta, contas):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente nao encontrado")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("Conta criada com sucesso")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(conta)

def Main():
    contas = []
    clientes = []


    while True:
        menu()
        opcao = input()

        if opcao == "u":
            criar_clientes(clientes)

        elif opcao == "c":
            numero_conta = len(contas)
            criar_conta(clientes, numero_conta, contas)

        elif opcao == "d":
            depositar(clientes)
        
        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione uma das operações")

Main()