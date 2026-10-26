# Swiss Influenza Monitor

### Features
- Interactive web-app 
- Allows Precise selection of reference look-back time.
- Visualizes weekly incidence rates of Influenza (flu) in Switzerland.
- Plots by age, sex, region, and influenza type.
- Customizable color schemes and area plots.
- Weekly data updates fetched from the official FOPH API.

### Dependencies
- Python 3.12 
- Streamlit 1.64.0
- Plotly 7.1.0

### Dependencies Data Source
- [FOPH Infectious Disease Data API](https://www.idd.bag.admin.ch/en/portal-data).


### Installation
1. **Clone the repository**  
2. **Create and activate a virtual environment**  
3. **Install dependencies**  
```bash
pip install -r requirements.txt
```

### Usage
Start the dashboard locally with:
```bash
streamlit run stmain.py
```

### Project Structure
```text
infectious_desease_mon/
├── app.py               # Main app's entry point
├── pages/               # Pages for frontend 
├── src/                 # Data processing and reusable utilities
├── .streamlit/          # Streamlit configuration and theme
├── resources/           # CSS styles and static codebooks  
├── historical_data/     # Historical 'fall-back' data files
├── pics/                # Images and logos
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
└── README.md            # Project documentation
```

### Credits
- Data management and curation: [Swiss Federal Office of Public Health (FOPH)](https://www.bag.admin.ch/)
- Web-app concept, analytics and implementation by Serge Zaugg ([Pollito-ML](https://github.com/sergezaugg))

### License

[MIT License](LICENSE)





