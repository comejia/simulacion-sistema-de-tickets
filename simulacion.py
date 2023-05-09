# from random import random, uniform
import math
import random


class Simulacion:
    HIGH_VALUE = 999999999999
    TIEMPO_SIMULACION = 365 * 24 * 60 * 60

    def __init__(self, var_control_junior, var_control_senior, tiempo_simulacion=TIEMPO_SIMULACION):
        self.juniors = var_control_junior
        self.seniors = var_control_senior
        self.tiempo_simulacion = tiempo_simulacion

    def get_variables_sistema(self) -> dict:
        return {
            "T": 0,
            "TPLL": 0,

            "TPS": [self.HIGH_VALUE] * self.get_total_puestos(),

            "STLLA": 0,
            "STLLM": 0,
            "STLLB": 0,

            "STAA": 0,
            "STAM": 0,
            "STAB": 0,

            "STSA": 0,
            "STSM": 0,
            "STSB": 0,

            "NT": 0,
            "NTA": 0,
            "NTM": 0,
            "NTB": 0,

            "PTO": [0] * self.get_total_puestos(),
            "STO": [0] * self.get_total_puestos(),
            "ITO": [0] * self.get_total_puestos(),

            "NSA": 0,
            "NSM": 0,
            "NSB": 0,

            "PECA": 0,
            "PECM": 0,
            "PECB": 0,

            "seniorities": self.crear_seniorities(self.seniors, self.juniors)
        }

    def get_total_puestos(self):
        return self.juniors + self.seniors

    def crear_seniorities(self, seniors, juniors) -> list:
        # sr = [('senior', "none")] * seniors
        # jr = [('junior', "none")] * juniors
        seniorities = list()
        # seniorities.append(sr)
        # seniorities.append(jr)

        for i in range(seniors):
            seniorities.append(('senior', 0))

        for i in range(juniors):
            seniorities.append(('junior', 0))

        return seniorities

    def get_menor_tps(self, proximas_salidas: list) -> int:
        # try:
        #     return proximas_salidas.index(self.HIGH_VALUE)
        # except:
        #     min_value = min(proximas_salidas)
        #     return proximas_salidas.index(min_value)

        min_value = min(proximas_salidas)
        return proximas_salidas.index(min_value)

    def get_calculo_de_prioridad(self, variables_sistema):
        num = round(random.random(), ndigits=4)
        if num < 0.4:
            variables_sistema["NSA"] = variables_sistema["NSA"] + 1
            variables_sistema["NTA"] = variables_sistema["NTA"] + 1
            return "ALTA"
        elif num < 0.7:
            variables_sistema["NSM"] = variables_sistema["NSM"] + 1
            variables_sistema["NTM"] = variables_sistema["NTM"] + 1
            return "MEDIA"
        else:
            variables_sistema["NSB"] = variables_sistema["NSB"] + 1
            variables_sistema["NTB"] = variables_sistema["NTB"] + 1
            return "BAJA"

    def acumular_stll(self, variables_sistema, prioridad):
        if prioridad == "ALTA":
            variables_sistema["STLLA"] = variables_sistema["STLLA"] + variables_sistema["TPLL"]
        elif prioridad == "MEDIA":
            variables_sistema["STLLM"] = variables_sistema["STLLM"] + variables_sistema["TPLL"]
        else:
            variables_sistema["STLLB"] = variables_sistema["STLLB"] + variables_sistema["TPLL"]

    def get_intervalo_entre_arribos(self):
        num = round(random.uniform(0.0001, 0.9999), 4)
        return -4489.54 * math.log(1.0 - num)  # -4489,54*log(1-x)

    def es_junior(self, seniorities: list, indice) -> bool:
        return seniorities[indice][0] == "junior"

    def generar_tiempo_resolucion_jr(self):
        num = round(random.uniform(0.0001, 0.9999), 4)
        # math.pow((1-num), 1.3368805)
        return 9000 / (math.pow(1 - num, 1.336880522987661))  # 9000/((1-x)^(1.3368805))

    def generar_tiempo_resolucion_sr(self):
        num = round(random.uniform(0.0001, 0.9999), 4)
        # -3945.5 ( -0.313522 - 1 ( -1 log(1 - 1 x ) )^0.5733616191732126 )
        return -3945.5 * (-0.313522 - math.pow(-1 * math.log(1 - num), 0.5733616191732126))

    def acumular_sta(self, variables, prioridad, tiempo_resolucion):
        if prioridad == "ALTA":
            variables["STAA"] = variables["STAA"] + tiempo_resolucion
        elif prioridad == "MEDIA":
            variables["STAM"] = variables["STAM"] + tiempo_resolucion
        else:
            variables["STAB"] = variables["STAB"] + tiempo_resolucion

    def acumular_sts(self, variables, prioridad, tiempo):
        if prioridad == "ALTA":
            variables["STSA"] = variables["STSA"] + tiempo
        elif prioridad == "MEDIA":
            variables["STSM"] = variables["STSM"] + tiempo
        else:
            variables["STSB"] = variables["STSB"] + tiempo

    def calculo_de_prioridad_salida(self, variables, prioridad):
        if variables["NSA"] >= 1:
            variables["NSA"] = variables["NSA"] - 1
            return "ALTA"
        elif variables["NSM"] >= 1:
            variables["NSM"] = variables["NSM"] - 1
            return "MEDIA"
        else:
            variables["NSB"] = variables["NSB"] - 1
            return "BAJA"

        # if prioridad == "ALTA":
        #     variables["NSA"] = variables["NSA"] - 1
        # elif prioridad == "MEDIA":
        #     variables["NSM"] = variables["NSM"] - 1
        # else:
        #     variables["NSB"] = variables["NSB"] - 1

    def get_high_value(self):
        return self.HIGH_VALUE

    def get_tiempo_simulacion(self):
        return self.tiempo_simulacion

    def get_juniors(self):
        return self.juniors

    def get_seniors(self):
        return self.seniors

    def get_puesto_libre(self, tps: list):
        # list_random = tps.copy()
        # random.shuffle(list_random)
        return list_random.index(self.HIGH_VALUE)

    def calcular_resultados(self, variables):
        for index, pto in enumerate(variables["PTO"]):
            variables["PTO"][index] = (variables["STO"][index] / variables["T"]) * 100

        variables["PECA"] = (variables["STSA"] - variables["STLLA"]) / variables["NT"]
        variables["PECM"] = (variables["STSM"] - variables["STLLM"]) / variables["NT"]
        variables["PECB"] = (variables["STSB"] - variables["STLLB"]) / variables["NT"]
