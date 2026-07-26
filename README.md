<img src="https://www.peamarte.it/env/html-guide/img/logo_circle_60x60_readme.png" width="100" height="100" style="vertical-align: middle; margin-bottom: -20px;">

# Envion  
Algorithmic Dynatext Envelope Sequencer for **Pure Data (PlugData & iPadOS)**  
by **Emiliano Pennisi** — 2025


### Foundational Statement

Envion is an artistic-research ecosystem conceived and developed by **Emiliano Pennisi (2024–2025)**.  
It represents the first procedural environment for *network-based sonic excavation* and *algorithmic composition* built entirely in Pure Data and PlugData.  
Envion introduces the notion of **Found Net Sound**, the **gesture as envelope** paradigm, and a modular architecture integrating network and local sound recontextualization.  
Documented across public repositories, websites, and media features (CDM, Reddit, YouTube), Envion constitutes an original framework for open, procedural musique concrète.

---

**Documentation & Tutorials:**  
[https://www.peamarte.it/env/envion_v3.6.html](https://www.peamarte.it/env/envion_v3.6.html)  
Please visit the website for the complete usage guide, module reference, and setup details.

---

## Overview

Envion is an envelope-first ecosystem for algorithmic and procedural composition in Pure Data (Pd).  
It redefines sampling as a gesture-based process: thousands of dynamic envelopes ("Dynatext triplets") continuously sculpt micro-events and temporal shapes.

The Net-Audio submodule fetches random sound atoms from online archives (Internet Archive, Wikimedia Commons, Freesound), transforming contingent data into acousmatic gestures.

Envion is open-source, compatible with PlugData on macOS, Windows, and iPadOS, and released under the MIT License (with Attribution).

---

## Requirements

- PlugData (includes `cyclone` and `else`)
- Mandatory Libraries:  
  - `ggee`  
  - `audiolab`  
- Optional Libraries:  
  - `ceammc`  
  - `simplex` (for 3D visualization)

---

## Quick Setup

Open `Envion_v4.5_Plugdata.pd` in PlugData to play presets, tweak behavior, and load new samples.

---

### Before you start — Envion is not a single `.pd` file

Envion will **not** work if you only download the `Envion_v5.1_Plugdata.pd` file.  
The patch depends on its full folder structure (`/libs`, `/core`, `/utils`, `/netsound`, `/data`, etc.).  
You must download the **entire repository**.

---

### Correct installation (desktop)

1. Download the full repository ZIP  
   https://github.com/aveniridm/envion/archive/refs/heads/main.zip
2. Unzip it — this creates a folder such as `envion-main/`
3. **Do not move** the `.pd` patch out of this folder
4. Open `Envion_v5.1_Plugdata.pd` from inside the same folder

envion-main/
  Envion_v5.1_Plugdata.pd
  [core]  [libs]  [netsound]  [utils]  [data]  [audio]

When the patch is moved outside its directory tree, PlugData cannot resolve abstractions or support files —  
this results in **silent loading**, **missing modules**, or inconsistent behaviour.  
Keeping the folder intact ensures everything loads correctly.

---

### First Run (quick start)

Once installed correctly:

- Turn on **DSP**
- Load the **main master preset** (large bang button on the right)
- Sound is immediate — no configuration required

| Preset Types | Description |
|-------------|-------------|
| Local        | uses audio included in the repo |
| Network      | fetches sound from the web (via netsound) |
| Custom       | you can load your own samples |

Take your time to explore the deeper functions later —  
for now, just **play, listen, and discover**.  
Envion is designed so that sound emerges instantly, while depth unfolds gradually.


## iPadOS/iOS Compatibility

PlugData for iPadOS/iOS includes core libraries.  
Optional libraries (ggee, ceammc, simplex, audiolab) add extra features but are not required for basic functionality.

If dependency warnings appear, they refer to optional libraries.  
The patch remains operational without them, except for features such as 3D scope visualization.

### Net-Audio module on iPadOS/iOS

**Important:**  
The Net-Audio module is **not functional on iPadOS** as of this release.  
Due to current limitations in PlugData for iPadOS/iOS, URL-based loading and fetching are not supported.  
As a result, the Net-Audio module will remain inactive in the iPadOS version until the necessary functionality is implemented upstream.  
A related issue has been opened in the PlugData repository; updates will be provided when support is available.

For detailed instructions and troubleshooting, refer to [IPAD_GUIDE.md](IPAD_GUIDE.md).

---

## Concept

Envion operates by writing trajectories on sound through textual sequences of triplets `(amplitude, duration, offset)` sent to `vline~`.  
Each line of a text file defines a gesture.  
Thousands of these triplets, stored in the `/data` folder, create a reservoir of living envelopes.

---

## Net-Audio Module (desktop only)

Net-Audio extends Envion by automatically fetching sonic material from public archives.  
Python scripts build `.txt` lists of direct URLs, which Envion reads and articulates through its envelope engine.

Module guide: [peamarte.it/env/envion_netaudio.html](https://www.peamarte.it/env/envion_netaudio.html)

---

## Video Playlist

[Envion — YouTube Playlist](https://www.youtube.com/watch?v=JEuB3KBAxeg&list=PLLITukQh1_l61lP6GMfa1Hz4Db7_wrTTT)

---

## License

Envion is released under the MIT License with Attribution.  
You are free to use, modify, and redistribute this project, including for commercial purposes, as long as you credit Envion and Emiliano Pennisi.  
See the [LICENSE](LICENSE) file for details.

---


Envion — © Emiliano Pennisi 2024–2025
First public release: GitHub Repository

## Links

- Website: [peamarte.it/env/envion_v3.6.html](https://www.peamarte.it/env/envion_v3.6.html)
- Portfolio: [http://www.emilianopennisi.it](http://www.emilianopennisi.it)
- YouTube Series: [Envion — Official Playlist](https://www.youtube.com/watch?v=gA-pdHQwibA&list=PLLITukQh1_l61lP6GMfa1Hz4Db7_wrTTT)
- Community: [r/musiconcrete](https://www.reddit.com/r/musiconcrete)
- Contact: [metrostation@gmail.com](mailto:metrostation@gmail.com)

---

Built in Pure Data / PlugData (2024–2025)  
© Emiliano Pennisi

<!--UPDATE_TS_START-->
_Last update: 2026-07-26 18:53 CEST_
<!--UPDATE_TS_END-->
=======
<!--UPDATE_TS_END-->
>>>>>>> Stashed changes
=======
_Last update: 2025-10-15 06:37 CEST_
<!--UPDATE_TS_END-->
>>>>>>> Stashed changes
