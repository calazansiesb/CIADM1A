from pynto import Pynto, Text, Title, List, Highlight

pagina = Pynto(title="Análise de Dados de Avicultura - IBGE 2017")

# Título principal
pagina.add(Title("Principais Características para Análise na Avicultura (IBGE 2017)"))

# Texto introdutório
pagina.add(Text("De qualquer forma, pensando nas informações que geralmente estão presentes em dados de avicultura do IBGE, aqui estão algumas ideias de características interessantes que podemos explorar:"))

# Lista de tópicos destacados
topicos = [
    Highlight("Distribuição da produção por região:"),
    "Podemos analisar como a produção de aves (frangos, galinhas poedeiras, etc.) se distribui entre as diferentes regiões do Brasil em 2017. Isso pode revelar quais regiões são os principais polos de produção.",
    
    Highlight("Tipos de produção predominantes:"),
    "Identificar quais tipos de produção avícola (corte, postura) eram mais significativos em termos de volume ou valor em 2017.",
    
    Highlight("Variação da produção ao longo do ano:"),
    "Se os dados permitirem, podemos analisar a sazonalidade da produção, verificando se houve meses com maior ou menor produção.",
    
    Highlight("Tamanho dos estabelecimentos:"),
    "Podemos investigar a distribuição do tamanho dos estabelecimentos avícolas, por exemplo, classificando-os por número de aves ou volume de produção. Isso pode indicar se a produção é mais concentrada em grandes ou pequenos produtores.",
    
    Highlight("Relação entre o tipo de estabelecimento e a produção:"),
    "Analisar se existe uma correlação entre o tipo de estabelecimento (familiar, empresarial, etc.) e o volume ou tipo de produção.",
    
    Highlight("Comparação com anos anteriores (se disponível):"),
    "Embora o foco seja 2017, se você tiver acesso a dados de anos anteriores, podemos fazer comparações para identificar tendências de crescimento ou declínio na produção avícola.",
    
    Highlight("Potencial para segmentação:"),
    "Identificar grupos de municípios ou regiões com características de produção semelhantes, o que pode ser útil para direcionar políticas ou investimentos.",
    
    Highlight("Outras variáveis relevantes:"),
    "Dependendo das variáveis específicas do dataset, podemos explorar outros aspectos como a tecnologia utilizada, a destinação da produção (abate, ovos para consumo, etc.), ou a geração de emprego no setor."
]

pagina.add(List(topicos, numbered=False))

# Renderiza a página
pagina.render()
