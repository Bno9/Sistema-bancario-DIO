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

def sacar(*, saldo, valor, numero_saques, limite_saques, extrato):
    SALDO_SUFICIENTE = valor <= saldo
    ATINGIU_LIMITE = numero_saques == limite_saques

    if not SALDO_SUFICIENTE:
        print("Saldo insuficiente na sua conta")
        return
    
    if ATINGIU_LIMITE:
        print("Você atingiu o limite de saques diarios, tente novamente amanhã")
        return

    saldo -= valor
    numero_saques += 1
    extrato.append((valor, "Saque"))
    return saldo, numero_saques


def depositar(saldo, valor, extrato, limite, /):
    VALOR_POSITIVO = valor > 0

    VALOR_DENTRO_DO_LIMITE = valor <= limite

    if not VALOR_POSITIVO:
        print("Digite apenas numeros acima de 0")
        return

    if not VALOR_DENTRO_DO_LIMITE:
        print(f"Você pode depositar apenas R${limite} por deposito")
        return
        
    saldo += valor
    extrato.append((valor, "Deposito"))
    return saldo

def ver_extrato(saldo, /, *, extrato):
    if not extrato:
        print("Nao foram encontrado extratos")
        return

    for valor, status in extrato:
        print(f"R${valor:.2f} - {status}")

    print(f"Saldo: R${saldo:.2f}")

    return

def criar_cliente(nome, nascimento, CPF, endereço, usuarios):
    for cliente, dados in usuarios.items():
        if CPF == cliente:
            print("Esse cpf ja está cadastrado")
            return
    
    usuarios[CPF] = {"nome": nome,
                     "data_nascimento": nascimento,
                     "endereço": endereço}
    
    return print("Usuario cadastrado")

def criar_conta_corrente(CPF, usuario, contas): 
    if CPF not in usuario:
        print("Cpf nao encontrado na base de dados")
        return
            
    conta = str(len(contas) + 1)
    AGENCIA = "-0001"

    contas.append({"conta": conta + AGENCIA, "usuario": usuario[CPF]})
    print("Conta criada com sucesso")

def listar_contas(contas):
    for i in contas:
        print(f"Conta: {i['conta']} Cliente: {i['usuario']['nome']}")
    

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

