import PySimpleGUI as sg

#                                           Definicion de mis pantallas del tab AFN's
#                     - Pantalla de la creacion de un AFN basico
ly_basico = [
    [sg.Text('CREACIÓN DE UN AUTOMATA BÁSICO')],
    [sg.Text('Carácter inferior', size=(20, 1)), sg.In('', key='-char_inf-')],
    [sg.Text('Carácter superior', size=(20, 1)), sg.In('', key='-char_sup-')],
    [sg.Text('Id del AFN', size=(20, 1)), sg.In('', key='-id_basico-')],
    [sg.Submit('Crear AFN', key='-BASICO-')],
]

#                     - Pantalla de la union de dos AFNs
ly_unir = [
    [sg.Text('UNIÓN DE DOS AUTOMATAS', size=(60, 1))],
    [
        sg.Text('Unir:', size=(20, 1)), sg.Combo([''], key='-id_1_union-', size=(8, 1)),
        sg.Text('con:', size=(20, 1)), sg.Combo([''], key='-id_2_union-', size=(8, 1)),
    ],
    [sg.Button('Realizar unión', key='-UNION-')]

]

#                     - Pantalla de la concatenación de dos AFNs
ly_concatenar = [
    [sg.Text('CONCATENACIÓN DE DOS AUTOMATAS', size=(60, 1))],
    [
        sg.Text('Concatenar:', size=(20, 1)), sg.Combo([''], key='-id_1_concatenar-', size=(8, 1)),
        sg.Text('con:', size=(20, 1)), sg.Combo([''], key='-id_2_concatenar-', size=(8, 1)),
    ],
    [sg.Button('Realizar concatenacion', key='-CONCATENAR-')]
]

#                     - Pantalla para aplicar la cerradura positiva a un AFN
ly_positiva = [
    [sg.Text('OPERACIÓN CERRADURA POSITIVA/TRANSITIVA', size=(60, 1))],
    [sg.Text('Aplicar operación + a:', size=(20, 1)), sg.Combo([''], key='-id_positiva-', size=(8, 1))],
    [sg.Button('Realizar operación +', key='-POSITIVA-')]
]

#                     - Pantalla para aplicar la cerradura de kleen a un AFN
ly_kleen = [
    [sg.Text('OPERACIÓN CERRADURA DE KLEEN', size=(60, 1))],
    [sg.Text('Aplicar operación * a:', size=(20, 1)), sg.Combo([''], key='-id_kleen-', size=(8, 1))],
    [sg.Button('Realizar operación *', key='-KLEEN-')]
]

ly_post = [
    [sg.Text('EVALUADOR DE EXPRESION Y CONVERSIÓN A POSTFIJA')],
    [sg.Text('Cadena a analizar:')],
    [sg.In('', key='-val_post-', size=(100, 1))],
    [sg.Button('Evaluar', key='-POSTFIJO-')],
    [sg.Text('Resultado:')],
    [sg.In('', key='-res_post-', size=(100, 1), disabled=True)],
    [sg.Text('Representacion posfija:')],
    [sg.In('', key='-ex_post-', size=(100, 1), disabled=True)],
]

ly_er_a_afn = [
    [sg.Text('CONERSION DE EXPRESION REGULAR A AFN')],
    [sg.Text('Expresion regular:')],
    [sg.In('', key='-in_er-', size=(100, 1))],
    [sg.Text('Id para el AFN:')],
    [sg.In('', key='-id_afn_er-', size=(20, 1))],
    [sg.Button('Crear AFN', key='-ER A AFN-')],
]

#                     - Pantalla para realizar la union para un analizador lexico
ly_union_lexico = [
    [sg.Text('CREACIÓN DE UN ANALAIZADOR LEXICO DE UN AFD', size=(60, 1))],
    [
        sg.Text('AFNs sin seleccionar', size=(25, 1)),
        sg.Text('AFNs seleccionados', size=(26, 1)),
    ],
    [
        sg.Table(
            values=[],
            headings=['id AFN'],
            justification='center',
            alternating_row_color='grey',
            key='-UNION BASE LEXICO-',
            num_rows=5,
            auto_size_columns=False,
            def_col_width=21,
        ),
        sg.Table(
            values=[[]],
            headings=['id AFN', 'Token'],
            justification='center',
            alternating_row_color='grey',
            key='-UNION RESULTADO LEXICO-',
            num_rows=5,
            auto_size_columns=False,
            def_col_width=11,
        ),
        sg.Column(
            [
                [sg.Text('Valor del token')],
                [sg.Text('* Ingresa el valor del token para la casilla seleccionada')],
                [sg.In('', key='-token_union_lexico-')],
                [sg.Button('Agregar', key='-TOKEN UNION LEXICO-')],
            ]
        )
    ],
    [
        sg.Button('Añadir seleccionado', key='-ANADIR UNION LEXICO-', size=(25, 1)),
        sg.Button('Eliminar seleccionado', key='-ELIMINAR UNION LEXICO-', size=(25, 1)),
    ],
    [sg.Button('Unir todos los seleccionados', key='-UNION LEXICO-', size=(50, 1))],

]

#                     - Pantalla para crear un AFD de un AFN
encabezados = [f'{chr(i)}' for i in range(32, 127)]  # IMPRESIÓN DE SIMBOLOS
# print(encabezados)
encabezados.append("Token")
ly_afn_a_afd = [
    [sg.Text('CONVERSION DE UN AUTOMATA AFN A AFD', size=(60, 1))],
    [
        sg.Text('Selecciona el automata que quieras convertir'),
        sg.Combo([''], key='-id_convertir_a_afd-', size=(8, 1)),
    ],
    [
        sg.Table(
            values=[[]],
            headings=encabezados,
            auto_size_columns=False,
            def_col_width=5,
            expand_x=False,
            vertical_scroll_only=False,
            display_row_numbers=True,
            justification='center',
            key='-resultado_conversion_afn_afd-'
        ),
    ],
    [sg.Text('Nombre del archivo (sin .txt)'), sg.In('', key='-nobre_archhivo_afn_afd-')],
    [sg.Button('Convetir', key='-CONVERTIR AFD A AFN-')],

]

ly_probar_analizador = [
    [sg.Text('PROBADOR DE UN ANALIZADOR LEXICO')],
    [sg.Text('Ingresa el nombre del archivo de tu afd (sin .txt)'), sg.In('', key='-nombre_afd_txt-', size=(24, 1))],
    [sg.Text('Cadena a analizar:')],
    [sg.Multiline('', size=(160, 5), key='-cadena_sigma_al-')],
    [sg.Button('Analizar', key='-PROBAR ANALIZADOR LEXICO-')],
    [
        sg.Table(
            values=[[]],
            headings=['Token', 'Lexema'],
            auto_size_columns=False,
            def_col_width=40,
            key='-tabla_res_al-',
            justification='center',
        )
    ]
]

#                                           Definicion de mis pantallas del tab Analizador sintáctico
#                     - Pantalla para...
# TODO Eliminar
placeholder_sigma_ll1 = "E -> T Ep ;\n" \
                        "Ep -> mas T Ep | menos T Ep | epsilon ;\n" \
                        "T -> F Tp ;\n" \
                        "Tp -> por F Tp | entre F Tp | epsilon ;\n" \
                        "F -> parenI E parenD | num ;"


ly_a_ll1 = [
    [sg.Text('ANALIZADOR LL(1)', size=(15, 1))],
    [
        sg.Column([
            [sg.Text('Gramatica', size=(71, 1))],
            [sg.Multiline(placeholder_sigma_ll1, size=(80, 10), key='-sigma_ll1-')],
            [
                sg.Button('Analizar gramatica', key='-ANALIZAR LL(1)-', size=(20, 1)),
                sg.Button('Mostrar tabla', key='-MOSTRAR TABLA LL(1)-', size=(20, 1))
            ],
            [
                sg.Table(
                    values=[],
                    headings=['No terminal'],
                    justification='center',
                    alternating_row_color='grey',
                    key='-ll1_no_terminales-',
                    num_rows=5,
                    auto_size_columns=False,
                    def_col_width=21,
                ),
                sg.Table(
                    values=[],
                    headings=['Terminal', 'Token'],
                    justification='center',
                    alternating_row_color='grey',
                    key='-ll1_terminales-',
                    num_rows=5,
                    auto_size_columns=False,
                    def_col_width=21,
                ),
                sg.Column(
                    [
                        [sg.Text('Valor del token')],
                        [sg.In('', key='-token_ll1-')],
                        [sg.Button('Agregar', key='-TOKEN LL(1)-')],
                    ]
                )
            ],
        ],
        ),
        sg.Column([
            [sg.Text('Archivo texto AFD Lexico (sin .txt)'), sg.In('./afd_fijos/afd_post_espacios3', key='-archivo_afd_ll1-')],
            [sg.Text('Sigma a evaluar sintacticamente')],
            [sg.In('', key='-sigma_eval_ll1-')],
            [sg.Button('Evaluar', key='-EVALUAR SIG LL1-')],
            [sg.Table(
                values=[],
                headings=['Pila', 'Cadena', 'Accion'],
                justification='center',
                alternating_row_color='grey',
                key='-ll1_pila-',
                num_rows=10,
                auto_size_columns=False,
                vertical_scroll_only=False,
                def_col_width=21,
            )],

        ], ),

    ],

]

placeholder_sigma_lr0 = "Ep -> E;\n" \
                        "E -> E mas T | T;\n" \
                        "T -> T por F | F;\n" \
                        "F -> parenI E parenD | num;"
ly_a_lr0 = [
    [sg.Text('ANALIZADOR LR(0)', size=(15, 1))],
    [
        sg.Column([
            [sg.Text('Gramatica', size=(71, 1))],
            [sg.Multiline(placeholder_sigma_lr0, size=(80, 10), key='-sigma_lr0-')],
            [
                sg.Button('Crear Tabla', key='-ANALIZAR LR(0)-', size=(20, 1)),
                sg.Button('Mostrar tabla', key='-MOSTRAR TABLA LR(0)-', size=(20, 1))
            ],
            [
                sg.Table(
                    values=[],
                    headings=['No terminal'],
                    justification='center',
                    alternating_row_color='grey',
                    key='-lr0_no_terminales-',
                    num_rows=5,
                    auto_size_columns=False,
                    def_col_width=21,
                ),
                sg.Table(
                    values=[],
                    headings=['Terminal', 'Token'],
                    justification='center',
                    alternating_row_color='grey',
                    key='-lr0_terminales-',
                    num_rows=5,
                    auto_size_columns=False,
                    def_col_width=21,
                ),
                sg.Column(
                    [
                        [sg.Text('Valor del token')],
                        [sg.In('', key='-token_lr0-')],
                        [sg.Button('Agregar', key='-TOKEN LR(0)-')],
                    ]
                )
            ],
        ],
        ),
        sg.Column([
            [
                sg.Text('Archivo texto AFD Lexico (sin .txt)'),
                sg.In('./afd_fijos/afd_post_espacios', key='-archivo_afd_lr0-')
            ],
            [sg.Text('Sigma a evaluar sintacticamente')],
            [sg.In('', key='-sigma_eval_lr0-')],
            [sg.Button('Evaluar', key='-EVALUAR SIG LR(0)-')],
            [sg.Table(
                values=[],
                headings=['Pila', 'Cadena', 'Accion'],
                justification='center',
                alternating_row_color='grey',
                key='-lr0_pila-',
                num_rows=10,
                auto_size_columns=False,
                vertical_scroll_only=False,
                def_col_width=21,
            )],

        ], ),

    ],

]

ly_a_lr1 = [
    [sg.Text('ANALIZADOR LR(1)', size=(15, 1))],
    [
        sg.Column([
            [sg.Text('Gramatica', size=(71, 1))],
            [sg.Multiline(placeholder_sigma_lr0, size=(80, 10), key='-sigma_lr1-')],
            [
                sg.Button('Crear Tabla', key='-ANALIZAR LR(1)-', size=(20, 1)),
                sg.Button('Mostrar tabla', key='-MOSTRAR TABLA LR(1)-', size=(20, 1))
            ],
            [
                sg.Table(
                    values=[],
                    headings=['No terminal'],
                    justification='center',
                    alternating_row_color='grey',
                    key='-lr1_no_terminales-',
                    num_rows=5,
                    auto_size_columns=False,
                    def_col_width=21,
                ),
                sg.Table(
                    values=[],
                    headings=['Terminal', 'Token'],
                    justification='center',
                    alternating_row_color='grey',
                    key='-lr1_terminales-',
                    num_rows=5,
                    auto_size_columns=False,
                    def_col_width=21,
                ),
                sg.Column(
                    [
                        [sg.Text('Valor del token')],
                        [sg.In('', key='-token_lr1-')],
                        [sg.Button('Agregar', key='-TOKEN LR(1)-')],
                    ]
                )
            ],
        ],
        ),
        sg.Column([
            [
                sg.Text('Archivo texto AFD Lexico (sin .txt)'),
                sg.In('./afd_fijos/afd_post_espacios', key='-archivo_afd_lr1-')
            ],
            [sg.Text('Sigma a evaluar sintacticamente')],
            [sg.In('', key='-sigma_eval_lr1-')],
            [sg.Button('Evaluar', key='-EVALUAR SIG LR(1)-')],
            [sg.Table(
                values=[],
                headings=['Pila', 'Cadena', 'Accion'],
                justification='center',
                alternating_row_color='grey',
                key='-lr1_pila-',
                num_rows=10,
                auto_size_columns=False,
                vertical_scroll_only=False,
                def_col_width=21,
            )],

        ], ),

    ],

]

#                                           Definicion de mi pantalla del subgrupo del tab de AFN's
ly_sbgrp1 = [[
    sg.TabGroup([[
        sg.Tab(
            'Creación de AFN básico',
            ly_basico,
            background_color='Blue',
            element_justification='center'
        ),
        sg.Tab(
            'Unir',
            ly_unir,
            title_color='Black',
            background_color='Pink'
        ),
        sg.Tab(
            'Concatenar',
            ly_concatenar,
            title_color='Black',
            background_color='Pink'
        ),
        sg.Tab(
            'Cerradura +',
            ly_positiva,
            title_color='Black',
            background_color='Pink'
        ),
        sg.Tab(
            'Cerradura *',
            ly_kleen,
            title_color='Black',
            background_color='RoyalBlue1'
        ),
        sg.Tab(
            'Evaluador y Posfijo',
            ly_post,
            title_color='Black',
            background_color='Pink'
        ),
        sg.Tab(
            'ER -> AFN',
            ly_er_a_afn,
            title_color='Black',
            background_color='Pink'
        ),
        sg.Tab(
            'Unión para analizador léxico',
            ly_union_lexico,
            title_color='Black',
            background_color='Pink'
        ),
        sg.Tab(
            'Convertir AFN a AFD',
            ly_afn_a_afd,
            title_color='Black',
            background_color='Pink'
        ),
        sg.Tab(
            'Probar analizador léxico',
            ly_probar_analizador,
            title_color='Black',
            background_color='Pink',
            element_justification='center'
        ),
    ]],
        tab_location='topleft', title_color='Grey', tab_background_color='White', selected_title_color='Black',
        selected_background_color='White', border_width=5)]]

#                                           Definicion de mi pantalla del subgrupo del tab de Analizador sintacatico
ly_sbgrp2 = [[
    sg.TabGroup([[
        sg.Tab(
            'Analizador LL(1)',
            ly_a_ll1,
            background_color='Blue',
        ),
        sg.Tab(
            'Analizador LLR0',
            ly_a_lr0,
            background_color='Blue',
        ),
        sg.Tab(
            'Analizador LLR1',
            ly_a_lr1,
            background_color='Blue',
        ),
    ]],
        tab_location='topleft', title_color='Grey', tab_background_color='White', selected_title_color='Black',
        selected_background_color='White', border_width=5)]]

#                                           Definicion de mi pantalla general
layout = [[
    sg.TabGroup([[
        sg.Tab('AFN\'s',
               ly_sbgrp1,
               background_color='Blue',
               element_justification='center',
               ),
        ]
    ],
        tab_location='topleft', title_color='Grey', tab_background_color='White', selected_title_color='Black',
        selected_background_color='White', border_width=5)]]