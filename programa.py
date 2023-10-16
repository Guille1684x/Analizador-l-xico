import copy
import pickle

from disenos import *
# import BUClases as clases
import clases
import time




TIEMPO_A_DORMIR = 3

main_afn = clases.AFN()
main_tabla_union = list()
tabla_resultado_union_lexico = list(list())
terminales_tokens_ll1 = list()
terminales_tokens_lr0 = list()
terminales_tokens_lr1 = list()

# Define Window
window = sg.Window("Compiladores", layout, size=(1500, 500))


# Read  values entered by user
def crear_popup(tipo, valores=None):
    if tipo == 'basico':
        mensaje = "Se ha creado un automata con:\n" \
                  "Caracter inferior: {}\n" \
                  "Caracter superior: {}\n" \
                  "ID: {}" \
            .format(valores['-char_inf-'], valores['-char_sup-'], valores['-id_basico-'])
        sg.popup(mensaje, title='Exito')
    elif tipo == 'Error':
        mensaje = 'Favor de verificar las entradas'
        sg.popup(mensaje, title='Error', text_color='Red')


def actualizar_campos():  # TODO cambiar a actualizar_todo()
    ordernados = []
    for afn in main_afn.conjunto_AFNs:
        ordernados.append(afn.id_AFN)
    ordernados.sort()

    window['-id_positiva-'].update(values=ordernados)

    window['-id_kleen-'].update(values=ordernados)

    window['-id_1_union-'].update(values=ordernados)
    window['-id_2_union-'].update(values=ordernados)

    window['-id_1_concatenar-'].update(values=ordernados)
    window['-id_2_concatenar-'].update(values=ordernados)

    window['-id_convertir_a_afd-'].update(values=ordernados)

    global main_tabla_union
    main_tabla_union = ordernados.copy()
    tabla_resultado_union_lexico.clear()
    window['-UNION BASE LEXICO-'].update(values=main_tabla_union)
    window['-UNION RESULTADO LEXICO-'].update(values=[])


def crear_basico(valores):
    if valores['-id_basico-'] == '' or valores['-char_inf-'] == '' or valores['-char_sup-'] == '':
        crear_popup('Error')
        return
    if ord(valores['-char_inf-']) > ord(valores['-char_sup-']):
        sg.popup("Ingrese de ingresar un rango adecuado de valores", title='Error', text_color='Red')
        return
    if not valores['-id_basico-'].isnumeric():
        sg.popup("Ingrese un valor  numerico para el id", title='Error', text_color='Red')
        return
    if int(valores['-id_basico-']) in [afn.id_AFN for afn in main_afn.conjunto_AFNs]:
        sg.popup("Ingrese otro id que no exista", title='Error', text_color='Red')
        return
    temp_afn = clases.AFN()
    main_afn.conjunto_AFNs.append(
        temp_afn.crear_afn_basico(values['-char_inf-'], values['-char_sup-'], int(values['-id_basico-'])))

    global main_tabla_union
    main_tabla_union.append(int(values['-id_basico-']))
    actualizar_campos()

    crear_popup('basico', values)
    window['-id_basico-'].update('')
    window['-char_sup-'].update('')
    window['-char_inf-'].update('')

    return True


def crear_positiva(valores):
    if valores['-id_positiva-'] == '':
        sg.popup("Favor de seleccionar un automata", title='Error', text_color='Red')
        return
    id_afn = int(valores['-id_positiva-'])
    for afn in main_afn.conjunto_AFNs:
        if afn.id_AFN == id_afn:
            afn.cerradura_positiva()
            actualizar_campos()
            sg.popup("Se ha aplicado la cerradura positiva al automata: {}".format(afn.id_AFN), title='Exito')
            return


def crear_kleen(valores):
    if valores['-id_kleen-'] == '':
        sg.popup("Favor de seleccionar un automata", title='Error', text_color='Red')
        return
    id_afn = int(valores['-id_kleen-'])
    for afn in main_afn.conjunto_AFNs:
        if afn.id_AFN == id_afn:
            afn.cerradura_kleen()
            actualizar_campos()
            sg.popup("Se ha aplicado la cerradura de kleen al automata: {}".format(afn.id_AFN), title='Exito')
            return


def agregar_union_lexico(valores):
    try:
        lugar = valores['-UNION BASE LEXICO-'][0]
        global main_tabla_union
        global tabla_resultado_union_lexico
        tabla_resultado_union_lexico.append([main_tabla_union.pop(lugar), 0])
        window['-UNION BASE LEXICO-'].update(values=main_tabla_union)
        window['-UNION RESULTADO LEXICO-'].update(values=tabla_resultado_union_lexico)
    except IndexError:
        sg.popup("No se ha seleccionado ningún elemento", title='Error', text_color='Red')


def eliminar_union_lexico(valores):
    try:
        lugar = valores['-UNION RESULTADO LEXICO-'][0]
        global main_tabla_union
        global tabla_resultado_union_lexico
        main_tabla_union.append(tabla_resultado_union_lexico.pop(lugar)[0])
        window['-UNION BASE LEXICO-'].update(values=main_tabla_union)
        window['-UNION RESULTADO LEXICO-'].update(values=tabla_resultado_union_lexico)
    except IndexError:
        sg.popup("No se ha seleccionado ningún elemento", title='Error', text_color='Red')


def token_union_lexico(valores):
    try:

        lugar = valores['-UNION RESULTADO LEXICO-'][0]
        token = values['-token_union_lexico-']
        global tabla_resultado_union_lexico
        tabla_resultado_union_lexico[lugar][1] = token
        window['-UNION RESULTADO LEXICO-'].update(values=tabla_resultado_union_lexico)
    except IndexError:
        sg.popup("Favor de seleccionar la casilla para agregar el token", title='Error', text_color='Red')


def unir_afns(valores):
    if valores['-id_1_union-'] == '' or valores['-id_2_union-'] == '':
        sg.popup("Favor de seleccionar los automatas a unir", title='Error', text_color='Red')
        return
    if valores['-id_1_union-'] == valores['-id_2_union-']:
        sg.popup("Selecciona dos automatas distintos", title='Error', text_color='Red')
        return
    id_1 = int(valores['-id_1_union-'])
    id_2 = int(valores['-id_2_union-'])
    for afn_1 in main_afn.conjunto_AFNs:
        if afn_1.id_AFN == id_1:
            for afn_2 in main_afn.conjunto_AFNs:
                if afn_2.id_AFN == id_2:
                    afn_1.unir_afn(afn_2)
                    main_afn.conjunto_AFNs.remove(afn_2)
                    actualizar_campos()
                    sg.popup("Se han unido exitosamente los automatas: {} y {}"
                             .format(afn_1.id_AFN, afn_2.id_AFN),
                             title='Exito')
                    # actualizar_todo() TODO implementar
                    return


def concatenar_afns(valores):
    if valores['-id_1_concatenar-'] == '' or valores['-id_2_concatenar-'] == '':
        sg.popup("Favor de seleccionar los automatas a concatenar", title='Error', text_color='Red')
        return
    if valores['-id_1_concatenar-'] == valores['-id_2_concatenar-']:
        sg.popup("Selecciona dos automatas distintos", title='Error', text_color='Red')
        return
    id_1 = int(valores['-id_1_concatenar-'])
    id_2 = int(valores['-id_2_concatenar-'])
    for afn_1 in main_afn.conjunto_AFNs:
        if afn_1.id_AFN == id_1:
            for afn_2 in main_afn.conjunto_AFNs:
                if afn_2.id_AFN == id_2:
                    afn_1.concatenar_afn(afn_2)
                    main_afn.conjunto_AFNs.remove(afn_2)
                    actualizar_campos()

                    sg.popup("Se han concatenado exitosamente los automatas: {} y {}"
                             .format(afn_1.id_AFN, afn_2.id_AFN),
                             title='Exito')
                    # actualizar_todo() TODO implementar
                    return


def crear_union_lexico():
    if len(tabla_resultado_union_lexico) < 1:
        sg.popup("Elija mas de un elemento para la union", title='Error', text_color='Red')
        return

    temp_afn = None
    list_res_afn = list()
    ids = list()
    tokens = list()
    for i in range(len(tabla_resultado_union_lexico)):
        ids.append(tabla_resultado_union_lexico[i][0])
        tokens.append(tabla_resultado_union_lexico[i][1])
    # copia_main = copy.deepcopy(main_afn.conjunto_AFNs)
    copia_main = main_afn.conjunto_AFNs.copy()
    sacados = 0
    for i in range(len(main_afn.conjunto_AFNs)):
        if copia_main[i].id_AFN == ids[0]:
            temp_afn = main_afn.conjunto_AFNs.pop(i - sacados)
            sacados += 1
        elif copia_main[i].id_AFN in ids:
            list_res_afn.append(main_afn.conjunto_AFNs.pop(i - sacados))
            sacados += 1
    main_afn.conjunto_AFNs.append(temp_afn.union_especial(list_res_afn, tokens))
    sg.popup("Se han unido exitosamente los automatas: {} y se ha colocado en el AFN con el id: {}"
             .format(ids, ids[0]),
             title='Exito')
    actualizar_campos()


def convertir_afd_a_afn(valores):
    if valores['-id_convertir_a_afd-'] == '':
        sg.popup("Favor de seleccionar un automata", title='Error', text_color='Red')
        return
    id_afn = int(valores['-id_convertir_a_afd-'])
    for afn in main_afn.conjunto_AFNs:
        if afn.id_AFN == id_afn:
            tabla = afn.convertir_a_afd(valores['-nobre_archhivo_afn_afd-'])
            window['-resultado_conversion_afn_afd-'].update(tabla)
            window['-id_convertir_a_afd-'].update('')
            actualizar_campos()
            sg.popup("El automata {} se ha convertido exitosamente".format(afn.id_AFN), title='Exito')
            return


def probar_analizador_lexico(valores):
    if valores['-nombre_afd_txt-'] == '':
        sg.popup("Favor de ingresar el nombre del archivo", title='Error', text_color='Red')
        return
    if valores['-cadena_sigma_al-'] == '':
        sg.popup("Favor de ingresar una cadena a evaluar", title='Error', text_color='Red')
        return
    sigma = valores['-cadena_sigma_al-']
    nom_txt = valores['-nombre_afd_txt-']

    try:
        open(f"{nom_txt}.txt", "r")
    except FileNotFoundError:
        sg.popup(f"El archivo {nom_txt}.txt no existe", title='Error', text_color='Red')
        return

    anal_lexico = clases.AnalizadorLexico(sigma, nom_txt)

    tabla_lexemas = list()

    # while anal_lexico.token != '«' and anal_lexico.token != 'ø' and anal_lexico.token is None:

    token = anal_lexico.yylex()

    while token != '0':
        # time.sleep(TIEMPO_A_DORMIR)
        holder_lexema = list()

        token_temp = anal_lexico.token
        yytext_temp = anal_lexico.yytext
        holder_lexema.append(token_temp)
        holder_lexema.append(yytext_temp)

        tabla_lexemas.append(holder_lexema)

        token = anal_lexico.yylex()

    window['-tabla_res_al-'].update(values=tabla_lexemas)


def evaluar_postfijo(valores):
    sigma = valores['-val_post-']

    evaluador_p = clases.DescensoRecursivoCalc(sigma)
    if evaluador_p.ini_eval():
        window['-res_post-'].update(value=evaluador_p.resultado)
        window['-ex_post-'].update(value=evaluador_p.e_post_fija)
    else:
        sg.popup("Expresión sintácticamente incorrecta", title='Error', text_color='Red')


def convertir_de_er(valores):
    # if valores['-nombre_afd_er_txt-'] == '':
    #     sg.popup("Favor de ingresar el nombre del archivo", title='Error', text_color='Red')
    #     return
    if valores['-in_er-'] == '':
        sg.popup("Favor de ingresar una cadena a evaluar", title='Error', text_color='Red')
        return
    try:
        id_er = int(valores['-id_afn_er-'])
        if id_er in [afn.id_AFN for afn in main_afn.conjunto_AFNs]:
            sg.popup("Ingrese otro id que no exista", title='Error', text_color='Red')
            return
        expresion_r = valores['-in_er-']

        convertidor = clases.ERaAFN(expresion_r)
        if not convertidor.ini_conversion():
            sg.popup("Verfique la expresion regular", title='Error', text_color='Red')
            return
        convertidor.afd_result.id_AFN = id_er
        main_afn.conjunto_AFNs.append(convertidor.afd_result)

        sg.popup("Se ha convertida la expresion regular correctamente", title='Exito')
        actualizar_campos()
    except ValueError:
        sg.popup("Favor de ingresar un valor entero para el id", title='Error', text_color='Red')


def analisis_ll1(valores):
    sigma = valores['-sigma_ll1-']

    terminales_tokens_ll1.clear()
    dr_gg = clases.DescensoRecGramGram(sigma)

    if not dr_gg.analizar_gramatica():
        sg.popup("Gramatica no LL(1)", title='Error', text_color='Red')
        return
    sg.popup("Gramatica aceptada", title='Exito')

    dr_gg.calcular_tabla_ll1()

    for index, simbolo in enumerate(dr_gg.v_t):
        terminales_tokens_ll1.append([simbolo, '-1'])

    window['-ll1_no_terminales-'].update(values=dr_gg.v_n)
    window['-ll1_terminales-'].update(values=terminales_tokens_ll1)

    with open("res_ll1.pickle", "wb") as f_res:
        pickle.dump(dr_gg, f_res)


def mostrar_tabla_ll1():
    try:
        with open("res_ll1.pickle", "rb") as archivo_t_ll1:
            r_ll1 = pickle.load(archivo_t_ll1)
            lista_encabezados = copy.copy(r_ll1.v_t)
            lista_encabezados.insert(0, 'Regla')
            lista_encabezados.append('$')

            diseno = [
                [sg.Text("Tabla LL(1)")],
                [
                    sg.Table(
                        values=r_ll1.tabla_ll1,
                        headings=lista_encabezados,
                        auto_size_columns=False,
                        def_col_width=10,
                        expand_x=False,
                        vertical_scroll_only=False,
                        # display_row_numbers=True,
                        row_height=20,
                        justification='center',
                        key='-tabla_ll1_ventana-',
                    ),
                ],
            ]

            ventana = sg.Window("Tabla LL(1)", diseno, finalize=True)

            while True:
                evento, info = ventana.read()
                if evento == "Exit" or evento == sg.WIN_CLOSED:
                    break

            ventana.close()

    except FileNotFoundError:
        sg.popup("Favor de analizar primero una gramatica", title='Error', text_color='Red')


def evaluar_sigma_ll1(valores):
    if valores['-archivo_afd_ll1-'] == '':
        sg.popup("Favor de ingresar el nombre del archivo", title='Error', text_color='Red')
        return
    if valores['-sigma_eval_ll1-'] == '':
        sg.popup("Favor de ingresar una cadena a evaluar", title='Error', text_color='Red')
        return

    if len(terminales_tokens_ll1) == 0:
        sg.popup("Favor de asignar todos los tokens", title='Error', text_color='Red')
        return
    for s, t in terminales_tokens_ll1:
        if t == '-1':
            sg.popup("Favor de asignar todos los tokens", title='Error', text_color='Red')
            return

    nom_txt = valores['-archivo_afd_ll1-']
    sigma = valores['-sigma_eval_ll1-']

    try:
        open(f"{nom_txt}.txt", "r")
    except FileNotFoundError:
        sg.popup(f"El archivo {nom_txt}.txt no existe", title='Error', text_color='Red')
        return

    with open("res_ll1.pickle", "rb") as archivo_t_ll1:
        r_ll1 = pickle.load(archivo_t_ll1)
        if not r_ll1.evaluar_con_ll1(sigma, nom_txt):
            sg.popup("Cadena sintacticamente incorrecta", title='Error', text_color='Red')
            window['-ll1_pila-'].update(values=r_ll1.tabla_txt_eval_ll1)
            return
        sg.popup("Gramatica sintacticamente correcta", title='Exito')
        window['-ll1_pila-'].update(values=r_ll1.tabla_txt_eval_ll1)


def evaluar_sigma_lr0(valores):
    # print("here")
    if valores['-archivo_afd_lr0-'] == '':
        sg.popup("Favor de ingresar el nombre del archivo", title='Error', text_color='Red')
        return
    if valores['-sigma_eval_lr0-'] == '':
        sg.popup("Favor de ingresar una cadena a evaluar", title='Error', text_color='Red')
        return

    if len(terminales_tokens_lr0) == 0:
        sg.popup("Favor de asignar todos los tokens", title='Error', text_color='Red')
        return
    for s, t in terminales_tokens_lr0:
        if t == '-1':
            sg.popup("Favor de asignar todos los tokens", title='Error', text_color='Red')
            return

    nom_txt = valores['-archivo_afd_lr0-']
    sigma = valores['-sigma_eval_lr0-']

    try:
        open(f"{nom_txt}.txt", "r")
    except FileNotFoundError:
        sg.popup(f"El archivo {nom_txt}.txt no existe", title='Error', text_color='Red')
        return

    with open("res_lr0.pickle", "rb") as archivo_t_lr0:
        r_lr0 = pickle.load(archivo_t_lr0)
        if not r_lr0.evaluar_con_lr0(sigma, nom_txt):
            sg.popup("Cadena sintacticamente incorrecta", title='Error', text_color='Red')
            window['-lr0_pila-'].update(values=r_lr0.tabla_txt_eval_lr0)
            return
        sg.popup("Gramatica sintacticamente correcta", title='Exito')
        window['-lr0_pila-'].update(values=r_lr0.tabla_txt_eval_lr0)


def evaluar_sigma_lr1(valores):
    # print("here")
    if valores['-archivo_afd_lr1-'] == '':
        sg.popup("Favor de ingresar el nombre del archivo", title='Error', text_color='Red')
        return
    if valores['-sigma_eval_lr1-'] == '':
        sg.popup("Favor de ingresar una cadena a evaluar", title='Error', text_color='Red')
        return

    if len(terminales_tokens_lr1) == 0:
        sg.popup("Favor de asignar todos los tokens", title='Error', text_color='Red')
        return
    for s, t in terminales_tokens_lr1:
        if t == '-1':
            sg.popup("Favor de asignar todos los tokens", title='Error', text_color='Red')
            return

    nom_txt = valores['-archivo_afd_lr1-']
    sigma = valores['-sigma_eval_lr1-']

    try:
        open(f"{nom_txt}.txt", "r")
    except FileNotFoundError:
        sg.popup(f"El archivo {nom_txt}.txt no existe", title='Error', text_color='Red')
        return

    with open("res_lr1.pickle", "rb") as archivo_t_lr1:
        r_lr1 = pickle.load(archivo_t_lr1)
        if not r_lr1.evaluar_con_lr1(sigma, nom_txt):
            sg.popup("Cadena sintacticamente incorrecta", title='Error', text_color='Red')
            window['-lr1_pila-'].update(values=r_lr1.tabla_txt_eval_lr1)
            return
        sg.popup("Gramatica sintacticamente correcta", title='Exito')
        window['-lr1_pila-'].update(values=r_lr1.tabla_txt_eval_lr1)


def asignar_token_ll1(valores):
    tokens_vt = valores['-token_ll1-']
    if tokens_vt == '':
        sg.popup("Favor de ingresar un token (LL1)", title='Error', text_color='Red')
        return
    try:
        with open("res_ll1.pickle", "rb") as archivo_t_ll1:
            r_ll1 = pickle.load(archivo_t_ll1)

            lugar = valores['-ll1_terminales-'][0]
            terminales_tokens_ll1[lugar][1] = tokens_vt

            # DICT = { [token] : [simbolo] }
            r_ll1.tokens_vt[terminales_tokens_ll1[lugar][1]] = terminales_tokens_ll1[lugar][0]

            window['-ll1_terminales-'].update(values=terminales_tokens_ll1)

        with open("res_ll1.pickle", "wb") as archivo_t_ll1:
            pickle.dump(r_ll1, archivo_t_ll1)
    except IndexError:
        sg.popup("Favor de seleccionar la casilla para agregar el token", title='Error', text_color='Red')


def asignar_token_lr0(valores):
    tokens_vt = valores['-token_lr0-']
    if tokens_vt == '':
        sg.popup("Favor de ingresar un token (LR0)", title='Error', text_color='Red')
        return
    try:
        with open("res_lr0.pickle", "rb") as archivo_t_lr0:
            r_lr0 = pickle.load(archivo_t_lr0)
            # print(r_lr0.tokens_vt)

            lugar = valores['-lr0_terminales-'][0]
            terminales_tokens_lr0[lugar][1] = tokens_vt

            # DICT = { [token] : [simbolo] }
            r_lr0.tokens_vt[terminales_tokens_lr0[lugar][1]] = terminales_tokens_lr0[lugar][0]

            window['-lr0_terminales-'].update(values=terminales_tokens_lr0)
            # print(r_lr0.tokens_vt)

        with open("res_lr0.pickle", "wb") as f_res:
            pickle.dump(r_lr0, f_res)
    except IndexError:
        sg.popup("Favor de seleccionar la casilla para agregar el token", title='Error', text_color='Red')


def asignar_token_lr1(valores):
    tokens_vt = valores['-token_lr1-']
    if tokens_vt == '':
        sg.popup("Favor de ingresar un token (LR1)", title='Error', text_color='Red')
        return
    try:
        with open("res_lr1.pickle", "rb") as archivo_t_lr1:
            r_lr1 = pickle.load(archivo_t_lr1)
            # print(r_lr0.tokens_vt)

            lugar = valores['-lr1_terminales-'][0]
            terminales_tokens_lr1[lugar][1] = tokens_vt

            # DICT = { [token] : [simbolo] }
            r_lr1.tokens_vt[terminales_tokens_lr1[lugar][1]] = terminales_tokens_lr1[lugar][0]

            window['-lr1_terminales-'].update(values=terminales_tokens_lr1)
            print(r_lr1.tokens_vt)

        with open("res_lr1.pickle", "wb") as f_res:
            pickle.dump(r_lr1, f_res)
    except IndexError:
        sg.popup("Favor de seleccionar la casilla para agregar el token", title='Error', text_color='Red')



def mostrar_tabla_lr0():
    try:
        with open("res_lr0.pickle", "rb") as archivo_t_lr0:
            a_lr0 = pickle.load(archivo_t_lr0)
            lista_encabezados = copy.copy(a_lr0.v)
            # lista_encabezados.insert(0, 'Regla')
            # lista_encabezados.append('$')

            diseno = [
                [sg.Text("Tabla LR(0)")],
                [
                    sg.Table(
                        values=a_lr0.tabla_lr0,
                        headings=lista_encabezados,
                        auto_size_columns=False,
                        def_col_width=10,
                        expand_x=False,
                        expand_y=True,
                        vertical_scroll_only=False,
                        display_row_numbers=True,
                        alternating_row_color='grey',
                        row_height=20,
                        justification='center',
                        key='-tabla_lr0_ventana-',
                    ),
                ],
            ]

            ventana = sg.Window("Tabla LR(0)", diseno, finalize=True, size=(1200, 800))

            # tabla = ventana['-tabla_ll1_ventana-'].Widget
            # tabla.heading('Row', text='Regla')

            while True:
                evento, info = ventana.read()
                if evento == "Exit" or evento == sg.WIN_CLOSED:
                    break

            ventana.close()

    except FileNotFoundError:
        sg.popup("Favor de analizar primero una gramatica", title='Error', text_color='Red')



def mostrar_tabla_lr1(valores):
    try:
        with open("res_lr1.pickle", "rb") as archivo_t_lr1:
            a_lr1 = pickle.load(archivo_t_lr1)
            lista_encabezados = copy.copy(a_lr1.v)
            # lista_encabezados.insert(0, 'Regla')
            # lista_encabezados.append('$')

            diseno = [
                [sg.Text("Tabla LR(1)")],
                [
                    sg.Table(
                        values=a_lr1.tabla_lr1,
                        headings=lista_encabezados,
                        auto_size_columns=False,
                        def_col_width=10,
                        expand_x=False,
                        expand_y=True,
                        vertical_scroll_only=False,
                        display_row_numbers=True,
                        alternating_row_color='grey',
                        row_height=20,
                        justification='center',
                        key='-tabla_lr1_ventana-',
                    ),
                ],
            ]

            ventana = sg.Window("Tabla LR(1)", diseno, finalize=True, size=(1200, 800))

            # tabla = ventana['-tabla_ll1_ventana-'].Widget
            # tabla.heading('Row', text='Regla')

            while True:
                evento, info = ventana.read()
                if evento == "Exit" or evento == sg.WIN_CLOSED:
                    break

            ventana.close()

    except FileNotFoundError:
        sg.popup("Favor de analizar primero una gramatica", title='Error', text_color='Red')


while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WINDOW_CLOSED:
        break
    elif event == "-BASICO-":
        crear_basico(values)
    elif event == "-UNION-":
        unir_afns(values)
    elif event == '-CONCATENAR-':
        concatenar_afns(values)
    elif event == "-POSITIVA-":
        crear_positiva(values)
    elif event == "-KLEEN-":
        crear_kleen(values)
    elif event == "-ANADIR UNION LEXICO-":
        agregar_union_lexico(values)
    elif event == "-ELIMINAR UNION LEXICO-":
        eliminar_union_lexico(values)
    elif event == "-TOKEN UNION LEXICO-":
        token_union_lexico(values)
    elif event == "-UNION LEXICO-":
        crear_union_lexico()
    elif event == "-CONVERTIR AFD A AFN-":
        convertir_afd_a_afn(values)
    elif event == '-PROBAR ANALIZADOR LEXICO-':
        probar_analizador_lexico(values)
    elif event == '-POSTFIJO-':
        evaluar_postfijo(values)
    elif event == '-ER A AFN-':
        convertir_de_er(values)
    elif event == "-ANALIZAR LL(1)-":
        analisis_ll1(values)
    elif event == "-MOSTRAR TABLA LL(1)-":
        mostrar_tabla_ll1()
    elif event == "-EVALUAR SIG LL1-":
        evaluar_sigma_ll1(values)
    elif event == "-EVALUAR SIG LR(0)-":
        evaluar_sigma_lr0(values)
    elif event == "-EVALUAR SIG LR(1)-":
        evaluar_sigma_lr1(values)
    elif event == "-TOKEN LL(1)-":
        asignar_token_ll1(values)
    elif event == "-TOKEN LR(0)-":
        asignar_token_lr0(values)
    elif event == "-TOKEN LR(1)-":
        asignar_token_lr1(values)
    # elif event == '-ANALIZAR LR(0)-':
    #     analisis_lr0(values)
    elif event == "-MOSTRAR TABLA LR(0)-":
        mostrar_tabla_lr0()
    # TODO Implementar tokens y evaluar sigma ll(1)
    # elif event == "-ANALIZAR LR(1)-":
    #     analisis_lr1(values)
    elif event == '-MOSTRAR TABLA LR(1)-':
        mostrar_tabla_lr1(values)

window.close()