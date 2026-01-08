import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configurazione della pagina
st.set_page_config(page_title="Test Stile di Apprendimento (Kolb)", layout="wide")

# --- CSS Personalizzato per nascondere elementi superflui e migliorare la grafica ---
st.markdown("""
<style>
    .stRadio > label {display: none;}
    .row-box {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #ddd;
    }
    .question-text {
        font-size: 16px;
        font-weight: 500;
        min-height: 80px;
    }
</style>
""", unsafe_allow_html=True)

# --- Dati del Test (Le 9 righe x 4 colonne) ---
data = [
    {
        "id": 1,
        "items": [
            "Apprendo meglio selezionando ciò che mi pare importante, valutando le differenze con un approccio critico e logico.",
            "Apprendo meglio immaginando possibili scenari: 'cosa succederebbe se...'. Preferisco la teoria alla certezza immediata.",
            "Apprendo meglio se mi immergo totalmente nell'esperienza, usando le emozioni e il contatto personale.",
            "Apprendo meglio provando ad applicare le conoscenze. Cerco l'utilità immediata e strumenti concreti."
        ]
    },
    {
        "id": 2,
        "items": [
            "Apprendo innanzitutto ascoltando e accogliendo dati esterni. Sono aperto alle informazioni senza giudicarle subito.",
            "Apprendo innanzitutto focalizzandomi su ciò che mi pare rilevante e appropriato al contesto specifico attuale.",
            "Apprendo scomponendo i concetti in parti più piccole. Uso la logica per esaminare i dettagli.",
            "Apprendo innanzitutto tenendo una posizione neutra e oggettiva: osservo i fatti evitando di coinvolgermi emotivamente."
        ]
    },
    {
        "id": 3,
        "items": [
            "Per lo più apprendo basandomi sull'intuito e seguendo le mie reazioni 'di pancia'.",
            "Per lo più apprendo osservando gli altri e gli eventi che accadono. Preferisco guardare per raccogliere dati prima di agire.",
            "Per lo più apprendo attraverso il ragionamento deduttivo. Tendo ad affidarmi all'intelletto e alla coerenza mentale.",
            "Per lo più apprendo facendo: ho bisogno di movimento, azione e interazione diretta con l'ambiente."
        ]
    },
    {
        "id": 4,
        "items": [
            "Imparo accogliendo le situazioni e le persone così come sono. Ho un approccio empatico e non giudicante.",
            "Imparo sfidando l'ignoto. Considero l'errore come parte del gioco e mi lancio in nuove prove.",
            "Imparo giudicando il valore delle idee: confronto i pro e i contro prima di assimilare un concetto.",
            "Imparo avendo piena coscienza di ciò che sto facendo. Cerco di essere lucido e presente nel processo."
        ]
    },
    {
        "id": 5,
        "items": [
            "Apprendo meglio cogliendo il senso generale nell'istante, senza seguire necessariamente una serie di passaggi logici.",
            "Apprendo meglio finalizzando lo sforzo al risultato. Voglio che l'apprendimento generi un output tangibile.",
            "Apprendo meglio seguendo un filo conduttore razionale, sequenziale e coerente (causa-effetto).",
            "Apprendo meglio ponendomi domande e sollevando dubbi. Per me l'apprendimento è una sfida da risolvere."
        ]
    },
    {
        "id": 6,
        "items": [
            "Apprendo meglio studiando concetti, teorie e formulando modelli mentali. Preferisco le idee alla realtà concreta.",
            "Apprendo meglio stando 'alla finestra' ad osservare. Poi rifletto su ciò che vedo, senza intervenire subito.",
            "Apprendo meglio “toccando con mano”. Preferisco esempi reali e cose concrete alle teorie.",
            "Apprendo meglio se intervengo direttamente: imparo 'in corsa' mentre eseguo un compito."
        ]
    },
    {
        "id": 7,
        "items": [
            "Per imparare mi focalizzo sul 'qui e ora': rispondo immediatamente agli stimoli del momento.",
            "Per imparare pondero le informazioni che raccolgo: ho necessità di un tempo per elaborare internamente i dati.",
            "Per imparare cerco di anticipare le conseguenze e pianificare azioni. Studio in funzione di obiettivi a lungo termine.",
            "Per imparare cerco soluzioni efficienti. Piuttosto che 'è vero?', la domanda che mi guida è 'funziona?'."
        ]
    },
    {
        "id": 8,
        "items": [
            "Apprendo meglio vivendo l'evento in prima persona. Per me la conoscenza deriva dal contatto diretto.",
            "Apprendo meglio analizzando l'evento “da fuori”. Per me la conoscenza deriva da una visione distaccata.",
            "Apprendo meglio creandomi dei modelli mentali. Per me la conoscenza deriva da una sintesi teorica.",
            "Apprendo meglio verificando le mie ipotesi nella realtà. Per me la conoscenza deriva da una prova pratica."
        ]
    },
    {
        "id": 9,
        "items": [
            "Apprendo con una forte carica emotiva ed energetica: mi impegna a fondo nella situazione.",
            "Apprendo mantenendo le distanze: tendo a proteggere il mio spazio per poter elaborare i dati con calma.",
            "Apprendo usando la ragione pura: cerco di escludere le emozioni per arrivare a conclusioni chiare.",
            "Apprendo facendomi carico delle conseguenze: agisco con impegno, senso del dovere e seguendo una direzione chiara."
        ]
    }
]

# --- Definizioni Stili ---
styles_description = {
    "Convergente": """
    **Stile Dominante: CONVERGENTE**
    *Combinazione di Concettualizzazione Astratta (CA) e Sperimentazione Attiva (SA)*.
    
    La tua grande forza risiede nell'applicazione pratica delle idee. Funzioni al meglio in situazioni dove esiste una singola risposta corretta o una soluzione specifica a un problema (come nei test tecnici). Organizzi la conoscenza attraverso il ragionamento ipotetico-deduttivo per focalizzarti su problemi specifici. Tendi ad essere meno emotivo e preferisci avere a che fare con oggetti e problemi tecnici piuttosto che con dinamiche interpersonali. Questo stile è tipico di molti ingegneri e specialisti tecnici.
    """,
    "Divergente": """
    **Stile Dominante: DIVERGENTE**
    *Combinazione di Esperienza Concreta (EC) e Osservazione Riflessiva (OR/CR)*.
    
    La tua forza risiede nelle capacità immaginative e nell'abilità di osservare le situazioni concrete da diverse prospettive. Sei eccellente nel generare idee (brainstorming). Ti interessi alle persone, tendi ad essere emotivo e ad avere vasti interessi culturali. Questo stile è spesso caratteristico di chi lavora nelle arti, nelle risorse umane o in ambiti umanistici.
    """,
    "Integratore": """
    **Stile Dominante: INTEGRATORE (Assimilatore)**
    *Combinazione di Concettualizzazione Astratta (CA) e Osservazione Riflessiva (OR/CR)*.
    
    La tua forza sta nella creazione di modelli teorici e nel ragionamento induttivo (integrare osservazioni disparate in una spiegazione unica). Sei più interessato ai concetti astratti che alle persone o all'uso pratico immediato delle teorie; per te è fondamentale che una teoria sia logicamente solida e precisa. Questo stile è tipico delle scienze di base, della ricerca e della pianificazione strategica.
    """,
    "Adattatore": """
    **Stile Dominante: ADATTATORE (Accomodatore)**
    *Combinazione di Esperienza Concreta (EC) e Sperimentazione Attiva (SA)*.
    
    La tua forza sta nel "fare", nel portare avanti piani ed esperimenti e nel lasciarti coinvolgere in nuove esperienze. Ti assumi rischi e ti adatti bene alle circostanze immediate. Se la teoria non coincide con i fatti, tendi a scartare la teoria. Sei a tuo agio con le persone, anche se a volte puoi apparire impaziente. Questo stile è tipico di chi lavora nel business, nel marketing, nelle vendite o in ruoli orientati all'azione.
    """
}

# --- Header ---
st.title("Autovalutazione Stile di Apprendimento (Modello di Kolb)")
st.markdown("""
Questo test ti aiuterà a definire la tua modalità di apprendimento. 
Per ogni riga (gruppo di 4 affermazioni), assegna un punteggio da **1** a **4** in base a quanto l'affermazione ti descrive:
* **4** = "Sono proprio io!" (Massima corrispondenza)
* **3** = "Qualche volta faccio così"
* **2** = "Non faccio quasi mai così"
* **1** = "Questo non sono io!" (Minima corrispondenza)

**ATTENZIONE:** In ogni riga, devi usare i numeri 1, 2, 3 e 4 **una sola volta ciascuno**. Non puoi assegnare lo stesso voto a due frasi nella stessa riga.
""")

st.divider()

# --- Form di Input ---
# Utilizziamo un dizionario per salvare le risposte
user_scores = {}

with st.form("kolb_form"):
    valid_form = True
    
    for row_idx, row_data in enumerate(data):
        st.markdown(f"### Gruppo {row_data['id']}")
        
        cols = st.columns(4)
        row_values = []
        
        # Creiamo 4 selectbox per la riga
        for col_idx, text in enumerate(row_data['items']):
            with cols[col_idx]:
                st.info(text)
                val = st.selectbox(
                    f"Voto per frase {col_idx+1} (Gruppo {row_data['id']})", 
                    options=[1, 2, 3, 4], 
                    key=f"R{row_idx}_C{col_idx}",
                    index=col_idx # Default diverso per facilitare il test visivo
                )
                row_values.append(val)
        
        # Validazione unicità riga (Visuale, non bloccante finché non si preme submit)
        if len(set(row_values)) != 4:
            st.warning(f"⚠️ Attenzione nel Gruppo {row_data['id']}: hai usato lo stesso numero più volte. Assicurati di usare 1, 2, 3, 4 una sola volta per riga.")
            valid_form = False
        
        st.divider()
        
        # Salviamo i dati strutturati per il calcolo
        user_scores[row_idx] = row_values

    submitted = st.form_submit_button("Calcola il mio Stile")

# --- Logica di Calcolo e Risultati ---
if submitted:
    if not valid_form:
        st.error("Ci sono degli errori nella compilazione (numeri duplicati nelle righe). Correggi i gruppi evidenziati in giallo e riprova.")
    else:
        # --- Calcolo dei Punteggi secondo le regole del prompt ---
        # Matrice user_scores[riga][colonna] (0-based index)
        
        # Colonna 1 (EC): righe 2,3,4,5,7,8 (Indici: 1,2,3,4,6,7)
        ec_indices = [1, 2, 3, 4, 6, 7]
        score_ec = sum([user_scores[i][0] for i in ec_indices])

        # Colonna 2 (OR): righe 1,3,6,7,8,9 (Indici: 0,2,5,6,7,8)
        or_indices = [0, 2, 5, 6, 7, 8]
        score_or = sum([user_scores[i][1] for i in or_indices])

        # Colonna 3 (CA): righe 2,3,4,5,8,9 (Indici: 1,2,3,4,7,8)
        ac_indices = [1, 2, 3, 4, 7, 8]
        score_ac = sum([user_scores[i][2] for i in ac_indices])

        # Colonna 4 (SA): righe 1,3,6,7,8,9 (Indici: 0,2,5,6,7,8)
        ae_indices = [0, 2, 5, 6, 7, 8]
        score_ae = sum([user_scores[i][3] for i in ae_indices])

        # --- Determinazione dello Stile ---
        # Logica: Confronto asse Y (Concreto vs Astratto) e asse X (Attivo vs Riflessivo)
        # Nota: EC (Concreto), AC (Astratto), AE (Attivo), OR (Riflessivo)
        
        dominant_style = ""
        
        # Determiniamo il quadrante
        is_concrete = score_ec >= score_ac
        is_active = score_ae >= score_or
        
        if is_concrete and is_active:
            dominant_style = "Adattatore"
        elif is_concrete and not is_active:
            dominant_style = "Divergente"
        elif not is_concrete and not is_active:
            dominant_style = "Integratore"
        elif not is_concrete and is_active:
            dominant_style = "Convergente"

        # --- Visualizzazione Risultati ---
        st.header("Il tuo Profilo di Apprendimento")
        
        col_res1, col_res2 = st.columns([1, 1])
        
        with col_res1:
            st.subheader("I Punteggi")
            st.write(f"**Esperienza Concreta (EC):** {score_ec}")
            st.write(f"**Osservazione Riflessiva (OR):** {score_or}")
            st.write(f"**Concettualizzazione Astratta (CA):** {score_ac}")
            st.write(f"**Sperimentazione Attiva (SA):** {score_ae}")
            
            # --- Grafico Radar ---
            categories = ['Esperienza Concreta', 'Osservazione Riflessiva', 
                          'Concettualizzazione Astratta', 'Sperimentazione Attiva']
            
            # Chiudiamo il poligono ripetendo il primo valore
            values = [score_ec, score_or, score_ac, score_ae]
            values += values[:1]
            categories += categories[:1]

            fig = go.Figure()

            # Aggiungiamo il poligono utente
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Il tuo profilo',
                line_color='#FF4B4B'
            ))

            # Configuriamo il layout per mostrare i quadranti
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 24] # Max teorico per colonna è 24 (6 righe * 4 punti)
                    )
                ),
                showlegend=False,
                title="Mappa dello Stile di Apprendimento"
            )
            
            st.plotly_chart(fig, use_container_width=True)

        with col_res2:
            st.success(f"Risultato: {dominant_style}")
            st.markdown(styles_description[dominant_style])
            
            st.info("Nota interpretativa: Il grafico mostra verso quale polo tendi maggiormente. Un poligono bilanciato indica flessibilità nell'apprendimento.")
