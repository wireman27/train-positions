import pandas as pd
import re
from datetime import datetime
final_list = list()



for fileno in range(0, 42):
    df = pd.read_csv("C:/Coursera/mumbai_wr/raw_files/tabula-wr_timetable-{x}.csv".format(x=fileno), header=-1)
    for serviceno in range(1,len(df.columns.tolist())):
        service = df[serviceno].tolist()
        orig_index = None
        dest_index = None
        #finding origin and destination, service type
        for x in service:
            try:
                y = re.search(r'\d+:\d+',x)
                if y is not None:
                    orig_index = service.index(x)
                    break
            except Exception:
                continue
        for x in reversed(service):
            try:
                y = re.search(r'\d+:\d+',x)
                if y is not None:
                    dest_index = service.index(x)
                    break
            except Exception:
                continue
        if orig_index is not None and dest_index is not None:
            orig = df.loc[orig_index,0]
            dest = df.loc[dest_index,0]
            true_service = service[orig_index:dest_index + 1]
            serv_type = 'S'
            for x in true_service:
                try:
                    y = re.search(r'\d+:\d+',x)
                except Exception:
                    serv_type = 'F'
                    break
            train_id = serv_type+'-'+orig.upper()[0:3]+'-'+dest.upper()[0:3]+'-'+service[orig_index]
            ##creating each movement
            for index in range(orig_index,dest_index+1):
                arow = dict()
                arow['station_name']=str(df.loc[index,0])
                arow['time']=service[index]
                arow['service']=train_id
                final_list.append(arow)

                
## standardising station names
final = pd.DataFrame(final_list)
final['station_name'] = final['station_name'].str.lower()
final['station_name'] = final['station_name'].str.replace("m'bai central\(l\)","mumbai central")
final['station_name'] = final['station_name'].str.replace("prabhadevi","elphinstone road")
final['station_name'] = final['station_name'].str.replace("mahim jn.","mahim")
final['station_name'] = final['station_name'].str.replace("nan","ram mandir")


## cleaning up time and removing rows which don't have time
clean_time_string = list()
clean_time_minutes = list()

for time in final['time'].tolist():
    try:
        time_re = re.search(r'(\d+:\d\d)',time)
        time_str = time_re.group(1)
        time_dt = datetime.strptime(time_str,'%H:%M').time()
        minutes = time_dt.hour * 60 + time_dt.minute
        clean_time_minutes.append(minutes)
        clean_time_string.append(time_str)
    except AttributeError:
        clean_time_string.append('time_fail')
        clean_time_minutes.append('time_fail')
    except TypeError:
        clean_time_string.append('time_fail')
        clean_time_minutes.append('time_fail')
    except ValueError as error:
        if str(error) == "time data '0:00' does not match format '%H:%M'":
            clean_time_string.append('0:00')
            clean_time_minutes.append(0)
        else:
            print(error)
            print(type(error))
            break

final['time_str']=clean_time_string
final['time_min']=clean_time_minutes
final = final[final['time_str']!='time_fail']


services = pd.DataFrame()
services['service']=final['service'].unique()

tr_time_min = list()
for time in final['time_min'].tolist():
    if time in range(0, 106):
        tr_time = 60 * 24 + time
        tr_time_min.append(tr_time)
    else:
        tr_time_min.append(time)

final['tr_time_min']=tr_time_min

start_time = list()
end_time = list()

for service in services['service']:
    start = final[final['service']==service]['tr_time_min'].tolist()[0]
    end = final[final['service']==service]['tr_time_min'].tolist()[-1]
    start_time.append(start)
    end_time.append(end)

services['start_time']=start_time
services['end_time']=end_time


## shit gets real here ## 1546

times_final = range(0,1546)

toplot_time = list()
toplot_station = list()
toplot_service = list()
toplot_diff = list()

for minute in times_final:
    print(minute)
    list_of_services = list()
    for service in services['service'].tolist():
        block1 = services[services['service']==service]['start_time'].iloc[0]
        block2 = services[services['service']==service]['end_time'].iloc[0]
        if minute >= block1 and minute <= block2:
            list_of_services.append(service)
    for service in list_of_services:
        diff_in_time = [minute - time for time in final[final['service']==service]['tr_time_min'].tolist()]
        diff = min(time for time in diff_in_time if time >= 0) 
        index = diff_in_time.index(diff)
        station = final[final['service']==service]['station_name'].iloc[index]
        toplot_time.append(minute)
        toplot_station.append(station)
        toplot_service.append(service)
        toplot_diff.append(diff)
        
        
toplot = pd.DataFrame()
toplot['time']=toplot_time
toplot['station']=toplot_station
toplot['service']=toplot_service
toplot['diff']=toplot_diff

station_meta = pd.read_csv('C:/Coursera/mumbai_wr/station_metadata.csv')
incr_table = pd.DataFrame()
incr_service =  list()
incr_station = list()
incr_lng = list()
incr_lat = list()

for service in toplot['service'].unique().tolist():
    print(service)
    stations = toplot[toplot['service']==service]['station'].unique().tolist()
    for station in stations:
        inc = len(toplot[(toplot['service']==service) & (toplot['station']==station)]['diff'].tolist())
        lng = station_meta[station_meta['station_name']==station]['lng'].iloc[0]
        lat = station_meta[station_meta['station_name']==station]['lat'].iloc[0]
        nxt = station_meta[station_meta['station_name']==station]['next_station'].iloc[0]
        nxt_lng = station_meta[station_meta['station_name']==nxt]['lng'].iloc[0]
        nxt_lat = station_meta[station_meta['station_name']==nxt]['lat'].iloc[0]
        lng_inc = (nxt_lng - lng) / inc
        lat_inc = (nxt_lat - lat) / inc
        incr_service.append(service)
        incr_station.append(station)
        incr_lng.append(lng_inc)
        incr_lat.append(lat_inc)

incr_table['incr_service']=incr_service
incr_table['incr_station']=incr_station
incr_table['incr_lng']=incr_lng
incr_table['incr_lat']=incr_lat


final_lng = list()
final_lat = list()


rows = len(toplot['time'].tolist())

for point in range(0, rows):
    service = toplot.iloc[point,2]
    station = toplot.iloc[point,1]
    diff = toplot.iloc[point,3]
    selector = incr_table[(incr_table['incr_service']==service) & (incr_table['incr_station']==station)]
    stn_lng = station_meta[station_meta['station_name']==station]['lng'].iloc[0]
    stn_lat = station_meta[station_meta['station_name']==station]['lat'].iloc[0]
    inc_lng = selector['incr_lng'].iloc[0]
    inc_lat = selector['incr_lat'].iloc[0]
    lng_final = stn_lng + diff * inc_lng
    lat_final = stn_lat + diff * inc_lat
    final_lng.append(lng_final)
    final_lat.append(lat_final)

toplot['final_lng']=final_lng
toplot['final_lat']=final_lat

toplot.to_csv('C:/Coursera/mumbai_wr/ready_for_plot_all.csv')



    
    
    
    

        
        
        
        
        








    
    

