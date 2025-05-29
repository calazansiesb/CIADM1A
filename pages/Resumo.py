import pandas as pd
import requests

# URL do dataset no GitHub (link raw)
URL_CSV = "https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv"

# Carregar os dados
df = pd.read_csv(URL_CSV)

# Calcular matriz de correlação
matriz_correlacao = df.corr()

# Salvar o arquivo localmente
matriz_correlacao.to_csv("correlacao_resultado.csv")

# Configuração do GitHub para upload
GITHUB_REPO = "calazansiesb/CIADM1A"
GITHUB_FILE_PATH = "correlacao_resultado.csv"
GITHUB_TOKEN = "seu_token_aqui"  # Substitua pelo seu token do GitHub

# Leitura do arquivo CSV gerado
with open("correlacao_resultado.csv", "r") as f:
    data = f.read()

# URL para atualização no GitHub
url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"

# Obter SHA do arquivo existente (necessário para sobrescrever)
response = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
sha = response.json()["sha"] if response.status_code == 200 else None

# Criar payload para upload no GitHub
payload = {
    "message": "Atualizando matriz de correlação",
    "content": data.encode("utf-8").decode("latin1"),  # Codificação correta
    "branch": "main"
}

if sha:
    payload["sha"] = sha  # Necessário para sobrescrever arquivo existente

# Enviar para GitHub
response = requests.put(url, json=payload, headers={"Authorization": f"token {GITHUB_TOKEN}"})

if response.status_code in [200, 201]:
    print("Arquivo atualizado no GitHub com sucesso!")
else:
    print("Erro ao atualizar o arquivo:", response.text)
