# AquaGuard AI 💧
## AI-Powered Water Loss Detection and Repair Prioritisation

AquaGuard AI is a hackathon prototype for **Track 3: Water Loss Detection**. It uses simulated flow, pressure and consumption readings to identify likely leaks, localise the affected zone, estimate water loss, and rank repairs.

### Features
- Synthetic sensor data generation (clearly labelled as simulated)
- Leak probability prediction using a Random Forest classifier
- Leak-zone localisation
- Severity and estimated water-loss scoring
- Repair-priority ranking
- Interactive Streamlit dashboard

### Quick start
```bash
pip install -r requirements.txt
python src/data_generation.py
python src/train_model.py
streamlit run app/dashboard.py
```

### Project structure
- `src/data_generation.py` — generates synthetic network sensor data
- `src/train_model.py` — trains the leak classifier
- `src/predict.py` — creates ranked predictions
- `app/dashboard.py` — interactive dashboard
- `data/` — generated datasets
- `models/` — trained model artifacts

### Responsible use
This is a prototype, not an operational water-utility control system. Synthetic data is used for the hackathon prototype. Real deployment requires validated utility data, field testing, cybersecurity review and human oversight.
