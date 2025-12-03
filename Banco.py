menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Digite o valor que deseja depositar: "))

        VALOR_POSITIVO = valor > 0

        VALOR_DENTRO_DO_LIMITE = valor <= limite

        if not VALOR_POSITIVO:
            print("Digite apenas numeros acima de 0")

        elif not VALOR_DENTRO_DO_LIMITE:
            print(f"Você pode depositar apenas R${limite} por deposito")
            
        elif VALOR_DENTRO_DO_LIMITE and VALOR_POSITIVO:
            saldo += valor
            extrato.append((valor, "Deposito"))

    
    elif opcao == "s":
        valor = float(input("Digite o valor que deseja sacar: "))

        SALDO_SUFICIENTE = valor < saldo

        ATINGIU_LIMITE = numero_saques == LIMITE_SAQUES

        if not SALDO_SUFICIENTE:
            print("Você não tem saldo suficiente")

        elif ATINGIU_LIMITE:
            print("Você atingiu o maximo de saques diario")

        elif SALDO_SUFICIENTE:
            saldo -= valor
            numero_saques += 1
            extrato.append((valor, "Saque"))


    elif opcao == "e":
        if not extrato:
            print("Nao foram encontrado extratos")

        for valor, status in extrato:
            print(f"R${valor:.2f} - {status}")

        print(f"Saldo: R${saldo:.2f}")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione uma das operações")