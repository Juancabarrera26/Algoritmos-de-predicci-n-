# Ejercicio 1 - PRIMEROS, SIGUIENTES y PREDICCIÓN
#
# S → A uno B C | S dos
# A → B C D | A tres | ε
# B → D cuatro C tres | ε
# C → cinco D B | ε
# D → seis | ε

gramatica = {
    "S": [["A", "uno", "B", "C"], ["S", "dos"]],
    "A": [["B", "C", "D"], ["A", "tres"], ["ε"]],
    "B": [["D", "cuatro", "C", "tres"], ["ε"]],
    "C": [["cinco", "D", "B"], ["ε"]],
    "D": [["seis"], ["ε"]],
}

no_terminales   = {"S", "A", "B", "C", "D"}
simbolo_inicial = "S"


# ── PRIMEROS ──────────────────────────────────────────────────────────────────

def calcular_first(gramatica):
    first = {nt: set() for nt in no_terminales}

    cambio = True
    while cambio:
        cambio = False
        for nt, producciones in gramatica.items():
            for prod in producciones:

                # Producción vacía
                if prod == ["ε"]:
                    if "ε" not in first[nt]:
                        first[nt].add("ε")
                        cambio = True
                    continue

                # Recorrer símbolos hasta encontrar uno que no derive ε
                for simbolo in prod:
                    if simbolo not in no_terminales:
                        # Terminal: se agrega y se para
                        if simbolo not in first[nt]:
                            first[nt].add(simbolo)
                            cambio = True
                        break
                    else:
                        # No-terminal: se agrega su FIRST (sin ε)
                        antes = len(first[nt])
                        first[nt].update(first[simbolo] - {"ε"})
                        if len(first[nt]) != antes:
                            cambio = True
                        # Solo se continúa si este símbolo puede ser ε
                        if "ε" not in first[simbolo]:
                            break
                else:
                    # Todos los símbolos pueden ser ε
                    if "ε" not in first[nt]:
                        first[nt].add("ε")
                        cambio = True

    return first


# ── FIRST de una secuencia (usado en SIGUIENTES y PREDICCIÓN) ─────────────────

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


# ── SIGUIENTES ────────────────────────────────────────────────────────────────

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
                        # El símbolo está al final: hereda FOLLOW del padre
                        antes = len(follow[simbolo])
                        follow[simbolo].update(follow[nt])
                        if len(follow[simbolo]) != antes:
                            cambio = True

    return follow


# ── PREDICCIÓN ────────────────────────────────────────────────────────────────

def calcular_predict(gramatica, first, follow):
    predict = {}
    for nt, producciones in gramatica.items():
        for prod in producciones:
            fa   = first_secuencia(prod, first)
            pred = fa - {"ε"}
            # Si la producción puede generar ε, se agregan los SIGUIENTES
            if "ε" in fa:
                pred = pred | follow[nt]
            predict[(nt, tuple(prod))] = pred
    return predict


# ── Resultados ────────────────────────────────────────────────────────────────

first   = calcular_first(gramatica)
follow  = calcular_follow(gramatica, first)
predict = calcular_predict(gramatica, first, follow)

orden = ["S", "A", "B", "C", "D"]

print("PRIMEROS")
for nt in orden:
    print(f"  FIRST({nt})  = {sorted(first[nt])}")

print("\nSIGUIENTES")
for nt in orden:
    print(f"  FOLLOW({nt}) = {sorted(follow[nt])}")

print("\nPREDICCIÓN")
for (nt, prod), conj in predict.items():
    print(f"  PREDICT({nt} → {' '.join(prod)}) = {sorted(conj)}")
