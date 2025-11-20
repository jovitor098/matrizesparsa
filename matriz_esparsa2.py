from arvore import ArvoreAVL


class MatrizEsparsa2:
    def __init__(self, dados=None, transposta=False):
        self.dados = ArvoreAVL() if dados is None else dados
        self.transposta = transposta
    
    def obter(self, i, j):
        if self.transposta:
            i, j = j, i
        return self.dados.buscar((i, j))
    def inserir(self, i, j, valor):
        if self.transposta:
            i, j = j, i
        self.dados.inserir((i, j), valor)
    
    def transpor(self):
        return MatrizEsparsa2(self.dados, not self.transposta)
    
    def soma(self, outra):
        resultado = MatrizEsparsa2()
    
        for (i, j), valor in self.dados.percorrer():
                if self.transposta:
                    i, j = j, i
                resultado.inserir(i, j, valor)
            
        for (i, j), valor in outra.dados.percorrer():
            if outra.transposta:
                i, j = j, i
            valor_atual = resultado.obter(i, j)
            resultado.inserir(i, j, valor_atual + valor)
        return resultado
    
    def multiplicar_escalar(self, escalar):
        resultado = MatrizEsparsa2(self.dados, self.transposta)
        self.multiplicar_auxiliar(self.dados.raiz, escalar)
        return resultado
    
    def multiplicar_auxiliar(self, raiz, escalar):
        if raiz is None:
            return
        self.multiplicar_auxiliar(raiz.esquerda, escalar)
        raiz.valor *= escalar
        self.multiplicar_auxiliar(raiz.direita, escalar)
    
    def multiplicar(self, outra):
        resultado = MatrizEsparsa2()
        itens_dados_A = self.dados.percorrer()
        itens_dados_B = outra.dados.percorrer()
        for (i, ka), valor_A in itens_dados_A:
            if self.transposta:
                i, ka = ka, i
            for (kb, j), valor_B in itens_dados_B:
                if outra.transposta:
                    kb, j = j, kb
                if ka == kb:
                    valor_atual = resultado.obter(i, j)
                    resultado.inserir(i, j, valor_atual + (valor_A * valor_B))
        
        return resultado
