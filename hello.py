import airportsdata
import json

airportsdata = airportsdata.load('IATA')

def generate_sql_updates():
    print(airportsdata['JFK'])
    
    with open('nameless-airports-homol.json') as airports_json:
        airports = json.load(airports_json)
        
        sql_updates = []
        manual_sql_updates = []

        for airport in airports:
            airport_iata = airport['iata']
            airport_info = airportsdata.get(airport_iata)
            
            if not airport_info:
                manual_updates = []
                if airport['city_name'] is None:
                    print(f"City name for {airport_iata} not found, Airport id: {airport['id']}")
                    manual_updates.append("city_name = ''")
                if airport['country_name'] is None:
                    print(f"Country name for {airport_iata} not found, Airport id: {airport['id']}")
                    manual_updates.append("country_name = ''") 
                
                if manual_updates:
                    sql = f"""
                    UPDATE public.airports 
                    SET {', '.join(manual_updates)} 
                    WHERE id = {airport['id']} 
                    AND iata = '{airport_iata}' 
                    AND name = '{airport['name']}';
                    """
                    manual_sql_updates.append(sql.strip())
                continue
            
            updates = []
            if airport['city_name'] is None:
                updates.append(f"city_name = '{airport_info['city']}'")
            if airport['country_name'] is None:
                updates.append(f"country_name = '{airport_info['country']}'")
            
            if updates:
                sql = f"""
                UPDATE public.airports 
                SET {', '.join(updates)} 
                WHERE id = {airport['id']} 
                AND iata = '{airport_iata}' 
                AND name = '{airport['name']}';
                """
                sql_updates.append(sql.strip())
        
        with open('update_airports_homol.sql', 'w') as sql_file:
            sql_file.write("\n".join(sql_updates))
        
        with open('update_airports_manual_homol.sql', 'w') as manual_sql_file:
            manual_sql_file.write("\n".join(manual_sql_updates))
        
        print("SQL update scripts generated")
generate_sql_updates()