from hash_table import HashTable, ListaLigada

class MatrizEsparsa1:
    def __init__(self, dados=None, transposta=False):
        self.dados = HashTable() if dados is None else dados
        self.transposta = transposta
    
    def obter(self, i, j):
        if self.transposta:
            i, j = j, i
        return self.dados.obter((i, j))
    
    def inserir(self, i, j, valor):
        if self.transposta:
            i, j = j, i
        
        if valor == 0:
            self.dados.remover((i, j))
        else:
            self.dados.inserir((i, j), valor)
    
    def transpor(self):
        return MatrizEsparsa1(self.dados, not self.transposta)
    
    def soma(self, outra):
        resultado = MatrizEsparsa1()
        
        itens = self.dados.obter_todos_itens()
        for chave, valor in itens:
            i, j = chave
            if self.transposta:
                i, j = j, i
            resultado.inserir(i, j, valor)
        
        itens_outra = outra.dados.obter_todos_itens()
        for chave, valor in itens_outra:
            i, j = chave
            if outra.transposta:
                i, j = j, i
            atual = resultado.obter(i, j)
            resultado.inserir(i, j, atual + valor)
        
        return resultado
    
    def multiplicar_escalar(self, escalar):
        resultado = MatrizEsparsa1()
        itens = self.dados.obter_todos_itens()
        for chave, valor in itens:
            i, j = chave
            if self.transposta:
                i, j = j, i
            resultado.inserir(i, j, valor * escalar)
        return resultado
    
    def multiplicar(self, outra):
        itens_dados_A = self.dados.obter_todos_itens()
        
        linhas_B = HashTable()
        itens_dados_B = outra.dados.obter_todos_itens()
        for chave, valor in itens_dados_B:
            i, j = chave
            if outra.transposta:
                i, j = j, i
            
            linha = linhas_B.obter((i, 0))
            if linha == 0:
                linha = ListaLigada()
                linhas_B.inserir((i, 0), linha)
            linha.inserir_inicio(j, valor) 
        
        resultado = MatrizEsparsa1()
        
        # Para cada elemento A[i,k] (ka elementos total)
        for chave, valor_A in itens_dados_A:
            i, k = chave
            if self.transposta:
                i, k = k, i
            # Acessa linha k de B 
            linha_B = linhas_B.obter((k, 0))
            if linha_B != 0:
                elementos_B = linha_B.obter_todos_itens()
                
                # Para cada elemento B[k,j] (db elementos em média)
                for j, valor_B in elementos_B:
                    atual = resultado.obter(i, j)
                    resultado.inserir(i, j, atual + valor_A * valor_B)
        
        return resultado
