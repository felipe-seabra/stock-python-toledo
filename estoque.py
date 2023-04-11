from time import sleep

estoque = []  # declarando uma lista vazia para controle


def arquivo_existe(nome):
    """ verificação se arquivo existe """
    try:
        a = open(nome, 'rt')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True


def criar_arquivo(nome):
    """ criar novo arquivo """
    try:
        a = open(nome, 'wt+')
        a.close()
    except:
        print('\033[31mHouve um ERRO na criação do arquivo!\033[0;0m')


def le_estoque():
    """ carregar o 'estoque.txt' no sistema e copia para a lista estoque """
    with open(arq, 'rt', encoding='utf-8') as arquivo:
        estoque.clear()  # limpando a lista antes de carregar o estoque.txt
        for i in arquivo.readlines():
            cod, nome, qtd, pc, pv = i.strip().split("#")
            estoque.append([cod, nome, qtd, pc, pv])
    arquivo.close()  # fechando o arquivo após o uso


def grava():
    """ função para gravar o 'estoque.txt' (nome 'estoque.txt' predefinido) """
    with open(arq, 'wt+', encoding='utf-8') as arquivo:
        for e in estoque:
            arquivo.write(f'{e[0]}#{e[1]}#{e[2]}#{e[3]}#{e[4]}\n')
    arquivo.close()  # fechando o arquivo após o uso


def ler_int(msg):
    """ ler números digitados pelo usuário """
    while True:
        try:
            v = int(input(f'\n{msg}'))
            return v
        except ValueError:
            print('\n\033[31mOops! Digite apenas NÚMEROS. Favor digitar novamente...\033[0;0m')
            sleep(1)


def ler_nome():
    """ ler nome digitado pelo usuário (str) """
    return input('\nNome do produto: ').upper()


def ler_float(parametro):
    """ ler os valores digitados pelo usuário R$ (float) """
    while True:
        try:
            v = float(input(f'\n{parametro}R$ '))
            return v
        except ValueError:
            print('\n\033[31mOops! O valor digitado não está correto. Use . (ponto) para separar casas.'
                  ' Favor digitar novamente...\033[0;0m')
            sleep(1)


def verifica_estoque():
    """ verifica se existe produtos em estoque """
    if len(estoque) > 0:
        return True
    else:
        print('\n\033[31mNão existe produtos em estoque.\033[0;0m')
        sleep(2)
        return False


def cadastro():
    """ cadastra o produto e gravar no .txt, mas antes é feito uma
     pesquisa se o código já está cadastrado """
    print(f'\n' * 10)
    cabecalho('CADASTRO DE PRODUTO')
    cod = ler_int('Código: ')
    if pesquisa(cod, 0) is None:  # pesquisando se o código já está cadastrado em outro produto
        nome = ler_nome()
        qtd = ler_int('Quantidade: ')
        pc = ler_float('Preço de custo: ')
        pv = ler_float('Preço de venda: ')
        estoque.append([cod, nome, qtd, pc, pv])
        grava()  # gravando a lista no .txt após receber os dados
        print(f'\n\033[32mPRODUTO:\033[0;0m {nome} \033[32mcadastrado com sucesso\n\033[0;0m')
        sleep(2)
    else:
        print(f'\n\033[31mO CÓDIGO:\033[0;0m {cod} \033[31mjá está cadastrado em outro produto!!\033[0;0m')
        sleep(2)
    return 0


def alterar_cadastro():
    """ alterar o cadastro de um produto, verificando se o mesmo
     existe antes de seguir o processo"""
    cabecalho('ALTERAÇÃO DE PRODUTO')
    if verifica_estoque():
        p = cod_nome()
        if p is not None:
            produto(p)
            nome = ler_nome()
            pc = ler_float('Novo preço de custo: ')
            pv = ler_float('Novo preço de venda: ')
            estoque[p] = [estoque[p][0], nome, estoque[p][2], pc, pv]
            grava()
        else:
            print('\n\033[31mPRODUTO NÃO ENCONTRADO!!\033[0;0m')
            sleep(2)


def excluir_produto():
    """ excluir um produto da lista e gravar no arquivo, é feito a busca
    antes na função pesquisa() para ver se o mesmo exise """
    print(f'\n'*6)
    cabecalho('ESCLUIR PRODUTO')
    if verifica_estoque():
        p = cod_nome()
        if p is not None:
            produto(p)
            op = input('\n\033[31mDeseja mesmo excluir? (S / N): \033[0;0m')
            if op.upper() == 'S':
                estoque.pop(p)  # remove o item da lista
                grava()
                print('\033[32mProduto excluido com sucesso\033[0;0m')
                sleep(2)
            elif op.upper() == 'N':
                print('\033[31mProduto NÃO foi excluido\033[0;0m')
                sleep(2)
            else:
                print('\n\033[31mOpção inválida!\033[0;0m')
                print('\n\033[31mProduto NÃO foi excluido\033[0;0m')
                sleep(2)
        else:
            print('\n\033[31mNÃO encontrado\033[0;0m')
            sleep(2)


def registrar_compra():
    """ registra uma compra de um determinado produto que foi pesquisado"""
    print(f'\n' * 10)
    cabecalho('REGISTRAR COMPRA DE PRODUTO')
    if verifica_estoque():
        p = cod_nome()
        if p is not None:
            produto(p)
            qtd = int(input('\nQuantidade: '))
            quantidade = int(estoque[p][2])
            quantidade = quantidade + qtd
            estoque[p][2] = quantidade
            grava()
            print('\n\033[32mCompra registrada\033[0;0m')
            sleep(2)
        else:
            print('\n\033[31mPRODUTO NÃO encontrado!\033[0;0m')
            sleep(2)


def registrar_venda():
    """ registar a venda de um produto, verificando se o mesmo existe, se existir
    é feito a verificação da quantidade para ser feito a subtração na lista, para
    ser gravado no arquivo """
    print(f'\n' * 10)
    cabecalho('REGISTRAR VENDA DE PRODUTO')
    if verifica_estoque():
        p = cod_nome()
        if p is not None:
            produto(p)
            qtd = ler_int('\nQuantidade: ')
            quantidade = int(estoque[p][2])
            if qtd <= quantidade:
                quantidade = quantidade - qtd
                estoque[p][2] = quantidade
                grava()
                print('\n\033[31mVenda registrada\033[0;0m')
                sleep(2)
            else:
                print('\n\033[31mQuantidade maior que estoque.\033[0;0m')
                sleep(2)
        else:
            print('\n\033[31mPRODUTO NÃO encontrado!\033[0;0m')
            sleep(2)


def consultar_estoque():
    """ consultar estoque por produto ou geral """
    print(f'\n' * 10)
    cabecalho('CONSULTA DE ESTOQUE')
    if verifica_estoque():
        opr = menu(['Consultar UM produto', 'Consultar TODOS os produtos'])
        if opr == 1:
            p = cod_nome()
            if p is not None:
                produto(p)
                input('\nAperte ENTER para continuar')
            else:
                print('\n\033[31mNÃO encontrado\033[0;0m')
                sleep(2)
        elif opr == 2:
            exibe_estoque()
            input('\nAperte qualquer ENTER para continuar')


def consultar_valor_estoque():
    """ fazer a soma dos custos e dos preços de venda """
    somac = 0.0
    somav = 0.0
    print(f'\n' * 10)
    cabecalho('CONSULTA VALOR EM ESTOQUE')
    if verifica_estoque():
        for e in estoque:
            somac = somac + (float(e[3]) * int(e[2]))
            somav = somav + (float(e[4]) * int(e[2]))
            lucro = somav - somac
        print(f'''
{linha(50)}
\033[1mTotal no estoque preço de CUSTO: \033[32mR$ {somac:.2f}\033[0;0m
{linha(50)}
\033[1mTotal no estoque preço de VENDA: \033[32mR$ {somav:.2f}\033[0;0m
{linha(50)}
\033[1mTotal de LUCRO: \033[32mR$ {lucro:.2f}\033[0;0m
{linha(50)}
        ''')
        input('\nAperte ENTER para continuar')


def pesquisa(busca, c):
    """ pesquisar um produto na lista carregada anteriormente do .txt
    busca sendo o parâmetro e c sendo a posição na lista """
    if c == 1:
        try:
            for p, e in enumerate(estoque):
                if e[c].lower() == busca.lower():
                    return p
        except:
            print('\n\033[31mNão existe produtos em estoque.\033[0;0m')
    elif c == 0:
        try:
            for p, e in enumerate(estoque):
                if int(e[c]) == busca:
                    return p
        except:
            print('\n\033[31mNão existe produtos em estoque.\033[0;0m')
    else:
        return None  # retornando None caso o código não está no cadastro, para ser usado na função cadastro()


def cod_nome():
    """ chama a função de pesquisa com a posição do código ou
     do nome, essa posição é recebida da função opcoes_cod_nome() """
    oper = opcoes_cod_nome()
    if oper == 1:
        pos = pesquisa(ler_int('Código: '), 0)
    elif oper == 2:
        pos = pesquisa(ler_nome(), 1)
    return pos


def opcoes_cod_nome():
    """ retorna a opção se é para ser pesquisado por código ou
     por nome """
    print(f'\n' * 4)
    oper = menu(['Buscar por CÓDIGO', 'Buscar por NOME'])
    return oper


def produto(p):
    """ recebe a posição do produto da função pesquisa(), alocando
    nas variaveis e chama a função de exibição """
    cod = estoque[p][0]
    nome = estoque[p][1]
    qtd = estoque[p][2]
    pc = estoque[p][3]
    pv = estoque[p][4]
    print('\n\033[32mPRODUTO ECONTRADO:\033[0;0m\n')
    exibe(cod, nome, qtd, pc, pv)


def exibe_estoque():
    """ exibe o estoque completo chamando a função exibe(), mas antes verifica
        se existe produtos cadastrados """
    if verifica_estoque():
        cabecalho('PRODUTOS EM ESTOQUE')
        for e in estoque:
            exibe(e[0], e[1], e[2], e[3], e[4])


def valida_faixa_opcoes(op, inicio, fim):
    """ valida as opções do menu """
    while True:
        try:
            valor = int(input(op))
            if inicio <= valor <= fim:
                return valor
            else:
                print(f"\033[31m\nValor inválido, favor digitar entre {inicio} e {fim}\n\033[0;0m")
                sleep(1)
        except ValueError:
            print(f"\033[31m\nValor inválido, favor digitar entre {inicio} e {fim}\033[0;0m\n")
            sleep(1)


def exibe(cod, nome, qtd, pc, pv):
    """ exibir os produtos cadastrados, recebendo os parâmetros """
    print(f'''\033[1m\033[32mCódigo: {cod}\t- Nome: {nome:<15}- Quantidade: {qtd:<4}- Preço de custo: \
R$ {float(pc):.2f}\t - Preço de venda: R$ {float(pv):.2f}\033[0;0m''')
    print(linha(115))


def linha(tam=42):
    """ retorna uma string com uma linha de 42 caracteres caso não receba nenhum parâmetro
     de entrada """
    return '-' * tam


def cabecalho(txt):
    """ formatação dos cabeçalhos """
    print('\n' * 10)
    print(linha())
    print(f'\033[31m\033[1m{txt.center(42).upper()}\033[0;0m')
    print(linha())
    print()


def menu(lista):
    """ formatação dos menus """
    c = 1
    for item in lista:
        print(f'\033[33m {c} - \033[34m{item}\033[0;0m')
        c += 1
    return valida_faixa_opcoes('\nEscolha uma opção: ', 1, c-1)  # 'c-1' pois c começa com 1


def main():
    """ loop principal do sistema com suas respectivas opções para chamada das funções """
    while True:
        cabecalho('MENU PRINCIPAL')
        op = menu(['Cadastrar produto', 'Alterar produto', 'Excluir produto',
                   'Registrar compra', 'Registrar venda', 'Consultar estoque',
                   'Consultar valor total em estoque\n', '\033[1mSAIR DO SISTEMA\033[0;0m'])
        if op == 8:  # opção de sair do sistema
            cabecalho('SAINDO DO SISTEMA...')
            break
        elif op == 1:
            cadastro()
        elif op == 2:
            alterar_cadastro()
        elif op == 3:
            excluir_produto()
        elif op == 4:
            registrar_compra()
        elif op == 5:
            registrar_venda()
        elif op == 6:
            consultar_estoque()
        elif op == 7:
            consultar_valor_estoque()


""" aqui começa o sistema, sendo feito a criação do arquivo caso
    o mesmo não exista e chamando as funções iniciais """
arq = 'estoque.txt'  # nome do arquivo .txt do estoque

if not arquivo_existe(arq):  # verificar se o arquivo existe
    criar_arquivo(arq)  # caso não exista, crie

le_estoque()  # ler o estoque e passa para uma lista de controle do sistema
main()  # chamando o main (opções do sistema)
