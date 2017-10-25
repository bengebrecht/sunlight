import ephem, datetime, time, os
from pyHS100 import SmartPlug

onoff = 1

f = open("log.txt", "w")

plug = SmartPlug("192.168.1.27")

while 1:

    #Make an observer
    fred      = ephem.Observer()

    #PyEphem takes and returns only UTC times. 15:00 is noon in Fredericton
    #fred.date = "2013-09-04 15:00:00"

    #Location of Fredericton, Canada
    fred.lon  = str(-91.6369485) #Note that lon should be in string format
    fred.lat  = str(42.0101096)      #Note that lat should be in string format

    #Elevation of Fredericton, Canada, in metres
    fred.elev = 252.799

    #To get U.S. Naval Astronomical Almanac values, use these settings
    fred.pressure= 0
    fred.horizon = '-0:34'

    sunrise=datetime.datetime.strptime(str(fred.previous_rising(ephem.Sun())),'%Y/%m/%d %H:%M:%S') #Sunrise
    noon   =datetime.datetime.strptime(str(fred.next_transit   (ephem.Sun(), start=sunrise)),'%Y/%m/%d %H:%M:%S') #Solar noon
    sunset =datetime.datetime.strptime(str(fred.next_setting   (ephem.Sun())),'%Y/%m/%d %H:%M:%S') #Sunset

    #We relocate the horizon to get twilight times
    fred.horizon = '-6' #-6=civil twilight, -12=nautical, -18=astronomical
    beg_twilight=fred.previous_rising(ephem.Sun(), use_center=True) #Begin civil twilight
    end_twilight=fred.next_setting   (ephem.Sun(), use_center=True) #End civil twilight

    f.write(str(sunset.hour-5) + ":" + str(sunset.minute) + ", " + str(sunrise.hour-5) + ":" + str(sunrise.minute) + ", " + str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute))
        
    if onoff == 1:
        if datetime.datetime.now().hour >= (sunset.hour-5) or datetime.datetime.now().hour <= (sunrise.hour-5):
            if datetime.datetime.now().minute >= sunset.minute:
                f.write(", Turning plug off")
                plug.turn_off()
                onoff = 0
    else:
        if datetime.datetime.now().hour <= (sunrise.hour-5):
            if datetime.datetime.now().minute <= sunrise.minute:
                print(", Turning plug on")
                plug.turn_on()
    f.write("\n")
    f.flush()
    os.fsync(f)
    time.sleep(30)