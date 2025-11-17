class No:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
        self.proximo = None

class ListaLigada:
    def __init__(self):
        self.cabeca = None
        self.tamanho = 0
    
    def inserir(self, chave, valor):
        novo_no = No(chave, valor)
        if self.cabeca is None:
            self.cabeca = novo_no
        else:
            atual = self.cabeca
            while atual.proximo is not None:
                if atual.chave == chave:
                    atual.valor = valor
                    return
                atual = atual.proximo
            if atual.chave == chave:
                atual.valor = valor
            else:
                atual.proximo = novo_no
        self.tamanho += 1

    def inserir_inicio(self, chave, valor):
        novo_no = No(chave, valor)
        novo_no.proximo = self.cabeca
        self.cabeca = novo_no
        self.tamanho += 1
    
    def obter(self, chave):
        atual = self.cabeca
        while atual is not None:
            if atual.chave == chave:
                return atual.valor
            atual = atual.proximo
        return 0
    
    def remover(self, chave):
        if self.cabeca is None:
            return
        
        if self.cabeca.chave == chave:
            self.cabeca = self.cabeca.proximo
            self.tamanho -= 1
            return
        
        anterior = self.cabeca
        atual = self.cabeca.proximo
        while atual is not None:
            if atual.chave == chave:
                anterior.proximo = atual.proximo
                self.tamanho -= 1
                return
            anterior = atual
            atual = atual.proximo
    
    def obter_todos_itens(self):
        itens = []
        atual = self.cabeca
        while atual is not None:
            itens.append((atual.chave, atual.valor))
            atual = atual.proximo
        return itens
    
    def obter_todas_chaves(self):
        chaves = []
        atual = self.cabeca
        while atual is not None:
            chaves.append(atual.chave)
            atual = atual.proximo
        return chaves
    
    def obter_todos_valores(self):
        valores = []
        atual = self.cabeca
        while atual is not None:
            valores.append(atual.valor)
            atual = atual.proximo
        return valores