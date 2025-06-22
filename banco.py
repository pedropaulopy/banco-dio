money = 0
saques = 0

operations = []
while(True):
    print("""
========== BANCO DIO ==========
1 - Depósito  
2 - Saque  
3 - Extrato
4 - Saldo atual  
5 - Sair
================================
""")
    option = input("Escolha uma operacao: ")
    match option:
        case "1":
            amount =  float(input("Quanto deseja depositar? R$"))
            money += amount
            operations.append(f"DEPOSITO. - R${amount:.2f}")
            continue

        case "2":
            if saques==3:
                print("Voce atingiu seu limite de saques diarios, tente novamente em 24h.")
                continue
            amount = float(input("Quanto deseja sacar? R$"))
            if amount<=500 and amount<=money and saques<3:
                money -= amount
                operations.append(f"SAQUE.- R${amount:.2f}")
                saques += 1
                continue
            elif amount>500:
                print("Somente saques menores ou iguais a R$500 sao permitidos.")
                continue
            elif amount>money:
                print("Seu saque excede o saldo atual.")
                continue

        case "3":
            for i in operations:
                print(i)
            continue
        case "4":
            print(f"Seu saldo atual e: R${money:.2f}")
        case "5":
            print("Exiting...")
            break
        case _:
            print("comand not found")
            continue
