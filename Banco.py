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

        if valor > limite:
            print(f"Você pode depositar apenas R${limite} por deposito")
            
        else:
            saldo += valor
            extrato.append((valor, "Deposito"))

    
    elif opcao == "s":
        valor = float(input("Digite o valor que deseja sacar: "))

        if valor > saldo:
            print("Você não tem saldo suficiente")

        elif numero_saques == LIMITE_SAQUES:
            print("Você atingiu o maximo de saques diario")

        else:
            saldo -= valor
            numero_saques += 1
            extrato.append((valor, "Saque"))


    elif opcao == "e":
        for valor, status in extrato:
            print(f"R${valor:.2f} - {status}")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione uma das operações")