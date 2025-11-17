from lista_ligada import ListaLigada


CAPACIDADE = 10000

class HashTable:
    def __init__(self):
        self.capacidade = CAPACIDADE
        self.tabela = [None] * self.capacidade
        self.quantidade = 0
    
    def hash(self, chave):
        return (103 * chave[0] + 31 * chave[1]) % self.capacidade
    
    def obter(self, chave):
        index = self.hash(chave)
        if self.tabela[index] is None:
            return 0
        return self.tabela[index].obter(chave)
    
    def inserir(self, chave, valor):
        if valor == 0:
            self.remover(chave)
            return
        
        index = self.hash(chave)
        if self.tabela[index] is None:
            self.tabela[index] = ListaLigada()
        
        valor_antigo = self.tabela[index].obter(chave)
        self.tabela[index].inserir(chave, valor)
        
        if valor_antigo == 0:
            self.quantidade += 1
    
    def remover(self, chave):
        index = self.hash(chave)
        if self.tabela[index] is not None:
            valor_antigo = self.tabela[index].obter(chave)
            self.tabela[index].remover(chave)
            if valor_antigo != 0:
                self.quantidade -= 1
    
    def obter_todos_itens(self):
        todos_itens = []
        for lista in self.tabela:
            if lista is not None:
                todos_itens.extend(lista.obter_todos_itens())
        return todos_itens
    
    def obter_todas_chaves(self):
        todas_chaves = []
        for lista in self.tabela:
            if lista is not None:
                todas_chaves.extend(lista.obter_todas_chaves())
        return todas_chaves
    
    def obter_todos_valores(self):
        todos_valores = []
        for lista in self.tabela:
            if lista is not None:
                todos_valores.extend(lista.obter_todos_valores())
        return todos_valores

