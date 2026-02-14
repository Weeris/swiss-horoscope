# Swiss Horoscope
A precision-powered horoscope app built with Swiss Ephemeris (via pyswisseph).

## Features
- Accurate planetary positions using Swiss Ephemeris (DE431)
- Birth chart (Natal chart) with all planets
- Rising sign (Ascendant) calculation
- House cusps (Placidus system)
- Aspect detection
- Multi-language support (EN, TH, CN)
- Daily/Weekly/Monthly predictions

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Tech Stack
- **Engine**: [pyswisseph](https://github.com/astrorigin/pyswisseph) (Swiss Ephemeris)
- **UI**: Streamlit
- **Language**: Python 3.9+

## License
MIT
