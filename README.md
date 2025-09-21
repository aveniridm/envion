# Envion

**Envion** è un ecosistema in Pure Data pensato per la composizione algoritmica, la musica concreta e l’elaborazione sperimentale del suono.  
Include strumenti per slicing, inviluppi dinamici, generazione di texture e gestione multi-canale.

---

## 📂 Struttura del progetto

- `Envion_v3.6.pd` → patch principale  
- `astrazioni-non-obbligatorie/` → subpatch e utility opzionali  
- `audio/` → sample di test e file audio (piccoli, caricabili su GitHub)  
- `data/` → dati e preset per slicing/algoritmi  
- `html-guide/` → guide e documentazione (anche in versione HTML/CSS)  
- `legacy version/` → versioni precedenti  
- `other version/` → varianti sperimentali  
- `preset.pd` → esempio di gestione preset

---

---

##  Il concetto di *Terne*

Uno degli elementi centrali di **Envion** è l’uso delle *terne* (triplette di valori numerici).  
Ogni terna definisce il comportamento di un frammento sonoro, attraverso tre parametri principali:

1. **Durata** – tempo relativo o assoluto dell’evento (in ms o fattore di scala).  
2. **Ampiezza** – livello del segnale, che può essere costante o modellato da un inviluppo.  
3. **Offset / Posizione** – punto di lettura o di partenza del frammento all’interno del campione.

Insieme, queste tre coordinate generano micro-articolazioni che Envion traduce in inviluppi e processi di slicing.  
Le *terne* funzionano quindi come una sorta di **partitura algoritmica**, dove la somma di centinaia o migliaia di triplette permette di costruire texture complesse, droni, ritmiche irregolari o veri e propri micro-montaggi.

 Grazie a questo approccio, Envion non lavora solo come un player di campioni, ma come un **motore di composizione dinamica**, capace di trasformare anche un suono di pochi secondi in una trama sonora estesa e in continua evoluzione.

---

---

## Dependencies

Envion requires Pure Data **vanilla** plus the following externals:

- [else] — main external library by Alexandre Porres (musical/synthesis utilities).
- [cyclone] — Max/MSP compatibility objects (`gate~`, `switch~`, `snapshot~`, `wrap~`, `clip~`, etc.).
- [zexy] — extra math and DSP utilities.
- [iemlib] — additional signal and control objects.
- [snake~], [simplex~], [pp.out~], [x/scope3d] — less common externals used in some subpatches.  
  (If missing, install via Deken or replace with equivalents.)

 All externals can be installed via Pd’s **Help → Find externals** (Deken).
