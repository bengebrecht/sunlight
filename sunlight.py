import ephem, datetime, time, os
from pyHS100 import SmartPlug

on = False

i = 0

f = open("log.txt", "w")

plug = SmartPlug("192.168.1.27")

plug.turn_off()

while True:

    #Make an observer
    ced = ephem.Observer()

    #PyEphem takes and returns only UTC times
    #ced.date = "2013-09-04 15:00:00"

    #Location of Cedar Rapids, IA
    ced.lon = str(-91.6369485) #Note that lon should be in string format
    ced.lat = str(42.0101096)      #Note that lat should be in string format

    #Elevation of Cedar Rapids, IA, in metres
    ced.elev = 252.799

    #To get U.S. Naval Astronomical Almanac values, use these settings
    ced.pressure = 0
    ced.horizon = '-0:34'

    sunrise = datetime.datetime.strptime(str(ced.previous_rising(ephem.Sun())),'%Y/%m/%d %H:%M:%S') #Sunrise
    noon = datetime.datetime.strptime(str(ced.next_transit(ephem.Sun(), start=sunrise)),'%Y/%m/%d %H:%M:%S') #Solar noon
    sunset = datetime.datetime.strptime(str(ced.next_setting(ephem.Sun())),'%Y/%m/%d %H:%M:%S') #Sunset

    #We relocate the horizon to get twilight times
    ced.horizon = '-6' #-6=civil twilight, -12=nautical, -18=astronomical
    beg_twilight = datetime.datetime.strptime(str(ced.previous_rising(ephem.Sun(), use_center=True)),'%Y/%m/%d %H:%M:%S') #Begin civil twilight
    end_twilight = datetime.datetime.strptime(str(ced.next_setting(ephem.Sun(), use_center=True)),'%Y/%m/%d %H:%M:%S') #End civil twilight

    if beg_twilight.minute < sunrise.minute:
        morning_minutes = range(end_twilight.minute, sunset.minute, -1)
    else:
        morning_minutes = range(sunset.minute, end_twilight.minute)

    if end_twilight.minute < sunset.minute:
        evening_minutes = range(end_twilight.minute, sunset.minute, -1)
    else:
        evening_minutes = range(sunset.minute, end_twilight.minute)

    #24hrs/15min = 96, so break the loop every day 
    while i < 96:

        i = i+1

        f.write(str(beg_twilight.hour-5) + ":" + str(beg_twilight.minute) + ", " + str(sunrise.hour-5) + ":" + str(sunrise.minute) + ", " + str(sunset.hour-5) + ":" + str(sunset.minute) + ", " + str(end_twilight.hour-5) + ":" + str(end_twilight.minute) + ", " + str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute))

        if on:
            if datetime.datetime.now().hour in range(sunset.hour-5, end_twilight.hour-5):
                if datetime.datetime.now().minute in evening_minutes:
                    f.write(", Turning plug off")
                    plug.turn_off()
                    on = False
        else:
            if datetime.datetime.now().hour in range(beg_twilight.hour-5, sunrise.hour-5):
                if datetime.datetime.now().minute in morning_minutes:
                    print(", Turning plug on")
                    plug.turn_on()
                    on = True
        f.write("\n")
        f.flush()
        os.fsync(f)
        time.sleep(900)