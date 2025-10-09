

# Envion
Algorithmic Dynatext Envelope Sequencer in Pure Data (Pd) developed by **Emiliano Pennisi 2025**

**Envion** is an ecosystem in Pure Data designed for algorithmic and procedural composition, musique concrète, and experimental sound processing.
It includes tools for slicing, dynamic envelopes, texture generation, and multi-channel management.

Per years, I explored different systems for handling envelopes dynamically — starting with software like *Composer Desktop Project*, and later with hardware generators such as **Zadar** in the Eurorack world.
I would like to emphasize how fascinating the world of **envelope dynamics** is, and how envelopes can imprint *transformative tonal characteristics* onto sounds. Out of this research, I developed Envion.

![Envion — Composite Overview](html-guide/img/enviaon-cmps.PNG "Envion — Composite Overview")

> ## ⚠️ Notes on this documentation
>
> Envion is in **continuous development**.  
> Some aspects of this documentation may change over time.
>
> If you notice inconsistencies, please open an [issue on GitHub](https://github.com/aveniridm/envion_v3.6/issues)  
> or write an email to [Emiliano Pennisi](mailto:metrostation@gmail.com).


> ## Envion — NET-AUDIO (Web Random Loader)
> **What it does:** streams *random audio atoms* from the web and articulates them through Envion’s Dynatext envelopes.
>
> **Key points**
> - Random sources from **[freesound.org](https://freesound.org/)** (drums) → each run generates **8 direct URLs**.  
> - No local storage: the `netsound/` folder only holds **URL lists** (one per line, each ending with `;`).  
> - Loaded sounds **inherit Envion patch parameters** — dynamics, envelopes, modulation depth, and the last preset.  
> - Example preset: **ÆTCHR** (Autechre-inspired) — dense, percussive, and procedural.
>
>  **Full guide, video & screenshots:**  
> **https://www.peamarte.it/env/envion_netaudio.html**



ℹ️ **Envion quick setup**

With **PlugData**, ~~cyclone~~ and ~~else~~ are already included.  
For the 3D scope you can (optionally) add: `ggee`, `audiolab`, `simplex`.

- ~~cyclone~~ — included in PlugData  
- ~~else~~ — included in PlugData  
- ggee - optional (for additional features)
- ceammc - optional (for additional features)
- simplex - optional (for 3D scope visualization)
- audiolab - optional (for enhanced audio features)

Open: `Envion_v3.9_Plugdata.pd` → play presets (bottom-right), tweak behavior, load new samples.

### 📱 **PlugData on iPadOS/iOS**

The core functionality of Envion works out-of-the-box on PlugData for iPadOS/iOS because **cyclone** and **else** libraries are built-in.

If you see dependency warnings when opening the patch on iPadOS:
- These warnings refer to **optional libraries** (ggee, ceammc, simplex, audiolab)
- **You can safely ignore these warnings** — the patch will work without them
- The optional libraries add extra features like 3D scope visualization, but are not required for core functionality
- Currently, installing external libraries on iPadOS/iOS is not supported through PlugData's interface

**What works on iPadOS without additional libraries:**
✅ All envelope sequencing and dynatext features  
✅ Audio playback and sample manipulation  
✅ All preset functionality  
✅ Recording and real-time processing  
✅ Manual and automatic triggering  

**What requires optional libraries (desktop only):**
⚠️ 3D scope visualization (requires `simplex`)  
⚠️ Some advanced audio processing features (requires `audiolab`, `ceammc`, `ggee`)

📖 **[Read the full iPadOS/iOS guide](IPAD_GUIDE.md)** for detailed instructions and troubleshooting.

---

The patch may look **intimidating** at first, but it is intentionally left **“alive”** (with formulas and functions visible) to encourage **exploration**.

<!-- TIP — place right after the paragraph mentioned -->
<div class="callout tip" id="kb-improvise">
  <h3 style="margin-top:0;">Tip — Keyboard improvisation & safety</h3>
  <p>
    Once you toggle <strong>KEY ON/OFF</strong>, your <strong>computer keyboard</strong> becomes a live controller.
    Know the shortcuts—but then <em>improvise</em>: play the QWERTY like an instrument and react to what Envion generates.
    MIDI mapping is of course possible, yet in Envion’s DIY spirit the motto is:
    <em>open the laptop and play—no cables, no menus, just gesture</em>.
  </p>

  <h4 style="margin:.6em 0 .2em;">Emergency stops</h4>
  <p style="margin-top:0;">
    If you experience <strong>sonic instability</strong> (runaway feedback or unpredictable behaviors):
  </p>
  <ul>
    <li><kbd>6</kbd> — <strong>Graceful stop</strong>: interrupts input and lets the <em>last trajectory complete</em>.</li>
    <li><kbd>7</kbd> — <strong>Hard stop (PANIC)</strong>: forces <code>vline~</code> to <code>0</code>, effectively muting almost any sound immediately.</li>
  </ul>
</div>

## Keyboard Shortcuts

**BACKSPACE** → Start

| Key   | Action             |
|-------|--------------------|
| KEY-1 | Manual Strike      |
| KEY-2 | Original Speed     |
| KEY-3 | Stop Original      |
| KEY-4 | Retrigger          |
| KEY-5 | Random Terna Seq   |

### Emergency block
| Key | Action   |
|-----|----------|
| 6   | Graceful Stop (lets last trajectory complete) |
| 7   | Hard Stop (PANIC) — forces `vline~` to 0 |

### Additional
| Key   | Action             |
|-------|--------------------|
| KEY-5 | Random Terna Seq   |
| KEY-6 | BREAKDOWN          |
| KEY-7 | PANIC              |


I soon realized that the most flexible way to manage **thousands of segments** was to use plain-text databases containing the necessary information. From there, I created the **Dynatext** system.

At the moment, I am working on formatting textual data from **external APIs**. In this way, **Envion** could become a powerful tool for generating *thousands of random articulations* not only generated internally, but also based on external data sources.

For example, by drawing on **stock market data**, **weather information**, or **NASA’s extensive library of APIs** — which are incredibly rich and fascinating. Even *Co-Star*, the app that calculates astrology and planetary positions, could provide inspiration for procedural envelope generation.


## What an Envelope-Driven System Can Do

To grasp, in simple terms, what a system that generates **thousands of envelopes** can achieve, consider this practical example:

In the video below, we start from a **very short single sample** (a few milliseconds — in this case, a percussive hit). Through the generation of *gestural trajectories*, that tiny fragment is multiplied into an infinite variety of sonic events.

This happens because at each trigger the sound receives not only an envelope — which can be quite complex, with multiple stages — but also a **stretch factor** that **remodels** the source material.

In this sense, the term **algorithmic drum machine** is appropriate. That said, time can be further deformed, both through manual stretching and through procedural processes.

> A single simple sample creates an almost infinite succession of events.

###  Example Video

[![Watch the video](https://img.youtube.com/vi/kByTGFL8rUI/0.jpg)](https://www.youtube.com/watch?v=kByTGFL8rUI)

*Video showing how a minimal percussive sample can give rise to a vast multiplicity of triggered events via gestural mapping and envelope/stretch transformations.*  

### How to Read a Triple (amp – dur – offset)

In the example patch, the message box contains a long list of numbers.  
`[list split 3]` breaks each sequence into **three values**:

![Envion terna example patch](https://www.peamarte.it/env/html-guide/img/terna.png)

- **Amplitude** (target value, e.g., 1 or 0.2)  
- **Duration** (in ms)  
- **Offset** (start time in ms)  

These are sent to `vline~`, which builds the temporal trajectory.

#### Timeline of the Example List

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

In practice, `vline~` reads the sequence as a **multi-stage envelope**,  
where each segment begins from the final value of the previous one.  
In the provided patch, the envelope output multiplies the oscillator,  
shaping the sound exactly according to the list.

#### Try it Yourself

Inside the Envion directory you’ll find a patch called **`terna-sample.pd`**.  
Open it and try **changing the content of the list**:

- pick a file from `/data`  
- copy and paste one of the envelope strings into the message box  
- listen to the result  

To be more exhaustive, further down I also explain in greater detail  
the concept of **Triplets** and how they are then handled by the algorithm.

This small exercise will help you better understand how the **triple-based system** works  
and how each gesture is constructed from amplitude, duration, and offset values.

## 📖 Documentation

A complete interactive guide (HTML + SVG) is available here:  
[Envion v3.6.1 — Full Documentation](https://www.peamarte.it/env/envion_v3.6.html)

> **License**  

Envion is released under the MIT License with Attribution.  
You are free to use, modify, and redistribute this project, including for commercial purposes, 
as long as you clearly attribute the original project name **Envion** and the author **Emiliano Pennisi**.  
See the [LICENSE](LICENSE) file for details.

![Envion - Plugdata version](html-guide/img/plug-data-black.png)  
*Envion - Plugdata version*

Inside the repository there is also a version tailored for **PlugData.**
It’s worth noting that this version is significantly more performant: unlike Pd-vanilla, where the audio and GUI share the same thread, PlugData (built on JUCE) separates the audio engine from the GUI.
This reduces overhead, prevents dropouts when interacting with the patch, and makes real-time processing smoother.
The JUCE-based architecture also improves GUI responsiveness, event handling, and CPU scheduling, resulting in noticeably faster and more stable performance, especially on older machines.

> ### What is?
> **Envion** is an *envelope-first* engine for **Pure Data (Pd)**: it drives the read index of stereo buffers through textual sequences of **triplets** *(value, time, delay)* sent to `vline~`.  
> Each line of a text file represents a complete envelope; switching line means switching gesture.  


## Musical Gesture Theory — why this matters to Envion

The seminal text *Gesture–Music* by Claude Cadoz and Marcelo M. Wanderley  
partly inspired the envelope-first design of **Envion**.  
Their view of instrumental gestures as an interplay of action/energy, perception, and meaning  
aligns with Envion’s approach: envelopes, slicing, and mappings behave as **digital gestures**  
written onto audio rather than merely playing files.

- **Ergotic** (action/energy): envelopes and triggers impart force to the material.  
- **Epistemic** (perception): trajectories shape how motion and form are perceived.  
- **Semiotic** (meaning): mappings and presets articulate musical intent.  

In short: Envion **writes trajectories** on sound.  
This envelope-driven, gesture-centric view helps explain why a single fragment  
can yield thousands of distinct, evolving articulations.  

> **Reference** — Cadoz, C. & Wanderley, M. M.,  
> [*Gesture–Music*](https://www.researchgate.net/publication/281419029_Gesture-Music).




[![Watch the video](https://img.youtube.com/vi/h8UiZJa_Q_Q/maxresdefault.jpg)](https://youtu.be/h8UiZJa_Q_Q)

▶ Click the image above to watch the video on YouTube

> The system is designed for **musique concrète/acousmatic music**, **sound design**, and **non-metric writing**.  


## What an Envelope-Driven System Can Do

To grasp, in simple terms, what a system that generates **thousands of envelopes** can achieve, consider this practical example:

In the video below, we start from a **very short single sample** (a few milliseconds — in this case, a percussive hit). Through the generation of *gestural trajectories*, that tiny fragment is multiplied into an infinite variety of sonic events.
It follows that a single sample in **Envion** never sounds the same:  
with each trigger, both time-stretch and temporal shape change,  
turning the sample into **thousands of sonic variations** instead of a static file.

This happens because the sound receives not only an envelope — which can be quite complex, with multiple stages — but also a **stretch factor** that **remodels** the source material, forcing it to become something new every time.

In this sense, the term **algorithmic drum machine** is appropriate. That said, time can be further deformed, both through manual stretching and through procedural processes.

>  
> **Key idea**  
> Instead of “playing” files, Envion **writes trajectories** on them through numeric envelopes (*dynatext*).  
> This enables **hyper-articulated hits**, **slow morphs**, **irregular internal delays**, and **pseudo-organic behaviors**.  
>  
> At its core, Envion adds an **algorithmic layer** that keeps the envelope and the sample tightly coupled.  
> This ensures that temporal gestures and sonic material remain bound together, preserving coherence while still allowing complex, generative transformations.  

> **Dependencies for Pure Data Vanilla**: Cyclone · ggee · ceammc · else · simplex (for 3D scope) | audiolab  
> **Dependencies for PlugData**: ~~Cyclone~~ (included) · ~~else~~ (included) · *ggee* (optional) · *ceammc* (optional) · *simplex* (optional) · *audiolab* (optional)

---

**Install via Deken (Pure Data Desktop)**

1. In Pure Data, go to **Help → Find Externals…** (opens *Deken*).  
2. Search and install each library: `cyclone`, `ggee`, `ceammc`, `else`, `simplex`, `audiolab`.  
3. If prompted for a location, install to your user externals folder (e.g., `~/Documents/Pd/externals`).  
4. Restart Pure Data so the new objects are available.  

**Note for PlugData users:** `cyclone` and `else` are already built-in. The other libraries are optional and provide enhanced features.

---

**Troubleshooting**  
- If you cannot find a library, check that you are connected to the internet and your Pd version is up-to-date.  
- Installed externals may not load until Pd is restarted.  
- On macOS, make sure you installed Pd with write access to the externals folder (sometimes you need to create `~/Documents/Pd/externals` manually).  
- **PlugData iPadOS/iOS users:** If you see dependency warnings about `ggee`, `ceammc`, `simplex`, or `audiolab`, you can safely ignore them. These are optional libraries that add extra features, but all core functionality works without them.  

[First step on Envion (youtube clip)](https://www.youtube.com/watch?v=BiTsPTQfgCY&feature=youtu.be)

[Deep HTML / SVG Guide here: ](https://www.peamarte.it/env/envion_v3.6.html)

---

![Envion Main Patch](html-guide/img/main-patch.png)

# Using Envion

As a **procedural environment**, in most cases it is sufficient to **load a sample**, record the output for several minutes, and then select the most interesting portions of the generated audio.

1. Load a sample into the main buffer.
2. Enable **Random Terna** (checkbox below the Dynatext Cloud).
3. Enable **Random List** (central checkbox).
4. Record the output for several minutes.
5. Select the most significant sections of the recorded audio.

This approach highlights Envion’s nature: it is not about “playing” directly, but about **generating emergent sonic material** from which fragments can be extracted for composition.

## Japanese Wood — Envion test (YouTube Shorts)

[![Japanese Wood — Envion test](https://img.youtube.com/vi/NG90a9NgMEc/hqdefault.jpg)](https://www.youtube.com/shorts/NG90a9NgMEc)

I loaded the *Japanese Wood (Akira Wood)* preset inside **Envion** to soundtrack a scene from *Dreams* (1990) by Akira Kurosawa — the Kitsune Wedding sequence, where the child wanders through the forest.

All the percussion comes from Envion, with a few strikes of *hyōshigi* (Japanese ritual wooden clappers) taken directly from the film.  

<details>
<summary>📋video description (YouTube)</summary>

**𝐉𝐚𝐩𝐚𝐧𝐞𝐬𝐞 𝐖𝐨𝐨𝐝 (𝐀𝐤𝐢𝐫𝐚 𝐖𝐨𝐨𝐝) — 𝐄𝐧𝐯𝐢𝐨𝐧 𝐭𝐞𝐬𝐭**

I loaded the *Japanese Wood (Akira Wood)* preset inside Envion to soundtrack a scene from *Dreams* (1990) by Akira Kurosawa — the Kitsune Wedding sequence, where the child wanders through the forest.
All the percussion comes from Envion, with a few strikes of *hyōshigi* (Japanese ritual wooden clappers) taken directly from the film.

**Hashtag**  
#puredata, #algorithmmusic, #algorithmiccomposition, #generativemusic, #musiqueconcrete, #envion, #electroacoustic, #sounddesign, #experimentalcomposition, #audiovisualart, #akirakurosawa, #dreams

</details>

# First Steps with included audio materials

To start experimenting, try loading the file:

`/audio/env_0001.wav`

This reel was created specifically for Envion using my **modular synthesizers** (Orthogonal Devices **ER-301**, **Morphagene**, and several **Low Pass Gates**).  
It was then **reamped** — played back through speakers and re-recorded in the room — to capture the **original ambient nuances** of the space.  

The result is a material that embodies a **contrast**:  
- **Surreal gestures** generated by modular synthesis.  
- Immersed within a **real acoustic environment** that imprints its own depth and imperfections.  

This interplay between the **synthetic and the real**, between **algorithmic articulation** and **spatial resonance**, is at the core of Envion’s aesthetic exploration.


### 💡 Stretch Automation — Envion v4.0

![Envion Stretch Automation (v4.0)](https://www.peamarte.it/env/html-guide/img/envion-stretch.png)  
*Stretch automation module (dual-matrix echo delay + LFO)*

With the new release of **Envion v4.0** several important updates have been introduced.  
In addition to the **dual-matrix echo delay**, there is now a dedicated **LFO for stretch automation**, allowing you to modulate the stretch factor from **1%** up to **40%**.  

Keep in mind: the higher the **stretch factor**, the more both the sound and its envelope will expand proportionally.  
To avoid unwanted artifacts, a **scaling limit at 40%** has been implemented — this prevents entering ranges where you’re more likely to hear **low-frequency clicks** instead of musical articulations.  

The **LFO** can be enabled or disabled via a dedicated **spigot**, and of course you’re free to tweak both the **LFO speed** and the **stretch percentage** to shape the behavior in real time.  

When you load a **preset**, you can always return to the **original stretch** by simply **re-triggering the preset**.  
If you’re experimenting with your own material and you find a moment that sounds inspiring, make sure to note the **stretch value** at that point.  

For convenience, next to the **LFO** you’ll find a **float reminder**: whenever you load or change a preset, this number will display the current stretch value, so you can keep track at a glance.  

**Very important note:** if you are using short percussive samples, start with stretch factors between **1%** and **7–8%**, and from there decide whether to lengthen or shorten. If you start from higher stretch values, you will only get a sound lasting a few milliseconds that is extremely elongated or even silence. This can of course be an intentional effect, but not always will the spectral characteristics of a short sound remain convincing under extreme time-stretching.


> 💡 **Tip**  
> When loading a very short sample (such as a percussive sound), adjust the *stretch factor* manually (use the **vertical slider**, not the horizontal *auto-stretch*).  
> Setting it to the minimum ensures that the envelope perfectly matches the duration of the sound, preventing unwanted stretching.

# Freeze and Stretch

[![Watch the video](https://img.youtube.com/vi/srLcQWzKQ2Y/maxresdefault.jpg)](https://youtu.be/srLcQWzKQ2Y)

▶ Click the image above to watch the video on YouTube  

---

💡 **Freeze a sample in ENVION (pseudo-FFT feel)**  

In this video I show how to “freeze” a sample in **ENVION**.  
I used an **Amen Break** as an example: by manually adjusting a few parameters, the final result strongly resembles an FFT transformation, even though the process itself is not technically spectral.

**Here’s the interesting part:** with the *vertical stretch factor slider* set to the minimum, the envelope is forced to perfectly match the duration of the sound, avoiding unwanted stretching;

Adding some reverb enhances the impression of a “frozen” texture.  
The outcome is a kind of **sonic illusion**: there’s no actual FFT analysis happening, but the resulting aesthetic easily evokes a spectral transformation. It’s basically a *“wannabe FFT”*.

---

🔗 [More about ENVION](https://www.peamarte.it/env/envion_v3.6.html)


NOTE: When loading material with **high headroom** (low volume), you can use the **array normalization** utility located in the top-left corner.  
If instead you load **mono audio material**, there is also a **Mono → Stereo** function in the top-right corner.  
This function creates a small loop and copies the data from the **left array** into the **right array**.

> Ultra-stereo material is recommended for this kind of application.  
> When loading and mirroring mono material, activate **Nuke** on alternate channels of the matrix mixer to emphasize differences between left and right arrays, **widening the stereo field**.


# Procedural Randomization Automation 

By enabling both checkboxes, Envion activates a **procedural randomization** process that automatically draws from **19,000 pre-defined triplets** and applies the X factor to each segment of the envelope.

* **Random Terna**: continuously loads text files from the `/data` folder (each file contains about 1,000 envelopes/triplets).
* **Random List**: randomly selects one of the 1,000 available lists.

This mechanism allows Envion to combine automatic loading and random selection, producing an ever-changing and potentially infinite stream of events.


Even though many operations seem **repeatable** (such as manually selecting a *terna* index from the list or triggering events by hand), the real nuances mainly emerge during the **automatic phase**.

At other times, depending on the **source material**, envelopes may generate **non-zero-cross points** or **glitches**. Yet this is part of the charm: when the program runs in **random mode** — unexpected sonic events and “happy accidents” are favored.

![Procedural Auto Screen](html-guide/img/screen-procedural-auto.png)

## Stereo Behavior and Enhanced aggression

The **Nuke** module processes the **left and right channels with slight differences** in the filter and clipping stages.  
These micro-variations introduce **phase shifts** and **asymmetries** between L and R, resulting in:

- **Stereo widening**: the left and right outputs are no longer exact copies, creating a broader spatial image.  
- **Perceptual instability**: small discrepancies between L+R cause the sound to feel more alive and shifting in space.  
- **Enhanced aggression**: distortion artifacts differ across channels, producing a **wider, noisier stereo field**.

![Nuke Distortion](html-guide/img/nuke-distorsion.png)  
*Distortion/overload utility snapshot*

This design choice makes Nuke not only a distortion stage but also a **stereo expander through destruction**.  
The contrast between **similar but non-identical processing** of L and R is what gives the module its strong sense of spatial depth.

## Echo — Stereo Delay & Feedback (else~ lib)

![Envion — Echo module detail](https://www.peamarte.it/env/html-guide/img/echo-det.png)  
*Echo section (L/R sends, feedback, flutter & post-reverb).*

### How the Echo works
- **Stereo**: L/R channels with slightly different times create a wider field.  
- **Feedback**: controls the number of repeats, from subtle to regenerating.  
- **Flutter**: small random variations of delay time, making it more “alive” and unstable.  
- **Post-Reverb**: reverb applied only to the echo tails, adding depth.  
- **Sends**: send amount to Echo-L / Echo-R from the mixer to decide how much signal enters.  

### The two synthesized sounds (demo on the right)
1. **Filtered burst**: a short envelope (`line~`) multiplies `noise~` inside a `bp~` (band-pass).  
   Result: sharp, bright hits.  
2. **Grainy tone**: `noise~` through `bp~` with variable frequency (MIDI scale → `mtof`), fast envelope.  
   Result: more “tonal” accents.  

Together, the two sounds fill the stereo space: the Echo’s micro-shifts create width and motion.

## 📂 Project structure

- `Envion_v3.6.1.pd` → main patch  
- `audio/` → test samples and audio files 
- `data/` → data terna and presets for slicing/algorithms  
- `html-guide/` → guides and documentation (also in HTML/CSS format)  

---

## The concept of *Terne*

One of the central elements of **Envion** is the use of *terne* (triplets of numerical values).  
Each terna defines the behavior of a sound fragment through three main parameters:

1. **Duration** – relative or absolute time of the event (in ms or scaling factor).  
2. **Amplitude** – the signal level, which can be constant or shaped by an envelope.  
3. **Offset / Position** – the reading point or starting position of the fragment within the sample.

![Terna Dynatext](html-guide/img/terna-dynatext.png)

## What are Dynatext?

Dynatext are the true databases of **Envion**: they are not “small” files, but **large archives** containing up to **1000 lines each**.  
Every line corresponds to a complete trajectory, described through a **numerical triplet** (*amplitude, time, offset*), which is interpreted by the engine to drive envelopes.  

These files, stored in the `/data` folder, form a vast repertoire of complex gestures ready to be activated, combined, and transformed.  
By exploring the text files, you can easily understand how they are structured and, if you wish, create your own — although the existing library already covers a wide range of sonic behaviors. 

---

## Why I use `vline~` instead of `line~`

- **`line~`** only accepts a target and a time → simple, linear ramps.  
- **`vline~`** accepts an entire sequence of **concatenated triplets** (*value, duration, delay*), enabling complex articulations such as micro-curves, pauses, multiple attacks, and temporal bounces.  

Instead of mere linear ramps, Envion works with fully-fledged **dynamic phrases**, richer and more expressive.  

---

## Random List and Random Terna

The system takes on an even more **non-deterministic** behavior when the two randomization checkboxes are enabled:

- **Random List** → randomly selects one of the 17 Dynatext files in `/data`.  
- **Random Terna** → within the chosen file, randomly picks one of the 1000 lines.  

This happens **simultaneously**: Envion randomly chooses both the file and the line inside it, yielding a very high degree of chance and variability. Each activation can produce a completely different gesture.

---

## The role of *Stretch*

The key control is the **Stretch** parameter, which adapts the trajectories to the **time domain** of the audio material (a term familiar to Max/MSP users).  

By adjusting Stretch, Dynatext trajectories are compressed or expanded in time:  

- **Low values** → fast, percussive, almost microscopic gestures.  
- **High values** → slow, broad, dramatic evolutions.  

---

## In summary

- **Large archives** (1000 lines × 17 files)  
- **Multi-level randomization** (file + line)  
- **Fine time-domain control** via Stretch  

Together, these elements make Dynatext not just predefined envelopes, but a true **generative machine of dynamic articulations**, capable of endlessly surprising outcomes.  

### Examples of terne
<pre>
0.452  80  0     ; → 452 ms duration, amplitude 80, offset at start of sample
0.210  45  600   ; → 210 ms duration, amplitude 45, offset 600 ms into the sample
0.879  100 1280  ; → 879 ms duration, full amplitude, offset 1280 ms
</pre>

# Semantic Class – List Validation and Categorization

The patch `duration_flag_800.pd` implements a basic **semantic check** for incoming lists (vline-style). It ensures structural validity and assigns each list to a category before it is passed on.

![Semantic Class](html-guide/img/semantic-class.png)

# Step-by-step logic

1. **Input (**`inlet`**)** A list in `vline~` format enters the patch (usually a triplet: *duration – amplitude – offset*).
2. **Length check (**`list length`**)**
   * The list must contain **at least 3 elements**.
   * If it has fewer than 3 → it is flagged as `list invalid`.
3. **Splitting and unpacking**
   * The list is split and the first three values are extracted (`unpack f f f`).
   * The **first element** is interpreted as *duration*.
4. **Duration test (**`moses 500`**)**
   * If duration **< 500 ms**, the list is classified as `list percussive`.
   * If duration **≥ 500 ms**, it is classified as `list hybrid`.
5. **Routing**
   * Invalid lists are discarded.
   * Valid lists are semantically tagged as *percussive* or *hybrid* and then sent to the `outlet`.

# In practice

This patch acts as a **semantic filter**:

* It first checks whether a list is **structurally valid** (minimum 3 items).
* Then it applies a **musical classification** based on duration: short events are *percussive*, longer ones are *hybrid*.

This guarantees that Envion only processes clean, meaningful lists and can route them according to their temporal behavior.

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
`0, <array_size> <durata_ms>` → scans the entire buffer in **durata_ms** at constant speed.

**WORKFLOW**

1. **Load a sample** → `openpanel ~ soundfiler` into **sampletabL/R**. If mono, use *Mono→Stereo* (array copy L→R).
2. **Load an envelope library** → `text define/get`. Each line = one *terna*. Select or randomize.
3. **Play** → via autoplay or manual keys: **KEY1–4** (strike, original-speed, stop, retrigger).
4. **Record** → from block **AUDIO RECORDER**.

**USEFUL PRESETS (IDEAS)**

# Lists of Terne (1000 envelopes each - total 19k list)

* **default.txt** – basic, neutral list, useful as a starting point.
* **perc.txt** – percussive envelopes with fast attacks and short decays.
* **vline_perc_1.txt / vline_perc_2.txt / vline_ultra_perc_3.txt** – percussive variants generated via `vline~`, from softer (1) to more extreme/fast (3).
* **zadar_style_4triplets.txt** – complex envelopes inspired by the *Zadar* generator, with four-way triplet structures.
* **complex_drone_plain.txt** – long, static envelopes designed for drones.
* **complex_percussive_plain.txt** – articulated, rhythmical envelopes with irregular variations.
* **emf_interference.txt** – patterns inspired by electromagnetic interference, with glitchy and fragmented shapes.
* **drone.txt** – very extended, continuous envelopes for static layered textures.
* **unstable-metro.txt** – “unstable metronome” sequences, irregular timing with micro-variations.
* **buchla.txt** – organic, *West Coast*-style envelopes, fluid and unpredictable curves.
* **sharpy.txt** – sharp envelopes with strong transients.
* **relaxed.txt** – smooth envelopes with slower times and softened curves.
* **random_delayed_perc.txt** – percussive hits with random delays, creating temporal irregularities.
* **vactrol.txt** – envelopes emulating a *vactrol low pass gate*, with natural attack/decay response.
* **polyrhythm.txt** – multi-layered, offset patterns generating polyrhythmic articulations.
* **bounded_kickdrum.txt** – envelopes constrained to kick-drum ranges, punchy with short sustain.
* **terne_1000_fadeout.txt** – 1000 terne with progressive fadeout, ideal for dissolving structures.

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

* `tabread4~ sampletabL/R` → interpolated 4-point reading, indexed by **vline~**
* `*~ / pow~` → amp control (envelope) + optional shaping
* `snake~` → stereo/multichannel routing
* `safety` → `clip~` adds headroom to avoid clipping

![Dynatext Cloud Sequencer](html-guide/img/dynatext-cloud-sequencer.png)

**Note:** `tabread4~` never stops. It runs until index=0 or out of buffer.  
For immediate stop: send **clear/stop** to `vline~`, or drop amp to 0.

**OUTPUT & RECORDER**

* Main out → **pd out~** (replace with `dac~`)
* **Normalization** (utility UI) before printing
* **Recorder**: internal block with **rec/stop** buttons

# Tricks & Best Practices

* **Library hygiene**: one envelope per line; always close with `;`. Avoid zero times anywhere.  
* **Headroom**: add `clip~` after the amplitude multiplier if you use `pow~` or boosting.  
* **Stagger stereo**: send the same envelope to L/R but offset *delays* by a few ms for micro-spatial instability.  
* **Param-mod**: use terne as *control-rate* (via `vline` + `snapshot~` or directly `vline~ → *~`) for resonance/FM index. `$0-factor` is optional.  
* **Original-speed**: build messages “0, size duration” for linear scans; useful as timbral reference.  
* **Debug**: print the raw line, then the list of segments; check that the sum of *time+delay* does not exceed sync expectations.  

---

# Quick Play & Algorithmic Drum Machine

Envion can also be approached in a very **hands-on** way, without diving into all the procedural automation.

> 💡 **Tip**  
> When loading a very short sample (such as a percussive sound), adjust the *stretch factor* manually (use the **vertical slider**, not the horizontal *auto-stretch*).  
> Setting it to the minimum ensures that the envelope perfectly matches the duration of the sound, preventing unwanted stretching.

![Envion Manual Strike](html-guide/img/envio-manual-strike.png)

## Manual Strike Mode
- Load any list from the **Dynatext Cloud**.
- Assign a sample (short percussive ones work best).
- Use **KEY-1 (Manual Strike)** to trigger individual gestures.  
Each line of the list becomes a distinct hit: quick to explore, immediate to hear.

This simple workflow turns Envion into an **algorithmic drum machine**: by browsing different lists and striking manually, you can generate unique **percussive articulations** and irregular rhythms.

[![Watch the video !  Algorithmic Drum Machine](https://img.youtube.com/vi/AsYjCjTsesY/maxresdefault.jpg)](https://youtu.be/AsYjCjTsesY)

▶ Click the image above to watch the video: Algorithmic Drum Machine

## Tips & Tricks
* Combine **short samples** (kicks, snares, metallic hits) with **percussive lists** (`perc.txt`, `random_delayed_perc.txt`) for rhythmic patterns.
* Try **drone or long lists** on short samples: unexpected stutters and stretched hits emerge.
* Map envelopes to **parameter modulation** (filters, FM index) instead of playback for complex timbres.
* Alternate between **manual strike** and **autoplay** to balance **control** and **emergence**.
* For **drum-like grooves**, use Random List + Random Terna but limit the sample length to ≤ 500 ms.

This way, Envion can be both a **tool for deep algorithmic exploration** and a **playful instrument** for instant, raw experimentation.

---

# FAQ

## Is a line with just one terna “valid”?  
Yes. **One line = one envelope**. With a single terna you get a one-step envelope. Multiple terne on the same line ⇒ multi-segment.  

## I want to use 12 terne in one line. Do I need to change `list split 3`?  
No. `list split 3` is correct: it iterates groups of three values. Instead, extend the receiving side (e.g. `unpack` to 36 floats) or implement a dynamic parser with `[until]` that sends each terna as a group.

## Sometimes no sound comes out with certain lists of terne. Why?  
* Zero times (or very long *delays*) ⇒ apparent silence.  
* *target* = 0 in all segments ⇒ zero amplitude.  
* Formatting errors (missing `;`, commas instead of dots, broken lines).  
* `$0-factor` too small/large ⇒ “micro” or “glacial” envelopes.  
* Out-of-buffer index (wrong messages to `vline~` for array scanning).  

**Procedure:** print the line → check triplets → verify sum of *time+delay* → try without `$0-factor` → try “original-speed”.  

## How do I immediately stop playback?  
Send `stop` or `clear` to `vline~` and attenuate with `*~ 0`.  
*tabread4~* follows the index: if the index doesn’t move and amp = 0, you hear nothing.  

## What does the “4” mean in `tabread4~`?  
It’s **4-point interpolation** (cubic). Improves quality when the index moves at non-integer speeds or oversampling.  

## Difference between `line`, `line~` and `vline~`?  
* `line`: control-rate ramp.  
* `line~`: audio-rate ramp, but only one segment per message.  
* `vline~`: audio-rate with a **sequence** of segments, each with its own *delay*.  

## Can I use terne to modulate filters/FM instead of audio?  
Yes. In that case map *targets* to the parameter’s range. `$0-factor` is only needed if you want to scale times; otherwise ignore it.  

## What input file “quality” is needed?  
44.1/48 kHz is more than enough; avoid peaks at 0 dBFS. Leave 3–6 dB of headroom for shaping.  

## How do I manage huge libraries (≈10k envelopes)?  
After preparing the text files, use the browse txt file option to load them. Then navigate with a numeric index or trigger a random selection button. Keep files thematic for coherent families. Use smaller files for quick testing.

---

---
<!--UPDATE_TS_START-->
_Last update: 2025-10-09 13:08 CEST_
<!--UPDATE_TS_END-->
