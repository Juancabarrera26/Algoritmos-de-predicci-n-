# Ejercicio 2

gramatica = {
    "S": [["A", "B", "uno"]],
    "A": [["dos", "B"], ["ε"]],
    "B": [["C", "D"], ["tres"], ["ε"]],
    "C": [["cuatro", "A", "B"], ["cinco"]],
    "D": [["seis"], ["ε"]],
}

no_terminales   = {"S", "A", "B", "C", "D"}
simbolo_inicial = "S"


# Primeros

def calcular_first(gramatica):
    first = {nt: set() for nt in no_terminales}

    cambio = True
    while cambio:
        cambio = False
        for nt, producciones in gramatica.items():
            for prod in producciones:

                # Produccion vacia
                if prod == ["ε"]:
                    if "ε" not in first[nt]:
                        first[nt].add("ε")
                        cambio = True
                    continue

                # Recorrer simbolos hasta encontrar uno que no derive ε
                for simbolo in prod:
                    if simbolo not in no_terminales:
                        # Terminal: se agrega y se para
                        if simbolo not in first[nt]:
                            first[nt].add(simbolo)
                            cambio = True
                        break
                    else:
                        # No-terminal: se agrega su first (sin ε)
                        antes = len(first[nt])
                        first[nt].update(first[simbolo] - {"ε"})
                        if len(first[nt]) != antes:
                            cambio = True
                        # Solo se continua si este simbolo puede ser ε
                        if "ε" not in first[simbolo]:
                            break
                else:
                    # Todos los simbolos pueden ser ε
                    if "ε" not in first[nt]:
                        first[nt].add("ε")
                        cambio = True

    return first


# FIRST de una secuencia (usado en siguientes y prediccion) 

def first_secuencia(secuencia, first):
    resultado = set()
    for simbolo in secuencia:
        if simbolo not in no_terminales:
            resultado.add(simbolo)
            break
        resultado.update(first[simbolo] - {"ε"})
        if "ε" not in first[simbolo]:
            break
    else:
        resultado.add("ε")
    return resultado


# Siguientes

def calcular_follow(gramatica, first):
    follow = {nt: set() for nt in no_terminales}
    follow[simbolo_inicial].add("$")

    cambio = True
    while cambio:
        cambio = False
        for nt, producciones in gramatica.items():
            for prod in producciones:
                if prod == ["ε"]:
                    continue
                for i, simbolo in enumerate(prod):
                    if simbolo not in no_terminales:
                        continue
                    resto = prod[i + 1:]
                    if resto:
                        fb = first_secuencia(resto, first)
                        antes = len(follow[simbolo])
                        follow[simbolo].update(fb - {"ε"})
                        # Si el resto puede ser ε, se hereda el FOLLOW del padre
                        if "ε" in fb:
                            follow[simbolo].update(follow[nt])
                        if len(follow[simbolo]) != antes:
                            cambio = True
                    else:
                        # El simbolo esta al final: hereda FOLLOW del padre
                        antes = len(follow[simbolo])
                        follow[simbolo].update(follow[nt])
                        if len(follow[simbolo]) != antes:
                            cambio = True

    return follow


# Prediccion 

def calcular_predict(gramatica, first, follow):
    predict = {}
    for nt, producciones in gramatica.items():
        for prod in producciones:
            fa   = first_secuencia(prod, first)
            pred = fa - {"ε"}
            # Si la produccion puede generar ε, se agregan los SIGUIENTES
            if "ε" in fa:
                pred = pred | follow[nt]
            predict[(nt, tuple(prod))] = pred
    return predict


# Resultados 

first   = calcular_first(gramatica)
follow  = calcular_follow(gramatica, first)
predict = calcular_predict(gramatica, first, follow)

orden = ["S", "A", "B", "C", "D"]

print("Primeros")
for nt in orden:
    print(f"  FIRST({nt})  = {sorted(first[nt])}")

print("Siguientes")
for nt in orden:
    print(f"  FOLLOW({nt}) = {sorted(follow[nt])}")

print("Prediccion")
for (nt, prod), conj in predict.items():
    print(f"  PREDICT({nt} → {' '.join(prod)}) = {sorted(conj)}")
