from arvore import ArvoreAVL

class MatrizEsparsa2:
    def __init__(self, dados=None, transposta=False):
        self.dados = ArvoreAVL() if dados is None else dados
        self.transposta = transposta
    
    # Obtém o valor na posição (i, j)
    def obter(self, i, j):
        # Se a matriz atual é uma transposta, inverte índices
        if self.transposta:
            i, j = j, i
        return self.dados.buscar((i, j))

    # Insere valor na posição (i, j)
    def inserir(self, i, j, valor):
        # Se transposta, troca índices
        if self.transposta:
            i, j = j, i
        self.dados.inserir((i, j), valor)
    
    # Retorna uma nova matriz esparsa, mas com transposta alternada
    def transpor(self):
        # Mantém os mesmos dados; apenas alterna o flag de transposição
        return MatrizEsparsa2(self.dados, not self.transposta)
    
    # Soma duas matrizes esparsas
    def soma(self, outra):
        resultado = MatrizEsparsa2()
    
        # Copia todos os elementos da primeira matriz
        for (i, j), valor in self.dados.percorrer():
            # Ajusta indices se estiver transposta
            if self.transposta:
                i, j = j, i
            resultado.inserir(i, j, valor)
            
        # Percorre elementos da segunda matriz e soma no resultado
        for (i, j), valor in outra.dados.percorrer():
            if outra.transposta:
                i, j = j, i
            # Busca o valor atual e soma
            valor_atual = resultado.obter(i, j)
            resultado.inserir(i, j, valor_atual + valor)

        return resultado
    
    # Multiplicação por escalar 
    def multiplicar_escalar(self, escalar):
        # Cria matriz resultado que compartilha os mesmos dados
        resultado = MatrizEsparsa2(self.dados, self.transposta)
        # Multiplica cada nó da AVL pelo escalar
        self.multiplicar_auxiliar(self.dados.raiz, escalar)
        return resultado
    
    # Função recursiva para multiplicação por escalar em todos os nós
    def multiplicar_auxiliar(self, raiz, escalar):
        if raiz is None:
            return
        # Percorre em ordem e multiplica cada valor
        self.multiplicar_auxiliar(raiz.esquerda, escalar)
        raiz.valor *= escalar
        self.multiplicar_auxiliar(raiz.direita, escalar)
    
    # Multiplicação entre matrizes esparsas
    def multiplicar(self, outra):
        resultado = MatrizEsparsa2()

        # Lista todos os elementos não-nulos de A e B
        itens_dados_A = self.dados.percorrer()
        itens_dados_B = outra.dados.percorrer()

        # Para cada elemento A(i, ka)
        for (i, ka), valor_A in itens_dados_A:
            # Ajustar indices se A for transposta
            if self.transposta:
                i, ka = ka, i

            # Para cada elemento B(kb, j)
            for (kb, j), valor_B in itens_dados_B:
                # Ajustar indices se B for transposta
                if outra.transposta:
                    kb, j = j, kb

                # Resultado(i, j) += A(i, k) * B(k, j)
                if ka == kb:
                    # Somar produto na posição (i, j)
                    valor_atual = resultado.obter(i, j)
                    resultado.inserir(i, j, valor_atual + (valor_A * valor_B))
        
        return resultado