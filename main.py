from typing import Union
from typing import Dict


class Simulacion:
    HIGH_VALUE = 999999999999

    def __init__(self, var_control_junior, var_control_senior, tiempo_simulacion=365 * 24 * 60):
        self.juniors = var_control_junior
        self.seniors = var_control_senior
        self.tiempo_simulacion = tiempo_simulacion

    def get_variables_sistema(self) -> dict:
        return {
            "T": 0,
            "TPLL": 0,
            "TPS": [self.HIGH_VALUE] * self.get_total_puestos(),
            "STLL": 0,
            "STS": 0,
            "STA": 0,
            "NT": 0,
            "NS": 0,
            "PTO": [0] * self.get_total_puestos(),
            "STO": [0] * self.get_total_puestos(),
            "ITO": [0] * self.get_total_puestos(),

            "NSA": 0,
            "NSM": 0,
            "NSB": 0,

            "seniorities": self.crear_seniorities(self.seniors, self.juniors)
        }

    def get_total_puestos(self):
        return self.juniors + self.seniors

    def crear_seniorities(self, seniors, juniors) -> list:
        seniorities = [('senior', False)] * seniors
        seniorities.append([('junior', False)] * juniors)
        return seniorities

    def get_indice_menor_tps(self, proximas_salidas: list) -> int:
        min_value = min(proximas_salidas)
        return proximas_salidas.index(min_value)

    def get_tiempo_proxima_llegada(self) -> int:
        return 20

    def get_prioridad_ticket(self, variables_sistema: dict):
        pass

    def es_junior(self, seniorities: list, indice) -> bool:
        return seniorities[indice][0] == "junior"

    def generar_tiempo_resolucion_jr(self) -> int:
        return 10

    def generar_tiempo_resolucion_sr(self) -> int:
        return 2


def sistema_de_tickets():
    print('INICIO DE SIMULACION')

    simulacion = Simulacion(4, 2)
    variables_de_sistema = simulacion.get_variables_sistema()

    print('VARIABLES DE SISTEMA')
    print(variables_de_sistema)

    while True:
        indice_menor_tps = simulacion.get_indice_menor_tps(variables_de_sistema["TPS"])

        if variables_de_sistema["TPLL"] <= variables_de_sistema["TPS"][indice_menor_tps]:
            rutina_llegada(simulacion, variables_de_sistema, indice_menor_tps)
        else:
            rutina_salida(simulacion, variables_de_sistema, indice_menor_tps)

        break

    print('VARIABLES DE SISTEMA FINAL')
    print(variables_de_sistema)


def rutina_llegada(simulacion, variables, indice):
    print("RUTINA LLEGADA")
    variables["T"] = variables["TPLL"]
    variables["STLL"] = variables["STLL"] + variables["T"]

    proxima_llegada = simulacion.get_tiempo_proxima_llegada()

    variables["TPLL"] = variables["T"] + proxima_llegada
    variables["NS"] = variables["NS"] + 1

    prioridad_ticket = simulacion.get_prioridad_ticket(variables)

    if variables["NSA"] + variables["NSM"] + variables["NSB"] <= simulacion.get_total_puestos():
        if simulacion.es_junior(variables["seniorities"], indice):
            atiende_junior(simulacion, variables, indice)
        else:
            atiende_senior(simulacion, variables, indice)

        variables["STO"][indice] = variables["STO"][indice] + (variables["T"] - variables["ITO"][indice])
    else: # ir a final
        pass


def atiende_junior(simulacion, variables, indice):
    print("ATIENDE JUNIOR")

    variables["STO"][indice] = variables["STO"][indice] + (variables["T"] - variables["ITO"][indice])

    tiempo_resolucion_jr = simulacion.generar_tiempo_resolucion_jr()

    variables["TPS"][indice] = variables["TPS"][indice] + tiempo_resolucion_jr
    variables["STA"] = variables["STA"] + tiempo_resolucion_jr


def atiende_senior(simulacion, variables, indice):
    print("ATIENDE SENIOR")

    tiempo_resolucion_sr = simulacion.generar_tiempo_resolucion_sr()
    variables["TPS"][indice] = variables["TPS"][indice] + tiempo_resolucion_sr
    variables["STA"] = variables["STA"] + tiempo_resolucion_sr


def rutina_salida(simulacion, variables, indice):
    print("RUTINA SALIDA")


if __name__ == '__main__':
    sistema_de_tickets()