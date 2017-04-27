import pandas as pd
import os
import time
from datetime import datetime

path="/Users/PHODU/Desktop/PYTHON/Data/intraQuarter"

def keyStats(gather="Total Debt/Equity (mrq)") :
    statspath=path+"/_keyStats//"
    stockList = [x[0] for x in os.walk(statspath)]

    df = pd.DataFrame(columns=['Date', 'Unix', 'Ticker', 'DE ratio'])

    for dir in stockList[1:5] :
        eachFileList = os.listdir(dir)
        ticker=dir.split("//")[1]

        if len(eachFileList) > 0:
            for file in eachFileList :
                dateStamp = datetime.strptime(file,"%Y%m%d%H%M%S.html")
                unixtime=time.mktime(dateStamp.timetuple())

                full_file_path=dir+"/"+file

                source = open(full_file_path,'r').read()
                try :
                    value=float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split("</td>")[0])
                    df=df.append({'Date':dateStamp,'Unix':unixtime,'Ticker':ticker,'DE ratio':value,},ignore_index=True)
                except Exception as e :
                    pass


            time.sleep(1)

    save = gather.replace(' ', '').replace(')', '').replace('(', '').replace('/', '') + ('.csv')
    print(save)
    df.to_csv("/Users/PHODU/Desktop/PYTHON/ParsedCSV/"+save)




keyStats()