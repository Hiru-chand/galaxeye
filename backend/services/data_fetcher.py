import requests
import random

def fetch_sdss_data(ra: float, dec: float):
    """
    Attempts to fetch data from SDSS, but falls back to MOCK data 
    if the connection fails. This ensures the App always works for demos.
    """
    # 1. Try Real Connection
    try:
        url = "http://skyserver.sdss.org/dr16/SkyServerWS/SearchTools/Sql"
        sql_query = f"SELECT top 1 objid, ra, dec, u, g, r, i, z, class FROM PhotoObj WHERE fGetNearbyObjEq({ra},{dec},2.0) = objid"
        params = {"cmd": sql_query, "format": "json"}
        
        # Short timeout so we don't wait forever
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "Rows" in data[0]:
                print(f"SUCCESS: Fetched real data for {ra}, {dec}")
                return data[0]["Rows"][0]
                
    except Exception as e:
        print(f"SDSS Connection failed ({e}). Switching to Mock Data.")

    # 2. Mock Data Fallback (If real data fails, we generate fake data)
    # This guarantees your Final Year Project demo NEVER crashes.
    print(f"WARNING: Generating MOCK data for {ra}, {dec}")
    
    return {
        "objid": 123456789,
        "ra": ra,
        "dec": dec,
        "u": round(random.uniform(14, 22), 2),
        "g": round(random.uniform(14, 22), 2),
        "r": round(random.uniform(14, 22), 2),
        "i": round(random.uniform(14, 22), 2),
        "z": round(random.uniform(14, 22), 2),
        "class": "UNKNOWN (Mock)" 
    }