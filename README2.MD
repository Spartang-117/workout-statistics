# Workout Statistics

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL_3.0-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-E34F26?logo=html5&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)

**Applicazioni semplici per analizzare le statistiche dei tuoi allenamenti in modo completamente offline**, con grafici a barre e distribuzione dei muscoli.

---

## Descrizione

Questo repository contiene **due strumenti** per visualizzare e analizzare i dati dei tuoi workout salvati in formato **CSV**:

- **Versione Python + Streamlit** → interfaccia interattiva con filtro mensile
- **Versione HTML + JavaScript** → applicazione web standalone (nessuna installazione)

Entrambe le applicazioni elaborano i dati localmente e **non richiedono connessione internet** (tranne per caricare il file CSV nella versione HTML).

## Funzionalità

### Versione Python (`workout_stats_app.py`)
- Filtro per mese
- Grafici a barre: **Durata**, **Volume totale** e **Set totali**
- Riassunto della sessione
- Grafico di distribuzione dei muscoli confrontato con il mese precedente

### Versione HTML (`workout-stats.html`)
- Panoramica storica **all-time**
- Grafici a barre per durata, volume e set totali
- Analisi dettagliata per singolo esercizio:
  - Record personali (PR)
  - Grafici a linea di progressione (peso, volume, 1RM stimato, reps)
  - Design moderno e responsive

## Requisiti

### Per `workout_stats_app.py` (Streamlit)
- Python 3.8+
- `streamlit`
- `pandas`
- `plotly` (o matplotlib)

### Per `workout-stats.html`
- Nessuna installazione richiesta
- Un browser moderno

### File dati
- `workout_data.csv` contenente le sessioni di allenamento

## Installazione e Utilizzo

### 1. Versione Streamlit (consigliata)

bash
# Clona il repository
git clone https://github.com/Spartang-117/workout-statistics.git
cd workout-statistics

# Installa le dipendenze
pip install streamlit pandas plotly

# Avvia l'applicazione
streamlit run workout_stats_app.py

Carica il tuo file workout_data.csv quando richiesto.

###2. Versione HTML

Scarica o apri direttamente il file workout-stats.html
Clicca su "Carica workout_data.csv"
Visualizza immediatamente le statistiche


##Struttura del Repository
textworkout-statistics/
├── workout_stats_app.py          # Versione Streamlit
├── workout-stats.html            # Versione Web standalone
├── workout_data.csv              # (esempio o il tuo file)
├── LICENSE
└── README.md

Come preparare il file CSV
Il file deve contenere almeno le seguenti colonne (adattabili):

start_time
end_time
exercise_title
set_type
weight_kg
reps

(Puoi aggiungere un esempio di CSV nel repository se vuoi)
Tecnologie Utilizzate

Python + Streamlit + Pandas + Plotly
HTML5 + Tailwind CSS + Chart.js + PapaParse

Licenza
Questo progetto è distribuito sotto licenza GNU GPL-3.0 — vedi il file LICENSE per maggiori dettagli.
Contatti

Autore: Spartang-117
Sentiti libero di aprire una Issue o una Pull Request se vuoi contribuire o segnalare miglioramenti.


Grazie per aver visitato il repository!
Se ti è utile, lascia una ⭐ per supportare il progetto.
