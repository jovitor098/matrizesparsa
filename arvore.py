
class No:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
        self.altura = 1
        self.esquerda = None
        self.direita = None

class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def altura(self, no):
        if no is None:
            return 0
        return no.altura

    def fator_balanceamento(self, no):
        if no is None:
            return 0
        return self.altura(no.esquerda) - self.altura(no.direita)

    def atualizar_altura(self, no):
        if no:
            no.altura = 1 + max(self.altura(no.esquerda), self.altura(no.direita))

    def rotacao_direita(self, y):
        x = y.esquerda
        T2 = x.direita

        x.direita = y
        y.esquerda = T2

        self.atualizar_altura(y)
        self.atualizar_altura(x)

        return x

    def rotacao_esquerda(self, x):
        y = x.direita
        T2 = y.esquerda

        y.esquerda = x
        x.direita = T2

        self.atualizar_altura(x)
        self.atualizar_altura(y)

        return y

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

        return no

    def inserir(self, chave, valor):
        if valor == 0:
            self.remover(chave)
        self.raiz = self.inserir_recursivo(self.raiz, chave, valor)

    def inserir_recursivo(self, no, chave, valor):
        if no is None:
            return No(chave, valor)

        if chave < no.chave:
            no.esquerda = self.inserir_recursivo(no.esquerda, chave, valor)
        elif chave > no.chave:
            no.direita = self.inserir_recursivo(no.direita, chave, valor)
        else:
            no.valor = valor
            return no

        return self.balancear(no)

    def buscar(self, chave):
        return self.buscar_recursivo(self.raiz, chave)

    def buscar_recursivo(self, no, chave):
        if no is None:
            return None
        if chave == no.chave:
            return no.valor
        elif chave < no.chave:
            return self.buscar_recursivo(no.esquerda, chave)
        else:
            return self.buscar_recursivo(no.direita, chave)

    def minimo(self, no):
        if no is None or no.esquerda is None:
            return no
        return self.minimo(no.esquerda)

    def remover(self, chave):
        self.raiz = self.remover_recursivo(self.raiz, chave)

    def remover_recursivo(self, no, chave):
        if no is None:
            return no

        if chave < no.chave:
            no.esquerda = self.remover_recursivo(no.esquerda, chave)
        elif chave > no.chave:
            no.direita = self.remover_recursivo(no.direita, chave)
        else:
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda
            else:
                sucessor = self.minimo(no.direita)
                no.chave = sucessor.chave
                no.valor = sucessor.valor
                no.direita = self.remover_recursivo(no.direita, sucessor.chave)

        return self.balancear(no)
    