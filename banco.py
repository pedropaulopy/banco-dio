from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# Variáveis globais para controle do sistema bancário
users = []  # Lista para armazenar usuários cadastrados
accounts = []  # Lista para armazenar contas criadas
next_account_number = 1  # Próximo número de conta a ser atribuído
transactions = 0


def find_account_obj():
    numero = int(input("Digite o número da conta: "))
    for conta in accounts:
        if hasattr(conta, "numero") and conta.numero == numero:
            return conta
    print("Conta não encontrada.")
    return None


def find_cliente_by_conta(conta):
    return getattr(conta, "cliente", None)


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        agora = datetime.now()
        # Filter transactions from the last 24 hours
        transacoes_hoje = [
            t for t in self.transacoes if agora - t.data_hora < timedelta(hours=24)
        ]
        if len(transacoes_hoje) >= 10:
            print("Limite de 10 transações em 24h atingido.")
            return False  # Block transaction
        with open("logs.txt", "a", encoding="utf-8") as file:
            file.write(
                f"TIPO: {type(transacao).__name__}, VALOR: R${transacao.valor}, DATAHORA: {transacao.data_hora}\n"
            )
        self.transacoes.append(transacao)
        return True


class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if conta in self.contas:
            # Check if transaction can be added before registering
            if not conta.historico.adicionar_transacao(transacao):
                return False
            sucesso = transacao.registrar(conta)
            if not sucesso:
                # If transaction fails, remove from historico
                conta.historico.transacoes.pop()
            return sucesso
        return False

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome: str, cpf: str, data_nascimento: datetime, endereco: str):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero: int, agencia: str, cliente: Cliente):
        self.numero = numero
        self.agencia = agencia
        self.saldo = 0.0
        self.cliente = cliente
        self.historico = Historico()

    def saldo_atual(self):
        return self.saldo

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):
        conta = cls(numero=numero, agencia="0001", cliente=cliente)
        cliente.adicionar_conta(conta)
        return conta

    def sacar(self, valor: float):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            return True
        return False

    def depositar(self, valor: float):
        if valor > 0:
            self.saldo += valor
            return True
        return False


class ContaCorrente(Conta):
    def __init__(
        self,
        numero: int,
        agencia: str,
        cliente: Cliente,
        limite: float = 500.0,
        limite_saques: int = 3,
    ):
        super().__init__(numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = []  # lista de datetimes dos saques

    def sacar(self, valor: float):
        agora = datetime.now()
        # Remove saques que não são das últimas 24h
        self.saques_realizados = [
            t for t in self.saques_realizados if agora - t < timedelta(hours=24)
        ]
        if len(self.saques_realizados) >= self.limite_saques:
            print("Limite de 3 saques em 24h atingido.")
            return False
        if valor > self.limite:
            print("Valor máximo por saque é R$500.")
            return False
        if 0 < valor <= (self.saldo + self.limite):
            self.saldo -= valor
            self.saques_realizados.append(agora)
            return True
        print("Saldo insuficiente ou valor inválido.")
        return False


class Transacao(ABC):
    def __init__(self, valor: float):
        self.valor = valor
        self.data_hora = datetime.now()

    @abstractmethod
    def registrar(self, conta: Conta):
        pass


class Saque(Transacao):
    def registrar(self, conta: Conta):
        if conta.sacar(self.valor):
            return True
        print("Saque não realizado. Saldo insuficiente ou limite atingido.")
        return False


class Deposito(Transacao):
    def registrar(self, conta: Conta):
        if conta.depositar(self.valor):
            return True
        print("Depósito não realizado. Valor inválido.")
        return False


def cadastrar_usuario():
    nome = input("Nome completo: ")
    cpf = input("CPF: ")
    data_nascimento = input("Data de nascimento (YYYY-MM-DD): ")
    endereco = input("Endereço: ")
    try:
        data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
    except ValueError:
        print("Data inválida.")
        return
    for u in users:
        if hasattr(u, "cpf") and u.cpf == cpf:
            print("Usuário já cadastrado.")
            return
    usuario = PessoaFisica(nome, cpf, data_nascimento, endereco)
    users.append(usuario)
    print("Usuário cadastrado com sucesso.")


def cadastrar_conta():
    global next_account_number
    cpf = input("CPF do titular: ")
    cliente = None
    for u in users:
        if hasattr(u, "cpf") and u.cpf == cpf:
            cliente = u
            break
    if not cliente:
        print("Cliente não encontrado. Cadastre o usuário primeiro.")
        return
    conta = ContaCorrente.nova_conta(cliente, next_account_number)
    accounts.append(conta)
    print(f"Conta criada com sucesso. Número: {conta.numero}")
    next_account_number += 1


def print_operations():
    conta = find_account_obj()
    if not conta:
        return
    for t in conta.historico.transacoes:
        print(f"{t.data_hora} - {type(t).__name__}: R${t.valor:.2f}")
    print(f"Seu saldo atual é: R${conta.saldo:.2f}")


def print_menu():
    print(
        """
========== BANCO DIO ==========
1 - Cadastrar usuário
2 - Cadastrar conta
3 - Depósito
4 - Saque
5 - Extrato
6 - Sair
================================
"""
    )


while True:
    print_menu()
    option = input("Escolha uma operacao: ")
    match option:
        case "1":
            cadastrar_usuario()
        case "2":
            cadastrar_conta()
        case "3":
            conta = find_account_obj()
            if not conta:
                continue
            cliente = find_cliente_by_conta(conta)
            valor = float(input("Digite o valor do depósito: R$"))
            transacao = Deposito(valor)
            sucesso = cliente.realizar_transacao(conta, transacao)
            if sucesso:
                print("Depósito realizado com sucesso.")
            else:
                print("Falha ao realizar depósito.")
        case "4":
            conta = find_account_obj()
            if not conta:
                continue
            cliente = find_cliente_by_conta(conta)
            valor = float(input("Digite o valor do saque: R$"))
            transacao = Saque(valor)
            sucesso = cliente.realizar_transacao(conta, transacao)
            if sucesso:
                print("Saque realizado com sucesso.")
            else:
                print("Falha ao realizar saque.")
        case "5":
            print_operations()
        case "6":
            print("Exiting...")
            break
        case _:
            print("comando não encontrado")
