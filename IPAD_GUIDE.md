# Envion on PlugData for iPadOS/iOS

[If you are on Desktop select this URL](https://www.peamarte.it/env/envion_v3.6.html)

## 📱 Quick Start Guide

**Good news!** Envion works perfectly on PlugData for iPadOS and iOS devices. The core functionality is fully operational without requiring any additional library installations.

## Understanding the Dependency Warnings

When you open Envion on PlugData for iPadOS, you may see warning messages about missing dependencies. **Don't worry — this is completely normal and expected!**
## iPadOS Sandbox Notes

On iPadOS, PlugData runs inside its own **sandbox**.  
This means it cannot access arbitrary folders on your device — it can only read and write inside its own **Documents directory**.  

### Why this matters
If the `audio/` or `data/` folders are placed outside of the sandbox, PlugData will show errors such as:
[soundfiler] read ... Operation not permitted
can't open file ...

### How to fix it
- Copy the **entire Envion repository** (including `audio/` and `data/`) into the PlugData sandbox.  
- You can do this via:
  - **Finder/iTunes File Sharing** (PlugData → Documents)  
  - **iCloud Drive** (place the folder in `PlugData/`)  
  - **Files app** (any location accessible by PlugData)  
- Always use **relative paths** (e.g. `./audio/sample.wav`) instead of absolute system paths.  
  This ensures PlugData looks for files in the same folder as the patch, fully compatible with iPadOS.

---


### What the warnings mean:

The warnings refer to these external libraries:
- `ggee`
- `ceammc`
- `simplex`
- `audiolab`

These libraries are:
1. **Optional** — they add extra features but are not required
2. **Desktop-only** — they cannot be installed on iPadOS/iOS through PlugData
3. **Safe to ignore** — you can dismiss these warnings and use Envion normally

## What Works on iPadOS (Without Additional Libraries)

✅ **Full envelope sequencing** — All dynatext functionality  
✅ **Audio playback** — Complete sample manipulation and playback  
✅ **All presets** — Load and use all included presets  
✅ **Recording** — Real-time recording of your output  
✅ **Manual triggers** — KEY-1 through KEY-5 controls  
✅ **Automatic mode** — Random list and random terna selection  
✅ **Stretch controls** — Time-stretching and envelope scaling  
✅ **Matrix mixer** — All routing and mixing features  
✅ **Effects** — Echo, reverb, distortion (Nuke module)  

## What Requires Optional Libraries (Desktop Only)

⚠️ **3D scope visualization** — Requires `simplex` library  
⚠️ **Advanced audio features** — Some enhanced features require `audiolab`  
⚠️ **Extended utilities** — Certain additional features require `ceammc` and `ggee`

**Important:** The absence of these libraries does not affect the core envelope sequencing, sample playback, or preset functionality of Envion.

## Built-in Libraries

PlugData includes these libraries by default (on all platforms including iPadOS):

✓ **cyclone** — Used for gate~ objects and routing  
✓ **else** — Used for LFO, reverb, note labels, and various utilities  

These built-in libraries provide all the essential functionality for Envion to work properly.

## How to Use Envion on iPadOS

1. **Download** the Envion repository and transfer the patch files to your iPad
2. **Open** `___ Envion_v3.9_Plugdata_WIN-Ipad.pd` in PlugData for iPadOS
3. **Dismiss** any dependency warning dialogs that appear
4. **Load a sample** using the "BROWSE audio" button
5. **Turn on DSP** (if not already on)
6. **Play presets** from the bottom-right preset section, or
7. **Use manual triggers** with KEY-1 to KEY-5

## Transferring Files to iPadOS

You can transfer Envion files to your iPad using:
- **iCloud Drive** — Place files in your PlugData folder
- **Airdrop** — Send files directly from a Mac
- **Files app** — Use any cloud storage service (Dropbox, Google Drive, etc.)
- **iTunes File Sharing** — Transfer via USB connection

Once transferred, open the `.pd` files directly in PlugData.

## Performance Tips for iPadOS
- **Start with preset** — The presets work fine — let me know if anything’s wrong
- **Monitor CPU usage** — Some iPads may struggle with very complex patches
- **Close other apps** — Free up system resources for better performance
- **Adjust buffer size** — In PlugData settings, if audio glitches occur

## Troubleshooting

### Problem: Dependency warnings appear on startup
**Solution:** This is normal! Simply dismiss the warnings and continue using the patch.

### Problem: No sound is produced
**Solution:** 
- Check that DSP is turned ON (toggle in PlugData)
- Verify that a sample is loaded into the buffer
- Ensure your iPad volume is up and PlugData has audio permissions

### Problem: Patch won't load
**Solution:**
- Make sure you're using the PlugData version: `___ Envion_v4.0_Plugdata.pd`
- Verify you have the latest version of PlugData for iOS
- Check that the file wasn't corrupted during transfer

### Problem: Missing preset files
**Solution:**
- Ensure you transferred the entire Envion folder structure
- The `/data` folder contains all the envelope preset files (dynatext)
- The `/audio` folder contains sample audio files

## Feature Comparison: Desktop vs iPadOS

| Feature | iPadOS | Desktop with Optional Libs |
|---------|--------|---------------------------|
| Core envelope sequencing | ✅ | ✅ |
| Sample playback | ✅ | ✅ |
| Preset management | ✅ | ✅ |
| Recording | ✅ | ✅ |
| Effects (Echo, Reverb, Nuke) | ✅ | ✅ |
| Manual/Auto triggering | ✅ | ✅ |
| 3D scope visualization | ❌ | ✅ |
| Advanced audio features | Partial | Full |

## Additional Resources

- **Main Documentation:** [README.md](README.md)
- **HTML Guide:** [html-guide/envion_v3.6.html](html-guide/envion_v3.6.html)
- **Video Tutorials:** See README for YouTube links
- **PlugData Website:** https://plugdata.org

## Still Have Questions?

If you encounter issues not covered in this guide:
1. Check the main [README.md](README.md) for general usage instructions
2. Review the HTML documentation in the `html-guide` folder
3. Open an issue on the GitHub repository with details about your problem

---

**Remember:** The dependency warnings are not errors — they're informational messages about optional features. Envion's core functionality is fully operational on iPadOS without any additional library installations! 🎵
