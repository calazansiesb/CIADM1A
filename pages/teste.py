import pandas as pd
import numpy as np

# Criando dados fictícios com base nas colunas fornecidas
np.random.seed(42)
num_rows = 100

data = {
    'SIST_CRIA': np.random.choice(['Ovos para Consumo', 'Frangos de Corte', 'Ovos para Incubação', 'Outros'], size=num_rows),
    'NIV_TERR': np.random.choice([1, 2, 3], size=num_rows, p=[0.7, 0.2, 0.1]),
    'COD_TERR': [f'{np.random.randint(10, 99):02d}' for _ in range(num_rows)],
    'NOM_TERR': np.random.choice(['São Paulo', 'Minas Gerais', 'Rio Grande do Sul', 'Paraná', 'Santa Catarina', 
                                'Goiás', 'Mato Grosso', 'Bahia', 'Pernambuco', 'Ceará'], size=num_rows),
    'CL_GAL': np.random.randint(1, 5, size=num_rows),
    'NOM_CL_GAL': np.random.choice(['Pequeno', 'Médio', 'Grande', 'Industrial'], size=num_rows),
    'GAL_TOTAL': np.random.randint(1000, 50000, size=num_rows),
    'GAL_ENG': np.random.randint(0, 10000, size=num_rows),
    'GAL_GALOS': np.random.randint(0, 5000, size=num_rows),
    'GAL_POED': np.random.randint(0, 30000, size=num_rows),
    'GAL_MATR': np.random.randint(0, 10000, size=num_rows),
    'GAL_VEND': np.random.randint(0, 40000, size=num_rows),
    'V_GAL_VEND': np.random.uniform(1000, 50000, size=num_rows).round(2),
    'Q_DZ_PROD': np.random.randint(0, 10000, size=num_rows),
    'Q_DZ_VEND': np.random.randint(0, 9000, size=num_rows),
    'V_Q_DZ_PROD': np.random.uniform(500, 20000, size=num_rows).round(2),
    'V_Q_DZ_VEND': np.random.uniform(500, 18000, size=num_rows).round(2),
    'A_TOTAL': np.random.uniform(1, 100, size=num_rows).round(2),
    'A_PAST_PLANT': np.random.uniform(0, 50, size=num_rows).round(2),
    'A_LAV_PERM': np.random.uniform(0, 30, size=num_rows).round(2),
    'A_LAV_TEMP': np.random.uniform(0, 40, size=num_rows).round(2),
    'A_APPRL': np.random.uniform(0, 20, size=num_rows).round(2),
    'N_TRAB_TOTAL': np.random.randint(1, 20, size=num_rows),
    'N_TRAB_LACOS': np.random.randint(0, 10, size=num_rows)
}

# Adicionando colunas binárias (0 ou 1) para as colunas que começam com "E_"
prefixos_E = ['CRIA_GAL', 'TEM_GAL', 'GAL_VEND', 'OVOS_PROD', 'OVOS_VEND', 'SUBS', 'COMERC', 
              'RECEBE_ORI', 'ORI_GOV', 'ORI_PROPRIA', 'ORI_COOP', 'ORI_EMP_INT', 'ORI_EMP_PRIV',
              'ORI_ONG', 'ORI_SIST_S', 'ORI_OUTRA', 'GAL_ENG', 'GAL_GALOS', 'GAL_POED', 'GAL_MATR',
              'ASSOC_COOP', 'FINANC', 'FINANC_COOP', 'FINANC_INTEG', 'DAP', 'AGRIFAM', 'N_AGRIFAM',
              'PRODUTOR', 'COOPERATIVA', 'SA_LDTA', 'CNPJ']

for prefix in prefixos_E:
    col_name = f'E_{prefix}'
    data[col_name] = np.random.choice([0, 1], size=num_rows, p=[0.3, 0.7])

# Criando o DataFrame
df = pd.DataFrame(data)

# Adicionando alguns valores nulos para simular dados reais
for col in df.columns:
    if np.random.rand() > 0.8:  # 20% de chance de adicionar nulos em cada coluna
        idx = np.random.choice(df.index, size=int(num_rows*0.1), replace=False)  # 10% dos valores
        df.loc[idx, col] = np.nan

# Ordenando as colunas para manter a mesma ordem do seu DataFrame original
col_order = [
    'SIST_CRIA', 'NIV_TERR', 'COD_TERR', 'NOM_TERR', 'CL_GAL', 'NOM_CL_GAL',
    'E_CRIA_GAL', 'E_TEM_GAL', 'E_GAL_VEND', 'E_OVOS_PROD', 'E_OVOS_VEND', 'E_SUBS',
    'E_COMERC', 'E_RECEBE_ORI', 'E_ORI_GOV', 'E_ORI_PROPRIA', 'E_ORI_COOP',
    'E_ORI_EMP_INT', 'E_ORI_EMP_PRIV', 'E_ORI_ONG', 'E_ORI_SIST_S', 'E_ORI_OUTRA',
    'E_GAL_ENG', 'E_GAL_GALOS', 'E_GAL_POED', 'E_GAL_MATR', 'E_ASSOC_COOP',
    'E_FINANC', 'E_FINANC_COOP', 'E_FINANC_INTEG', 'E_DAP', 'E_AGRIFAM',
    'E_N_AGRIFAM', 'E_PRODUTOR', 'E_COOPERATIVA', 'E_SA_LDTA', 'E_CNPJ',
    'GAL_TOTAL', 'GAL_ENG', 'GAL_GALOS', 'GAL_POED', 'GAL_MATR', 'GAL_VEND',
    'V_GAL_VEND', 'Q_DZ_PROD', 'Q_DZ_VEND', 'V_Q_DZ_PROD', 'V_Q_DZ_VEND',
    'A_TOTAL', 'A_PAST_PLANT', 'A_LAV_PERM', 'A_LAV_TEMP', 'A_APPRL',
    'VTP_AGRO', 'RECT_AGRO', 'N_TRAB_TOTAL', 'N_TRAB_LACOS'
]

# Mantendo apenas as colunas que temos dados (algumas não foram simuladas)
available_cols = [col for col in col_order if col in df.columns]
df = df[available_cols]

# Exibindo informações do DataFrame
print(f"DataFrame criado com {len(df)} linhas e {len(df.columns)} colunas")
print("Colunas disponíveis:", df.columns.tolist())
