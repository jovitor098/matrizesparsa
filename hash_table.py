from lista_ligada import ListaLigada

CAPACIDADE = 10000

class HashTable:
    def __init__(self):
        self.capacidade = CAPACIDADE               
        self.tabela = [None] * self.capacidade     
    
    # Função hash: mapeia um par (i, j) para um índice dentro da capacidade
    def hash(self, chave):
        # chave é uma tupla (i, j)
        return (103 * chave[0] + 31 * chave[1]) % self.capacidade
    
    # Obtém o valor associado à chave
    def obter(self, chave):
        index = self.hash(chave)                   # Calcula o index
        if self.tabela[index] is None:             # Nenhum elemento 
            return 0                               # Valor padrão
        return self.tabela[index].obter(chave)     # Busca na lista ligada
    
    # Insere um elemento na tabela hash
    def inserir(self, chave, valor):
        # Se valor for 0, remove
        if valor == 0:
            self.remover(chave)
            return
        
        index = self.hash(chave)

        # Se estiver vazio, cria uma nova lista ligada
        if self.tabela[index] is None:
            self.tabela[index] = ListaLigada()
        
        # Insere ou atualiza na lista ligada
        self.tabela[index].inserir(chave, valor)
    
    # Remove um elemento da tabela hash
    def remover(self, chave):
        index = self.hash(chave)

        if self.tabela[index] is not None:
            # Remove da lista ligada
            self.tabela[index].remover(chave)
    
    # Retorna todos os itens armazenados como lista de pares (chave, valor)
    def obter_todos_itens(self):
        todos_itens = []

        # Percorre todos os elementos
        for lista in self.tabela:
            if lista is not None:
                # Adiciona todos os elementos da lista ligada
                todos_itens.extend(lista.obter_todos_itens())
        
        return todos_itens
