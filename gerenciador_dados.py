# gerenciador_dados.py
import os
import json
from datetime import datetime
from config import ARQUIVO_DADOS, LIVROS_INICIAIS

def carregar_dados():
    """Carrega dados do arquivo ou cria nova estrutura"""
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                
                # Converter estrutura antiga para nova
                for usuario in dados['usuarios'].values():
                    livros_atualizados = []
                    for livro in usuario['livros']:
                        if isinstance(livro, str):
                            livros_atualizados.append({
                                'titulo': livro,
                                'data_emprestimo': datetime.now().strftime("%d/%m/%Y %H:%M")
                            })
                        else:
                            livros_atualizados.append(livro)
                    usuario['livros'] = livros_atualizados
                
                # Garante que os livros são uma lista válida
                if not isinstance(dados['livros'], list):
                    dados['livros'] = LIVROS_INICIAIS.copy()
                else:
                    for categoria in dados['livros']:
                        if not isinstance(categoria, dict) or 'itens' not in categoria:
                            dados['livros'] = LIVROS_INICIAIS.copy()
                            break
                
                return dados
        except Exception as e:
            print(f"Erro ao carregar dados: {e}. Criando nova base...")
    
    return {
        'usuarios': {},
        'livros': LIVROS_INICIAIS.copy(),
        'senha': 'admin'
    }

def salvar_dados(dados):
    """Salva dados no arquivo JSON"""
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
