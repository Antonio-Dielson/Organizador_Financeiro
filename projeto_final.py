import json
from datetime import datetime
import csv

def validar_indice(registros: list[dict]) -> int:
    '''
    Valida a entrada de um índice para exclusão de registros financeiros.

    Args:
        registros (list[dict]): 
            Lista de registros financeiros para verificar o índice válido.

    Returns:
        int: 
            O índice validado.
    '''
    while True:
        try:
            indice = int(input('digite o indice: '))
            if 0 <= indice < len(registros):
                return indice
            else:
                print(f'Digite ídices de 0 a {len(registros) - 1}')
        except ValueError:
            print('Digite apenas números inteiros')

def validar_data(msg: str) -> dict:
    """
    Valida uma string de data no formato 'DD/MM/AAAA' e retorna um dicionário com dia, mês, ano e a data completa como strings.

    Returns:
        dict: Dicionário contendo dia, mês, ano e a data completa separados como strings.

    Raises:
        ValidarDadosGeneric: Se a data não estiver no formato correto ou for inválida.
    """
    while True:
        try:
            data_str = input(f"{msg}: ")

            data_valida = datetime.strptime(data_str, '%d/%m/%Y')
            if data_valida > datetime.now():
                print('Data não pode ser superior à data de hoje.')
                continue
            
            dia = str(data_valida.day).zfill(2)
            mes = str(data_valida.month).zfill(2)
            ano = str(data_valida.year)
            
            data = f"{dia}/{mes}/{ano}"
            
            data_dict = {
                "data_completa": data,
                "dia": dia,
                "mes": mes,
                "ano": ano  
            }
            
            return data_dict

        except ValueError:
            print('Data inválida. Por favor, digite no formato esperado - Exemplo: 18/01/2024 (DD/MM/AAAA)') 


def validar_valor(msg: str = "Digite o valor: ") -> float:
    '''
    Valida a entrada de um valor numérico inserida pelo usuário.
    
    Returns:
        float: 
            Retorna o valor validado.
    '''
    while True:
        valor = input("Digite o valor: ").replace(',', '.')
        try: 
            valor = float(valor)
            if valor < 0:
                raise ValueError('Digite apenas valores numericos e positivos')
            return valor
        except ValueError:
            print('Digite apenas valores numericos e positivos')

def validar_tipo(msg: str) -> str:
    '''
    Valida a entrada de um tipo de movimentação inserida pelo usuário.

    Returns:
        str: 
            Retorna o tipo de movimentação validado ('Receita', 'Despesa' ou 'Investimento').
    '''
    while True:
        tipo = input(msg).capitalize()
        if tipo in ['Receita','Despesa','Investimento']:
            return tipo
        else:
            print('Erro, tipo invalido')

def tempo(data: str) -> int:
    '''
    Faz o cálculo da diferença em dias entre a data fornecida e a data atual,
    baseado na conversão do formato 'dd/mm/aaaa' para 'datetime'.

    Args:
        data (str): 
            Recebe a data em formato de string no (dd/mm/aaaa).

    Returns:
        int: 
            Retorna a diferença em dias entre a data fornecida e a data atual.
    '''
    data_convertido = datetime.strptime(data, '%d/%m/%Y')
    data_referencia = datetime.now()
    diferenca = data_referencia - data_convertido
    diferenca_days = diferenca.days
    return diferenca_days

def criar_registro() -> dict:
    '''
    Cria um novo registro financeiro com interação do usuário.

    Solicita ao usuário que digite uma data, tipo de movimentação (Receita, Despesa ou Investimento),
    e o valor. 
    Se o usuário selecionar 'Investimento' ela irá calcular o montante e o rendimento com base em um percentula de juros fixo.

    Returns:
        Dict
        Retorna um dicionário representando o registro financeiro que contém as chaves:
        'id', 'data', 'tipo', 'valor', 'montante', e 'rendimento'.
    '''
    data = validar_data('Insira uma data no formáto válido, dd/mm/yyyy')
    tipo = validar_tipo('Digite o tipo que deseja criar. [Receita, Despesa, Investimento]: ')
    valor = validar_valor()

    montante = None
    rendimento = None

    if tipo == 'Investimento':

        juros = 0.01

        montante_inicial = valor * (1+((juros)))**(tempo(data['data_completa']))
        montante = round(montante_inicial, 2)
        rendimento_inicial = montante - valor
        rendimento = round(rendimento_inicial, 2)

    registro = {
        'data': data,
        'tipo': tipo,
        'valor': valor if tipo != 'Despesa' else -valor, 
        'montante': montante,
        'rendimento': rendimento,
        'data_atualizacao': None
        
        }

    return registro

def ler_registros(arquivo):
    """Lê os registros financeiros do arquivo JSON."""

    try:
        with open(arquivo, 'r') as f:
            registros = json.load(f)
    except FileNotFoundError:
        registros = [] 

    return registros

def ler_registros_por(arquivo: list[dict]) -> list[dict]:
    
    '''
     Recebe todos os registros e realiza filtros de acordo com os critérios escolhidos.

    Filtra por Data, Tipo ou Valor.

    Args:
        list[Dict]: 
            Todos os registros.

    Returns:
        list[Dict]: 
            Retorna uma lista de dicionários com os registros financeiros.
     '''
    registros = arquivo

    while True:
        print("\n--- Ler registros ---")
        print("1. Por Data")
        print("2. Por Tipo")
        print("3. Por valor")
        print("9. Todos")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nova_data = validar_data('Data pela qual deseja filtrar: ')
            registros_filtrados = []
            for registro in registros:
                if registro['data'] == nova_data:
                    registros_filtrados.append(registro)
            break
        if opcao == '2':
            tipo = validar_tipo('Digite o tipo que deseja filtrar. [Receita, Despesa, Investimento]: ')
            registros_filtrados = []
            for registro in registros:
                if registro['tipo'] == tipo:
                    registros_filtrados.append(registro)
            break
        if opcao == '3':
            novo_valor = validar_valor("Digite o valor pelo qual filtrar: ")
            registros_filtrados = []
            for registro in registros:
                if abs(registro['valor']) == novo_valor:
                    registros_filtrados.append(registro)
            break
        if opcao == '9':
            registros_filtrados = registros
            break
        else:
            print("Escolha uma opção válida")
            continue

    return registros_filtrados

def atualizar_registro(registros: list[dict]) -> None:
    '''Atualiza um registro já existente conforme solicitação do usuário.
    
            O usuário pode selecionar um registro financeiro de uma lista e atualizar seus valores.
            Também pode optar em alterar o valor já existente, o tipo e a data.
            Se o usuário deixar algum valor em branco, o valor atual do registro será mantido.
         
        Args:
            registros (list[dict]): 
                Recebe uma lista de dicionários onde cada dicionário representa um registro financeiro 
                com as chaves 'valor', 'tipo', e 'data'.

        Returns:
            None: 
                Não retorna nenhum valor, apenas atualiza o registro. 
    '''

    if not registros:
        print("Nenhum registro encontrado.")
        return

    for i, registro in enumerate(registros):
        print(f"{i}: {registro}")
    
    indice = validar_indice(registros)
    novo_valor = validar_valor()
    novo_tipo = validar_tipo('Digite o tipo que deseja alterar. [Receita, Despesa, Investimento]: ')
    nova_data = validar_data('Nova data: ')

    if novo_valor:
        registros[indice]['valor'] = float(novo_valor) if novo_tipo != 'Despesa' else -float(novo_valor)
    if novo_tipo:
        registros[indice]['tipo'] = novo_tipo
    if nova_data:
        registros[indice]['data'] = nova_data
    registros[indice]['data_atualizacao'] = datetime.now().strftime("%d/%m/%Y")

    if novo_tipo == 'Investimento':

        juros = 0.01
        montante_inicial = novo_valor * (1+((juros)))**(tempo(registros[indice]['data']['data_completa']))
        montante = round(montante_inicial, 2)
        rendimento_inicial = montante - novo_valor
        rendimento = round(rendimento_inicial, 2)
    atualiza_rendimento(registros)
        
def deletar_registro(registros: list[dict])-> None:
    
    '''Deleta um registro financeiro, se solicitado pelo usuário.

            Essa função vai exibir uma lista de registros e permitir que o usuário delete o registro que escolher.
            Se a lista estiver vazia uma mensagem será exibida informando que nenhum registro foi encontrado.
            Se a informação fornecida pelo usuário estiver incorreta, a função também notificará.
        
        Args:
            registros (list[dict]):
                Recebe uma lista de dicionários, cada dicinário representa um registro.

        Returns:
            None: 
                Não retorna nenhum valor, apenas deleta o registro da lista.
    '''
    if not registros:
        print("Nenhum registro encontrado.")
        return

    for i, registro in enumerate(registros):
        print(f"{i}: {registro}")

    indice = validar_indice(registros)
    del registros[indice]
    print(f'O registro {indice} foi deletado com sucesso')

def salvar_registros(registros: list[dict], arquivo: str) -> None:
    '''
    Salva os registros no arquivo JSON.

    Grava uma lista de registros em um arquivo JSON.

    Args:
        registros: list[dict]
            Lista de dicionários que contém os registros a serem salvos.
        arquivo (str): 
            Caminho do arquivo onde os registros serão salvos.

    Returns:
        Não retorna nada, apenas salva os registros.
    '''

    with open(arquivo, 'w') as f:
        json.dump(registros, f, indent=4)

def atualiza_rendimento(registros: list[dict]) -> None:
    '''Atualiza o rendimento dos investimentos informados pelo usuário.
    
            A função calcula cada registro de 'investimento' com base na data da aplicação e na taxa juros informada pelo usuário.
            O rendimento será adicionado ao registro 'rendimento'.
    
        Args:
            registros (list[dict]): lista de dicionários que recebe str e float
                Cada dicionário representa um registro financeiro. 
                Cada registro contém as chaves 'valor' (valor do investimento), 'tipo' (tipo do registro),
                e 'data' (data do investimento).
            
         Returns:
            None: 
                Não retorna nenhum valor, apenas atualiza o registro.
    '''

    hoje = datetime.now()

    for registro in registros:
        if registro['tipo'] == 'Investimento':
            data_investimento = datetime.strptime(registro['data']['data_completa'], '%d/%m/%Y')
            dias = (hoje - data_investimento).days
            capital = float(registro['valor'])
            taxa_juros = 0.01 
            rendimento = capital * (1 + taxa_juros) ** dias - capital
            montante = capital * (1 + taxa_juros) ** dias
            registro['rendimento'] = round(rendimento, 2)
            registro['montante'] = round(montante, 2)
            registro['data_atualizacao'] = datetime.now().strftime("%d/%m/%Y")
        else:
            registro['rendimento'] = None
            registro['montante'] = None
def exportar_relatorio(registros: list[dict], arquivo: str, formato: str = 'csv') -> None:

    '''Exporta o relatório dos registros financeiros para um arquivo nos formatos CSV ou JSON.
    
         Args:
            registros (list[dict]): 
                Recebe uma lista de dicionários onde cada dicionário representa um registro.
            arquivo (str): 
                Nome do arquivo de saída para o relatório.
            formato (str): 
                Formato do arquivo de saída, que pode ser 'csv' ou 'json'.
                
        Returns:
            None: 
                Não retorna nenhum valor, apenas vai exportar os registros para o arquivo especificado.
    '''
    if formato == 'csv':
        try:
            with open(arquivo, 'w', newline='', encoding='utf-8') as f:
                cabecalho = registros[0].keys() if registros else []
                writer = csv.DictWriter(f, fieldnames=cabecalho)
                writer.writeheader()
                writer.writerows(registros)
            print("Relatório exportado com sucesso!")
        except Exception as e:
            print(f"Erro ao exportar relatório CSV: {e}")
    elif formato == 'json':
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(registros, f, indent=4, ensure_ascii=False)
            print("Relatório exportado com sucesso!")
        except Exception as e:
            print(f"Erro ao exportar relatório JSON: {e}")
    else:
        print("Formato inválido. Use 'csv' ou 'json'.")

def agrupar_por(registros: list[dict]) -> None:
    '''
    Agrupa os registros por mês e tipo, calculando o total de cada um.

    Args:
        registros (List[Dict]): 
            Lista de dicionários contendo os registros financeiros.
            Cada registro contém uma chave 'data' com outra chave 'data_completa',
            e uma chave 'tipo' para categorizar o registro.

    Returns:
        None: 
           Imprime o resultado dos agrupamentos, mas não retorna nenhum valor.
    '''
    
    tipo_desejado = validar_tipo('Digite o tipo que deseja agrupar. [Receita, Despesa, Investimento]: ')
    while True:
        mes_desejado = input('Digite o mês e ano que deseja agrupar (mm/aaaa): ')
        try:
            mes_desejado = datetime.strptime(mes_desejado, '%m/%Y').strftime('%m/%Y')
            break
        except ValueError:
            print('Digite o mês e o ano de acordo com o exemplo: 05/2000')

    total_rendimento = 0
    valor = 0

    nenhum_registro = True

    for registro in registros:
        mes = datetime.strptime(registro['data']['data_completa'], '%d/%m/%Y').strftime('%m/%Y')
        if mes == mes_desejado and registro['tipo'] == tipo_desejado:
            nenhum_registro = False
            if tipo_desejado == 'Investimento':
                valor += float(registro['valor'])
                total_rendimento += float(registro.get('rendimento', 0))
            else:
                valor += float(registro['valor'])

    if nenhum_registro:
        print(f'Nenhum registro encontrado para {mes_desejado} com o tipo {tipo_desejado}.')
    else:
        if tipo_desejado == 'Investimento':
            print(f'Total investido em {mes_desejado}: {valor}')
            print(f'Total do rendimento em {mes_desejado}: {total_rendimento}')
        else:
            print(f'Total para {mes_desejado} ({tipo_desejado}): {valor}')

def menu():
    """Exibe o menu interativo e processa as escolhas do usuário."""

    arquivo = 'financas.json'
    registros = ler_registros(arquivo)

    while True:
        print("\n--- Menu ---")
        print("1. Criar registro")
        print("2. Ler registros")
        print("3. Atualizar registro")
        print("4. Deletar registro")
        print("5. Atualizar rendimento")
        print("6. Exportar relatório")
        print("7. Agrupar por mês e tipo")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            novo_registro = criar_registro()
            registros.append(novo_registro)
            salvar_registros(registros, arquivo)
            print("Registro criado com sucesso!")
        elif opcao == '2':
            registros_filtrados = ler_registros_por(registros)
            if registros_filtrados:
                for registro in registros_filtrados:
                    print(registro)
            else:
                print("Nenhum registro encontrado.")
        elif opcao == '3':
            atualizar_registro(registros)
            salvar_registros(registros, arquivo)
        elif opcao == '4':
            deletar_registro(registros)
            salvar_registros(registros, arquivo)
        elif opcao == '5':
            atualiza_rendimento(registros)
            salvar_registros(registros, arquivo)
            print("Rendimento atualizado!")
        elif opcao == '6':
            formato = input("Formato do relatório (csv ou json): ")
            exportar_relatorio(registros, 'relatorio.' + formato, formato)
        elif opcao == '7':
            resultado = agrupar_por(registros)
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
