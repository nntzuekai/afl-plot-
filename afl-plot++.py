import datetime                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                               
import numpy as np                                                                                                                                                                                                                                                             
import pylab as plt                                                                                                                                                                                                                                                            
import matplotlib
import matplotlib.dates as mdates

import sys
import csv
import os

if __name__=='__main__':
    file_name=sys.argv[1]
    time_limit=int(sys.argv[2])*3600


    time0=[]
    crashes=[]

    time1=[]
    paths=[]

    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        prev_uniq_crashes=None
        prev_path_total=None
        t0=None
        t1=None
        next(reader)
        for row in reader:
            t=int(row[0])
            if t0==None:
                t0=t
            if t1==None:
                t1=t

            cr=int(row[7])
            if cr!=prev_uniq_crashes:
                prev_uniq_crashes=cr
                time0.append(t-t0)
                crashes.append(prev_uniq_crashes)

            path=int(row[3])
            if path!=prev_path_total:
                prev_path_total=path
                time1.append(t-t1)
                paths.append(path)

            if (t-t0)>time_limit:
                break
    
    # exit()

    if time0[-1]<time_limit:
        time0.append(time_limit)
        q=crashes[-1]
        crashes.append(q)
    
    if time1[-1]<time_limit:
        time1.append(time_limit)
        p=paths[-1]
        paths.append(p)

    
    assert(len(time0)==len(crashes))
    assert(len(time1)==len(paths))

    time0=np.array(time0)
    crashes=np.array(crashes)

    time1=np.array(time1)
    paths=np.array(paths)

    def timeTicks(x, pos):                                                                                                                                                                                                                                                         
        # d = datetime.timedelta(seconds=x)                                                                                                                                                                                                                                          
        # return str(d)[:-3]

        return x/3600

    

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    color = 'tab:red'
    ax.step(time0, crashes,color=color) 

    # plt.xticks([0,30*60*60])
    formatter = matplotlib.ticker.FuncFormatter(timeTicks)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_locator(plt.MultipleLocator(30*60))

    plt.xlim(xmin=0.0
        ,xmax=time_limit
    )
    plt.ylim(ymin=0.0)
    # plt.yticks(np.arange(0,(max(crashes)//25+2)*25,25))

    plt.grid()

    plt.xlabel('run time')
    plt.ylabel('uniq crashes',color=color)
    ax.tick_params(axis='y', labelcolor=color)
    plt.title(os.path.abspath(file_name))

    color2 = 'tab:blue'
    ax2=ax.twinx()
    ax2.step(time1,paths,color=color2)
    ax2.set_ylabel('total paths',color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    fig.tight_layout()

    plt.show()

