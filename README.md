# API de Relatórios de Anúncios

Uma API em Flask para geração de relatórios de métricas de anúncios de diversas plataformas. A aplicação se conecta com uma API externa para coletar dados e gera relatórios em formato CSV.

## 🚀 Funcionalidades

- Geração de relatórios detalhados por plataforma
- Relatórios resumidos com dados agregados
- Relatório geral com dados de todas as plataformas
- Cálculo automático de métricas (ex: custo por clique no Google Analytics)
- Exportação em formato CSV
- Tratamento de erros robusto

## 📋 Pré-requisitos

- Python 3.6 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd [NOME_DA_PASTA]
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

As principais configurações estão no início do arquivo:

```python
URL_BASE_API = "https://sidebar.stract.to/api"
TOKEN = "ProcessoSeletivoStract2025"
```

Certifique-se de que:
- A URL base da API está correta
- O token de acesso é válido

## 🖥️ Uso

1. Inicie o servidor:
```bash
python app.py
```

2. O servidor estará disponível em `http://127.0.0.1:8000`

### Endpoints Disponíveis

- **GET /** 
  - Retorna informações do desenvolvedor
  - Resposta em JSON

- **GET /{plataforma}**
  - Gera relatório detalhado de uma plataforma específica
  - Retorna arquivo CSV
  - Exemplo: `/google-analytics`

- **GET /{plataforma}/resumo**
  - Gera relatório resumido de uma plataforma
  - Dados agregados por conta
  - Retorna arquivo CSV
  - Exemplo: `/facebook/resumo`

- **GET /geral**
  - Relatório completo de todas as plataformas
  - Inclui cálculo de custo por clique para Google Analytics
  - Retorna arquivo CSV

- **GET /geral/resumo**
  - Relatório resumido de todas as plataformas
  - Dados agregados por plataforma
  - Retorna arquivo CSV

## 📊 Formato dos Dados

### Exemplo de Saída CSV
```csv
Plataforma,Conta,impressions,clicks,spend,Custo por Clique
Google Analytics,Conta1,1000,100,500,5.0
Facebook,Conta2,2000,150,600,
```

## 🛠️ Tecnologias Utilizadas

- [Flask](https://flask.palletsprojects.com/) - Framework web
- [Requests](https://docs.python-requests.org/) - Cliente HTTP
- CSV - Biblioteca padrão Python para manipulação de arquivos CSV

## ✒️ Autor

* **Guilherme Henrique** - [ghpxd](https://linkedin.com/in/ghpxd)

## 📌 Observações Importantes

1. Todos os dados são obtidos em tempo real da API externa
2. Os relatórios são gerados dinamicamente
3. Erros de conexão são tratados graciosamente
4. Métricas específicas são calculadas para cada plataforma

## 🗂️ Estrutura do Projeto

```
.
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências do projeto
└── README.md          # Este arquivo
```

## 📄 Licença

Este projeto está sob a licença [MIT](https://opensource.org/licenses/MIT).

## 🚦 Status do Projeto

- ✅ Totalmente funcional
- ✅ Pronto para produção
- ✅ Documentação completa

## 💡 Exemplos de Uso

### Curl
```bash
# Obter relatório do Google Analytics
curl http://127.0.0.1:8000/google-analytics > relatorio_ga.csv

# Obter resumo geral
curl http://127.0.0.1:8000/geral/resumo > resumo_geral.csv
```

### Python
```python
import requests

# Obter relatório do Facebook
response = requests.get('http://127.0.0.1:8000/facebook')
with open('relatorio_facebook.csv', 'w') as f:
    f.write(response.text)
```

## ⚠️ Requisitos de Sistema

- Memória: 512MB RAM (mínimo)
- Espaço em disco: 100MB (mínimo)
- Sistema Operacional: Windows/Linux/MacOS
- Conexão com Internet: Obrigatória

## 🆘 Suporte

Em caso de dúvidas ou problemas, entre em contato através do email: ghp17@outlook.com
