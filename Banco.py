class Conta:
    def __init__(self, saldo: float, numero: str, agencia: str, cliente: Cliente):
        self.saldo = saldo
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.extrato = []
        self.LIMITE_SAQUES = 3
        self.numero_saques = 0
        self.limite = 500

    def sacar(self, *, valor: float) -> bool:
        SALDO_SUFICIENTE = valor <= self.saldo
        ATINGIU_LIMITE = self.numero_saques == self.LIMITE_SAQUES

        if not SALDO_SUFICIENTE:
            print("Saldo insuficiente na sua conta")
            return False
        
        if ATINGIU_LIMITE:
            print("Você atingiu o limite de saques diarios, tente novamente amanhã")
            return False

        self.saldo -= valor
        self.numero_saques += 1
        self.extrato.append((valor, "Saque"))
        return True


    def depositar(self, valor: float, /) -> bool:
        VALOR_POSITIVO = valor > 0

        VALOR_DENTRO_DO_LIMITE = valor <= self.limite

        if not VALOR_POSITIVO:
            print("Digite apenas numeros acima de 0")
            return False

        if not VALOR_DENTRO_DO_LIMITE:
            print(f"Você pode depositar apenas R${self.limite} por deposito")
            return False
            
        self.saldo += valor
        self.extrato.append((valor, "Deposito"))
        return True

    def ver_extrato(self):
        if not self.extrato:
            print("Nao foram encontrado extratos")
            return False

        for valor, status in self.extrato:
            print(f"R${valor:.2f} - {status}")

        print(f"Saldo: R${self.saldo:.2f}")

class Cliente:
    def __init__(self, endereço: str, cpf: str, nome: str, data_nascimento: str):
        self.endereço = endereço
        self.cpf = cpf
        self.nome = nome,
        self.data_nascimento = data_nascimento
        self.contas = []



    def criar_cliente(self, nome, nascimento, CPF, endereço, usuarios) -> bool:
        for cliente, dados in usuarios.items():
            if CPF == cliente:
                print("Esse cpf ja está cadastrado")
                return False
        
        usuarios[CPF] = {"nome": nome,
                        "data_nascimento": nascimento,
                        "endereço": endereço}
        
        print("Usuario cadastrado")
        return True

    def criar_conta_corrente(self, CPF, usuario, contas) -> bool: 
        if CPF not in usuario:
            print("Cpf nao encontrado na base de dados")
            return False
                
        conta = str(len(contas) + 1)
        AGENCIA = "-0001"

        contas.append({"conta": conta + AGENCIA, "usuario": usuario[CPF]})
        print("Conta criada com sucesso")
        return True

    def listar_contas(contas):
        if not contas:
            print("Nenhuma conta encontrada")
            return False
        
        for i in contas:
            print(f"Conta: {i['conta']} Cliente: {i['usuario']['nome']}")


def menu():
    print( """

    [u] Criar usuario
    [c] Criar conta
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [l] listar contas
    [q] Sair

    => """)

def main():
    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = {}
    contas = []


    while True:

        menu()
        opcao = input()

        if opcao == "u":
            nome = input("Digite o nome: ")
            data_nascimento = input("Digite a data de nascimento: ")
            CPF = input("Digite o CPF: ")
            endereço = input("Digite o endereço nesse formato -> logradouro, numero - bairro - cidade/sigla estado\n")
            criar_cliente(nome, data_nascimento, CPF, endereço, usuarios)

        elif opcao == "c":
            CPF = input("Digite seu cpf")

            criar_conta_corrente(CPF, usuarios, contas)

        elif opcao == "d":
            valor = float(input("Digite o valor que deseja depositar: "))
            saldo = depositar(saldo, valor, extrato, limite)
        
        elif opcao == "s":
            valor = float(input("Digite o valor que deseja sacar: "))
            saldo, numero_saques = sacar(saldo=saldo, valor=valor, limite_saques=LIMITE_SAQUES, numero_saques=numero_saques, extrato=extrato)

        elif opcao == "e":
            ver_extrato(saldo, extrato=extrato)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione uma das operações")

main()

