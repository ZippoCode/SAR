# Sistemi e Applicazioni di Reti

Implementazione degli esercizi e del materiale didattico fornito durante il corso di **Sistemi e Applicazioni di Rete** presso l'Università di Modena e Reggio Emilia.


## SETUP
Linee guida per utilizzare il materiale

### Installare i plugin
E' necessario installare Python3 e Python2 (dipende dalla tipologia di esercizi). Inoltre, installare **Google App Engine** seguendo le istruzioni presenti al seguente [link](https://cloud.google.com/appengine/docs/standard/python/download).

#### Installazione PIP e moduli
Per installare i moduli necessari per le funzionalità installare il modulo *PIP* che è possibile scaricare al seguente [indirizzo](https://docs.python.org/3/installing/index.html).
Per eseguire gli applicativi utilizzare i comandi:
```
cd /path/to/folder
mkdir lib
pip install -t lib -r requirements.txt
```
### Avviare Flask APP
Nel caso in cui si desideri avviare solamente la Flask app (cartella numero quattro del package - 04.Flask)
è necessario giungere nella cartella che contiene lo script python con l'applicazione e digitare
```
export FLASK_APP=flask_app
flask run
```
E per utilizzarla collegarsi al seguente indirizzo [http:://127.0.0.1:5000](http:://127.0.0.1:5000)

### Avviare Google App Engine
Se invece si sta utilizzando una Google App Engine, dopo aver installato tutti i moduli necessari,
è possibile eseguire l'applicativo con il comando:
```
dev_appserver.py app.yaml
```

### GCloud
Se si volesse estendere l'applicazione dall'ambiente locale a quello di Google App Engine è possibile fare tremite le seguenti istruzioni:

**Attenzione:** E' necessario aver creato un account GAE per poter effettuare l'upload del codice.
```
gcloud init
gcloud app deploy
```

### Mosquitto
Per eseguire il tool Mosquitto è necessario innanzitutto aver installato Python3 e avviare *virtualenv* nel quale siano installati i moduli richiesti. Successivamente si avviano tre diversi terminali e, in particolare, nel primo si avvia il broker
```
source /<path to env>/bin/activate
# A seconda della modalità
  - mosquitto
  - mosquitto -p <numero porta>
  - mosquitto -c mosquitto.conf
```

Mentre negli altri si avviano gli script:
```
python3 <nome script subscriber>.py
python3 <nome script publisher>.py
```
