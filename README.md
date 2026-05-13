# workout-statistics
simple apps to check workouts statitics offline with bars graph and muscle distribution

## Requisiti
per file .py necessario installare python su pc e anche streamlit e pandas per far partire il programma

per il file .html nessun prerequisito

file .csv dove sono salvati le sessioni di allenamento

## Come funziona
file .py:
aprire un terminale e lanciare comando streamlit run workout_stats_app.py, si aprirà una finestra browser dove chiederà di caricare file .csv;
una volta caricato avrete le vostre statistiche
(non è necessario internet)

file .html:
aprire il file su un browser e vi chiederà un file .csv; una volta caricato avrete le vostre statistiche
(necessario internet per caricare .csv)

## Cosa vedrai
### file .py 
 statistiche con filtro mensile
 1. sessione con grafici a barre di durata, volume e sets totali e un riassunto
 2. sessione grafico distribuazione dei muscoli comparando il mese precedente

### file .html
panoramica storico alltime
grafiici a barre per durata, volume e sets totali
analisi degli esercizi, usando il filtro selezioni l'esercizio e mostrerà un riassunto e dei grafici a linea
