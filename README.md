# train-positions

Simple theoretical visualisation of where Mumbai's trains are at any given minute. 

**wr_timetable.pdf** - Raw pdf from the Western Railway website - http://www.wr.indianrailways.gov.in/uploads/files/1523538301376-UP.pdf <br>
**gen_db_all** - Use Tabula-converted CSV files from wr_timetable.pdf to create a major chunk of all.geojson <br>
**geojson.py** - Use station coordinates to ultimately create all.geojson
