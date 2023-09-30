from simulacion import Simulacion


def sistema_de_tickets():
    print('INICIO DE SIMULACION')

    simulacion = Simulacion(0, 2)
    variables_de_sistema = simulacion.get_variables_sistema()

    print('VARIABLES DE SISTEMA INICIAL')
    print(variables_de_sistema)

    while True:
        indice_menor_tps = simulacion.get_menor_tps(variables_de_sistema["devs"])

        if variables_de_sistema["TPLL"] < variables_de_sistema["devs"][indice_menor_tps]["TPS"]:
            rutina_llegada(simulacion, variables_de_sistema, indice_menor_tps)
        else:
            rutina_salida(simulacion, variables_de_sistema, indice_menor_tps)

        if variables_de_sistema["T"] < simulacion.get_tiempo_simulacion():
            continue
        else:
            if variables_de_sistema["NSA"] + variables_de_sistema["NSM"] + variables_de_sistema["NSB"] == 0:
                break
            else:
                variables_de_sistema["TPLL"] = simulacion.get_high_value()
                continue

    imprimir_resultados(simulacion, variables_de_sistema, indice_menor_tps)


def rutina_llegada(simulacion, variables, indice_menor_tps):
    print("RUTINA LLEGADA")
    variables["T"] = variables["TPLL"]

    prioridad_ticket = simulacion.get_calculo_de_prioridad(variables)

    simulacion.acumular_stll(variables, prioridad_ticket)

    ia = simulacion.get_intervalo_entre_arribos()

    variables["TPLL"] = variables["T"] + ia
    variables["NT"] = variables["NT"] + 1

    if variables["NSA"] + variables["NSM"] + variables["NSB"] <= simulacion.get_total_puestos():
        i_puesto_libre = simulacion.get_puesto_libre(variables["devs"])
        if simulacion.es_junior(variables["devs"], i_puesto_libre):
            atiende_junior(simulacion, variables, i_puesto_libre, prioridad_ticket)
        else:
            atiende_senior(simulacion, variables, i_puesto_libre, prioridad_ticket)

        variables["devs"][i_puesto_libre]["STO"] = variables["devs"][i_puesto_libre]["STO"] + (variables["T"] - variables["devs"][i_puesto_libre]["ITO"])


def atiende_junior(simulacion, variables, indice_menor_tps, prioridad):
    print("ATIENDE JUNIOR")

    # variables["seniorities"][indice_menor_tps] = (variables["seniorities"][indice_menor_tps][0], variables["seniorities"][indice_menor_tps][1] + 1)
    variables["devs"][indice_menor_tps]["atendidos"] = variables["devs"][indice_menor_tps]["atendidos"] + 1

    # variables["seniorities"][indice_menor_tps] = (variables["seniorities"][indice_menor_tps][0], prioridad)
    tiempo_resolucion_jr = simulacion.generar_tiempo_resolucion_jr()
    variables["devs"][indice_menor_tps]["TPS"] = variables["T"] + tiempo_resolucion_jr

    # simulacion.acumular_sta(variables, prioridad, tiempo_resolucion_jr) # esta mal, no hay q hacerlo


def atiende_senior(simulacion, variables, indice_menor_tps, prioridad):
    print("ATIENDE SENIOR")

    # variables["seniorities"][indice_menor_tps] = (variables["seniorities"][indice_menor_tps][0], variables["seniorities"][indice_menor_tps][1] + 1)
    variables["devs"][indice_menor_tps]["atendidos"] = variables["devs"][indice_menor_tps]["atendidos"] + 1

    # variables["seniorities"][indice_menor_tps] = (variables["seniorities"][indice_menor_tps][0], prioridad)
    tiempo_resolucion_sr = simulacion.generar_tiempo_resolucion_sr()
    variables["devs"][indice_menor_tps]["TPS"] = variables["T"] + tiempo_resolucion_sr

    # simulacion.acumular_sta(variables, prioridad, tiempo_resolucion_sr)


def rutina_salida(simulacion, variables, indice_menor_tps):
    print("RUTINA SALIDA")

    variables["T"] = variables["devs"][indice_menor_tps]["TPS"]

    # prioridad_salida = simulacion.calculo_de_prioridad_salida(variables, variables["seniorities"][indice_menor_tps][1])
    prioridad_salida = simulacion.calculo_de_prioridad_salida(variables, "")

    simulacion.acumular_sts(variables, prioridad_salida, variables["devs"][indice_menor_tps]["TPS"])

    if variables["NSA"] + variables["NSM"] + variables["NSB"] >= simulacion.get_total_puestos():
        if simulacion.es_junior(variables["devs"], indice_menor_tps):
            atiende_junior(simulacion, variables, indice_menor_tps, prioridad_salida)
        else:
            atiende_senior(simulacion, variables, indice_menor_tps, prioridad_salida)
    else:
        variables["devs"][indice_menor_tps]["ITO"] = variables["T"]
        variables["devs"][indice_menor_tps]["TPS"] = simulacion.get_high_value()


def imprimir_resultados(simulacion, variables, indice):
    print('FINAL SIMULACION')
    print('VARIABLES DE SISTEMA FINAL')
    print(variables)

    simulacion.calcular_resultados(variables)

    print("=========================")
    print(f'Tickets totales: {variables["NT"]}')
    print(f'Tickets con prioridad ALTA: {variables["NTA"]}')
    print(f'Tickets con prioridad MEDIA: {variables["NTM"]}')
    print(f'Tickets con prioridad BAJA: {variables["NTB"]}')

    print("=========================")
    print("Porcentaje de tiempo ocioso")
    pto = list(map(lambda dev: (dev["seniority"], dev["PTO"]), variables["devs"]))
    print(pto)

    print("=========================")
    print(f'Cantidad Junior: {simulacion.get_juniors()}')
    print(f'Cantidad Senior: {simulacion.get_seniors()}')

    print("=========================")
    print(f'Promedio de espera en cola ALTA: {variables["PECA"]}')
    print(f'Promedio de espera en cola MEDIA: {variables["PECM"]}')
    print(f'Promedio de espera en cola BAJA: {variables["PECB"]}')


if __name__ == '__main__':
    sistema_de_tickets()
