y__author__ = 'patelmm79'


import numpy
import scipy.stats
from pandas import Series
from pandas import DataFrame
import pandas
from ggplot import *
import pandasql

fileimport="turnstile_weather_v2.csv"



  

def compare_averages(filename):
    """
    Performs a t-test on two sets of baseball data (left-handed and right-handed hitters).

    You will be given a csv file that has three columns.  A player's
    name, handedness (L for lefthanded or R for righthanded) and their
    career batting average (called 'avg'). You can look at the csv
    file via the following link:
    https://www.dropbox.com/s/xcn0u2uxm8c4n6l/baseball_data.csv

    Write a function that will read that the csv file into a pandas data frame,
    and run Welch's t-test on the two cohorts defined by handedness.

    One cohort should be a data frame of right-handed batters. And the other
    cohort should be a data frame of left-handed batters.

    We have included the scipy.stats library to help you write
    or implement Welch's t-test:
    http://docs.scipy.org/doc/scipy/reference/stats.html

    With a significance level of 95%, if there is no difference
    between the two cohorts, return a tuple consisting of
    True, and then the tuple returned by scipy.stats.ttest.

    If there is a difference, return a tuple consisting of
    False, and then the tuple returned by scipy.stats.ttest.

    For example, the tuple that you return may look like:
    (True, (9.93570222, 0.000023))
    """
    theframe=pandas.read_csv(filename)
    turnstile_weather=theframe
    q="select * from theframe where rain = 1"
    #wasraining=theframe[theframe['rain']==1]
    wasraining=pandasql.sqldf(q.lower(), locals())
    r ="select * from theframe where rain = 0"
    wasnotraining=pandasql.sqldf(r.lower(), locals())
    #wasraining=theframe[['ENTRIESn_hourly']][theframe['rain']==1]
    #numpy.nan_to_num(wasraining)

    wasnotraining=theframe[['ENTRIESn_hourly']][theframe['rain']==0]
    #numpy.nan_to_num(wasnotraining)
    result=scipy.stats.mannwhitneyu(turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==1], turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==0])
    #result=scipy.stats.mannwhitneyu(wasraining['ENTRIESn_hourly'],wasnotraining['ENTRIESn_hourly'])
    #result=scipy.stats.ttest_ind(wasraining['ENTRIESn_hourly'],wasnotraining['ENTRIESn_hourly'],equal_var=False)    
    print len(wasraining.index)
    print len(wasnotraining.index)
    
    
    return result
#print compare_averages(fileimport)

def plotrainhistogram (inputfile):
     theframe=pandas.read_csv(inputfile)
     wasraining=theframe[['ENTRIESn_hourly']][theframe['rain']==1]
    
     gg = ggplot(wasnotraining,aes('ENTRIESn_hourly')) + geom_histogram() + ggtitle("Histogram of Subway Entries--Raining") + xlab("Number of Entries") + ylab ("Frequency")
     return gg
     
     
def plotnorainhistogram (inputfile):
     theframe=pandas.read_csv(inputfile)
     wasnotraining=theframe[['ENTRIESn_hourly']][theframe['rain']==0]
     
    
     gg = ggplot(wasnotraining,aes('ENTRIESn_hourly')) + geom_histogram() + ggtitle("Histogram of Subway Entries--Not raining") + xlab("Number of Entries") + ylab ("Frequency")
     return gg
   
 


def plotdaysweekbarchart(inputfile):
    theframe=pandas.read_csv(inputfile)
    days_week=[0,1,2,3,4,5,6]    
    means=[]
    
   
    for i in range (0,7):
        means.append(numpy.mean(theframe['ENTRIESn_hourly'][theframe['day_week']==i]))
    dayweekdict={'day_week':Series(days_week),'means_Entries':Series(means)}
    dayweekframe=DataFrame(dayweekdict)    
    print dayweekframe[0:7]
    #print type(theframe)
    #wasraining=theframe[['ENTRIESn_hourly']][[theframe['rain']==1]]
    #q="select * from theframe where rain = 1"
    #wasraining=theframe[theframe['rain']==1]
    #wasraining=pandasql.sqldf(q.lower(), locals())
    #print type(wasraining)
    
    
    #gg = ggplot(wasraining,aes('ENTRIESn_hourly')) + geom_histogram(binwidth=500) + ggtitle("Histogram of Subway Entries--Raining") + xlab("Number of Entries per Hour") + ylab ("Frequency")

    gg = ggplot(dayweekframe,aes(x='day_week',y= 'means_Entries')) +geom_bar(aes(weight='means_Entries'))+ ggtitle("Average Ridership by Day of Week") + xlab("Day of Week") + ylab ("Average Number of Entries") 
    #+ scale_y_continuous(limits=(0,5))

  #  gg = ggplot(theframe,aes('day_week')) + geom_bar() + ggtitle("Ridership by Day of Week") + xlab("Day of Week") + ylab ("Frequency")
    #gg = ggplot(theframe,aes('hour')) + geom_bar(") + ggtitle("Ridership by Day of Week") + xlab("Day of Week")
       
    #gg = ggplot(theframe,aes('meanprecipi','ENTRIESn_hourly'))  +geom_point(color='red')

    return gg
    
#print compare_averages(fileimport)
