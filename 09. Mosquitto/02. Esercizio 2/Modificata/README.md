#### Esercizio 2


L'esercizio è stato leggermente modificato per renderlo simile alle tracce d'esame, la soluzione origale è presente
all'interno del file .rar

Nella soluzione impostata da me è presente un modo per salvare gli stati delle stanze di ogni piano.

    - GET ('/api/v1.0/get/<piano>')
       Restituisce lo stato delle stato della piano indicato


Nella parte MQTT sono presenti due script uno con il compito di accedere allo stato di un piano
indicato come argomento e di pubblicarlo mentre il subscriber stampa lo stato.