# Procesadores de Lenguaje — FIRST, FOLLOW y PREDICCION

> Calculo de los conjuntos de **PRIMEROS**, **SIGUIENTES** y **PREDICCION** para dos gramáticas libres de contexto.

-----

## Convenciones

|Símbolo                              |Significado                              |
|-------------------------------------|-----------------------------------------|
|Letras mayusculas (`S`, `A`, `B`…)   |No-terminales                            |
|Palabras en minuscula (`uno`, `dos`…)|Terminales                               |
|`ε`                                  |Cadena vacia                             |
|`$`                                  |Fin de cadena (marcador de fondo de pila)|

-----

## Ejercicio 1

### Gramática

```
S → A uno B C
S → S dos
A → B C D
A → A tres
A → ε
B → D cuatro C tres
B → ε
C → cinco D B
C → ε
D → seis
D → ε
```

-----

### FIRST

#### FIRST(D)

- `D → seis` → `seis` es terminal → lo añadimos
- `D → ε` → producción vacía → añadimos `ε`

> **FIRST(D) = { seis, ε }**

-----

#### FIRST(C)

- `C → cinco D B` → `cinco` es terminal → lo añadimos
- `C → ε` → produccion vacia → añadimos `ε`

> **FIRST(C) = { cinco, ε }**

-----

#### FIRST(B)

- `B → D cuatro C tres`:
  - FIRST(D) = { seis, ε } → añadimos `seis`
  - D puede ser `ε` → miramos el siguiente simbolo: `cuatro` es terminal → añadimos `cuatro`
- `B → ε` → añadimos `ε`

> **FIRST(B) = { seis, cuatro, ε }**

-----

#### FIRST(A)

- `A → B C D`:
  - FIRST(B) \ {ε} = { seis, cuatro } → los añadimos
  - B puede ser `ε` → FIRST(C) \ {ε} = { cinco } → añadimos `cinco`
  - C puede ser `ε` → FIRST(D) \ {ε} = { seis } → ya estaba
  - D puede ser `ε` → toda la cadena puede ser `ε` → añadimos `ε`
- `A → A tres` (recursion izquierda): como A puede llegar a `ε`, el simbolo `tres` es alcanzable → añadimos `tres`
- `A → ε` → `ε` ya esta

> **FIRST(A) = { seis, cuatro, cinco, tres, ε }**

-----

#### FIRST(S)

- `S → A uno B C`:
  - FIRST(A) \ {ε} = { seis, cuatro, cinco, tres } → los añadimos
  - A puede ser `ε` → siguiente simbolo `uno` es terminal → añadimos `uno`
  - `uno` no puede ser `ε` → paramos
- `S → S dos` (recursion izquierda): FIRST(S) ya contiene lo calculado; S nunca deriva `ε` porque `uno` siempre aparece

> **FIRST(S) = { seis, cuatro, cinco, tres, uno }**

-----

### FOLLOW

#### FOLLOW(S)

- S es el simbolo inicial → añadimos `$`
- `S → S dos`: S aparece seguido de `dos` → añadimos `dos`

> **FOLLOW(S) = { dos, $ }**

-----

#### FOLLOW(A)

- `S → A uno B C`: A está seguido de `uno` (terminal) → añadimos `uno`
- `uno` no puede ser `ε` → paramos aquí

> **FOLLOW(A) = { uno }**

-----

#### FOLLOW(B)

- `S → A uno B C`: B seguido de C
  - FIRST(C) \ {ε} = { cinco } → añadimos `cinco`
  - C puede ser `ε` → añadimos FOLLOW(S) = { dos, $ }
- `A → B C D`: B seguido de C D
  - FIRST(C) \ {ε} = { cinco } → ya estaba
  - C puede ser `ε` → FIRST(D) \ {ε} = { seis } → añadimos `seis`
  - D puede ser `ε` → añadimos FOLLOW(A) = { uno }
- `C → cinco D B`: B al final → añadimos FOLLOW(C) = { dos, $, seis, uno, tres } → añadimos `tres`

> **FOLLOW(B) = { cinco, seis, uno, dos, tres, $ }**

-----

#### FOLLOW(C)

- `S → A uno B C`: C al final → añadimos FOLLOW(S) = { dos, $ }
- `A → B C D`: C seguido de D
  - FIRST(D) \ {ε} = { seis } → añadimos `seis`
  - D puede ser `ε` → añadimos FOLLOW(A) = { uno }
- `B → D cuatro C tres`: C seguido de `tres` (terminal) → añadimos `tres`

> **FOLLOW(C) = { dos, $, seis, uno, tres }**

-----

#### FOLLOW(D)

- `B → D cuatro C tres`: D seguido de `cuatro` → añadimos `cuatro`
- `A → B C D`: D al final → añadimos FOLLOW(A) = { uno }
- `C → cinco D B`: D seguido de B
  - FIRST(B) \ {ε} = { seis, cuatro } → añadimos `seis`
  - B puede ser `ε` → añadimos FOLLOW(C) = { dos, $, seis, uno, tres }

> **FOLLOW(D) = { cuatro, uno, seis, dos, tres, $ }**

-----

### PREDICCION

> **Regla:** `PREDICT(A → α) = FIRST(α) \ {ε}`, y si `ε ∈ FIRST(α)` entonces tambien se añade `FOLLOW(A)`.

|Regla                |PREDICT                            |
|---------------------|-----------------------------------|
|`S → A uno B C`      |{ seis, cuatro, cinco, tres, uno } |
|`S → S dos`          |{ seis, cuatro, cinco, tres, uno } |
|`A → B C D`          |{ seis, cuatro, cinco, tres, uno } |
|`A → A tres`         |{ seis, cuatro, cinco, tres }      |
|`A → ε`              |{ uno }                            |
|`B → D cuatro C tres`|{ seis, cuatro }                   |
|`B → ε`              |{ cinco, seis, uno, dos, tres, $ } |
|`C → cinco D B`      |{ cinco }                          |
|`C → ε`              |{ dos, $, seis, uno, tres }        |
|`D → seis`           |{ seis }                           |
|`D → ε`              |{ cuatro, uno, seis, dos, tres, $ }|


> **La gramatica 1 NO es LL(1)**: las reglas de `S` y `A` tienen conjuntos de PREDICCION solapados, por lo que un parser descendente determinista no puede elegir unívocamente que produccion aplicar.

-----

-----

## Ejercicio 2

### Gramatica

```
S → A B uno
A → dos B
A → ε
B → C D
B → tres
B → ε
C → cuatro A B
C → cinco
D → seis
D → ε
```

-----

### FIRST

#### FIRST(D)

- `D → seis` → `seis` es terminal → lo añadimos
- `D → ε` → produccion vacia → añadimos `ε`

> **FIRST(D) = { seis, ε }**

-----

#### FIRST(C)

- `C → cuatro A B` → `cuatro` es terminal → lo añadimos
- `C → cinco` → `cinco` es terminal → lo añadimos
- Ninguna produccion de C genera `ε` directamente

> **FIRST(C) = { cuatro, cinco }**

-----

#### FIRST(B)

- `B → C D`: FIRST(C) = { cuatro, cinco } y C **no** deriva `ε` → añadimos ambos y paramos
- `B → tres` → `tres` es terminal → lo añadimos
- `B → ε` → añadimos `ε`

> **FIRST(B) = { cuatro, cinco, tres, ε }**

-----

#### FIRST(A)

- `A → dos B` → `dos` es terminal → lo añadimos; `dos` no puede ser `ε` → paramos
- `A → ε` → añadimos `ε`

> **FIRST(A) = { dos, ε }**

-----

#### FIRST(S)

- `S → A B uno`:
  - FIRST(A) \ {ε} = { dos } → añadimos `dos`
  - A puede ser `ε` → FIRST(B) \ {ε} = { cuatro, cinco, tres } → los añadimos
  - B puede ser `ε` → siguiente simbolo `uno` es terminal → añadimos `uno`
  - `uno` no puede ser `ε` → paramos
- S nunca puede derivar `ε` porque `uno` siempre aparece

> **FIRST(S) = { dos, cuatro, cinco, tres, uno }**

-----

### FOLLOW

#### FOLLOW(S)

- S es el simbolo inicial → añadimos `$`
- S no aparece en el lado derecho de ninguna produccion

> **FOLLOW(S) = { $ }**

-----

#### FOLLOW(A)

- `S → A B uno`: A seguido de B uno
  - FIRST(B) \ {ε} = { cuatro, cinco, tres } → los añadimos
  - B puede ser `ε` → siguiente es `uno` (terminal) → añadimos `uno`
- `C → cuatro A B`: A seguido de B
  - FIRST(B) \ {ε} = { cuatro, cinco, tres } → ya están
  - B puede ser `ε` → añadimos FOLLOW(C)
  - FOLLOW(C) incluye `seis` (calculado abajo) → añadimos `seis`

> **FOLLOW(A) = { cuatro, cinco, tres, uno, seis }**

-----

#### FOLLOW(B)

- `S → A B uno`: B seguido de `uno` → añadimos `uno`
- `A → dos B`: B al final → añadimos FOLLOW(A)
- `C → cuatro A B`: B al final → añadimos FOLLOW(C)
- FOLLOW(A) = FOLLOW(C) = { cuatro, cinco, tres, uno, seis } (dependencias circulares resueltas por iteracion)

> **FOLLOW(B) = { cuatro, cinco, tres, uno, seis }**

-----

#### FOLLOW(C)

- `B → C D`: C seguido de D
  - FIRST(D) \ {ε} = { seis } → añadimos `seis`
  - D puede ser `ε` → añadimos FOLLOW(B) = { cuatro, cinco, tres, uno, seis }

> **FOLLOW(C) = { cuatro, cinco, tres, uno, seis }**

-----

#### FOLLOW(D)

- `B → C D`: D al final → añadimos FOLLOW(B) = { cuatro, cinco, tres, uno, seis }

> **FOLLOW(D) = { cuatro, cinco, tres, uno, seis }**

-----

### PREDICCION

> **Regla:** `PREDICT(A → α) = FIRST(α) \ {ε}`, y si `ε ∈ FIRST(α)` entonces tambien se añade `FOLLOW(A)`.

|Regla           |PREDICT                           |
|----------------|----------------------------------|
|`S → A B uno`   |{ dos, cuatro, cinco, tres, uno } |
|`A → dos B`     |{ dos }                           |
|`A → ε`         |{ cuatro, cinco, seis, tres, uno }|
|`B → C D`       |{ cuatro, cinco }                 |
|`B → tres`      |{ tres }                          |
|`B → ε`         |{ cuatro, cinco, seis, tres, uno }|
|`C → cuatro A B`|{ cuatro }                        |
|`C → cinco`     |{ cinco }                         |
|`D → seis`      |{ seis }                          |
|`D → ε`         |{ cuatro, cinco, seis, tres, uno }|


> **La gramática 2 SÍ es LL(1)**: los conjuntos de PREDICCION de todas las reglas con el mismo no-terminal son disjuntos, por lo que un parser descendente determinista puede elegir unívocamente que produccion aplicar en cada caso.