class No:
    def __init__(self, chave, valor):
        self.chave = chave      
        self.valor = valor      
        self.altura = 1          
        self.esquerda = None     
        self.direita = None     

# Implementação da Árvore AVL
class ArvoreAVL:
    def __init__(self):
        self.raiz = None         

    # Retorna a altura de um nó (0 se for None)
    def altura(self, no):
        if no is None:
            return 0
        return no.altura

    # Calcula o fator de balanceamento (altura esquerda - altura direita)
    def fator_balanceamento(self, no):
        if no is None:
            return 0
        return self.altura(no.esquerda) - self.altura(no.direita)

    # Atualiza a altura de um nó baseado nos filhos
    def atualizar_altura(self, no):
        if no:
            no.altura = 1 + max(self.altura(no.esquerda), self.altura(no.direita))

    # Rotação simples à direita
    def rotacao_direita(self, y):
        x = y.esquerda          # Novo topo da subárvore
        T2 = x.direita          # Subárvore temporária

        # Rotação
        x.direita = y
        y.esquerda = T2

        # Atualizar alturas
        self.atualizar_altura(y)
        self.atualizar_altura(x)

        return x                # Novo nó raiz da subárvore

    # Rotação simples à esquerda
    def rotacao_esquerda(self, x):
        y = x.direita           # Novo topo da subárvore
        t2 = y.esquerda         # Subárvore temporária

        # Rotação
        y.esquerda = x
        x.direita = t2

        # Atualizar alturas
        self.atualizar_altura(x)
        self.atualizar_altura(y)

        return y                # Novo nó raiz da subárvore

    # Balanceia um nó após inserção ou remoção
    def balancear(self, no):
        self.atualizar_altura(no)
        fator = self.fator_balanceamento(no)

        if fator > 1 and self.fator_balanceamento(no.esquerda) >= 0:
            return self.rotacao_direita(no)

        if fator < -1 and self.fator_balanceamento(no.direita) <= 0:
            return self.rotacao_esquerda(no)

        if fator > 1 and self.fator_balanceamento(no.esquerda) < 0:
            no.esquerda = self.rotacao_esquerda(no.esquerda)
            return self.rotacao_direita(no)

        if fator < -1 and self.fator_balanceamento(no.direita) > 0:
            no.direita = self.rotacao_direita(no.direita)
            return self.rotacao_esquerda(no)

        return no  # Já balanceado

    def inserir(self, chave, valor):
        # Se valor é zero, remove o nó em vez de inserir
        if valor == 0:
            self.remover(chave)
            return
        self.raiz = self.inserir_recursivo(self.raiz, chave, valor)

    def inserir_recursivo(self, no, chave, valor):
        if no is None:
            return No(chave, valor)

        # Inserção na subárvore esquerda
        if chave < no.chave:
            no.esquerda = self.inserir_recursivo(no.esquerda, chave, valor)
        # Inserção na subárvore direita
        elif chave > no.chave:
            no.direita = self.inserir_recursivo(no.direita, chave, valor)
        else:
            # Atualiza o valor caso a chave já exista
            no.valor = valor
            return no

        # Após inserir, balanceia a subárvore
        return self.balancear(no)

    def buscar(self, chave):
        return self.buscar_recursivo(self.raiz, chave)

    def buscar_recursivo(self, no, chave):
        if no is None:
            return 0              # Valor padrão se não encontrado
        if chave == no.chave:
            return no.valor
        elif chave < no.chave:
            return self.buscar_recursivo(no.esquerda, chave)
        else:
            return self.buscar_recursivo(no.direita, chave)

    # Retorna o nó mínimo da subárvore (menor chave)
    def minimo(self, no):
        if no is None or no.esquerda is None:
            return no
        return self.minimo(no.esquerda)

    def remover(self, chave):
        self.raiz = self.remover_recursivo(self.raiz, chave)

    def remover_recursivo(self, no, chave):
        if no is None:
            return no

        # Percorre à esquerda
        if chave < no.chave:
            no.esquerda = self.remover_recursivo(no.esquerda, chave)
        # Percorre à direita
        elif chave > no.chave:
            no.direita = self.remover_recursivo(no.direita, chave)
        # Nó encontrado
        else:
            # Caso 1: apenas filho direito
            if no.esquerda is None:
                return no.direita
            # Caso 2: apenas filho esquerdo
            elif no.direita is None:
                return no.esquerda
            # Caso 3: dois filhos
            else:
                sucessor = self.minimo(no.direita)
                no.chave = sucessor.chave
                no.valor = sucessor.valor
                # Remove o sucessor da subárvore direita
                no.direita = self.remover_recursivo(no.direita, sucessor.chave)

        # Balanceia na subida da recursão
        return self.balancear(no)

    # Percurso em ordem (retorna lista de pares)
    def percorrer(self):
        resultado = []
        self.percurso_recursivo(self.raiz, resultado)
        return resultado

    # Percurso em ordem
    def percurso_recursivo(self, no, resultado):
        if no:
            self.percurso_recursivo(no.esquerda, resultado)
            resultado.append((no.chave, no.valor))
            self.percurso_recursivo(no.direita, resultado)
