# train-positions

A simple theoretical visualisation of where Mumbai's trains are at any given minute. Current version is Western line, slow, non-Sunday trains going towards Churchgate. Drag the slider to select time.<br>

**Sources** <br>

**wr_timetable.pdf** - Raw pdf from the Western Railway website - http://www.wr.indianrailways.gov.in/uploads/files/1523538301376-UP.pdf <br>
**gen_db_all** - Use Tabula-converted CSV files from wr_timetable.pdf to create a major chunk of all.geojson <br>
**geojson.py** - Use station coordinates to ultimately create all.geojson
