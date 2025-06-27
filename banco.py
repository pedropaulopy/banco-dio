# Variáveis globais para controle do sistema bancário
users = []  # Lista para armazenar usuários cadastrados
accounts = []  # Lista para armazenar contas criadas
next_account_number = 1  # Próximo número de conta a ser atribuído

def create_user(name, birthday, cpf, address):
    # Verifica se o CPF já está cadastrado
    if cpf in users:
       return print("CPF ja cadastrado.")
        
    user = [(name, birthday, cpf, address)]
    users.append(user)  # Adiciona novo usuário à lista

def create_account(cpf):
    global next_account_number
    # Verifica se o CPF está cadastrado antes de criar a conta
    if cpf not in users:
        return print("CPF nao cadastrado.")
    
    # Cria conta como dicionário com saldo, extrato e contador de saques
    account = {
        "agencia": "0001",
        "numero": next_account_number,
        "cpf": cpf,
        "saldo": 0,
        "extrato": [],
        "saques": 0
    }
    next_account_number += 1  # Incrementa o número para a próxima conta
    accounts.append(account)  # Adiciona conta à lista de contas

def find_account():
    # Solicita número da conta ao usuário e retorna a conta correspondente
    numero = int(input("Digite o número da conta: "))
    for conta in accounts:
        if conta["numero"] == numero:
            return conta
    print("Conta não encontrada.")
    return None

def deposit():
    conta = find_account()
    if not conta:
        return
    # Solicita valor de depósito ao usuário
    amount = float(input("Quanto deseja depositar? R$"))
    conta["saldo"] += amount  # Atualiza saldo da conta
    conta["extrato"].append(f"DEPOSITO. +R${amount:.2f}")  # Registra operação

def withdraw():
    conta = find_account()
    if not conta:
        return
    # Verifica limite diário de saques
    if conta["saques"] == 3:
        print("Voce atingiu seu limite de saques diarios, tente novamente em 24h.")
        return
    amount = float(input("Quanto deseja sacar? R$"))
    # Verifica se o valor do saque está dentro dos limites permitidos
    if amount <= 500 and amount <= conta["saldo"] and conta["saques"] < 3:
        conta["saldo"] -= amount  # Atualiza saldo da conta
        conta["extrato"].append(f"SAQUE. -R${amount:.2f}")  # Registra operação
        conta["saques"] += 1  # Incrementa contador de saques
    elif amount > 500:
        print("Somente saques menores ou iguais a R$500 sao permitidos.")
    elif amount > conta["saldo"]:
        print("Seu saque excede o saldo atual.")

def print_operations():
    conta = find_account()
    if not conta:
        return
    # Exibe todas as operações realizadas na conta
    for i in conta["extrato"]:
        print(i)
    print(f"Seu saldo atual é: R${conta['saldo']:.2f}")

def print_menu():
    # Exibe o menu principal do sistema bancário
    print("""
========== BANCO DIO ==========
1 - Depósito  
2 - Saque  
3 - Extrato  
5 - Sair
================================
""")
    
# Loop principal do sistema bancário
while(True):
    print_menu()  # Exibe o menu
    
    option = input("Escolha uma operacao: ")
    match option:
        case "1":
            deposit()  # Realiza depósito
            continue

        case "2":
            withdraw()  # Realiza saque
            continue

        case "3":
            print_operations()  # Exibe extrato de operações
            continue 
        
        case "4":
            print("Exiting...")  # Sai do sistema
            break
        case _:
            print("comand not found")
            continue
