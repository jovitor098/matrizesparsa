class No:
    def __init__(self, chave, valor):
        self.chave = chave     
        self.valor = valor      
        self.proximo = None    

class ListaLigada:
    def __init__(self):
        self.cabeca = None     
    
    # Insere um nó no final da lista ou atualiza caso a chave já exista
    def inserir(self, chave, valor):
        novo_no = No(chave, valor)
        
        # Lista vazia
        if self.cabeca is None:
            self.cabeca = novo_no
        else:
            atual = self.cabeca

            # Percorre a lista procurando chave
            while atual.proximo is not None:
                # Se a chave já existir, atualiza o valor e sai
                if atual.chave == chave:
                    atual.valor = valor
                    return
                atual = atual.proximo
            
            # Verifica o último nó após sair do laço
            if atual.chave == chave:
                atual.valor = valor
            else:
                atual.proximo = novo_no


    # Insere no início da lista
    def inserir_inicio(self, chave, valor):
        novo_no = No(chave, valor)
        novo_no.proximo = self.cabeca  # Aponta para o antigo primeiro nó
        self.cabeca = novo_no          # Atualiza a cabeça da lista
    
    # Obtém o valor associado a uma chave
    def obter(self, chave):
        atual = self.cabeca
        while atual is not None:
            if atual.chave == chave:
                return atual.valor
            atual = atual.proximo
        return 0  # Retorna 0 caso não exista
    
    # Remove o nó que possui a chave dada
    def remover(self, chave):
        # Lista vazia
        if self.cabeca is None:
            return
        
        # Caso o nó a remover seja o primeiro
        if self.cabeca.chave == chave:
            self.cabeca = self.cabeca.proximo
            return
        
        # Percorre procurando o nó a remover
        anterior = self.cabeca
        atual = self.cabeca.proximo
        while atual is not None:
            if atual.chave == chave:
                # Remove ligando o anterior ao próximo
                anterior.proximo = atual.proximo
                return
            anterior = atual
            atual = atual.proximo
    
    # Retorna todos os pares (chave, valor) da lista
    def obter_todos_itens(self):
        itens = []
        atual = self.cabeca
        # Percorre toda a lista e adiciona à lista de retorno
        while atual is not None:
            itens.append((atual.chave, atual.valor))
            atual = atual.proximo
        return itens
