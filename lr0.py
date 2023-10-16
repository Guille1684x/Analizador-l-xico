import copy

from clasesExtra import ItemLR0, SetItemsLR0
from clases import DescensoRecGramGram, AnalizadorLexico


class ConjuntoSjLR0(object):
    def __init__(self):
        self.j = -1
        self.sj = SetItemsLR0()  # Set de items LR0


class AnalizadorLR0(object):
    def __init__(self, cad_gramatica, archivo_a_lex):
        self.gram = cad_gramatica
        self.desc_rec_gg = DescensoRecGramGram(cad_gramatica)
        self.a_lex = None

        self.num_renglones_ira = 0
        self.sigma = ""
        self.tabla_lr0 = list()
        self.v_t = list()
        self.tokens_vt = dict()
        self.v_n = list()
        self.v = list()

        self.res_sigma_lr0 = list()
        self.tabla_txt_eval_lr0 = list()

    # noinspection DuplicatedCode
    def crear_tabla_lr0(self):
        # Conjunto de todos los Sj
        c = list()

        # Conjunto Sj
        conj_sj = ConjuntoSjLR0()

        # Conj temporal de Items
        conj_items = SetItemsLR0()

        # Sj sin analizar, quedan en cola
        q = list()

        if not self.desc_rec_gg.analizar_gramatica():
            print("Gramatica no aceptada")
            return False

        iter_simbolos = list()

        pos_insert = 0
        for simb in self.desc_rec_gg.v_t:
            self.v.append(simb)
            self.v_t.append(simb)
            iter_simbolos.append(simb)
        self.v.append('$')
        for simb in self.desc_rec_gg.v_n:
            self.v.append(simb)
            self.v_n.append(simb)
            iter_simbolos.insert(pos_insert, simb)
            pos_insert += 1
        # iter_simbolos.pop(0)

        # for i in range(0, 5):
        self.tabla_lr0.append(['-1' for j in range(0, len(self.v))])

        conj_items.agregar(ItemLR0(0, 0))

        j = 0
        conj_sj.sj = self.cerradura_lr0(conj_items)
        # print("De mi cerradura obtuve", len(conj_sj.sj.conjunto))
        conj_sj.j = j
        c.append(copy.deepcopy(conj_sj))
        # for conjunto in c:
        #     print(conjunto.j)
        q.append(copy.deepcopy(conj_sj))

        self.num_renglones_ira += 1

        # Contador de conjuntos sj
        j += 1

        while len(q) > 0:
            # for i in [1]:
            conj_sj = q.pop(0)

            # Ahora se calcula el IrA del Sj con cada simbolo de V = V_t U V_n
            # print(f"Analizando S_{conj_sj.j}")
            for simb in iter_simbolos:

                # Aux para guardar temporalmente el resultado de un IrA
                sj_aux = self.ir_a_lr0(conj_sj.sj, simb)

                # print(f"El ira con el con el conjunto tuvo {sj_aux.tamano()} elementos")

                if sj_aux.tamano() == 0:
                    continue

                # Verificar si este conjunto sj_aux ya existe en c
                existe = False

                for elem_sj in c:
                    if elem_sj.sj.tamano() == sj_aux.tamano():
                        if elem_sj.sj.igual_a(sj_aux):
                            existe = True

                            index_simb = self.v.index(simb)
                            if simb in self.v_t:
                                self.tabla_lr0[conj_sj.j][index_simb] = f"d{elem_sj.j}"
                            else:
                                self.tabla_lr0[conj_sj.j][index_simb] = elem_sj.j

                            self.num_renglones_ira += 1

                            break
                # print(f"\t--->{simb}")
                if not existe:
                    # Conjunto Sj
                    # print(f"Creando S_{j}")
                    conj_sj_aux = ConjuntoSjLR0()
                    conj_sj_aux.sj = sj_aux
                    conj_sj_aux.j = j

                    index_simb = self.v.index(simb)
                    if simb in self.v_t:
                        self.tabla_lr0[conj_sj.j][index_simb] = f"d{j}"
                    else:
                        self.tabla_lr0[conj_sj.j][index_simb] = j

                    self.tabla_lr0.append(['-1' for j in range(0, len(self.v))])

                    self.num_renglones_ira += 1
                    j += 1

                    c.append(copy.deepcopy(conj_sj_aux))
                    q.append(conj_sj_aux)
        # for linea in self.tabla_lr0:
        #     print(linea)

        for paquete_sj in c:
            # print(f"CHECANDO {paquete_sj.j}")
            for conjunto_sj in paquete_sj.sj.conjunto:
                no_regla = conjunto_sj.numero_regla
                # print(f"\tEvaluando {no_regla} con pos punto {conjunto_sj.pos_punto}")

                if len(self.desc_rec_gg.arr_reglas[no_regla].lista_lado_derecho) == conjunto_sj.pos_punto:

                    simbolo_eval_regla = self.desc_rec_gg.arr_reglas[no_regla].info_simbolo.simbolo
                    # print(f"\t--->FOUND last from {paquete_sj.j} to {no_regla}[{simbolo_eval_regla}]")

                    simbs_follow = self.desc_rec_gg.follow(simbolo_eval_regla)
                    for sim in simbs_follow:
                        if no_regla != 0:
                            index_simb = self.v.index(sim)
                            self.tabla_lr0[paquete_sj.j][index_simb] = f"r{no_regla}"
                            continue

                        index_simb = self.v.index(sim)
                        self.tabla_lr0[paquete_sj.j][index_simb] = "ACEPTAR"

        # for i in range(0, len(self.tabla_lr0)):
        #     self.tabla_lr0
        #     print(linea)
        return True

    def mover_lr0(self, c: SetItemsLR0, simbolo: str):  # c: es un set de Item_LR0
        # print(f"Moviendo a {simbolo}")
        # for conj in c.conjunto:
        #     print(f"\t{conj.}")
        r = SetItemsLR0()

        for i in c.conjunto:
            lista = self.desc_rec_gg.arr_reglas[i.numero_regla].lista_lado_derecho

            if i.pos_punto < len(lista):
                n = lista[i.pos_punto]
                if n.simbolo == simbolo:
                    r.agregar(ItemLR0(i.numero_regla, i.pos_punto + 1))
        return r

    def cerradura_lr0(self, c: SetItemsLR0):  # c: es un set de Item_LR0
        r = SetItemsLR0()
        temporal = SetItemsLR0()

        if c.tamano() == 0:
            return r
        r.unir(c)

        # Itero mi conjunto de items
        for i in c.conjunto:

            # Saco mi lado derecho de la regla de mi item
            lista = self.desc_rec_gg.arr_reglas[i.numero_regla].lista_lado_derecho
            # print("Sacando lado derecho de la regla", i.numero_regla)

            # Verifico si mi punto no esta ya al final
            if i.pos_punto < len(lista):

                # Saco mi nodo en la posicion del punto
                n = lista[i.pos_punto]
                if not n.terminal:
                    # print("*****Searching for", n.simbolo)

                    # Como no fue terminal el nodo de lista lado derecho itero en toda mi lista para
                    # encontrar otras reglas con el no terminal encontrado
                    for k in range(0, self.desc_rec_gg.numero_reglas):

                        # Verifico si ya encontre una coincidencia
                        if self.desc_rec_gg.arr_reglas[k].info_simbolo.simbolo == n.simbolo:

                            aux = ItemLR0(k, 0)

                            if not c.contiene(aux):
                                # print("NOT FOUND IN #", n.simbolo)
                                # print("RULE ", k)
                                temporal.agregar(aux)

        # print("Antes de unir tenia ", r.tamano())
        r.unir(self.cerradura_lr0(temporal))
        # print("Despues de unir tengo ", r.tamano())
        return r

    def ir_a_lr0(self, c: SetItemsLR0, simbolo: str):
        return self.cerradura_lr0(self.mover_lr0(c, simbolo))

    # noinspection DuplicatedCode
    def evaluar_con_lr0(self, cadena, archivo_afd):
        # print("Analizando ", cadena)

        a_cadena_lr0 = AnalizadorCadenaLR0(cadena, archivo_afd)

        self.v_t.append('$')
        self.tokens_vt['0'] = '$'

        q_reglas = list()
        q_reglas.append('0')

        posicion_sigma = 0
        # posicion_pila = 1

        if not a_cadena_lr0.obtener_tokens():
            return False

        # print(q_reglas, a_cadena_lr0.lista_lexemas[posicion_sigma:])
        # print(q_reglas)

        while len(q_reglas) != 0:
            # Recupero el ultimo valor de mi pila
            elemento_pila = q_reglas[-1]

            token_sigma = a_cadena_lr0.lista_tokens[posicion_sigma]
            terminal_sigma = self.tokens_vt.get(token_sigma)

            # Verifico si mi ultimo elemento de la pila es regla o terminal
            if elemento_pila.isnumeric():
                # print(int(elemento_pila))
                no_regla = int(elemento_pila)
                pos_v = self.v.index(terminal_sigma)

                regla_destino = self.tabla_lr0[no_regla][pos_v]
                # print(regla_destino)
                if regla_destino == '-1':
                    tupla = list()
                    tupla.append(copy.deepcopy(q_reglas))
                    tupla.append(a_cadena_lr0.lista_lexemas[posicion_sigma:])
                    tupla.append("-1, ERROR")
                    self.res_sigma_lr0.append(tupla)
                    self.format_tabla_resultante()
                    return False
                if regla_destino.isnumeric():
                    if regla_destino == '-1':
                        return False
                    return True

                elif regla_destino[0] == 'd':
                    # print("Desplazamiento: ", regla_destino)
                    tupla = list()
                    tupla.append(copy.deepcopy(q_reglas))
                    tupla.append(a_cadena_lr0.lista_lexemas[posicion_sigma:])
                    tupla.append(regla_destino)
                    # print(tupla)
                    # print(q_reglas)
                    # print(q_reglas, a_cadena_lr0.lista_lexemas[posicion_sigma:])
                    self.res_sigma_lr0.append(tupla)

                    q_reglas.append(terminal_sigma)
                    q_reglas.append(regla_destino[1:])

                    posicion_sigma += 1

                    # print(q_reglas, a_cadena_lr0.lista_lexemas[posicion_sigma:])

                elif regla_destino[0] == 'r':
                    # print("Reduccion: ", regla_destino)
                    tupla = list()
                    tupla.append(copy.deepcopy(q_reglas))
                    tupla.append(a_cadena_lr0.lista_lexemas[posicion_sigma:])

                    no_regla_destino = int(regla_destino[1:])

                    regla_izquierda = self.desc_rec_gg.arr_reglas[no_regla_destino].info_simbolo.simbolo
                    str_accion = f"{regla_destino}, {regla_izquierda} -> "
                    for nodo in self.desc_rec_gg.arr_reglas[no_regla_destino].lista_lado_derecho:
                        str_accion += f"{nodo.simbolo} "
                        q_reglas.pop()
                        q_reglas.pop()

                    no_regla_previa = int(q_reglas[-1])

                    q_reglas.append(regla_izquierda)
                    pos_regla_izquierda = self.v.index(regla_izquierda)

                    tupla.append(str_accion)
                    q_reglas.append(str(self.tabla_lr0[no_regla_previa][pos_regla_izquierda]))

                    # print(tupla)
                    self.res_sigma_lr0.append(tupla)
                    # print("here")
                    # print(q_reglas)
                    # print(q_reglas, a_cadena_lr0.lista_lexemas[posicion_sigma:])
                elif regla_destino == 'ACEPTAR':
                    tupla = list()
                    tupla.append(copy.deepcopy(q_reglas))
                    tupla.append(a_cadena_lr0.lista_lexemas[posicion_sigma:])
                    tupla.append("r0, aceptar")

                    self.res_sigma_lr0.append(tupla)

                    self.format_tabla_resultante()

                    return True

    # noinspection DuplicatedCode
    def format_tabla_resultante(self):
        for pila, cadena, accion in self.res_sigma_lr0:
            str_pila = ""
            str_cadena = ""
            # str_accion = ""
            for elemento in pila:
                str_pila = str_pila + f" {elemento}"
            for yylex in cadena:
                str_cadena += yylex
            # for elemento in accion:
            #     str_accion = f"{}"
            self.tabla_txt_eval_lr0.append([str_pila, str_cadena, accion])


# noinspection DuplicatedCode
class AnalizadorCadenaLR0(object):
    def __init__(self, sigma, archivo_afd):
        self.a_lex = AnalizadorLexico(sigma, archivo_afd)
        self.lista_tokens = list()
        self.lista_lexemas = list()

    def obtener_tokens(self):
        while True:
            token = self.a_lex.yylex()
            if token == 'ERROR':
                return False
            elif token == '0':
                self.lista_tokens.append('0')
                self.lista_lexemas.append('$')
                return True
            self.lista_tokens.append(token)
            self.lista_lexemas.append(self.a_lex.yytext)