import pandas as pd
import networkx as nx

def ler_bairros_recife():
    """
    Lê o arquivo CSV de bairros do Recife e extrai a lista de bairros e suas conexões.
    """
    try:
        # Lê o arquivo CSV
        df = pd.read_csv('bairros_recife.csv')
        
        # Extrai todos os bairros únicos (ignorando células vazias)
        bairros = set()
        conexoes = []
        
        # Processa cada linha do CSV
        for _, row in df.iterrows():
            # Filtra células não vazias
            bairros_linha = [bairro for bairro in row if pd.notna(bairro) and bairro.strip()]
            bairros.update(bairros_linha)
            
            # Cria conexões entre bairros da mesma linha
            for i in range(len(bairros_linha) - 1):
                conexoes.append((bairros_linha[i], bairros_linha[i + 1]))
        
        # Converte o conjunto de bairros para lista
        bairros = sorted(list(bairros))
        
        print("\nBairros do Recife encontrados:")
        for bairro in bairros:
            print(f"- {bairro}")
            
        print(f"\nTotal de bairros encontrados: {len(bairros)}")
        print(f"Total de conexões encontradas: {len(conexoes)}")
        
        return bairros, conexoes
        
    except FileNotFoundError:
        print("Erro: Arquivo 'bairros_recife.csv' não encontrado.")
        return None, None
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")
        return None, None

def criar_grafo_bairros(bairros, conexoes):
    """
    Cria um grafo onde os vértices são os bairros do Recife
    e as arestas representam conexões entre bairros vizinhos.
    """
    if bairros is None or conexoes is None:
        return None
        
    # Cria um grafo vazio
    G = nx.Graph()
    
    # Adiciona os bairros como vértices
    G.add_nodes_from(bairros)
    
    # Adiciona as conexões ao grafo
    G.add_edges_from(conexoes)
    
    return G

def salvar_conexoes_csv(G, nome_arquivo='conexoes_bairros.csv'):
    """
    Salva as conexões entre os bairros em um arquivo CSV.
    
    Args:
        G: Grafo com as conexões
        nome_arquivo: Nome do arquivo CSV a ser salvo
    """
    if G is None:
        return
        
    # Cria um DataFrame vazio
    conexoes_df = pd.DataFrame(columns=['Bairro', 'Rua de ligação', 'Bairro de destino'])
    
    # Adiciona cada conexão ao DataFrame
    for origem, destino in G.edges():
        # Usa o nome da rua como a conexão entre os bairros
        rua = f"Rua entre {origem} e {destino}"
        
        # Adiciona a conexão ao DataFrame
        nova_linha = pd.DataFrame({
            'Bairro': [origem],
            'Rua de ligação': [rua],
            'Bairro de destino': [destino]
        })
        conexoes_df = pd.concat([conexoes_df, nova_linha], ignore_index=True)
    
    # Salva o DataFrame em um arquivo CSV
    conexoes_df.to_csv(nome_arquivo, index=False)
    print(f"\nArquivo {nome_arquivo} salvo com sucesso!")

def analisar_grafo(G):
    """
    Realiza análises básicas do grafo.
    """
    if G is None:
        return
        
    print("\nAnálise do Grafo:")
    print(f"Número de bairros (vértices): {G.number_of_nodes()}")
    print(f"Número de conexões (arestas): {G.number_of_edges()}")
    
    # Calcula o grau de cada bairro (número de conexões)
    graus = dict(G.degree())
    print("\nBairros com mais conexões:")
    for bairro, grau in sorted(graus.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{bairro}: {grau} conexões")

def main():
    """
    Função principal que executa todo o processo.
    """
    # 1. Lê os bairros e conexões do CSV
    bairros, conexoes = ler_bairros_recife()
    
    if bairros is not None and conexoes is not None:
        # 2. Cria o grafo
        G = criar_grafo_bairros(bairros, conexoes)
        
        if G is not None:
            # 3. Salva as conexões em CSV
            salvar_conexoes_csv(G)
            
            # 4. Analisa o grafo
            analisar_grafo(G)

if __name__ == "__main__":
    main() 