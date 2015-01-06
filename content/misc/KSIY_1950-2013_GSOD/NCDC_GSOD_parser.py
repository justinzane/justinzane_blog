#!/usr/bin/python
# encoding: utf-8
'''
 -- shortdesc
 is a description
It defines classes_and_methods
@author:    Justin Chudgar <justin@justinzane.com>
@updated:    2013-07-09 16:09:04
@license:
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import datetime as dt
import numpy as np
import matplotlib
matplotlib.use('Qt4Agg', warn=True, force=False)
matplotlib.interactive(False)
from matplotlib import pylab as pl

class GSOD(object):
    ''' 
    Python object model of the US NCDC GSOD.
    
    > **Global Summary of the Day (GSOD)**
    > 
    > The data used in building these daily summaries are obtained from the USAF Climatology 
    > Center. The latest daily summary data are updated approximately daily. Data from more 
    > than 9,000 stations are included.
    > [http://www7.ncdc.noaa.gov/CDO/GSOD_DESC.txt](http://www7.ncdc.noaa.gov/CDO/GSOD_DESC.txt)
    >
    > - First record--header record.
    > - All ensuing records--data records as described below.
    > - All 9's in a field (e.g., 99.99 for PRCP) indicates no report or insufficient data.

    0000000000111111111122222222223333333333444444444455555555556666666666777777777788888888889999999999
    0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
    ----------------------------------------------------------------------------------------------------
    STN--- WBAN   YEARMODA    TEMP       DEWP      SLP        STP       VISIB      WDSP     MXSPD   GUST
        MAX     MIN   PRCP   SNDP   FRSHTT
    725955 24259  19500101  0025.0 16    22.4 16  1018.6 16   922.2 16  007.9 16    1.6 16    7.0  999.9
        33.1*   21.9*  0.00I 999.9  100000
    '''

    def __init__(self, filename):
        lines = open(filename, mode='r').readlines()[1:-1]

        self.date_start = dt.date(int(lines[0][14:18]), int(lines[0][18:20]), int(lines[0][20:22]))
        self.date_end = dt.date(int(lines[-1][14:18]), int(lines[-1][18:20]), int(lines[-1][20:22]))
        date_range = self.date_end - self.date_start
        self.num_days = date_range.days
        self.num_years = self.date_end.year - self.date_start.year + 1

        _intar = np.zeros([self.num_days], dtype=int)
        _fltar = np.zeros([self.num_days], dtype=float)
        self.station = np.ma.masked_all_like(_intar)
        self.wban = np.ma.masked_all_like(_intar)
        self.entry_year = np.ma.masked_all_like(_intar)
        self.entry_month = np.ma.masked_all_like(_intar)
        self.entry_day = np.ma.masked_all_like(_intar)
        self.temp_mean = np.ma.masked_all_like(_fltar)
        self.temp_mean_count = np.ma.masked_all_like(_intar)
        self.temp_max = np.ma.masked_all_like(_fltar)
        self.temp_min = np.ma.masked_all_like(_fltar)
        self.temp_dew = np.ma.masked_all_like(_fltar)
        self.press_sealevel = np.ma.masked_all_like(_fltar)
        self.press_ground = np.ma.masked_all_like(_fltar)
        self.wind_mean = np.ma.masked_all_like(_fltar)
        self.wind_mean_count = np.ma.masked_all_like(_intar)
        self.wind_max = np.ma.masked_all_like(_fltar)
        self.wind_gust = np.ma.masked_all_like(_fltar)

        for num in range(0, self.num_days):
            # STN---  1-6       Int.   Station number (WMO/DATSAV3 number) for the location.
            self.station[num] = np.int(line[0:6])

            # WBAN    8-12      Int.   WBAN number -- the historical "Weather Bureau Air Force Navy"
            self.wban[num] = np.int(line[7:12])

            # YEAR    15-18     Int.   The year.
            # MODA    19-22     Int.   The month and day.
            self.entry_year[num] = np.int(line[14:18])
            self.entry_month[num] = np.int(line[18:20])
            self.entry_day[num] = np.int(line[20:22])

            # TEMP    25-30     Real   Mean temperature for the day in degrees Fahrenheit to tenths.
            self.temp_mean[num] = np.float(line[24:30])
            if self.temp_mean == 9999.9:
                self.temp_mean = None
                self.temp_mean_count = None
            else:
                # Count   32-33     Int.   Number of observations used in calculating mean temperature.
                self.temp_mean_count[num] = np.int(line[31:33])

            # DEWP    36-41     Real   Mean dew point for the day in degrees Fahrenheit to tenths.
            self.temp_dewpoint[num] = np.float(line[35:41])
            if self.temp_dewpoint == 9999.9:
                self.dewpoint = None

            # SLP     47-52     Real   Mean sea level pressure for the day in millibars to tenths.
            self.press_sealevel_mean[num] = np.float(line[46:52])
            if self.press_sealevel_mean == 9999.9:
                self.press_sealevel_mean = None
                self.press_sealevel_mean_count = None
            else:
                # Count   54-55     Int.   Number of observations used in calculating mean sea level pressure.
                self.press_sealevel_mean_count[num] = np.int(line[53:55])

            # STP     58-63     Real   Mean station pressure for the day in millibars to tenths.
            self.press_ground_mean[num] = np.float(line[57:63])
            if self.press_ground_mean == 9999.9:
                self.press_ground_mean = None
                self.press_ground_mean_count = None
            else:
                # Count   65-66     Int.   Number of observations used in calculating mean station pressure.
                self.press_ground_mean_count[num] = np.int(line[64:66])

            # VISIB   69-73     Real   Mean visibility for the day in miles.
            self.visib_mean[num] = np.float(line[68:73])
            if self.visib_mean == 999.9:
                self.visib_mean = None
                self.visib_mean_count = None
            else:
                #  Count   75-76     Int.   Number of observations used in calculating mean visibility.
                self.visib_mean_count[num] = np.int(line[74:76])

            # WDSP    79-83     Real   Mean wind speed for the day in knots to tenths.  Missing = 999.9
            self.wind_mean[num] = np.float(line[78:83])
            if self.wind_mean == 999.9:
                self.wind_mean = None
                self.wind_mean_count = None
            else:
                # Count   85-86     Int.   Number of observations used in  calculating mean wind speed.
                self.wind_mean_count[num] = np.int(line[84:86])

            # MXSPD   89-93     Real   Maximum sustained wind speed reported  for the day in knots to tenths.
            self.wind_max[num] = np.float(line[88:93])
            if self.wind_max == 999.9:
                self.wind_max = None

            # GUST    96-100    Real   Maximum wind gust reported for the day in knots to tenths.  Missing = 999.9
            self.wind_gust[num] = np.float(line[95:100])
            if self.wind_gust == 999.9:
                self.wind_gust = None

            # MAX     103-108   Real   Maximum temperature reported during the day in Fahrenheit to tenths--time of max
            #                          temp report varies by country and region, so this will sometimes not be
            #                          the max for the calendar day.
            self.temp_max[num] = np.float(line[102:108])
            if self.temp_max == 9999.9:
                self.temp_max = None
                self.temp_max_accurate = None
            else:
                # Flag    109-109   Char   Blank indicates max temp was taken from the explicit max temp report and not from the
                #                          'hourly' data.  * indicates max temp was  derived from the hourly data (i.e., highest
                #                          hourly or synoptic-reported temperature).
                if line[108:109] == '*':
                    self.temp_max_accurate = False
                else:
                    self.temp_max_accurate = True

            # MIN     111-116   Real   Minimum temperature reported during the day in Fahrenheit to tenths--time of min
            #                          temp report varies by country and region, so this will sometimes not be
            #                          the min for the calendar day.
            self.temp_min[num] = np.float(line[110:116])
            if self.temp_min == 9999.9:
                self.temp_min = None
                self.temp_min_accurate = False
            else:
                # Flag    117-117   Char   Blank indicates from the explicit min temp report.
                #                          * indicates min temp was from the hourly data.
                if line[116:117] == '*':
                    self.temp_min_accurate = False
                else:
                    self.temp_min_accurate = True

            # PRCP    119-123   Real   Total precipitation (rain and/or melted snow) reported; will
            #                          usually not end midnight observation.
            #                          .00 indicates no measurable precipitation (includes a trace).
            #                          Missing = 99.99
            #                          Note:  Many stations do not report '0' on days with no precipitation--therefore,
            #                          '99.99' will often appear on these days. Also, for example, a station may only
            #                          report a 6-hour amount for the period during which rain fell.
            self.precip_tot[num] = np.float(line[118:123])
            if self.precip_tot == 99.99:
                self.precip_tot = None

            # Flag    124-124   Char   A = 1 report of 6-hour precipitation amount.
            #                          B = Summation of 2 reports of 6-hour precipitation amount.
            #                          C = Summation of 3 reports of 6-hour precipitation amount.
            #                          D = Summation of 4 reports of 6-hour precipitation amount.
            #                          E = 1 report of 12-hour precipitation amount.
            #                          F = Summation of 2 reports of 12-hour precipitation amount.
            #                          G = 1 report of 24-hour precipitation amount.
            #                          H = Station reported '0' as the amount for the day (eg, from 6-hour reports),
            #                              but also reported at least one occurrence of precipitation in hourly
            #                              observations--this could indicate a trace occurred, but should be considered
            #                              as incomplete data for the day.
            #                          I = Station did not report any precip data for the day and did not report any
            #                              occurrences of precipitation in its hourly observations--it's still possible that
            #                              precip occurred but was not reported.
            # self. = line[:]
            # SNDP    126-130   Real   Snow depth in inches to tenths--last report for the day if reported more than
            #                          once.  Missing = 999.9 Note:  Most stations do not report '0' on
            #                          days with no snow on the ground--therefore,'999.9' will often appear on these days.
            # self. = line[:]
            # FRSHTT  133-138   Int.   Indicators (1 = yes, 0 = no/not reported) for the occurrence
            #                          during the day of:
            #                          Fog ('F' - 1st digit).
            #                          Rain or Drizzle ('R' - 2nd digit).
            #                          Snow or Ice Pellets ('S' - 3rd digit).
            #                          Hail ('H' - 4th digit).
            #                          Thunder ('T' - 5th digit).
            #                          Tornado or Funnel Cloud ('T' - 6th digit).
            # self. = line[:]



class gsod_entry(object):
    ''' 
    Python object model of the US NCDC GSOD.
    
    > **Global Summary of the Day (GSOD)**
    > 
    > The data used in building these daily summaries are obtained from the USAF Climatology 
    > Center. The latest daily summary data are updated approximately daily. Data from more 
    > than 9,000 stations are included.
    > [http://www7.ncdc.noaa.gov/CDO/GSOD_DESC.txt](http://www7.ncdc.noaa.gov/CDO/GSOD_DESC.txt)
    >
    > - First record--header record.
    > - All ensuing records--data records as described below.
    > - All 9's in a field (e.g., 99.99 for PRCP) indicates no report or insufficient data.

    0000000000111111111122222222223333333333444444444455555555556666666666777777777788888888889999999999
    0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
    ----------------------------------------------------------------------------------------------------
    STN--- WBAN   YEARMODA    TEMP       DEWP      SLP        STP       VISIB      WDSP     MXSPD   GUST
        MAX     MIN   PRCP   SNDP   FRSHTT
    725955 24259  19500101  0025.0 16    22.4 16  1018.6 16   922.2 16  007.9 16    1.6 16    7.0  999.9
        33.1*   21.9*  0.00I 999.9  100000
    '''

    def __init__(self, line):
        # STN---  1-6       Int.   Station number (WMO/DATSAV3 number) for the location.
        self.station = int(line[0:6])

        # WBAN    8-12      Int.   WBAN number -- the historical "Weather Bureau Air Force Navy"
        self.wban = int(line[7:12])

        # YEAR    15-18     Int.   The year.
        # MODA    19-22     Int.   The month and day.
        self.entry_date = dt.date(int(line[14:18]), int(line[18:20]), int(line[20:22]))

        # TEMP    25-30     Real   Mean temperature for the day in degrees Fahrenheit to tenths.
        if line[24:30] == 9999.9:
            self.temp_mean[num] = np.float(line[24:30])

        # Count   32-33     Int.   Number of observations used in calculating mean temperature.
            self.temp_mean_count = np.int(line[31:33])

        # DEWP    36-41     Real   Mean dew point for the day in degrees Fahrenheit to tenths.
        if line[35:41] == '9999.9':
            self.temp_dew[num] = np.float(line[35:41])

        # SLP     47-52     Real   Mean sea level pressure for the day in millibars to tenths.
        self.press_sealevel_mean[num] = np.float(line[46:52])
        if self.press_sealevel_mean == 9999.9:
            self.press_sealevel_mean = None
            self.press_sealevel_mean_count = None
        else:
            # Count   54-55     Int.   Number of observations used in calculating mean sea level pressure.
            self.press_sealevel_mean_count = int(line[53:55])

        # STP     58-63     Real   Mean station pressure for the day in millibars to tenths.
        self.press_ground_mean[num] = np.float(line[57:63])
        if self.press_ground_mean == 9999.9:
            self.press_ground_mean = None
            self.press_ground_mean_count = None
        else:
            # Count   65-66     Int.   Number of observations used in calculating mean station pressure.
            self.press_ground_mean_count = int(line[64:66])

        # VISIB   69-73     Real   Mean visibility for the day in miles.
        self.visib_mean[num] = np.float(line[68:73])
        if self.visib_mean == 999.9:
            self.visib_mean = None
            self.visib_mean_count = None
        else:
            #  Count   75-76     Int.   Number of observations used in calculating mean visibility.
            self.visib_mean_count = int(line[74:76])

        # WDSP    79-83     Real   Mean wind speed for the day in knots to tenths.  Missing = 999.9
        self.wind_mean[num] = np.float(line[78:83])
        if self.wind_mean == 999.9:
            self.wind_mean = None
            self.wind_mean_count = None
        else:
            # Count   85-86     Int.   Number of observations used in  calculating mean wind speed.
            self.wind_mean_count = int(line[84:86])

        # MXSPD   89-93     Real   Maximum sustained wind speed reported  for the day in knots to tenths.
        self.wind_max[num] = np.float(line[88:93])
        if self.wind_max == 999.9:
            self.wind_max = None

        # GUST    96-100    Real   Maximum wind gust reported for the day in knots to tenths.  Missing = 999.9
        self.wind_gust[num] = np.float(line[95:100])
        if self.wind_gust == 999.9:
            self.wind_gust = None

        # MAX     103-108   Real   Maximum temperature reported during the day in Fahrenheit to tenths--time of max
        #                          temp report varies by country and region, so this will sometimes not be
        #                          the max for the calendar day.
        self.temp_max[num] = np.float(line[102:108])
        if self.temp_max == 9999.9:
            self.temp_max = None
            self.temp_max_accurate = None
        else:
            # Flag    109-109   Char   Blank indicates max temp was taken from the explicit max temp report and not from the
            #                          'hourly' data.  * indicates max temp was  derived from the hourly data (i.e., highest
            #                          hourly or synoptic-reported temperature).
            if line[108:109] == '*':
                self.temp_max_accurate = False
            else:
                self.temp_max_accurate = True

        # MIN     111-116   Real   Minimum temperature reported during the day in Fahrenheit to tenths--time of min
        #                          temp report varies by country and region, so this will sometimes not be
        #                          the min for the calendar day.
        self.temp_min[num] = np.float(line[110:116])
        if self.temp_min == 9999.9:
            self.temp_min = None
            self.temp_min_accurate = False
        else:
            # Flag    117-117   Char   Blank indicates from the explicit min temp report.
            #                          * indicates min temp was from the hourly data.
            if line[116:117] == '*':
                self.temp_min_accurate = False
            else:
                self.temp_min_accurate = True

        # PRCP    119-123   Real   Total precipitation (rain and/or melted snow) reported; will
        #                          usually not end midnight observation.
        #                          .00 indicates no measurable precipitation (includes a trace).
        #                          Missing = 99.99
        #                          Note:  Many stations do not report '0' on days with no precipitation--therefore,
        #                          '99.99' will often appear on these days. Also, for example, a station may only
        #                          report a 6-hour amount for the period during which rain fell.
        if int(line[118:123]) != 99.99:
            self.precip_tot[num] = np.float(line[118:123])

        # Flag    124-124   Char   A = 1 report of 6-hour precipitation amount.
        #                          B = Summation of 2 reports of 6-hour precipitation amount.
        #                          C = Summation of 3 reports of 6-hour precipitation amount.
        #                          D = Summation of 4 reports of 6-hour precipitation amount.
        #                          E = 1 report of 12-hour precipitation amount.
        #                          F = Summation of 2 reports of 12-hour precipitation amount.
        #                          G = 1 report of 24-hour precipitation amount.
        #                          H = Station reported '0' as the amount for the day (eg, from 6-hour reports),
        #                              but also reported at least one occurrence of precipitation in hourly
        #                              observations--this could indicate a trace occurred, but should be considered
        #                              as incomplete data for the day.
        #                          I = Station did not report any precip data for the day and did not report any
        #                              occurrences of precipitation in its hourly observations--it's still possible that
        #                              precip occurred but was not reported.
        # self. = line[:]
        # SNDP    126-130   Real   Snow depth in inches to tenths--last report for the day if reported more than
        #                          once.  Missing = 999.9 Note:  Most stations do not report '0' on
        #                          days with no snow on the ground--therefore,'999.9' will often appear on these days.
        # self. = line[:]
        # FRSHTT  133-138   Int.   Indicators (1 = yes, 0 = no/not reported) for the occurrence
        #                          during the day of:
        #                          Fog ('F' - 1st digit).
        #                          Rain or Drizzle ('R' - 2nd digit).
        #                          Snow or Ice Pellets ('S' - 3rd digit).
        #                          Hail ('H' - 4th digit).
        #                          Thunder ('T' - 5th digit).
        #                          Tornado or Funnel Cloud ('T' - 6th digit).
        # self. = line[:]

    def __str__(self):
        retval = 'Date:  %s\n' % self.entry_date.isoformat()
        retval += 'Temps:\n'
        retval += '\tMin:  %5.1f\n' % self.temp_min
        retval += '\tMean: %5.1f\n' % self.temp_mean
        retval += '\tMax:  %5.1f\n' % self.temp_max
        retval += '\tDewP: %5.1f\n' % self.temp_dewpoint
        retval += 'Winds:\n'
        retval += '\tMean: %5.1f\n' % self.wind_mean
        retval += '\tMax:  %5.1f\n' % self.wind_max
        retval += '\tGust: %5.1f\n' % self.wind_gust
        retval += 'Pressures:\n'
        retval += '\tSealevel: %5.1f\n' % self.press_sealevel_mean
        retval += '\tGround:   %5.1f\n' % self.press_ground_mean
        return retval

def plot_month(entrylist, month):
    minyr = 2099
    maxyr = 0
    for e in entrylist:
        if e.entry_date.year > maxyr:
            maxyr = e.entry_date.year
        if e.entry_date.year < minyr:
            minyr = e.entry_date.year
    num = 1 + maxyr - minyr

    np.array
    max_ar = np.empty([31, num], dtype=np.float)
    max_ar.fill(np.nan)
    mean_ar = np.empty([31, num], dtype=np.float)
    mean_ar.fill(np.nan)
    min_ar = np.empty([31, num], dtype=np.float)
    min_ar.fill(np.nan)

    for e in entrylist:
        if e.entry_date.month == month:
            if e.temp_max:
                max_ar[e.entry_date.year - minyr][e.entry_date.day - 1] = np.float(e.temp_max)
            if e.temp_mean:
                mean_ar[e.entry_date.day - 1][e.entry_date.year - minyr][e.entry_date.day - 1] = np.float(e.temp_mean)
            if e.temp_min:
                min_ar[e.entry_date.day - 1][e.entry_date.year - minyr][e.entry_date.day - 1] = np.float(e.temp_min)

    max_mar = np.ma.MaskedArray(max_ar, np.isnan(max_ar))
    mean_mar = np.ma.MaskedArray(mean_ar, np.isnan(mean_ar))
    min_mar = np.ma.MaskedArray(min_ar, np.isnan(min_ar))

    max_mean = np.mean(max_mar.data[~max_mar.mask])
    max_std = np.std(max_mar.data[~max_mar.mask])
    mean_mean = np.mean(mean_mar.data[~mean_mar.mask])
    mean_std = np.std(mean_mar.data[~mean_mar.mask])
    min_mean = np.mean(min_mar.data[~min_mar.mask])
    min_std = np.std(min_mar.data[~min_mar.mask])

    ax = pl.axes()
    ax.set_title("KSIY Hist. Temp. Data")
    ax.axhspan(max_mean - max_std, max_mean + max_std, facecolor='#ff0000', alpha=0.5)
    ax.axhspan(mean_mean - mean_std, mean_mean + mean_std, facecolor='#00ff00', alpha=0.5)
    ax.axhspan(min_mean - min_std, min_mean + min_std, facecolor='#0000ff', alpha=0.5)
    ax.plot(max_mar.data[~max_mar.mask], 'ro')
#    ax.plot(mean_mar.data[~mean_mar.mask], 'go')
#    ax.plot(min_mar.data[~min_mar.mask], 'bo')
    pl.show()

def parse_txt(filename):
    gsod_list = []
    for line in open(filename, mode='r').readlines()[1:-1]:
        gsod_list.append(gsod_entry(line))
    plot_month(gsod_list, 7)

if __name__ == '__main__':
    parse_txt('CDO4965586458127.txt')
