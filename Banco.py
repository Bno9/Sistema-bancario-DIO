from abc import ABC, abstractproperty, abstractclassmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
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
    [l] listar contas
    [q] Sair

    => """)

def Main():
    contas = []


    while True:
        menu()
        opcao = input()

        if opcao == "u":
            nome = input("Digite o nome: ")
            data_nascimento = input("Digite a data de nascimento: ")
            CPF = input("Digite o CPF: ")
            endereço = input("Digite o endereço nesse formato -> logradouro, numero - bairro - cidade/sigla estado\n")
            cliente = PessoaFisica(endereco=endereço, nome=nome, cpf=CPF, data_nascimento=data_nascimento)

        elif opcao == "c":
            CPF = input("Digite seu cpf: ")
            conta = ContaCorrente.nova_conta(0, cliente)
            cliente.adicionar_conta(conta)

        elif opcao == "d":
            valor = float(input("Digite o valor que deseja depositar: "))
            Deposito(valor).registrar(conta)
            #pessoa.realizar_transacao(conta, Deposito)
        
        elif opcao == "s":
            valor = float(input("Digite o valor que deseja sacar: "))
            Saque(valor).registrar(conta)

        elif opcao == "e":
            print(conta.historico.transacoes)

        elif opcao == "l":
            for i in cliente.contas:
                print(f"Cliente: {i.cliente.nome}, Saldo: {i.saldo}, numero: {i.numero}, agencia: {i.agencia}")

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione uma das operações")

Main()