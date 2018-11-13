## Comandi per avviare l'esercizio
Dopo aver avviato l'ambiente virtuale.
Spostarsi nella cartella che contengono i file e digitare su tre terminali distinti i tre comandi

```
mosquitto -c mosquitto.conf
python3 flask_app.py
python3 subscriber.py [0,1,2]
```
I numeri ***[0,1,2]*** identificano i piani:
  * Piano seminterrato
  * Primo terra
  * Primo piano

Successivamente digitare sul browser *http://localhost:5000*
