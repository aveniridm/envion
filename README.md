# Envion

**Envion** is an ecosystem in Pure Data designed for algorithmic composition, musique concrète, and experimental sound processing.  
It includes tools for slicing, dynamic envelopes, texture generation, and multi-channel management.

---

## 📂 Project structure

- `Envion_v3.6.pd` → main patch  
- `astrazioni-non-obbligatorie/` → optional subpatches and utilities  
- `audio/` → test samples and audio files (small, uploadable to GitHub)  
- `data/` → data and presets for slicing/algorithms  
- `html-guide/` → guides and documentation (also in HTML/CSS format)  
- `legacy version/` → previous versions  
- `other version/` → experimental variants  
- `preset.pd` → example of preset management

---

## The concept of *Terne*

One of the central elements of **Envion** is the use of *terne* (triplets of numerical values).  
Each terna defines the behavior of a sound fragment through three main parameters:

1. **Duration** – relative or absolute time of the event (in ms or scaling factor).  
2. **Amplitude** – the signal level, which can be constant or shaped by an envelope.  
3. **Offset / Position** – the reading point or starting position of the fragment within the sample.

Together, these three coordinates generate micro-articulations that Envion translates into envelopes and slicing processes.  
The *terne* thus work as a kind of **algorithmic score**, where the sum of hundreds or thousands of triplets allows the creation of complex text
