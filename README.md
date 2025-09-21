# Envion

**Envion** is an ecosystem in Pure Data designed for algorithmic and procedural sound design composition, musique concrète, and experimental sound processing.  
It includes tools for slicing, dynamic envelopes, texture generation, and multi-channel management.

> ### What is?
> **Envion** is an *envelope-first* engine for **Pure Data (Pd)**: it drives the read index of stereo buffers through textual sequences of **triplets** *(value, time, delay)* sent to `vline~`.  
> Each line of a text file represents a complete envelope; switching line means switching gesture.  
> The system is designed for **musique concrète/acousmatic music**, **sound design**, and **non-metric writing**.  
>  
> **Key idea**  
> Instead of “playing” files, it **writes trajectories** on them through numeric envelopes (*dynatext*).  
> This enables **hyper-articulated hits**, **slow morphs**, **irregular internal delays**, and **pseudo-organic behaviors**.  


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

### Examples of terne
<pre>
0.452  80  0     ; → 452 ms duration, amplitude 80, offset at start of sample
0.210  45  600   ; → 210 ms duration, amplitude 45, offset 600 ms into the sample
0.879  100 1280  ; → 879 ms duration, full amplitude, offset 1280 ms
</pre>


## Quick Start

1. **Load a list** from **Dynatext Cloud** (or select a local `.txt` in `data/`).  
2. **Browse a sample** (WAV) and assign it as the playback buffer.  
3. **Turn on DSP** and explore.

- Use the **manual triggers** and sliders to test sequences.  
- Adjust the **stretch factor** to compress/expand time.  
- Try the **ready-made presets** (bottom area).  


v.3.6 last update domenica 21 settembre / 2229
