from flask import Flask, jsonify, Response
import requests
import csv
from io import StringIO

app = Flask(__name__)

# Configurações básicas da API externa
URL_BASE_API = "https://sidebar.stract.to/api"
TOKEN = "ProcessoSeletivoStract2025"

def gerar_csv(dados):
    """
    Converte uma lista de dados em formato CSV.
    
    Args:
        dados: Lista de dicionários contendo os dados a serem convertidos
        
    Returns:
        String no formato CSV ou string vazia se não houver dados
    """
    if not dados:
        return ""
    
    saida = StringIO()
    # Pega as colunas do primeiro item para criar o cabeçalho
    colunas = list(dados[0].keys())
    escritor = csv.DictWriter(saida, fieldnames=colunas)
    escritor.writeheader()
    
    for linha in dados:
        escritor.writerow(linha)
    
    return saida.getvalue()

def buscar_contas(plataforma):
    """
    Obtém a lista de contas de anúncios de uma determinada plataforma.
    
    Args:
        plataforma: Nome da plataforma de anúncios
        
    Returns:
        Lista de contas ou lista vazia em caso de erro
    """
    url = f"{URL_BASE_API}/accounts?platform={plataforma}&token={TOKEN}"
    try:
        resposta = requests.get(url)
        return resposta.json()
    except Exception as erro:
        print(f"Não foi possível obter as contas da plataforma {plataforma}: {erro}")
        return []

def buscar_metricas(plataforma, conta):
    """
    Obtém as métricas de desempenho de uma conta específica.
    
    Args:
        plataforma: Nome da plataforma de anúncios
        conta: Nome da conta de anúncios
        
    Returns:
        Lista de métricas ou lista vazia em caso de erro
    """
    url = f"{URL_BASE_API}/insights?platform={plataforma}&account={conta}&token={TOKEN}"
    try:
        resposta = requests.get(url)
        return resposta.json()
    except Exception as erro:
        print(f"Não foi possível obter as métricas da conta {conta} na plataforma {plataforma}: {erro}")
        return []

def agregar_dados(dados, chave_agrupamento):
    """
    Agrupa e soma os dados com base em uma chave específica.
    
    Args:
        dados: Lista de dicionários com os dados a serem agrupados
        chave_agrupamento: Chave usada para agrupar os dados
        
    Returns:
        Lista com os dados agregados
    """
    dados_agrupados = {}
    
    for linha in dados:
        chave = linha.get(chave_agrupamento)
        if chave is None:
            continue
            
        if chave not in dados_agrupados:
            dados_agrupados[chave] = dict(linha)
        else:
            for campo, valor in linha.items():
                if campo == chave_agrupamento:
                    continue
                if isinstance(valor, (int, float)):
                    dados_agrupados[chave][campo] = dados_agrupados[chave].get(campo, 0) + valor
                else:
                    dados_agrupados[chave][campo] = ""
                    
    return list(dados_agrupados.values())

@app.route('/')
def pagina_inicial():
    """
    Rota inicial que retorna informações do desenvolvedor.
    """
    return jsonify({
        "nome": "Guilherme Henrique",
        "email": "ghp17@outlook.com",
        "linkedin": "https://linkedin.com/in/ghpxd"
    })

@app.route('/<plataforma>', methods=['GET'])
def relatorio_plataforma(plataforma):
    """
    Gera um relatório detalhado dos anúncios de uma plataforma específica.
    
    Args:
        plataforma: Nome da plataforma desejada
        
    Returns:
        Arquivo CSV com os dados de todas as contas da plataforma
    """
    contas = buscar_contas(plataforma)
    lista_metricas = []
    
    for conta in contas:
        nome_conta = conta.get("name", "") if isinstance(conta, dict) else conta
        metricas = buscar_metricas(plataforma, nome_conta)
        
        for metrica in metricas:
            linha = {
                "Plataforma": plataforma,
                "Conta": nome_conta
            }
            linha.update(metrica)
            lista_metricas.append(linha)
            
    csv_gerado = gerar_csv(lista_metricas)
    return Response(csv_gerado, mimetype="text/csv")

@app.route('/<plataforma>/resumo', methods=['GET'])
def relatorio_resumido_plataforma(plataforma):
    """
    Gera um relatório resumido dos anúncios de uma plataforma, agrupado por conta.
    
    Args:
        plataforma: Nome da plataforma desejada
        
    Returns:
        Arquivo CSV com os dados agregados por conta
    """
    contas = buscar_contas(plataforma)
    lista_metricas = []
    
    for conta in contas:
        nome_conta = conta.get("name", "") if isinstance(conta, dict) else conta
        metricas = buscar_metricas(plataforma, nome_conta)
        
        for metrica in metricas:
            linha = {"Conta": nome_conta}
            linha.update(metrica)
            lista_metricas.append(linha)
            
    resumo = agregar_dados(lista_metricas, "Conta")
    csv_gerado = gerar_csv(resumo)
    return Response(csv_gerado, mimetype="text/csv")

@app.route('/geral', methods=['GET'])
def relatorio_geral():
    """
    Gera um relatório completo com dados de todas as plataformas.
    Para o Google Analytics, calcula também o custo por clique.
    
    Returns:
        Arquivo CSV com todos os dados de todas as plataformas
    """
    url_plataformas = f"{URL_BASE_API}/platforms?token={TOKEN}"
    try:
        resposta = requests.get(url_plataformas)
        plataformas = resposta.json()
    except Exception as erro:
        print(f"Não foi possível obter a lista de plataformas: {erro}")
        plataformas = []
    
    dados_gerais = []
    for plataforma in plataformas:
        nome_plataforma = plataforma.get("name", "") if isinstance(plataforma, dict) else plataforma
        contas = buscar_contas(nome_plataforma)
        
        for conta in contas:
            nome_conta = conta.get("name", "") if isinstance(conta, dict) else conta
            metricas = buscar_metricas(nome_plataforma, nome_conta)
            
            for metrica in metricas:
                linha = {
                    "Plataforma": nome_plataforma,
                    "Conta": nome_conta
                }
                linha.update(metrica)
                
                # Calcula custo por clique apenas para Google Analytics
                if nome_plataforma.lower() == "google analytics":
                    gastos = linha.get("spend", 0)
                    cliques = linha.get("clicks", 0)
                    try:
                        custo_por_clique = gastos / cliques if cliques != 0 else 0
                    except Exception:
                        custo_por_clique = 0
                    linha["Custo por Clique"] = custo_por_clique
                    
                dados_gerais.append(linha)
                
    csv_gerado = gerar_csv(dados_gerais)
    return Response(csv_gerado, mimetype="text/csv")

@app.route('/geral/resumo', methods=['GET'])
def relatorio_geral_resumido():
    """
    Gera um relatório resumido com dados agregados de todas as plataformas.
    
    Returns:
        Arquivo CSV com dados agregados por plataforma
    """
    url_plataformas = f"{URL_BASE_API}/platforms?token={TOKEN}"
    try:
        resposta = requests.get(url_plataformas)
        plataformas = resposta.json()
    except Exception as erro:
        print(f"Não foi possível obter a lista de plataformas: {erro}")
        plataformas = []
    
    dados_gerais = []
    for plataforma in plataformas:
        nome_plataforma = plataforma.get("name", "") if isinstance(plataforma, dict) else plataforma
        contas = buscar_contas(nome_plataforma)
        
        for conta in contas:
            nome_conta = conta.get("name", "") if isinstance(conta, dict) else conta
            metricas = buscar_metricas(nome_plataforma, nome_conta)
            
            for metrica in metricas:
                linha = {
                    "Plataforma": nome_plataforma,
                    "Conta": nome_conta
                }
                linha.update(metrica)
                
                if nome_plataforma.lower() == "google analytics":
                    gastos = linha.get("spend", 0)
                    cliques = linha.get("clicks", 0)
                    try:
                        custo_por_clique = gastos / cliques if cliques != 0 else 0
                    except Exception:
                        custo_por_clique = 0
                    linha["Custo por Clique"] = custo_por_clique
                    
                dados_gerais.append(linha)
                
    resumo = agregar_dados(dados_gerais, "Plataforma")
    csv_gerado = gerar_csv(resumo)
    return Response(csv_gerado, mimetype="text/csv")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)