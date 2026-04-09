# Ejercicios 1 y 2

## Gramática del Ejercicio 1
Reglas:
	•	S → A uno B C
	•	S → S dos
	•	A → B C D
	•	A → A tres
	•	A → ε
	•	B → D cuatro C tres
	•	B → ε
	•	C → cinco D B
	•	C → ε
	•	D → seis
	•	D → ε

# PRIMEROS (FIRST)
Recuerda: FIRST(X) = conjunto de terminales con los que puede comenzar cualquier cadena derivable desde X. Si X puede derivar ε, también incluimos ε.
FIRST(D)
	•	D → seis → {seis}
	•	D → ε → {ε}
FIRST(D) = {seis, ε}
FIRST(C)
	•	C → cinco D B → {cinco}
	•	C → ε → {ε}
FIRST(C) = {cinco, ε}
FIRST(B)
	•	B → D cuatro C tres: tomamos FIRST(D) = {seis, ε}
	•	Como D puede ser ε, seguimos: añadimos cuatro
	•	→ {seis, cuatro}
	•	B → ε → {ε}
FIRST(B) = {seis, cuatro, ε}
FIRST(A)
	•	A → B C D: tomamos FIRST(B) = {seis, cuatro, ε}
	•	Como B puede ser ε → FIRST(C) = {cinco, ε}
	•	Como C puede ser ε → FIRST(D) = {seis, ε}
	•	Como D puede ser ε → añadimos ε
	•	→ {seis, cuatro, cinco, ε}
	•	A → A tres: FIRST(A) contiene lo que ya tenemos (recursivo izquierdo, no añade nada nuevo sobre terminales, excepto que A puede generar ε, entonces añadimos tres)
	•	→ añade tres
	•	A → ε → {ε}
FIRST(A) = {seis, cuatro, cinco, tres, ε}
FIRST(S)
	•	S → A uno B C: FIRST(A) = {seis, cuatro, cinco, tres, ε}
	•	Como A puede ser ε → añadimos uno
	•	→ {seis, cuatro, cinco, tres, uno}
	•	S → S dos: recursivo izquierdo, FIRST(S) ya contiene lo anterior; como S puede derivar ε? Solo si A uno B C puede ser ε — pero uno es terminal obligatorio, así que S no deriva ε.
	•	No añade ε.
FIRST(S) = {seis, cuatro, cinco, tres, uno}
