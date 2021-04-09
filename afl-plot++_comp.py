import datetime                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                               
import numpy as np                                                                                                                                                                                                                                                             
import pylab as plt                                                                                                                                                                                                                                                            
import matplotlib
import matplotlib.dates as mdates

import argparse

import sys
import csv
import os

def parse_file(file_path, time_limit):
    t_c=[]
    crash_delta=[]

    t_p=[]
    path_delta=[]

    with open(file_path, newline='') as csvfile:
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
                t_c.append(t-t0)

                if prev_uniq_crashes==None:
                    prev_uniq_crashes=0

                crash_delta.append(cr-prev_uniq_crashes)
                prev_uniq_crashes=cr

            path=int(row[3])
            if path!=prev_path_total:
                t_p.append(t-t1)

                if prev_path_total==None:
                    prev_path_total=0

                path_delta.append(path-prev_path_total)
                prev_path_total=path

            if (t-t0)>time_limit:
                break
    
    if t_c[-1]<time_limit:
        t_c.append(time_limit)
        c=crash_delta[-1]
        crash_delta.append(c)

    if t_p[-1]<time_limit:
        t_p.append(time_limit)
        p=path_delta[-1]
        path_delta.append(p)

    return t_c,crash_delta,t_p,path_delta

def get_total(time_seqs,deltas):
    assert(len(time_seqs)==len(deltas))
    total_time=[0]
    total_count=[0]

    all_time=sum(time_seqs,[])
    all_delta=sum(deltas,[])
    pairs=zip(all_time,all_delta)

    pairs=sorted(pairs)

    cur_time=0
    cur_count=0

    for t,d in pairs:
        if d==0:
            continue

        if t!=cur_time:
            cur_count+=d
            cur_time=t
            total_time.append(t)
            total_count.append(cur_count)
        else:
            cur_count+=d
            total_count[-1]=cur_count

    return total_time,total_count


def get_avg(time_seqs,deltas):
    t,c=get_total(time_seqs,deltas)

    t=np.array(t)/3600
    c=np.array(c)/len(deltas)

    return t,c

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t',type=float,required=True)
    parser.add_argument('-a', nargs='+',required=True,help='folders for group a')
    parser.add_argument('-b', nargs='+',help='folders for group b')
    parser.add_argument('-c', nargs='+',help='folders for group c')
    parser.add_argument('-al','--a_label',help='name for group a')
    parser.add_argument('-bl','--b_label',help='name for group b')
    parser.add_argument('-cl','--c_label',help='name for group c')
    parser.add_argument("-l", "--linestyle", action="store_true",help="use different linestyles")
    args = parser.parse_args()

    hours=args.t
    time_limit=hours*3600

    color_a='tab:blue'
    color_b='tab:red'
    color_c='tab:green'
    if args.linestyle:
        linestyle_a='-'
        linestyle_b='--'
        linestyle_c='-.'
    else:
        linestyle_a='-'
        linestyle_b='-'
        linestyle_c='-'
    
    fig0 = plt.figure(0)
    plot0=fig0.add_subplot(1,1,1)

    fig1=plt.figure(1)
    plot1=fig1.add_subplot(1,1,1)
    # plt.xlim(xmin=0.0
    #     # ,xmax=time_limit
    #     ,xmax=hours
    # )
    # plt.ylim(ymin=0.0)



    if args.a:
        if args.a_label:
            label=args.a_label
        else:
            label='line a'

        time_seqs_path=[]
        time_seqs_crash=[]
        path_seqs=[]
        crash_seqs=[]
        for folder_name in args.a:
            data=parse_file(os.path.join(folder_name,'plot_data'),time_limit)

            time_seqs_crash.append(data[0])
            crash_seqs.append(data[1])
            time_seqs_path.append(data[2])
            path_seqs.append(data[3])
        

        total_time1,avg_crash=get_avg(time_seqs_crash,crash_seqs)
    
        plot0.step(total_time1,avg_crash,color=color_a,label=label,linestyle=linestyle_a)

        total_time2,avg_path=get_avg(time_seqs_path,path_seqs)

        plot1.step(total_time2,avg_path,color=color_a,label=label,linestyle=linestyle_a)

    if args.b:
        if args.b_label:
            label=args.b_label
        else:
            label='line b'
            
        time_seqs_path=[]
        time_seqs_crash=[]
        path_seqs=[]
        crash_seqs=[]
        for folder_name in args.b:
            data=parse_file(os.path.join(folder_name,'plot_data'),time_limit)

            time_seqs_crash.append(data[0])
            crash_seqs.append(data[1])
            time_seqs_path.append(data[2])
            path_seqs.append(data[3])


        total_time1,avg_crash=get_avg(time_seqs_crash,crash_seqs)
    
        plot0.step(total_time1,avg_crash,color=color_b,label=label,linestyle=linestyle_b)

        total_time2,avg_path=get_avg(time_seqs_path,path_seqs)

        plot1.step(total_time2,avg_path,color=color_b,label=label,linestyle=linestyle_b)

    if args.c:
        if args.c_label:
            label=args.c_label
        else:
            label='line c'
        time_seqs_path=[]
        time_seqs_crash=[]
        path_seqs=[]
        crash_seqs=[]
        for folder_name in args.c:
            data=parse_file(os.path.join(folder_name,'plot_data'),time_limit)

            time_seqs_crash.append(data[0])
            crash_seqs.append(data[1])
            time_seqs_path.append(data[2])
            path_seqs.append(data[3])


        total_time1,avg_crash=get_avg(time_seqs_crash,crash_seqs)
    
        plot0.step(total_time1,avg_crash,color=color_c,label=label,linestyle=linestyle_c)

        total_time2,avg_path=get_avg(time_seqs_path,path_seqs)

        plot1.step(total_time2,avg_path,color=color_c,label=label,linestyle=linestyle_c)
       
    plt.figure(0)
    plt.xticks(np.arange(0, hours+1, step=0.5))
    plt.xlim(xmin=0.0
        # ,xmax=time_limit
        ,xmax=hours
    )
    plt.ylim(ymin=0.0)

    plt.xlabel('run time (hours)')
    plt.ylabel('unique crashes')

    plt.grid()
    plt.legend()

    plt.figure(1)
    plt.xticks(np.arange(0, hours+1, step=0.5))
    plt.xlim(xmin=0.0
        # ,xmax=time_limit
        ,xmax=hours
    )
    plt.ylim(ymin=0.0)

    plt.xlabel('run time (hours)')
    plt.ylabel('total paths')
    plt.grid()
    plt.legend()
    
    plt.show()
    exit()


    
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

