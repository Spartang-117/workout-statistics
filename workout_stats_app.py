import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Statistiche Allenamenti", layout="wide")
st.title("📊 Statistiche Allenamenti – Dashboard Offline")

# ====================== CARICAMENTO ======================
st.sidebar.header("Carica il tuo file")
uploaded_file = st.sidebar.file_uploader("Seleziona workout_data.csv", type=["csv"])

if uploaded_file is None:
    st.info("👆 Carica il file CSV per iniziare")
    st.stop()

df = pd.read_csv(uploaded_file)

# ====================== PULIZIA DATI ======================
df['start_time'] = pd.to_datetime(df['start_time'], format='%d %b %Y, %H:%M', errors='coerce')
df['end_time'] = pd.to_datetime(df['end_time'], format='%d %b %Y, %H:%M', errors='coerce')
df = df.dropna(subset=['start_time']).sort_values('start_time')

df['volume_kg'] = (df['weight_kg'] * df['reps']).fillna(0)
df['date'] = df['start_time'].dt.date
df['year_month'] = df['start_time'].dt.strftime('%Y-%m')

# ====================== DURATA REALE PER SESSIONE ======================
title_col = 'title' if 'title' in df.columns else df.columns[0]
sessions = df.groupby([title_col, 'start_time']).agg(
    end_time=('end_time', 'first')
).reset_index()

sessions['duration_min'] = (sessions['end_time'] - sessions['start_time']).dt.total_seconds() / 60

df = df.merge(sessions[[title_col, 'start_time', 'duration_min']],
              on=[title_col, 'start_time'], how='left')

# ====================== MAPPATURA MUSCOLI PRINCIPALI E SECONDARI ======================
muscle_map = {
    "Bench Press (Barbell)":          {"primary": ["chest"],      "secondary": ["shoulders", "arms"]},
    "Incline Bench Press (Dumbbell)": {"primary": ["chest"],      "secondary": ["shoulders", "arms"]},
    "Chest Fly (Dumbbell)":           {"primary": ["chest"],      "secondary": ["shoulders"]},
    "Low Cable Fly Crossovers":       {"primary": ["chest"],      "secondary": []},
    "Cable Fly Crossovers":           {"primary": ["chest"],      "secondary": []},

    "Pull Up":                        {"primary": ["back"],       "secondary": ["arms"]},
    "Lat Pulldown (Cable)":           {"primary": ["back"],       "secondary": ["arms"]},
    "Straight Arm Lat Pulldown (Cable)": {"primary": ["back"],    "secondary": []},
    "Single Arm Cable Row":           {"primary": ["back"],       "secondary": ["arms"]},
    "Dumbbell Row":                   {"primary": ["back"],       "secondary": ["arms"]},
    "Inverted Row":                   {"primary": ["back"],       "secondary": []},

    "Overhead Press (Barbell)":       {"primary": ["shoulders"],  "secondary": ["arms"]},
    "Rear Delt Reverse Fly (Machine)":{"primary": ["shoulders"],  "secondary": []},

    "Single Arm Triceps Pushdown (Cable)": {"primary": ["arms"], "secondary": []},
    "Triceps Extension (Cable)":      {"primary": ["arms"],    "secondary": []},
    "Single Arm Curl (Cable)":        {"primary": ["arms"],     "secondary": []},

    "Single Leg Press (Machine)":     {"primary": ["legs"],       "secondary": []},
    "Squat (Barbell)":                {"primary": ["legs"],       "secondary": ["core"]},
    "Walking Lunge (Dumbbell)":       {"primary": ["legs"],       "secondary": []},
    "Hip Thrust (Barbell)":           {"primary": ["legs"],     "secondary": ["legs"]},
    "Hip Abduction (Machine)":        {"primary": ["legs"],       "secondary": []},
    "Hip Adduction (Machine)":        {"primary": ["legs"],       "secondary": []},
    "Standing Calf Raise (Machine)":  {"primary": ["legs"],       "secondary": []},
    "Deadlift (Barbell)":             {"primary": ["legs"],       "secondary": ["back"]},

    "Hanging Leg Raise":              {"primary": ["core"],       "secondary": []},
    "Crunch":                         {"primary": ["core"],       "secondary": []},
    "Decline Crunch":                 {"primary": ["core"],       "secondary": []},

    "Running":                        {"primary": ["cardio"],     "secondary": []},
    "Jump Rope":                      {"primary": ["cardio"],     "secondary": []},
    "Boxing":                         {"primary": ["cardio"],     "secondary": []},

    "Stretching":                     {"primary": ["full body"],  "secondary": []},
    "Warm Up":                        {"primary": ["shoulders"],  "secondary": ["legs"]},
}

# ====================== ESPANSIONE MUSCOLI CON PESI ======================
def expand_muscle_groups(df, muscle_map):
    records = []
    for _, row in df.iterrows():
        ex = row['exercise_title']
        if ex in muscle_map:
            mapping = muscle_map[ex]
            # Muscoli principali (peso 1.0)
            for muscle in mapping.get("primary", []):
                records.append({**row.to_dict(), "muscle_group": muscle, "weight": 1.0})
            # Muscoli secondari (peso 0.5)
            for muscle in mapping.get("secondary", []):
                records.append({**row.to_dict(), "muscle_group": muscle, "weight": 0.5})
        else:
            records.append({**row.to_dict(), "muscle_group": "full body", "weight": 1.0})
    return pd.DataFrame(records)

expanded_df = expand_muscle_groups(df, muscle_map)

# ====================== FILTRO MENSILE ======================
st.sidebar.header("Filtro Mensile")
unique_months = sorted(df['year_month'].unique())

month_names_it = {
    '01':'Gennaio','02':'Febbraio','03':'Marzo','04':'Aprile','05':'Maggio',
    '06':'Giugno','07':'Luglio','08':'Agosto','09':'Settembre',
    '10':'Ottobre','11':'Novembre','12':'Dicembre'
}

month_options = [f"{month_names_it[m[5:7]]} {m[:4]}" for m in unique_months]
month_options.append("Tutto il periodo")

selected_label = st.sidebar.selectbox("Seleziona mese", month_options)

if selected_label == "Tutto il periodo":
    filtered_df = df.copy()
    filtered_expanded = expanded_df.copy()
    prev_month_df = pd.DataFrame()
    prev_expanded = pd.DataFrame()
else:
    month_str = selected_label.split()[0]
    year_str = selected_label.split()[1]
    month_num = [k for k, v in month_names_it.items() if v == month_str][0]
    selected_ym = f"{year_str}-{month_num}"
    
    filtered_df = df[df['year_month'] == selected_ym].copy()
    filtered_expanded = expanded_df[expanded_df['year_month'] == selected_ym].copy()
    
    prev_date = datetime.strptime(selected_ym, '%Y-%m') - timedelta(days=35)
    prev_ym = prev_date.strftime('%Y-%m')
    prev_month_df = df[df['year_month'] == prev_ym].copy()
    prev_expanded = expanded_df[expanded_df['year_month'] == prev_ym].copy()

# ====================== CONFIGURAZIONE GRAFICI ======================
config_fixed = {'staticPlot': True, 'displayModeBar': False}

# ====================== 1. PROGRESSO GIORNALIERO + RIEPILOGO ======================
st.header("1. Progresso Giornaliero")

daily = filtered_df.groupby('date').agg({
    'duration_min': 'sum',
    'volume_kg': 'sum',
    'exercise_title': 'count'
}).rename(columns={'exercise_title': 'sets'}).reset_index()

# Riepilogo Mensile
st.subheader("📋 Riepilogo Periodo Selezionato")

num_workouts = filtered_df.groupby(['start_time', title_col]).ngroups if not filtered_df.empty else 0
total_duration = filtered_df['duration_min'].sum()
total_volume = filtered_df['volume_kg'].sum()
total_sets = filtered_df['exercise_title'].count()

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Workout", f"{num_workouts}")
with col_m2:
    st.metric("Durata Totale", f"{total_duration:.0f} min")
with col_m3:
    st.metric("Volume Totale", f"{total_volume:,.0f} kg")
with col_m4:
    st.metric("Sets Totali", f"{total_sets:,}")

st.markdown("---")

# Grafici Giornalieri
col1, col2, col3 = st.columns(3)
with col1:
    fig_dur = px.bar(daily, x='date', y='duration_min', 
                     title="Durata totale per giorno (minuti)",
                     color_discrete_sequence=['#1f77b4'])
    st.plotly_chart(fig_dur, use_container_width=True, config=config_fixed)

with col2:
    fig_vol = px.bar(daily, x='date', y='volume_kg', 
                     title="Volume sollevato per giorno (kg)",
                     color_discrete_sequence=['#ff7f0e'])
    st.plotly_chart(fig_vol, use_container_width=True, config=config_fixed)

with col3:
    fig_sets = px.bar(daily, x='date', y='sets', 
                      title="Sets totali per giorno",
                      color_discrete_sequence=['#2ca02c'])
    st.plotly_chart(fig_sets, use_container_width=True, config=config_fixed)

# ====================== 2. RADAR GRUPPI MUSCOLARI ======================
st.header("2. Radar Gruppi Muscolari (Sets ponderati) – vs Mese Precedente")

def get_avg_sets(data):
    if data.empty:
        return [0] * 6
    days = (data['start_time'].max() - data['start_time'].min()).days + 1
    weeks = max(days / 7, 0.01)
    summary = data.groupby('muscle_group')['weight'].sum()
    groups = ['chest', 'back', 'core', 'shoulders', 'arms', 'legs']
    return [summary.get(g, 0) / weeks for g in groups]

categories = ['Chest', 'Back', 'Core', 'Shoulders', 'Arms', 'Legs']
values_current = get_avg_sets(filtered_expanded)
values_prev = get_avg_sets(prev_expanded)

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=values_current + [values_current[0]], theta=categories + [categories[0]],
    fill='toself', name='Mese selezionato', line_color='royalblue'
))
fig_radar.add_trace(go.Scatterpolar(
    r=values_prev + [values_prev[0]], theta=categories + [categories[0]],
    fill='toself', name='Mese precedente', line_color='lightgray'
))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, max(values_current + values_prev) * 1.2])),
    title="Confronto Sets medi settimanali ponderati (Principale=1 | Secondario=0.5)",
    height=650
)
st.plotly_chart(fig_radar, use_container_width=True, config=config_fixed)

# ====================== 3. CLASSIFICA GRUPPI MUSCOLARI ======================
st.header("3. Main Muscle Groups – Classifica per Sets Ponderati")

muscle_rank = filtered_expanded.groupby('muscle_group')['weight'].sum().reset_index()
muscle_rank.columns = ['Gruppo Muscolare', 'Sets Ponderati']
muscle_rank = muscle_rank.sort_values('Sets Ponderati', ascending=False)

fig_rank = px.bar(muscle_rank, x='Sets Ponderati', y='Gruppo Muscolare', orientation='h',
                  title="Classifica gruppi muscolari più allenati (Principale = 1 | Secondario = 0.5)",
                  color='Sets Ponderati', color_continuous_scale='Blues', text='Sets Ponderati')

fig_rank.update_traces(textposition='outside')
fig_rank.update_layout(yaxis={'categoryorder': 'total ascending'}, height=600)

st.plotly_chart(fig_rank, use_container_width=True, config=config_fixed)
st.dataframe(muscle_rank.style.hide(axis="index").format({"Sets Ponderati": "{:.1f}"}), 
             use_container_width=True)

# ====================== FINE ======================
st.success("✅ Dashboard aggiornata e stabile!")
st.caption("Muscoli principali = 1 • Muscoli secondari = 0.5 • Tutti i grafici sono fissi")