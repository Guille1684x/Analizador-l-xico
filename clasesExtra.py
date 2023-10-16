import copy


class ItemLR0:
    def __init__(self, num_regla=-1, pos_punto=-1):
        self.numero_regla = num_regla
        self.pos_punto = pos_punto

    def to_string(self):
        return f"[{self.numero_regla},{self.pos_punto}]"


class ItemLR1(object):
    def __init__(self, numero_regla=-1, pos_punto=-1, simbolo=""):
        self.numero_regla = numero_regla
        self.pos_punto = pos_punto

        self.simbolo = simbolo

    def to_string(self):
        return f"[{self.numero_regla},{self.pos_punto},{self.simbolo}]"


# noinspection DuplicatedCode
class SetItemsLR0(object):
    def __init__(self):
        self.conjunto = list()

        self.identificadores = list()

    def agregar(self, item: ItemLR0):
        # string_new = f"[{item.numero_regla},{item.pos_punto}]"
        hash_str = hash(item.to_string())

        if hash_str in self.identificadores:
            return

        self.conjunto.append(copy.deepcopy(item))
        self.identificadores.append(copy.deepcopy(hash_str))

    def unir(self, set_extra):
        for index, identificador in enumerate(set_extra.identificadores):
            if identificador in self.identificadores:
                continue

            self.agregar(copy.deepcopy(set_extra.conjunto[index]))

    def igual_a(self, set_extra):
        for identi in set_extra.identificadores:
            if identi not in self.identificadores:
                return False
        return True

    def tamano(self):
        return len(self.conjunto)

    def contiene(self, item: ItemLR0):
        # string_new = f"[{item.numero_regla},{item.pos_punto}]"
        hash_str = hash(item.to_string())

        if hash_str in self.identificadores:
            return True
        return False


# noinspection DuplicatedCode
class SetItemsLR1(object):
    def __init__(self):
        self.conjunto = list()

        self.identificadores = list()

    def agregar(self, item: ItemLR1):
        # string_new = f"[{item.numero_regla},{item.pos_punto},{item.simbolo}]"
        hash_str = hash(item.to_string())

        if hash_str in self.identificadores:
            return

        self.conjunto.append(copy.deepcopy(item))
        self.identificadores.append(copy.deepcopy(hash_str))

    def unir(self, set_extra):
        for index, identi in enumerate(set_extra.identificadores):
            if identi in self.identificadores:
                continue

            self.agregar(copy.deepcopy(set_extra.conjunto[index]))

    def igual_a(self, set_extra):
        for identi in set_extra.identificadores:
            if identi not in self.identificadores:
                return False
        return True

    def tamano(self):
        return len(self.conjunto)

    def contiene(self, item: ItemLR1):
        # string_new = f"[{item.numero_regla},{item.pos_punto},{item.simbolo}]"
        hash_str = hash(item.to_string())

        if hash_str in self.identificadores:
            return True
        return False