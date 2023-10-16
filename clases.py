from multipledispatch import dispatch
import copy

SLEEP_TIME = 1


class Estado(object):
    """Clase para el estado de los automatas

    Attibutes:
        _edo_aceptacion (bool): Indicara si el estado es de aceptacion\n
        _token (int): Indicara cual es el token del estado\n
        _id_estado (int): Indicara el id del estado\n
        _transiciones (List[Transicion]): Lista de las transiciones que cuenta el estado
    """
    contador_estado = 0

    def __init__(self):
        self._edo_aceptacion = False
        self._token = "-1"
        self._id_estado = self.contador_estado
        Estado.contador_estado += 1
        self._transiciones = list()

    # Getter y Setter del estado de aceptacion
    def get_edo_aceptacion(self):
        return self._edo_aceptacion

    def set_edo_aceptacion(self, edo_aceptacion: bool):
        self._edo_aceptacion = edo_aceptacion

    # Getter y Setter del token
    def get_token(self):
        return self._token

    def set_token(self, token: int):
        self._token = token

    # Getter y Setter del id del estado
    def get_id_estado(self):
        return self._id_estado

    def set_id_estado(self, id_estado: int):
        self._id_estado = id_estado

    # Getter y Setter de las transiciones
    def get_transiciones(self):
        return self._transiciones

    def set_transiciones(self, transiciones):
        self._transiciones = transiciones

    edo_aceptacion = property(get_edo_aceptacion, set_edo_aceptacion)
    token = property(get_token, set_token)
    id_estado = property(get_id_estado, set_id_estado)
    transiciones = property(get_transiciones, set_transiciones)


class EstadoIj(object):
    def __init__(self):
        self.id_ij = 0
        self.conjunto_ij = set()
        self.token_ij = '-1'

        # noinspection PyUnusedLocal
        self.tabla_transiciones = ['-1' for i in range(32, 128)]


class Transicion(object):
    """Clase para las transiciones de los automatas

        Attibutes:
            _simbolo_inf (str): Indicara el primer valor del rango de transicion\n
            _simbolo_sup (str): Indicara el ultimo valor del rango de transicion\n
            _estado (Estado): Indicara el estado al cual esta apuntando\n
        """

    def __init__(self, estado=None, simbolo_inf: str = None, simbolo_sup: str = None):
        if estado is None:
            self._simbolo_inf = self._simbolo_sup = self._estado = None
            return
        elif simbolo_sup is None:
            self._simbolo_inf = self._simbolo_sup = simbolo_inf
            self._estado = estado
            return
        self._simbolo_inf = simbolo_inf
        self._simbolo_sup = simbolo_sup
        self._estado = estado

    # Set transicion
    def set_transicion(self, simbolo_inf, estado, simb_sup=None):
        if simb_sup is None:
            self._simbolo_inf = self._simbolo_sup = simbolo_inf
        self._estado = estado

    # Get estado
    def get_estado(self, caracter: str):
        if ord(caracter) in range(ord(self._simbolo_inf), ord(self._simbolo_sup) + 1):
            return self._estado
        return None

    # Getter y Setter del simbolo inferior
    def get_simbolo_inf(self):
        return self._simbolo_inf

    def set_simbolo_inf(self, simbolo_inf: str):
        self._simbolo_inf = simbolo_inf

    # Getter y Setter del simbolo superior
    def get_simbolo_sup(self):
        return self._simbolo_sup

    def set_simbolo_sup(self, simbolo_sup):
        self._simbolo_sup = simbolo_sup

    simbolo_inf = property(get_simbolo_inf, set_simbolo_inf)
    simbolo_sup = property(get_simbolo_sup, set_simbolo_sup)


class AutomataBase(object):
    def __init__(self):
        self.id_AFN = 0
        self.edo_inicial = None
        self.edos_AFN = list()
        self.edos_aceptacion = set()
        self.alfabeto = set()


class AFN(AutomataBase):
    def __init__(self):
        super().__init__()
        self.se_agrego_union_lexico = False
        self.conjunto_AFNs = list()

    @dispatch(str, int)
    def crear_afn_basico(self, simbolo_inf: str, identi=-1):
        edo_ini = Estado()
        edo_fin = Estado()
        t = Transicion(edo_fin, simbolo_inf)
        edo_ini.transiciones.append(t)
        edo_fin.edo_aceptacion = True
        self.alfabeto.add(simbolo_inf)
        self.edo_inicial = edo_ini
        self.edos_AFN.append(edo_ini)
        self.edos_AFN.append(edo_fin)
        self.edos_aceptacion.add(edo_fin)
        self.se_agrego_union_lexico = False
        self.id_AFN = identi
        return self

    @dispatch(str, str, int)
    def crear_afn_basico(self, simbolo_inf: str, simbolo_sup: str, identi=-1):
        edo_ini = Estado()
        edo_fin = Estado()
        t = Transicion(edo_fin, simbolo_inf, simbolo_sup)
        edo_ini.transiciones.append(t)
        edo_fin.edo_aceptacion = True
        for i in range(ord(simbolo_inf), ord(simbolo_sup) + 1):
            self.alfabeto.add(chr(i))
        self.edo_inicial = edo_ini
        self.edos_AFN.append(edo_ini)
        self.edos_AFN.append(edo_fin)
        self.edos_aceptacion.add(edo_fin)
        self.se_agrego_union_lexico = False
        self.id_AFN = identi
        return self

    def unir_afn(self, afn_2):
        edo_ini = Estado()
        edo_fin = Estado()

        edo_ini.transiciones.append(Transicion(self.edo_inicial, 'ε'))
        edo_ini.transiciones.append(Transicion(afn_2.edo_inicial, 'ε'))

        for edo in self.edos_aceptacion:
            edo.transiciones.append(Transicion(edo_fin, 'ε'))
            edo.edo_aceptacion = False

        for edo in afn_2.edos_aceptacion:
            edo.transiciones.append(Transicion(edo_fin, 'ε'))
            edo.edo_aceptacion = False

        self.edos_aceptacion.clear()

        self.edo_inicial = edo_ini
        edo_fin.edo_aceptacion = True

        self.edos_aceptacion.add(edo_fin)

        for e in afn_2.edos_AFN:
            self.edos_AFN.append(e)

        self.edos_AFN.append(edo_ini)
        self.edos_AFN.append(edo_fin)

        self.alfabeto.update(afn_2.alfabeto)

    def concatenar_afn(self, afn_2):
        for transicion in afn_2.edo_inicial.transiciones:
            for estado in self.edos_aceptacion:
                estado.transiciones.append(transicion)
                estado.edo_aceptacion = False

        self.edos_aceptacion = afn_2.edos_aceptacion

        for e in afn_2.edos_AFN:
            self.edos_AFN.append(e)
            self.edos_AFN.append(e)
        self.alfabeto.update(afn_2.alfabeto)

    def opcional(self):
        edo_ini = Estado()
        edo_fin = Estado()

        edo_ini.transiciones.append(Transicion(self.edo_inicial, 'ε'))
        edo_ini.transiciones.append(Transicion(edo_fin, 'ε'))

        for edo in self.edos_aceptacion:
            edo.transiciones.append(Transicion(edo_fin, 'ε'))
            edo.edo_aceptacion = False

        self.edo_inicial = edo_ini
        edo_fin.edo_aceptacion = True
        self.edos_aceptacion.clear()
        self.edos_aceptacion.add(edo_fin)
        self.edos_AFN.append(edo_ini)
        self.edos_AFN.append(edo_fin)

    # noinspection DuplicatedCode
    def cerradura_positiva(self):
        edo_ini = Estado()
        edo_fin = Estado()

        edo_ini.transiciones.append(Transicion(self.edo_inicial, 'ε'))
        for edo in self.edos_aceptacion:
            edo.transiciones.append(Transicion(edo_fin, 'ε'))
            edo.transiciones.append(Transicion(self.edo_inicial, 'ε'))
            edo.edo_aceptacion = False

        self.edo_inicial = edo_ini
        edo_fin.edo_aceptacion = True
        self.edos_aceptacion.clear()
        self.edos_aceptacion.add(edo_fin)
        self.edos_AFN.append(edo_ini)
        self.edos_AFN.append(edo_fin)

    # noinspection DuplicatedCode
    def cerradura_kleen(self):
        edo_ini = Estado()
        edo_fin = Estado()

        edo_ini.transiciones.append(Transicion(self.edo_inicial, 'ε'))
        edo_ini.transiciones.append(Transicion(edo_fin, 'ε'))
        for edo in self.edos_aceptacion:
            edo.transiciones.append(Transicion(edo_fin, 'ε'))
            edo.transiciones.append(Transicion(self.edo_inicial, 'ε'))
            edo.edo_aceptacion = False

        self.edo_inicial = edo_ini
        edo_fin.edo_aceptacion = True
        self.edos_aceptacion.clear()
        self.edos_aceptacion.add(edo_fin)
        self.edos_AFN.append(edo_ini)
        self.edos_AFN.append(edo_fin)

    # noinspection PyMethodMayBeStatic
    def cerradura_epsilon(self, estado):
        conjunto_resultado = set()
        conjunto_evaluacion = [estado]

        while len(conjunto_evaluacion) != 0:
            edo_temp = conjunto_evaluacion.pop()
            conjunto_resultado.add(edo_temp)
            for transicion in edo_temp.transiciones:
                edo_if = transicion.get_estado('ε')
                if edo_if is None:
                    continue
                if edo_if in conjunto_resultado:
                    continue
                conjunto_evaluacion.append(edo_if)

        return conjunto_resultado

    # noinspection PyMethodMayBeStatic
    def mover(self, estados, simbolo):
        conjunto_resultado = set()
        for estado in estados:
            for transicion in estado.transiciones:
                edo_temp = transicion.get_estado(simbolo)
                if edo_temp is not None:
                    conjunto_resultado.add(edo_temp)
        return conjunto_resultado

    def ir_a(self, estados, simbolo):  #
        conjunto_resultado = set()
        conjunto_evaluar_ce = self.mover(estados, simbolo)
        for estado in conjunto_evaluar_ce:
            conjunto_resultado.update(self.cerradura_epsilon(estado))
        return conjunto_resultado

    def union_especial(self, afns, tokens):
        edo_ini = Estado()
        edo_ini.transiciones.append(Transicion(self.edo_inicial, 'ε'))
        for edo in self.edos_aceptacion:
            edo.token = tokens[0]

        i_token = 1
        for afn in afns:
            for edo in afn.edos_aceptacion:
                edo.token = tokens[i_token]
                self.edos_aceptacion.add(edo)
            for edo in afn.edos_AFN:
                self.edos_AFN.append(edo)
            self.alfabeto.update(afn.alfabeto)
            i_token += 1
            edo_ini.transiciones.append(Transicion(afn.edo_inicial, 'ε'))
        self.edo_inicial = edo_ini
        return self

    def convertir_a_afd(self, nom_txt):
        print(self.alfabeto)
        """
        Funcion para convertir un automata no determinista a determinista.
        La funcion cuenta con las siguientes variables:
            - conjunto_edos_resultante_ij: esta variable sera mi conjunto de los estados Ij resultantes la cual
            contiene objetos del tipo EstadoIj
            - conjunto_edos_evaluacion_ij: esta variable sera mi conjunto de nuevos estados estados Ij que se hayan
            detectado y que no se encuentran en mi conjunto ya evaluado.
            - edoij_aux: esta variable sera la que reciba mi estado a evaluar, es decir, con esta variable realizare
            mis IrA's.
            - conjunto_edos_aux: esta variable sera la variable temporal que reciba el conjunto de estados regresados
            por la funcion Ir_A(I_j, caracter) y el cual se usara para ver si este conjunto recibido ya se encuentra
            dentro de mis resultantes y si no para tambien agregarlos a mi conjunto de evaluacion.


        :return:
        """
        conjunto_edos_resultante_ij = list()
        conjunto_edos_evaluacion_ij = list()

        id_resultante = 0  # j

        edoij_aux = EstadoIj()
        edoij_aux.conjunto_ij = self.cerradura_epsilon(self.edo_inicial)

        edoij_aux.id_ij = id_resultante

        conjunto_edos_resultante_ij.append(edoij_aux)
        conjunto_edos_evaluacion_ij.append(edoij_aux)

        id_resultante += 1

        alfabeto_lista = list(self.alfabeto)
        alfabeto_lista.sort()

        # CICLO EN EL CUAL REALIZARE MIS IrA's CON MIS NUEVOS Ij's QUE VAYA ENCONTRANDO
        while len(conjunto_edos_evaluacion_ij) != 0:

            # RECIBO A Ij CON EL CUAL REALIZARE MIS IrA's CON MI ALFABETO
            edoij_aux = conjunto_edos_evaluacion_ij.pop(0)

            for caracter in alfabeto_lista:  # CICLO FOR PARA REALIZAR MI IrA's(Ij, c) CON MI ALFABETO

                # RECIBO UN CONJUNTO RESULTANTE DE MI IrA QUE EL CUAL EVUALUARE SI AUN NO SE ENCUENTRA EN MIS CONJUNTOS
                # RESULTANTES
                conjunto_edos_aux = self.ir_a(edoij_aux.conjunto_ij, caracter)
                if conjunto_edos_aux is None or len(conjunto_edos_aux) == 0:
                    continue
                tamano_ijs = len(conjunto_edos_resultante_ij)

                # CICLO PARA VERFICAR SI MI CONJUNTO ANTERIOR AUN NO SE ENCUENTRA EN ALGUNO GUARDADO
                for edoij in conjunto_edos_resultante_ij:
                    if conjunto_edos_aux == edoij.conjunto_ij:
                        # SI LO ENCUENTRA SIGNIFICA QUE SOY EL MISMO Y ME ESTOY APUNTANDO A MI MISMO
                        # POR LO TANTO GUARDO EN MI TABLA MI ID EN MI MISMA POSICION DE Ij
                        for edo in conjunto_edos_resultante_ij:
                            if edo.id_ij == edoij_aux.id_ij:
                                edo.tabla_transiciones[ord(caracter) - 32] = str(edoij.id_ij)
                                break
                        break
                    if tamano_ijs == 1:
                        # COMO NO SE ENCONTRO EN NINGUNO DE MIS ESTADOS YA REGISTRADOS EN MI CONJUNTO,
                        # SIGNIFICA QUE ESTE CARACTER ME LLEVARA A OTRO ESTADO NUEVO NO REGISTRADO
                        # Y POR LO TANTO EN MI TABLA PONGO QUE DE DONDE ESTOY, ME VA A DIRIGIR A UN NUEVO ID
                        # (ID_RESULTANTE YA FUE ADELANTADO PREVIAMENTE)
                        temp_edo = EstadoIj()
                        temp_edo.id_ij = id_resultante
                        temp_edo.conjunto_ij = conjunto_edos_aux

                        encontrado = False
                        for estado_aceptacion in self.edos_aceptacion:
                            for estado_ij in temp_edo.conjunto_ij:
                                if estado_ij.id_estado == estado_aceptacion.id_estado:
                                    estado_ij.token = estado_aceptacion.token
                                    encontrado = True
                                    break
                            if encontrado:
                                break

                        for edo in conjunto_edos_resultante_ij:
                            if edo.id_ij == edoij_aux.id_ij:
                                edo.tabla_transiciones[ord(caracter) - 32] = str(id_resultante)
                                edo.tabla_transiciones[-1] = temp_edo.token_ij
                                break
                        conjunto_edos_resultante_ij.append(temp_edo)
                        conjunto_edos_evaluacion_ij.append(temp_edo)
                        id_resultante += 1
                        break
                    tamano_ijs -= 1

        for estado_aceptacion in self.edos_aceptacion:
            for estados_en_ij in conjunto_edos_resultante_ij:
                for e in estados_en_ij.conjunto_ij:
                    if e.id_estado == estado_aceptacion.id_estado:
                        estados_en_ij.token = estado_aceptacion.token
                        estados_en_ij.tabla_transiciones[-1] = estado_aceptacion.token
                        break

        lista_final = []
        for ij in conjunto_edos_resultante_ij:
            lista_final.append(ij.tabla_transiciones)

        print(conjunto_edos_resultante_ij)
        with open(f"{nom_txt}.txt", "w") as afd_en_txt:
            for fila in lista_final:
                for valor in fila:
                    print(valor, end=';', file=afd_en_txt)
                print(file=afd_en_txt)
        return lista_final


class AnalizadorLexico(object):
    def __init__(self, sigma=None, archivo_afd=None):

        self.caracter_actual = ''
        self.edo_actual = None
        self.edo_transicion = None
        self.yytext = ""

        self.pila = list()
        self.token = '-1'
        self.fin_lexema = -1
        self.paso_por_edo_acept = False

        if all(v is None for v in [sigma, archivo_afd]):
            self.cadena_sigma = ""
            self.ini_lexema = -1
            self.indice_caracter_actual = -1
            self.automata_fd = None
            return

        self.automata_fd = list()
        self.cadena_sigma = sigma
        self.ini_lexema = 0
        self.indice_caracter_actual = 0

        with open(f"{archivo_afd}.txt", "r") as afd_en_txt:
            total_lineas = afd_en_txt.readlines()
            for linea in total_lineas:
                arr_linea = linea.split(sep=';')
                arr_linea.pop()
                self.automata_fd.append(arr_linea)

    # noinspection DuplicatedCode
    def analizador_lexico_snapshot(self):
        return copy.deepcopy(self)
        # snap_analizador_l = AnalizadorLexico()
        #
        # snap_analizador_l.caracter_actual = self.caracter_actual
        # snap_analizador_l.edo_actual = self.edo_actual
        # snap_analizador_l.edo_transicion = self.edo_transicion
        # snap_analizador_l.fin_lexema = self.fin_lexema
        # snap_analizador_l.indice_caracter_actual = self.indice_caracter_actual
        # snap_analizador_l.ini_lexema = self.ini_lexema
        # snap_analizador_l.yytext = self.yytext
        # snap_analizador_l.paso_por_edo_acept = self.paso_por_edo_acept
        # snap_analizador_l.token = self.token
        # snap_analizador_l.pila = self.pila
        #
        # return snap_analizador_l

    # noinspection DuplicatedCode
    def analizador_lexico_restore(self, snapshot):
        self.caracter_actual = snapshot.caracter_actual
        self.edo_actual = snapshot.edo_actual
        self.edo_transicion = snapshot.edo_transicion
        self.fin_lexema = snapshot.fin_lexema
        self.indice_caracter_actual = snapshot.indice_caracter_actual
        self.ini_lexema = snapshot.ini_lexema
        self.yytext = snapshot.yytext
        self.paso_por_edo_acept = snapshot.paso_por_edo_acept
        self.token = snapshot.token
        self.pila = snapshot.pila

    def set_sigma(self, sigma):
        self.cadena_sigma = sigma

        self.paso_por_edo_acept = False
        self.ini_lexema = 0
        self.fin_lexema = -1
        self.indice_caracter_actual = 0
        self.token = '-1'
        self.pila.clear()

    def yylex(self):
        while True:

            # Aqui almacenamos los inicios de TODOS nuestros lexemas
            self.pila.append(self.indice_caracter_actual)

            # Verficamos que la posicion a la que queremos llegar ya no existe y que por lo tanto es fin de cadena
            if self.indice_caracter_actual >= len(self.cadena_sigma):
                self.yytext = ""
                self.token = '0'
                return self.token

            # Iniciamos nuestro lexema donde nos quedamos, o si es la primera vez iniciamos desde 0
            self.ini_lexema = self.indice_caracter_actual

            # Iniciamos a analizar nuestro lexema desde el estado 0
            self.edo_actual = 0

            # Como apenas estamos iniciando ponemos que no hemos pasado por estado de aceptacion
            self.paso_por_edo_acept = False

            # Como apenas estamos iniciando no sabemos si nuestro lexema es valido o no entonces lo ponemos en -1
            self.fin_lexema = -1

            # Como apenas estamos iniciando no sabemos si el lexema es valido y por lo tanto el token es desconocido
            self.token = '-1'

            # Recorremos la cadena
            while self.indice_caracter_actual < len(self.cadena_sigma):

                # Saco el caracter en la posicion que esta indicando mi indice
                self.caracter_actual = self.cadena_sigma[self.indice_caracter_actual]

                if self.caracter_actual == "\n":
                    break

                # Del caracter que saque, checo en mi tabla a que estado me va a llevar.
                self.edo_transicion = int(self.automata_fd[self.edo_actual][ord(self.caracter_actual) - 32])

                # Verifico si mi estado al que llege existe, es decir, que sea diferente a -1
                if self.edo_transicion != -1:

                    # Verifico si mi estado es de aceptacion, es decir, que es diferente a -1
                    if self.automata_fd[self.edo_transicion][-1] != '-1':
                        # Como es de aceptacion:

                        # Pongo que pase por estado de aceptacion
                        self.paso_por_edo_acept = True

                        # Pongo el token correspondiente del estado en que me encuentro
                        self.token = self.automata_fd[self.edo_transicion][-1]

                        # Actualizo mi fin de lexema que es en la posicion donde estoy
                        self.fin_lexema = self.indice_caracter_actual

                    # Avanzo al siguiente caracter
                    self.indice_caracter_actual += 1

                    # Mi estado actual ahora sera el estado al que tuve la transicion
                    self.edo_actual = self.edo_transicion
                    continue

                break

            # Aqui llegamos una vez que hayamos terminado nuestra cadena a analizar
            # o
            # Cuando no podamos llegar a un estado con el caracter actual de donde estabamos

            # Verificamos si nuestro lexema anterior no fue valido
            if not self.paso_por_edo_acept:
                # Como no tuvimos un lexema valido desde mi inicio, me muevo al siguiente caracter para ver si el
                # desde el suiguiente caracter consigo uno valido
                self.indice_caracter_actual = self.ini_lexema + 1

                # Partimos la cadena que nos dio el error
                self.yytext = self.cadena_sigma[self.ini_lexema:self.ini_lexema + 1]

                if self.yytext == "\n":
                    continue

                # Regreso un token que indique que tuve un error
                self.token = 'ERROR'
                return self.token

            # En caso contrario significa que tenemos un lexema:

            # Partimos nuestra cadena sigma desde donde se identifico el lexema hasta su fin
            self.yytext = self.cadena_sigma[self.ini_lexema:self.fin_lexema + 1]

            # Avanzamos al siguiente caracter
            self.indice_caracter_actual = self.fin_lexema + 1

            # Si este lexema que se obtuvo tiene el valor de 'OMITIR' significa que vamos a descartar lo que se
            # consiguio entonces continuamos con otro lexema y reiniciamos todito
            if self.token == '-700':
                continue

            # Aqui llegamos si el lexema que se obtuvo es de importancia y por lo tanto regresamos el lexema y el token
            # que se obtuvo por este lexema
            else:
                return self.token

    def undo_token(self):
        if len(self.pila) == 0:
            return False
        self.indice_caracter_actual = self.pila.pop()
        return True


# noinspection PyPep8Naming
class DescensoRecursivoCalc(object):
    def __init__(self, sigma):
        self.e_post_fija = ""
        self.resultado = None
        self.expresion = sigma
        self.a_lex = AnalizadorLexico(sigma, './afd_fijos/afd_post_espacios')

    def set_expresion(self, sigma):
        self.expresion = sigma
        self.a_lex.set_sigma(sigma)

    def ini_eval(self):
        v = 0.0
        post_fijo = ""
        res_e, v, post_fijo = self.f_E(v, post_fijo)
        if res_e is True:
            token = self.a_lex.yylex()
            if token == "0":  # 0 es el token de fin de cadena
                self.resultado = v
                self.e_post_fija = post_fijo
                return True
        return False

    def f_E(self, v, post):
        res_t, v, post = self.f_T(v, post)
        if res_t is True:
            res_ep, v, post = self.f_Ep(v, post)
            if res_ep is True:
                return True, v, post
        return False, v, post

    def f_Ep(self, v, post):
        v2 = 0.0
        post2 = ""
        token = self.a_lex.yylex()
        if token == "10" or token == "20":  # si el token es + o -
            res_t, v2, post2 = self.f_T(v2, post2)
            if res_t is True:
                if token == "10":
                    v = v + v2
                    # post = post + " " + post2 + " +"
                    post = f"{post} {post2} +"
                elif token == "20":
                    v = v - v2
                    # post = post + " " + post2 + " -"
                    post = f"{post} {post2} -"
                res_ep, v, post = self.f_Ep(v, post)
                if res_ep is True:
                    return True, v, post
            return False, v, post
        self.a_lex.undo_token()
        return True, v, post

    def f_T(self, v, post):
        res_f, v, post = self.f_F(v, post)
        if res_f is True:
            res_tp, v, post = self.f_Tp(v, post)
            if res_tp is True:
                return True, v, post
        return False, v, post

    def f_Tp(self, v, post):
        v2 = 0.0
        post2 = ""
        token = self.a_lex.yylex()
        if token == "30" or token == "40":  # Simbolo * o /
            res_f, v2, post2 = self.f_F(v2, post2)
            if res_f is True:
                if token == "30":  # Simbolo *
                    v = v * v2
                    # post = post + " " + post2 + " *"
                    post = f"{post} {post2} *"
                elif token == "40":  # Simbolo /
                    v = v / v2
                    # post = post + " " + post2 + " /"
                    post = f"{post} {post2} /"

                res_tp, v, post = self.f_Tp(v, post)
                if res_tp is True:
                    return True, v, post
            return False, v, post
        self.a_lex.undo_token()
        return True, v, post

    def f_F(self, v, post):
        token = self.a_lex.yylex()
        if token == "50":  # Parentesis izquierdo
            res_e, v, post = self.f_E(v, post)
            if res_e is True:
                token = self.a_lex.yylex()
                if token == "60":  # Parentesis derecho
                    return True, v, post
            return False, v, post
        if token == "70" or token == "80":  # Entero o flotante
            v = float(self.a_lex.yytext)
            post = self.a_lex.yytext
            return True, v, post
        return False, v, post


# noinspection PyPep8Naming
class ERaAFN(object):
    def __init__(self, expresion_r):
        self.expresion_r = expresion_r
        self.afd_result = AFN()
        self.a_lex = AnalizadorLexico(expresion_r, './afd_fijos/afd_er_especiales')

    def ini_conversion(self):
        f = AFN()
        res_e, f = self.f_E(f)
        if res_e is True:
            token = self.a_lex.yylex()
            if token == "0":
                self.afd_result = f
                return True
        return False

    def f_E(self, f):
        res_t, f = self.f_T(f)
        if res_t is True:
            res_ep, f = self.f_Ep(f)
            if res_ep is True:
                return True, f
        return False, f

    def f_Ep(self, f):
        f2 = AFN()
        token = self.a_lex.yylex()
        if token == "10":  # TOKEN DEL 'OR'
            rest_t, f2 = self.f_T(f2)
            if rest_t is True:
                f.unir_afn(f2)
                res_ep, f = self.f_Ep(f)
                if res_ep is True:
                    return True, f
            return False, f
        self.a_lex.undo_token()
        return True, f

    def f_T(self, f):
        res_c, f = self.f_C(f)
        if res_c is True:
            res_tp, f = self.f_Tp(f)
            if res_tp is True:
                return True, f
        return False, f

    def f_Tp(self, f):
        f2 = AFN()
        token = self.a_lex.yylex()
        if token == "20":  # TOKEN DE LA CONCATENACION
            res_c, f2 = self.f_C(f2)
            if res_c is True:
                f.concatenar_afn(f2)
                res_tp, f = self.f_Tp(f)
                if res_tp is True:
                    return True, f
            return False, f
        self.a_lex.undo_token()
        return True, f

    def f_C(self, f):
        res_f, f = self.f_F(f)
        if res_f is True:
            res_cp, f = self.f_Cp(f)
            if res_cp is True:
                return True, f
        return False, f

    def f_Cp(self, f):
        token = self.a_lex.yylex()
        if token == "30":  # CERRADURA TRANSITIVA
            f.cerradura_positiva()
        elif token == "40":  # CERRADURA KLEEN
            f.cerradura_kleen()
        elif token == "50":  # OPCIONAL
            f.opcional()
        else:
            self.a_lex.undo_token()
            return True, f

        res_cp, f = self.f_Cp(f)
        if res_cp is True:
            return True, f
        return False, f

    def f_F(self, f):
        token = self.a_lex.yylex()

        if token == "60":  # PARENTESIS IZQUIERDO
            res_e, f = self.f_E(f)
            if res_e is True:
                token = self.a_lex.yylex()
                if token == "70":  # PARENTESIS DERECHO
                    return True, f
            return False, f

        elif token == "80":  # CORCHETE IZQUIERDO
            token = self.a_lex.yylex()

            if token == "110":  # SIMBOLO

                if self.a_lex.yytext[0] == "\\":
                    simbolo_1 = self.a_lex.yytext[1]
                else:
                    simbolo_1 = self.a_lex.yytext[0]

                token = self.a_lex.yylex()

                if token == "100":  # GUION
                    token = self.a_lex.yylex()

                    if token == "110":  # SIMBOLO

                        if self.a_lex.yytext[0] == "\\":
                            simbolo_2 = self.a_lex.yytext[1]
                        else:
                            simbolo_2 = self.a_lex.yytext[0]

                        token = self.a_lex.yylex()

                        if token == "90":  # CORCHETE DERECHO
                            f.crear_afn_basico(simbolo_1, simbolo_2, -1)
                            return True, f
            return False, f

        elif token == "110":  # SIMBOLO

            if self.a_lex.yytext[0] == "\\":
                simbolo = self.a_lex.yytext[1]
            else:
                simbolo = self.a_lex.yytext[0]

            f.crear_afn_basico(simbolo, simbolo, -1)
            return True, f

        return False, f


# CLASE 3 - 11
# noinspection PyPep8Naming
class DescensoRecGramGram(object):
    def __init__(self, sigma):
        self.tabla_ll1 = list()
        self.tokens_vt = dict()
        self.gramatica = sigma
        self.a_lex = AnalizadorLexico(sigma, './afd_fijos/afd_dr_gg')

        self.arr_reglas = list()
        self.numero_reglas = 0
        self.res_sigma_ll1 = list()
        self.tabla_txt_eval_ll1 = list()
        # self.tokens_vt = list()

        self.v_n = list()  # SIMBOLOS NO TERMINALES
        self.v_t = list()  # SIMBOLOS TERMINALES

    def set_gramatica(self, sigma):
        self.gramatica = sigma
        self.a_lex.set_sigma(sigma)

    # INICIO DEL PROGRAMA
    def analizar_gramatica(self):
        if self.f_G():
            token = self.a_lex.yylex()

            if token == "0":
                self.identificar_terminales()
                return True

        return False

    def f_G(self):
        if self.f_Lista_Reglas():
            return True
        return False

    def f_Lista_Reglas(self):
        if self.f_Reglas():
            token = self.a_lex.yylex()
            if token == "10":  # PUNTO Y COMA
                if self.f_Lista_Reglas_p():
                    return True
        return False

    def f_Lista_Reglas_p(self):
        bu_a_lex = self.a_lex.analizador_lexico_snapshot()
        if self.f_Reglas():
            token = self.a_lex.yylex()
            if token == "10":  # PUNTO Y COMA
                if self.f_Lista_Reglas_p():
                    return True
            return False
        self.a_lex = copy.deepcopy(bu_a_lex)
        return True

    def f_Reglas(self):
        simbolo = ""

        res_lado_izquierdo, simbolo = self.f_Lado_Izquierdo(simbolo)
        if res_lado_izquierdo is True:

            self.v_n.append(simbolo)
            token = self.a_lex.yylex()

            if token == "20":  # FLECHA
                if self.f_Lados_Derechos(simbolo):
                    return True
        return False

    def f_Lado_Izquierdo(self, simbolo):
        token = self.a_lex.yylex()

        if token == "30":  # SIMBOLO
            simbolo = self.a_lex.yytext
            return True, simbolo
        return False, simbolo

    def f_Lados_Derechos(self, simbolo):
        if self.f_Lado_Derecho(simbolo):
            if self.f_Lados_Derechos_p(simbolo):
                return True
        return False

    def f_Lados_Derechos_p(self, simbolo):
        token = self.a_lex.yylex()
        if token == "40":  # OR
            if self.f_Lado_Derecho(simbolo):
                if self.f_Lados_Derechos_p(simbolo):
                    return True
        self.a_lex.undo_token()
        return True

    def f_Lado_Derecho(self, simbolo):

        lista = list()
        res_sec_simb, lista = self.f_Secuencia_Simbolos(lista)
        if res_sec_simb is True:
            self.arr_reglas.append(ElementoArreglo())

            self.arr_reglas[self.numero_reglas].info_simbolo = ClaseNodo(simbolo, False)

            self.arr_reglas[self.numero_reglas].lista_lado_derecho = lista

            self.numero_reglas = self.numero_reglas + 1
            return True
        return False

    def f_Secuencia_Simbolos(self, lista):
        token = self.a_lex.yylex()

        if token == "30":  # SIMBOLO

            nodo = ClaseNodo(self.a_lex.yytext, False)

            res_sec_simb_p, lista = self.f_Secuencia_Simbolos_p(lista)
            if res_sec_simb_p is True:
                lista.insert(0, nodo)

                return True, lista
        return False, lista

    def f_Secuencia_Simbolos_p(self, lista):
        token = self.a_lex.yylex()
        if token == "30":  # SIMBOLO

            nodo = ClaseNodo(self.a_lex.yytext, False)

            res_sec_simb_p, lista = self.f_Secuencia_Simbolos_p(lista)
            if res_sec_simb_p is True:
                lista.insert(0, nodo)

                return True, lista
            return False, lista
        self.a_lex.undo_token()
        return True, lista

    def identificar_terminales(self):
        for i in range(0, self.numero_reglas):
            for nodo in self.arr_reglas[i].lista_lado_derecho:
                if nodo.simbolo not in self.v_n and nodo.simbolo != 'epsilon':
                    nodo.terminal = True
                    if nodo.simbolo not in self.v_t:
                        self.v_t.append(nodo.simbolo)

    # Lista: lista_lado_derecho
    def first(self, lista):
        r = set()

        # Checamos si la lista esta vacia
        if len(lista) == 0:
            # Regresamos el set vacio ya que no se agrego ningun elemento por la lista vacia
            return r

        # print("->Realzando el first de: ")
        # for n in lista:
        #     print(n.simbolo, end=' ')
        # print()

        # Como la lista no esta vacia iteramos nodo por nodo o
        # elemento por elemento
        for j in range(0, len(lista)):

            # Sacamos el elemento en la posicion j de nuestra lista
            n = lista[j]

            # Checamos si el nodo sacado es un simbolo terminal o si es epsilon
            if n.terminal or n.simbolo == 'epsilon':
                # Como fue cierta la condicion anterior agregamos este simbolo al first y
                # regresamos el set
                r.add(n.simbolo)
                return r

            # n NO es un terminal, entonces se iteran TODAS las reglas para encontrar este simbolo
            # en nuestros [lado izquierdo] de la lista de reglas
            for i in range(0, self.numero_reglas):

                # Checamos si [lado izquierdo] es igual al simbolo no terminal que nos aparecio
                if self.arr_reglas[i].info_simbolo.simbolo == n.simbolo:
                    # Como si fue igual al simbolo entonces hacemos el first de su regla
                    r.update(self.first(self.arr_reglas[i].lista_lado_derecho))

            # Si 'epsilon' no se encuetra en nuestro set r y finalmente llegamos al final de la lista
            # entonces regresamos r
            if 'epsilon' not in r or (j + 1) == len(lista):
                return r

            # Como si se econtro, quitamos 'epsilon' y realizamos el first() del contenido restante
            # de nuestra regla o [lista_lado_derecho]
            r.remove('epsilon')
            r.update(self.first(lista[j + 1:]))
            return r

    def follow(self, s: str):
        r = set()

        # Si el simbolo del follow es el inicial entonces se agrega el simbolo de pesos
        if s == self.arr_reglas[0].info_simbolo.simbolo:
            r.add('$')

        # Como no fue el inicial iteramos en todos nuestros [lado izquierdo] para encontrar las
        # apariciones del simbolo del follow en su regla
        for i in range(0, self.numero_reglas):

            # Sacamos la regla o [lista_lado_derecho] de nuestro [lado izquierdo]
            aux = self.arr_reglas[i].lista_lado_derecho

            # Iteramos el contendio de nuestra [lista_lado_derecho], es decir, nodo por nodo o
            # elemento por elemento
            for index, nodo in enumerate(aux):

                # Comparamos si el el simbolo de nuestro nodo de la [lista_lado_derecho] es igual
                # al que estamos buscando en el follow
                if nodo.simbolo == s:

                    # Entrando significa que ya encontramos el simbolo en nuestra [lista_lado_derecho]
                    # del i [lado izquierdo]

                    # 1. Checamos si aun no llegamos al final o aun hay elementos por recorrer
                    # 2. Checamos si existe un elemento despues del que estamos evaluando en el
                    #       follow()
                    if len(aux) != (index + 1):
                        # Entrando significa que si tenemos mas elementos adelante

                        # Realizamos el first() de sel contenido que se encutra adelante de
                        # nuestro simbolo que estamos en folow()
                        temp = self.first(aux[index + 1:])

                        # Checamos si se encuentra epsilon de lo que se hizo del first()
                        if 'epsilon' in temp:
                            # Entrando significa que si se encontro 'epsilon' en nuestro conjunto

                            # Quitamos 'epsilon' de nuestro set
                            temp.remove('epsilon')

                            # Actualizamos nuestro set resultante con nuestro temporal sin 'epsilon'
                            r.update(temp)

                            # Checamos si no vamos a repetir el follow con el que justo ahora estamos
                            # realizando
                            if self.arr_reglas[i].info_simbolo.simbolo == s:
                                break

                            # No se repitiendo el follow(), entonces procedemos
                            r.update(self.follow(self.arr_reglas[i].info_simbolo.simbolo))
                        else:
                            # No se encontro 'epsilon' entonces procedemos a guardar o actualizar
                            # nuestro set
                            r.update(temp)

                    # Llegamos a esta parte cuando se encontro el simbolo pero como ultimo elemento
                    # en la lista, es decir, ya no hay mas elementos en [lista_lado_derecho] por lo
                    # tanto realizaremos el follow de nuestro [lado izquierdo]
                    else:

                        # Checamos si no vamos a repetir el follow con el que justo ahora estamos
                        # realizando
                        if self.arr_reglas[i].info_simbolo.simbolo == s:
                            break

                        # No se repitiendo el follow(), entonces procedemos
                        r.update(self.follow(self.arr_reglas[i].info_simbolo.simbolo))
        return r

    def calcular_tabla_ll1(self):
        temp_terminales = copy.deepcopy(self.v_t)
        temp_terminales.append('$')

        temp_no_terminales = copy.deepcopy(self.v_n)
        temp_no_terminales.append('$')

        for fila in range(0, len(temp_no_terminales)):
            self.tabla_ll1.append(['-1'] * len(temp_terminales))

        for index, elemento_arr in enumerate(self.arr_reglas):
            f = self.first(elemento_arr.lista_lado_derecho)

            no_fila = temp_no_terminales.index(elemento_arr.info_simbolo.simbolo)

            if 'epsilon' in f:

                f.update(self.follow(elemento_arr.info_simbolo.simbolo))
                f.remove('epsilon')

            for item in f:
                self.tabla_ll1[no_fila][temp_terminales.index(item)] = f'{index + 1}'
        # self.tabla_ll1[-1][0] = '$'
        self.tabla_ll1[-1][-1] = 'ACEPTAR'
        for index, simb in enumerate(temp_no_terminales):
            self.tabla_ll1[index].insert(0, simb)

    def evaluar_con_ll1(self, cadena, archivo_afd):
        a_cadena_ll1 = AnalizadorCadenaLL1(cadena, archivo_afd)

        self.v_t.append('$')
        self.tokens_vt['0'] = '$'

        q_reglas = list()
        q_reglas.append('$')
        q_reglas.append(self.v_n[0])

        posicion_sigma = 0
        posicion_pila = 1

        if not a_cadena_ll1.obtener_tokens():
            return False
        # print("Cadena a andalizar es:", a_cadena_ll1.lista_lexemas)
        # print("Tokens a andalizar es:", a_cadena_ll1.lista_tokens)

        while len(q_reglas) != 0:

            # Recupero el ultimo valor de mi pila
            simb_regla = q_reglas[-1]

            # Obtengo el token y terminal correspondiente a mi simb sigma
            token_sigma = a_cadena_ll1.lista_tokens[posicion_sigma]
            terminal_sigma = self.tokens_vt.get(token_sigma)

            # Verifico si mi simbolo de regla es igual a mi simb terminal, para realizar el pop
            if simb_regla == terminal_sigma:
                # Imprimo en consola mi operacion
                # print(self.res_sigma_ll1[-1], '-> POP')

                # for elemento_izquierdo in self.arr_reglas[]

                # Lineas para guardar mi pila
                tupla = list()
                tupla.append(copy.deepcopy(q_reglas))
                tupla.append(a_cadena_ll1.lista_lexemas[posicion_sigma:])
                tupla.append("POP")
                self.res_sigma_ll1.append(tupla)

                # Saco mi simbolo terminal de pila
                q_reglas.pop()

                # Avanzo en mi cadena un valor
                posicion_sigma += 1

                # Retrocedo un valor en cual se insertara en mi pila
                posicion_pila -= 1

                continue

            elif simb_regla == 'epsilon':
                # Imprimo en consola mi operacion
                # print(self.res_sigma_ll1[-1], '-> MOVE')

                # Saco a epsilon
                q_reglas.pop()

                # Retrocedo un valor en cual se insertara en mi pila
                posicion_pila -= 1
                continue

            # Lineas para guardar mi pila
            tupla = list()
            tupla.append(copy.deepcopy(q_reglas))
            tupla.append(a_cadena_ll1.lista_lexemas[posicion_sigma:])

            # Guardo el index de mi simbolo terminal y le sumo uno debido a que en la primera columna se
            # encuentran mis no terminales
            index = int(self.v_t.index(terminal_sigma)) + 1

            # Busco la posicion de mi regla de q en mi tabla
            try:
                posicion_regla = self.v_n.index(simb_regla)
            except ValueError:
                self.format_tabla_resultante()
                tupla.append("ERROR")
                self.res_sigma_ll1.append(tupla)
                return False

            # Obtengo la regla a la cual llege con mi tabla con mi simbolo de sigma
            regla = self.tabla_ll1[posicion_regla][index]

            # accion = ""
            # for r_ld in self.arr_reglas[int(regla)]

            # print(self.res_sigma_ll1[-1], '->', regla)

            # Si la regla es -1 significa que la cadena sigma es sinctacticamente incorrecta
            if regla == '-1':
                tupla.append("ERROR")
                self.res_sigma_ll1.append(tupla)
                self.format_tabla_resultante()
                return False

            # Como se llegue a una regla entonces la guardo y le resto -1 por el arreglo
            regla = int(regla) - 1

            # Inicializo una variable para saber cuantas reglas se han agregado
            reglas_agregadas = 0

            # Saco la regla de mi pila y la reemplazo con su respectiva regla
            q_reglas.pop()

            # Saco mi lado derecho de la regla a la que se llego y agrego el simbolo en mi pila para ser
            # analizado en la posicion posicion_pila
            accion= ""
            for nodo in self.arr_reglas[regla].lista_lado_derecho:
                accion = accion + f"{nodo.simbolo} "
                q_reglas.insert(posicion_pila, nodo.simbolo)
                reglas_agregadas += 1
            accion = accion + f", {regla}"
            tupla.append(accion)
            self.res_sigma_ll1.append(tupla)
            #
            # if q_reglas[-1] == 'epsilon':
            #     q_reglas.pop(-1)
            #     posicion_pila -= 1
            #     continue

            # Modifico la posicion en la cual estare agregando a mi pila
            posicion_pila += reglas_agregadas - 1

        self.v_t.remove('$')
        self.format_tabla_resultante()
        # print('*' * 12)
        # for linea in self.res_sigma_ll1:
        #     print(linea)
        return True

    # noinspection DuplicatedCode
    def format_tabla_resultante(self):
        for pila, cadena, accion in self.res_sigma_ll1:
            str_pila = ""
            str_cadena = ""
            # str_accion = ""
            for regla in pila:
                str_pila = str_pila + f" {regla}"
            for yylex in cadena:
                str_cadena = str_cadena + yylex
            # for elemento in accion:
            #     str_accion = f"{}"
            self.tabla_txt_eval_ll1.append([str_pila, str_cadena, accion])
        # print('*'*12)
        # for linea in self.tabla_txt_eval_ll1:
        #     print(linea)


class ClaseNodo(object):
    def __init__(self, cadena, terminal):
        self.simbolo = cadena
        self.terminal = terminal


class ElementoArreglo(object):
    def __init__(self):
        self.info_simbolo = None
        self.lista_lado_derecho = None


# noinspection DuplicatedCode
class AnalizadorCadenaLL1(object):
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

# class ItemLR0:
#     def __init__(self, num_regla=-1, pos_punto=-1):
#         self.numero_regla = num_regla
#         self.pos_punto = pos_punto