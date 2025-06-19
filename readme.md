# Swiss Influenza Monitoring Visualization

### Summary
* A simple dashboard to visualize Influenza monitoring 
* Data updated weekly by the Data API of the Swiss Federal Office of Public Health (FOPH).
* Only incidence rate of Infuenza (flu) is visualized.

### Dependencies 
* At startup, data is fetched from FOPH Data API
* https://api.idd.bag.admin.ch/api
* Developed under Python 3.12.8

### Intallation
* First make a venv, then:
```
pip install -r requirements.txt
pip install --upgrade -r requirements.txt
```

### Usage 
*  Start dashboard
```bash 
streamlit run stmain.py
```

### Credits 
* Data management, coordination, and curation kindly performed by FOPH 
* https://www.bag.admin.ch


