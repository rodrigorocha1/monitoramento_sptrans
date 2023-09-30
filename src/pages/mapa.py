try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
from streamlit_folium import st_folium
from src.database.carregar_mapa_desagrupados import load_mapa


m = load_mapa()

st_mapa = st_folium(m)
