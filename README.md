# Envion

**Envion** is an ecosystem in Pure Data designed for algorithmic and procedural composition, musique concrète, and experimental sound processing.
It includes tools for slicing, dynamic envelopes, texture generation, and multi-channel management.

> ### What is?
> **Envion** is an *envelope-first* engine for **Pure Data (Pd)**: it drives the read index of stereo buffers through textual sequences of **triplets** *(value, time, delay)* sent to `vline~`.  
> Each line of a text file represents a complete envelope; switching line means switching gesture.  
> The system is designed for **musique concrète/acousmatic music**, **sound design**, and **non-metric writing**.  
>  
> **Key idea**  
> Instead of “playing” files, Envion **writes trajectories** on them through numeric envelopes (*dynatext*).  
> This enables **hyper-articulated hits**, **slow morphs**, **irregular internal delays**, and **pseudo-organic behaviors**.  
>  
> At its core, Envion adds an **algorithmic layer** that keeps the envelope and the sample tightly coupled.  
> This ensures that temporal gestures and sonic material remain bound together, preserving coherence while still allowing complex, generative transformations.  



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

**Timebase & $0-factor**  
The timebase module retrieves the buffer duration (samples → milliseconds), exposes it as **$0-durata**, and calculates **$0-factor** for the global stretch of envelopes.

**TYPICAL CONVERSIONS**

    // from samples to milliseconds (44.1 kHz)
    expr round((($f1 * 1000.) / 44100) * 100) / 100
    

* **$0-factor** applies to times of each segment.
* Not mandatory when using *terne* as parameter modulations (e.g., FM resonance, filter index, temporal stretching).

**Original-speed playback:**  
`0, <array_size> <durata_ms>` → scans the entire buffer in **durata\_ms** at constant speed.

**WORKFLOW**

1. **Load a sample** → `openpanel ~ soundfiler` into **sampletabL/R**. If mono, use *Mono→Stereo* (array copy L→R).
2. **Load an envelope library** → `text define/get`. Each line = one *terna*. Select or randomize.
3. **Play** → via autoplay or manual keys: **KEY1–4** (strike, original-speed, stop, retrigger).
4. **Record** → from block **AUDIO RECORDER**.

**USEFUL PRESETS (IDEAS)**

* **Percussive:** fast attack, natural decay
* **Hybrid:** step + soft transition
* **Slow morph:** long, very slow envelopes
* **Vector/LPG:** “breathing” LPG-like response

**LIBRARY FORMATTING**

    1 0.0 0.58 19 0.8 22 29 1 25 41;
    0.7 120 0.0 38 80;
    

* Line 1 = **4-segment envelope**
* Line 2 = **2-segment envelope** Avoid all-zero lines (silent)

**AUTOPLAY & MANUAL PLAYER**

* **Autoplay**: a metro drives `text get`; last strike duration can trigger next step (*END* listener).
* **Manual**:
   * **KEY1** = strike
   * **KEY2** = original-speed
   * **KEY3** = stop
   * **KEY4** = retrigger

*Smart concatenation*: internal delays in *terne* allow irregular patterns without reprogramming the metro.

**PLAYBACK ENGINE**

* `tabread4~ sampletabL/R` → interpolated 4-point reading, indexed by **vline\~**
* `*~ / pow~` → amp control (envelope) + optional shaping
* `snake~` → stereo/multichannel routing
* `safety` → `clip~` adds headroom to avoid clipping

**Note:** `tabread4~` never stops. It runs until index=0 or out of buffer.  
For immediate stop: send **clear/stop** to `vline~`, or drop amp to 0.

**OUTPUT & RECORDER**

* Main out → **pd out\~** (replace with `dac~`)
* **Normalization** (utility UI) before printing
* **Recorder**: internal block with **rec/stop** buttons


v.3.6 last update domenica 21 settembre / 2229
