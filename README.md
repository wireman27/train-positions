# train-positions

Simple visualisation of where Mumbai's trains are at any given minute. 

As of 11th April 2018, only Western Railway Slow Line to Churchgate

wr_timetable.pdf - Raw pdf from the Western Railway website
gen_db_all - Use Tabula-converted CSV files from wr_timetable.pdf to create a major chunk of all.geojson
geojson.py - Use station coordinates to ultimately create all.geojson
