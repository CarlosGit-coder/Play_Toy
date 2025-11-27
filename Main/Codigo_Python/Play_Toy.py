brinquedos = []

id_set = set()

def atualizar_id_set():
    global id_set
    id_set = set([item['id'] for item in brinquedos])


def cadastrar_item():
    brinquedo = {}
    id = input('Digite o ID do brinquedo (somente número inteiro positivo): ')

    id_verificado = verificar_id(id)
    if id_verificado is False:
        return

    brinquedo['id'] = id_verificado

    nome = input('Digite o nome do brinquedo: ')
    brinquedo['nome do brinquedo'] = nome

    marca = input('Digite a marca do brinquedo: ')
    brinquedo['marca'] = marca

    preço = input('Digite o preço do brinquedo: R$')
    brinquedo['preço'] = preço

    status = input('Esse brinquedo tem estoque (S/N)? ').lower()
    if status == 's':
        disponibilidade = 'Brinquedo com Estoque'
    elif status == 'n':
        disponibilidade = 'Brinquedo sem Estoque'
    else:
        print('-------------------------------')
        print('A resposta deve ser somente "S" ou "N"!')
        print('Cadastro Interrompido! Tente Novamente.')
        return

    brinquedo['disponibilidade'] = disponibilidade

    brinquedos.append(brinquedo)
    atualizar_id_set()

    print('-------------------------------')
    print('Cadastro realizado com sucesso!')


def verificar_id(id):
    try:
        id = int(id)
        if id in id_set:
            print('-------------------------------')
            print('ID já utilizado.')
            print('Cadastro Interrompido! Tente Novamente.')
            return False
        if id < 0:
            print('-------------------------------')
            print('ID não pode ser negativo.')
            print('Cadastro Interrompido! Tente Novamente.')
            return False

    except ValueError:
        print('-------------------------------')
        print('ID do brinquedo só pode conter números inteiros positivos!')
        print('Cadastro Interrompido! Tente Novamente.')
        return False

    return id

def buscar_brinquedo_especifico():
    busca = input('Digite o nome, marca ou ID do brinquedo: ').lower()

    try:
         busca_ID = int(busca)
    except:
         busca_ID = None

    localizados = []

    for item in brinquedos:
        if busca_ID is not None and item['id'] == busca_ID:
            localizados.append(item)
        elif busca in item['nome do brinquedo'].lower():
            localizados.append(item)
        elif busca in item['marca'].lower():
            localizados.append(item)

    if not localizados:
        print('Nenhum brinquedo encontrado!')
        return

    for item in localizados:
        print('-------------------------------')
        for categoria, valor in item.items():
            if categoria == 'preço':
                print(f'{categoria} : R$ {float(valor):.2f}')
            else:
                print(f'{categoria} : {valor}')


def listar_itens():
    if not brinquedos:
        print('Nenhum brinquedo cadastrado!')
        return

    for brinquedo in brinquedos:
        for categoria, resultado in brinquedo.items():
            if categoria == 'preço':
                print(f'{categoria} : R$ {float(resultado.replace(",", ".")):.2f}')
            else:
                print(f'{categoria} : {resultado}')
        print('-------------------------------')


def buscar_brinquedo(item_id):
    try:
        item_id = int(item_id)

        for brinquedo in brinquedos:
            if brinquedo['id'] == item_id:
                print('-------------------------------')
                print('Brinquedo encontrado!')
                for categoria, resultado in brinquedo.items():
                    if categoria == 'preço':
                        print(f'{categoria} : R$ {float(resultado.replace(",", ".")):.2f}')
                    else:
                        print(f'{categoria} : {resultado}')
                return brinquedo

        print('-------------------------------')
        print('Brinquedo não encontrado.')
        return None

    except ValueError:
        print('-------------------------------')
        print('Valor inserido tem que ser inteiro!')
        return None


def atualizar_item():
    item_id = input('Digite o ID do brinquedo que deseja atualizar: ')
    brinquedo = buscar_brinquedo(item_id)

    if brinquedo is None:
        return

    categoria = input(
        'Que campo deseja atualizar (id / nome do brinquedo / marca / preço / disponibilidade)? '
    ).lower()

    if categoria not in brinquedo:
        print('-------------------------------')
        print('Categoria inválida! Tente novamente.')
        return

    novo_valor = input('Digite o novo valor: ')

    if categoria == 'id':
        id_verificado = verificar_id(novo_valor)
        if id_verificado is False:
            return
        brinquedo['id'] = id_verificado
        atualizar_id_set()
    else:
        brinquedo[categoria] = novo_valor

    print('-------------------------------')
    print('Atualização realizada com sucesso!')


def remover_item():
    item_id = input('Digite o ID do brinquedo que deseja remover: ')
    brinquedo = buscar_brinquedo(item_id)

    if brinquedo is None:
        return

    brinquedos.remove(brinquedo)
    atualizar_id_set()

    print('-------------------------------')
    print('Brinquedo removido com sucesso!')


def mostrar_menu_relatorios():
    print("\n=== MENU RELATÓRIOS ===")
    print("1 - Brinquedos cadastrados")
    print("2 - Brinquedos por marca")
    print("3 - Disponíveis e sem estoque")
    print("0 - Voltar")
    return input("Escolha uma opção: ")


def gerar_relatorio():
    if not brinquedos:
        print("Nenhum brinquedo cadastrado! Impossível gerar relatório.\n")
        return

    while True:
        opcao = mostrar_menu_relatorios()

        if opcao == '1':
            print("\n=== Brinquedos cadastrados ===")
            for b in brinquedos:
                print(f"- {b['nome do brinquedo']} (ID: {b['id']})")
            print()

        elif opcao == '2':
            marcas = {}
            for brinquedo in brinquedos:
                marca = brinquedo['marca']
                if marca not in marcas:
                    marcas[marca] = []
                marcas[marca].append(brinquedo['nome do brinquedo'])

            print("\n=== Brinquedos por Marca ===")
            for marca, itens in marcas.items():
                print(f"Marca: {marca}")
                for item in itens:
                    print(f"  - {item}")
            print()

        elif opcao == '3':
            disponiveis = [b['nome do brinquedo'] for b in brinquedos
                           if b['disponibilidade'] == 'Brinquedo com Estoque']
            sem_estoque = [b['nome do brinquedo'] for b in brinquedos
                           if b['disponibilidade'] == 'Brinquedo sem Estoque']

            print("\n=== Brinquedos com estoque ===")
            print(*disponiveis, sep="\n") if disponiveis else print("Nenhum disponível.")

            print("\n=== Brinquedos sem estoque ===")
            print(*sem_estoque, sep="\n") if sem_estoque else print("Nenhum sem estoque.")
            print()

        elif opcao == '0':
            break
        else:
            print("Opção inválida! Tente novamente.")


def menu():
    print('-------------------------------')
    print('------ Sistema de Brinquedos ------')
    print('-------------------------------')
    print('1- Cadastrar Brinquedo')
    print('2- Listar Brinquedos')
    print('3- Atualizar Brinquedo')
    print('4- Remover Brinquedo')
    print('5- Gerar Relatório')
    print('6- Buscar Brinquedo')
    print('7- Sair do Programa')
    print('-------------------------------')

    return input('Escolha uma opção: ')


while True:
    escolha = menu()

    if escolha == '1':
        cadastrar_item()
    elif escolha == '2':
        listar_itens()
    elif escolha == '3':
        atualizar_item()
    elif escolha == '4':
        remover_item()
    elif escolha == '5':
        gerar_relatorio()
    elif escolha == '6':
        buscar_brinquedo_especifico()
    elif escolha == '7':
        print('Sistema finalizado!')
        break
    else:
        print('Opção inválida! Tente novamente.')