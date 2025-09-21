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

## Dependencies

Envion requires Pure Data **vanilla** plus the following externals:

- [else] — main external library by Alexandre Porres (musical/synthesis utilities).
- [cyclone] — Max/MSP compatibility objects (`gate~`, `switch~`, `snapshot~`, `wrap~`, `clip~`, etc.).
- [zexy] — extra math and DSP utilities.
- [iemlib] — additional signal and control objects.
- [snake~], [simplex~], [pp.out~], [x/scope3d] — less common externals used in some subpatches.  
  (If missing, install via Deken or replace with equivalents.)

👉 All externals can be installed via Pd’s **Help → Find externals** (Deken).
