# EMIDSSV-GUI
Mancilla, M. et al. (2024). Design of an Automotive Embedded System for Stratospheric Environments (EMIDSS-V). AUSJAL / ITESO. https://repositorio.ausjal.org/handle/20.500.12032/160112

Desktop GUI to communicate with the EMIDSS-V (LEO Nanosatellite) over a
UART serial link, built as part of the EMIDSS-V mission software for
stratospheric/low-Earth-orbit data collection.

## Features
- **Read Service** — query satellite Time, Memory, or SW Version
  (UDS-style request/response, e.g. `S2201`, `S2202`, `S2203`)
- **Write Service** — set onboard Hour value (`S2301`)
- **Reset Service** — reset Sensor or Memory subsystems (`S1101`, `S1102`)
- **Raw command console** — send arbitrary serial commands and view live
  UART output
- **Mission data visualization** — plot temperature, humidity, and
  pressure over time from logged Excel data (`GraphicData.py`)
- **Data integrity check** — scan mission data for missing/out-of-range
  values before analysis (`CheckIntegrity.py`)

## Tech Stack
- Python 3
- [PySimpleGUI](https://pypi.org/project/PySimpleGUI/) — GUI framework
- `pyserial` — UART communication
- `pandas` / `matplotlib` — data analysis and plotting
- `Pillow` — image handling for UI assets

## How It Works
On launch, the app opens a UART configuration window (port + baud rate).
Once connected, the main window sends service-style commands over serial
and displays the satellite's responses in a live console. Mission
telemetry logged to `EMIDSS_V_Data.xlsx` can be checked for integrity and
plotted directly from the GUI.

## Running Locally
```bash
pip install pysimplegui pyserial pandas matplotlib pillow
python EMIDSSV_GUI.py
```

## Project Context
Developed as part of EMIDSS-V, a NASA-related stratospheric/LEO
nanosatellite project (ITESO), where this GUI served as the ground-side
interface for mission data retrieval and satellite configuration.
