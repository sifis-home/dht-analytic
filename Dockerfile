# Usa un'immagine di base di Python
FROM ubuntu:latest
# Installa le dipendenze richieste
RUN apt-get update && apt-get -y install python3 python3-pip
RUN mkdir /app

# Imposta la directory di lavoro all'interno del contenitore
WORKDIR /app

# Installa le dipendenze necessarie
COPY requirements.txt /app/requirements.txt

# Copia il codice nella directory di lavoro dell'immagine Docker
ADD dht_analytic /

#COPY catch_dht_inquiry.py /app
#COPY classification_server.py /app
#COPY send_results.py /app
#COPY model.joblib /app


# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get install nano


