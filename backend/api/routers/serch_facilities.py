import requests
import numpy as np

facilities_tags = {
    "toilet": [{"key": "amenity", "value": "toilets"}],
    "station": [{"key": "railway", "value": "station"}, {"key": "railway", "value": "halt"}],
    "bus_stop": [{"key": "highway", "value": "bus_stop"}, {"key": "amenity", "value": "bus_station"}]
}

def serch_facilities(lat: float, lon: float, facility_type: str):
    facility_tags = facilities_tags[facility_type]
    overpass_url = "http://overpass-api.de/api/interpreter"
    output_latlon = {}
    faculities_list = []
    for facility_tag in facility_tags:
        overpass_query = f"""
            [out:json][timeout:25];
            (
                node[{facility_tag["key"]}={facility_tag["value"]}](around:1000,{lat},{lon});
                way[{facility_tag["key"]}={facility_tag["value"]}](around:1000,{lat},{lon});
                relation[{facility_tag["key"]}={facility_tag["value"]}](around:1000,{lat},{lon});
            );
            out body;
            >;
            out skel qt;
            """
        response = requests.get(
            overpass_url, params={"data": overpass_query}
        )
        res_json = response.json()
        for facility in res_json["elements"]:
            try:
                faculities_list.append({"lat": facility["lat"], "lon": facility["lon"]})
            except:
                pass
    for i, latlon_dict in enumerate(faculities_list):
        output_latlon[i] = latlon_dict
    return output_latlon

def calc_haversine(lat1, lon1, lat2, lon2):
    RADIUS = 6_367_000
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    d = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    dist = 2 * RADIUS * np.arcsin(d**0.5)
    return dist

def get_nearest_facility(current_lat, current_lon, facilities_dict):
    dist_list = []
    for i in range(len(facilities_dict)):
        dist = calc_haversine(current_lat, current_lon, facilities_dict[i]["lat"], facilities_dict[i]["lon"])
        dist_list.append(dist)
    if len(dist_list) == 0:
        return {"lat": 999.0, "lon": 999.0}
    else:
        nearest_idx = dist_list.index(min(dist_list))
        return facilities_dict[nearest_idx]