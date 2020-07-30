# POIExtraction
Extracts POIs from OSM Maps



### Prerequisites
1. Install PyOsmium (https://github.com/osmcode/pyosmium)
```
pip install osmium
```
2. Download OSM Convert for Windows (https://wiki.openstreetmap.org/wiki/Osmconvert) and place the .exe in the same folder as the .py  
3. Download the OSM-Map you want to crawl. See "Download Maps" for a brief description
4. Download a .poly file if you first want to extract a map from (3)

### Download Maps / Polygons
1. You can download maps via the Overpass API (https://overpass-turbo.eu/). Copy & Paste this code and navigate to a city, then run it. You can change the borders of the map by changing the administrative level. A (german) overview on administrative levels and their implication can be found here (https://wiki.openstreetmap.org/wiki/DE:Grenze)
```
/*
“admin_level=6: Regierungsbezirk”
“admin_level=7: Städte”
*/
[out:json][timeout:25];
// gather results
(
  // query part for: “admin_level=6”
  relation["admin_level"="6"]({{bbox}});
);
// print results
out body;
>;
out skel qt;
```

2. Several maps can as well be found here: https://download.geofabrik.de/
3. Precompiled .poly files, that allow to extract a map (e.g. a city) from a larger map (e.g. NRW) can be found here: https://wambachers-osm.website/boundaries/
