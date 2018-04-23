# train-positions

![](https://user-images.githubusercontent.com/126868/39108890-ef27209c-46e7-11e8-8747-30d9eff98785.gif)<br>
_**[View demo](https://wireman27.github.io/train-positions/)**_

Simple visualisation of where Mumbai's trains are at any given minute. 

**Lines**
- Virar->Churchgate (Slow)

**Source**
- Western Railways timetable

## Contributing

- wr_timetable.pdf - Raw pdf from the Western Railway website <br>
- gen_db_all - Use Tabula-converted CSV files from wr_timetable.pdf to create a major chunk of all.geojson <br>
- geojson.py - Use station coordinates to ultimately create all.geojson
