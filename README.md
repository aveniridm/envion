# Envion v3.6 — Algorithmic Dynatext Envelope Sequencer

Envion is an **envelope‑first** ecosystem for **Pure Data (Pd)** designed for algorithmic and procedural composition, *musique concrète*, and experimental sound processing.  
Instead of “playing” files, Envion **writes trajectories** on them via numeric envelopes (*Dynatext*), turning even a tiny fragment into **thousands of sonic variations**.

> 🔖 **License** — MIT with Attribution. You may use, modify, and redistribute (including commercially) as long as you clearly attribute **Envion** and **Emiliano Pennisi**.

---

## 📦 Repository & Docs

- **Repo:** [GitHub — Envion v3.6](https://github.com/aveniridm/envion_v3.6)
- **Full Documentation:** https://www.peamarte.it/env/envion_v3.6.html

> There is also a version tailored for **PlugData** (JUCE‑based), which decouples audio and GUI threads and often runs more smoothly than Pd‑vanilla, especially on older machines.

---

## 🚀 Quick Start

### PlugData
1. Download **PlugData** and open the patch:
   ```
   Envion_v3.9_Plugdata.pd
   ```
2. Use the **built‑in presets** (bottom‑right), tweak behavior, and load new samples.

### Pure Data (Pd‑vanilla)
1. Open the main patch:
   ```
   Envion_v3.6.pd
   ```
2. Load a sample (WAV), enable DSP, and explore manual/auto triggering.

---

## 🔧 Dependencies

In **PlugData**, the libraries **~~cyclone~~** and **~~else~~** are already included.  
For full compatibility (e.g., scope utilities), install the following libraries in Pd (via **Deken**):

- ~~cyclone~~ *(included in PlugData)*  
- ~~else~~ *(included in PlugData)*  
- ggee  
- ceammc  
- simplex *(3D scope)*  
- audiolab  

### Install via Deken (Pure Data)
1. Pd → **Help → Find Externals…** (opens *Deken*)  
2. Search and install: `cyclone`, `ggee`, `ceammc`, `else`, `simplex`, `audiolab`  
3. If asked, install to your user externals folder (e.g., `~/Documents/Pd/externals`)  
4. **Restart Pd** so the new objects are available

---

## 🎛️ What is Envion?

**Envion** drives the read index of stereo buffers using textual sequences of **triplets** (`value, time, delay`) sent to `vline~`.  
Each **line of text** is a complete envelope; **switching line** = **switching gesture**.

- **Micro‑Assembly, Texture Generator, Stereo‑ready** (multichannel‑friendly)
- **Algorithmic drum machine** behavior via manual strikes or auto‑randomization
- **Dynatext**: large text archives (up to **1000 lines** each) of pre‑composed gestures

### Key idea
> Envion layers an **algorithmic engine** that keeps envelope and sample tightly coupled, maintaining coherence while allowing complex, generative transformations (hyper‑articulated hits, slow morphs, irregular delays, pseudo‑organic behaviors).

---

## 📚 How to Read a Triple (amp – dur – offset)

In example patches, `list split 3` breaks sequences into **three values**:
- **Amplitude** (e.g., `1` or `0.2`)
- **Duration** (ms)
- **Offset** (ms)

`vline~` interprets the result as a **multi‑stage envelope** where each segment starts from the end of the previous one; the envelope multiplies the oscillator (or controls playback), shaping the sound exactly according to the list.

### Timeline of the Example List
```text
1 50 0       → start at 0, ramp to 1 in 50ms  → end = 50
0.2 200 50   → start at 50, ramp to 0.2 in 200ms → end = 250
0.8 100 250  → start at 250, ramp to 0.8 in 100ms → end = 350
0 20 350     → start at 350, ramp to 0 in 20ms → end = 370
1 10 370     → start at 370, ramp to 1 in 10ms → end = 380
0 50 380     → start at 380, ramp to 0 in 50ms → end = 430
1 10 430     → start at 430, ramp to 1 in 10ms → end = 440
0 50 440     → start at 440, ramp to 0 in 50ms → end = 490
1 10 490     → start at 490, ramp to 1 in 10ms → end = 500
0 50 500     → start at 500, ramp to 0 in 50ms → end = 550
```

### Try it Yourself
Open **`terna-sample.pd`** and modify the list:
- pick a file from `/data`
- paste one of the envelope strings into the message
- listen to the result

---

## 🧠 Dynatext (Envelope Databases)

**Dynatext** are large text files (in `/data`) with up to **1000 lines** each; every line is a complete gestural trajectory (`amplitude, time, offset`). Envion can **randomize** both the file and the line, yielding high variability:

- **Random List** → randomly picks one of the Dynatext files
- **Random Terna** → randomly picks one line within that file

**Stretch** is the key control mapping trajectories onto the time domain:
- **Low values** → fast, percussive, microscopic gestures  
- **High values** → slow, broad, dramatic evolutions

> Together, large archives + multi‑level randomization + stretch form a **generative machine of dynamic articulations**.

---

## 🛠️ Workflow (Quick)

1. **Load a list** from Dynatext Cloud (or a `.txt` from `data/`)
2. **Browse a sample** (WAV) into the stereo buffers
3. **Turn on DSP** and explore

Tips:
- Manual triggers to test sequences
- Adjust **stretch factor**
- Use **ready‑made presets** (bottom area)

### Timebase & `$0`‑factor
The timebase module converts **samples → ms** and exposes `$0-durata` and `$0-factor` (global stretch for segments):
```c
// from samples to ms (44.1 kHz)
expr round((($f1 * 1000.) / 44100) * 100) / 100
```
- `$0-factor` applies to segment times
- Not mandatory when using *terne* as **parameter modulation** (FM index, filters, etc.)

**Original‑speed playback:** `0, <array_size> <durata_ms>` — scans the entire buffer in `durata_ms` at constant speed.

---

## 📂 Project Structure
```
Envion_v3.6.pd           → main patch
audio/                   → test samples and audio files
data/                    → dynatext libraries (terne) & presets
html-guide/              → guides and documentation (HTML/CSS)
```

---

## 🪄 Lists of Terne (examples)

- `default.txt` — neutral baseline  
- `perc.txt` — fast attacks, short decays  
- `vline_perc_1/2`, `vline_ultra_perc_3.txt` — percussive variants from soft to extreme  
- `zadar_style_4triplets.txt` — four‑way triplet structures  
- `complex_drone_plain.txt` — long static drones  
- `complex_percussive_plain.txt` — articulated rhythmic envelopes  
- `emf_interference.txt` — glitchy, fragmented shapes  
- `drone.txt` — extended continuous textures  
- `unstable-metro.txt` — irregular micro‑timing  
- `buchla.txt` — organic West‑Coast‑style curves  
- `sharpy.txt` — sharp transients  
- `relaxed.txt` — slower, softened curves  
- `random_delayed_perc.txt` — hits with random delays  
- `vactrol.txt` — LPG‑like natural A/D  
- `polyrhythm.txt` — multi‑layered offsets  
- `bounded_kickdrum.txt` — punchy, short sustain  
- `terne_1000_fadeout.txt` — progressive fadeouts  

**Formatting example**
```text
1 0.0 0.58 19 0.8 22 29 1 25 41; 0.7 120 0.0 38 80;
```

---

## 🎚️ Playback Engine (core)

- `tabread4~ sampletabL/R` — 4‑point interpolation, driven by `vline~`
- `*~` / `pow~` — amplitude control + shaping
- `snake~` — stereo/multichannel routing
- safety headroom via `clip~`

> `tabread4~` keeps reading until index=0 or out‑of‑buffer. For immediate stop: send `clear/stop` to `vline~`, or force amp to `0`.

---

## 🔀 Quick Play & Algorithmic Drum Machine

**Manual Strike Mode**
- Load any list from **Dynatext Cloud**
- Assign a (short) sample
- Use **KEY‑1** to trigger gestures: each line becomes a distinct hit

**Tips & Tricks**
- Pair **short samples** (kicks/snares/metallics) with **percussive lists** (`perc.txt`, `random_delayed_perc.txt`)
- Try **drone/long lists** on short samples for stutters & stretched hits
- Map envelopes to **parameters** (filters, FM index) instead of playback
- Alternate **manual strike** and **autoplay**
- For drum‑like grooves: Random List + Random Terna, sample ≤ 500 ms

---

## 🧊 Freeze & Stretch (pseudo‑FFT feel)

- With **stretch factor** at **minimum**, the envelope matches the sample’s duration (no unwanted stretching)
- By **massively increasing stretch**, rhythmic articulation dissolves into a **suspended sound mass**
- Add **reverb** to enhance the frozen texture illusion

🎥 Video: *Freeze a sample (Amen Break)* — https://www.youtube-nocookie.com/embed/srLcQWzKQ2Y?rel=0

---

## 🔥 NUKE — Stereo Behavior & Enhanced Aggression

**Nuke** processes L/R with **slight differences** in filtering and clipping:
- **Stereo widening** via non‑identical channels
- **Perceptual instability** (lively, shifting space)
- **Enhanced aggression** (asymmetric distortion artifacts)

> A **stereo expander through destruction**: similar but non‑identical L/R processing yields strong spatial depth.

---

## 🕳️ Echo — Stereo Delay & Feedback (module snapshot)

- **Stereo**: slightly different L/R times widen the field
- **Feedback**: from subtle to regenerating repeats
- **Flutter**: small time variations for a lively, unstable feel
- **Post‑Reverb**: applied only to echo tails
- **Sends**: per‑channel send from the mixer

---

## ✅ Notes & Utilities

- **Normalization** tool (top‑left) for low‑level material
- **Mono → Stereo** (top‑right) mirrors L into R
- For **ultra‑stereo** results, when mirroring mono, toggle **NUKE** on alternate mixer channels

**Tip**  
When loading a very short sample (e.g., a percussive sound), adjust the **stretch factor** manually using the **vertical slider** (not auto‑stretch). Minimum stretch ensures the envelope aligns with the sample duration.

---

## 📹 Video Examples

- Algo LPG Drums — https://www.youtube.com/embed/kByTGFL8rUI  
- Clip‑Shaping Sonic Textures — https://www.youtube.com/watch?v=TuJRD6aVqsc  
- First step on Envion — https://www.youtube.com/watch?v=BiTsPTQfgCY

**YouTube Shorts — Japanese Wood (Akira Wood)**  
I loaded the *Japanese Wood (Akira Wood)* preset inside Envion to soundtrack a scene from *Dreams* (1990) by Akira Kurosawa — Kitsune Wedding sequence. All percussion comes from Envion, with a few strikes of *hyōshigi* directly from the film.  
Video: https://www.youtube.com/embed/NG90a9NgMEc

---

## 🙌 Credits

**Envion** — by **Emiliano Pennisi** (2025)

If the repository is private and you wish to test Envion, send your GitHub username or email for access.

