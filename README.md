# Trust in government regulation of AI, 2025

Reproduces Figure 9.3.1 of the Stanford HAI AI Index Report 2026 (Chapter 9, Public Opinion)
as a ranked bar chart. Underlying data: Ipsos AI Monitor 2025, item
"I trust the government of [country] to regulate AI responsibly" (% agree).

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python get_data.py   # -> data/raw/fig_9.3.1.csv (from HAI's public Google Drive)
.venv/bin/python plot.py       # -> figures/trust_gov_regulate_ai_2025.png / .pdf
```

Notes
- Percentages are Ipsos's published, already-weighted country estimates; no weighting is applied here.
- "Global" (54%) is Ipsos's unweighted 30-country average, not a population-weighted figure.
- The Ipsos AI Monitor 2026 does not report this item, so the series stops at 2025.
