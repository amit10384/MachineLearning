import pandas as pd
import os
import time
from datetime import datetime
import matplotlib.pyplot  as plt
from matplotlib import style
import re

style.use("dark_background")

path="/Users/PHODU/Desktop/PYTHON/Data/intraQuarter"

def keyStats(gather="Total Debt/Equity (mrq)") :
    statspath=path+"/_keyStats//"
    stockList = [x[0] for x in os.walk(statspath)]

    df = pd.DataFrame(columns=['Date',
                               'Unix',
                               'Ticker',
                               'DE ratio',
                               'price',
                               'sp500_p_change',
                               'stock_p_change',
                               'difference'])

    sp_500_df = pd.DataFrame.from_csv("/Users/PHODU/Desktop/PYTHON/Data/SP500.csv")

    ticker_list = []

    for dir in stockList[1:25] :
        eachFileList = os.listdir(dir)
        ticker = dir.split("//")[1]
        ticker_list.append(ticker)
        starting_stock_value = False
        starting_sp_value = False
        if len(eachFileList) > 0:
            for file in eachFileList :
                dateStamp = datetime.strptime(file,"%Y%m%d%H%M%S.html")
                unixtime = time.mktime(dateStamp.timetuple())

                full_file_path=dir+"/"+file

                source = open(full_file_path,'r').read()
                try :
                    try :
                      value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split("</td>")[0])
                    except :
                        try :
                            value = float(source.split(gather+':</td>\n<td class="yfnc_tabledata1">')[1].split("</td>")[0])
                        except :
                            print("value gathering ",source.split(gather+':</td>\n<td class="yfnc_tabledata1">')[1].split("</td>")[0])

                    try :
                        sp_500_date = datetime.fromtimestamp(unixtime).strftime("%Y-%m-%d")
                        row =sp_500_df[(sp_500_df.index == sp_500_date)]
                        sp500_p_change = float(row["VALUE"])
                    except :
                        sp_500_date = datetime.fromtimestamp(unixtime-259200).strftime("%Y-%m-%d")
                        row = sp_500_df[(sp_500_df.index == sp_500_date)]
                        sp500_p_change = float(row["VALUE"])



                    try :
                       stock_price = float(source.split("</small><big><b>")[1].split("</b></big>")[0])
                    except :
                        try :
                           stock_price = (source.split("</small><big><b>")[1].split("</b></big>")[0])
                           stock_price = re.search(r'(\d{1,8}\.\d{1,8})',stock_price)
                           stock_price = float(stock_price.group(1))
                           #print("stock price {0}".format(stock_price))
                        except Exception as ee :
                            stock_price = source.split('<span class = "time_rtq_ticker"')[1].split('</span>')[0]
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                            stock_price = float(stock_price.group(1))
                            print("latest stock price {0}".format(stock_price))


                    if not starting_stock_value :
                        starting_stock_value = stock_price

                   # if not starting_sp_value :
                   #    starting_sp_value = here if we calculate adjusted close value in above
                        #then calculate sp_500_p_change



                    stock_p_change =((stock_price - starting_stock_value)/starting_stock_value)*100

                    df = df.append({'Date':dateStamp,
                                  'Unix':unixtime,
                                  'Ticker':ticker,
                                  'DE ratio':value,
                                  'price':stock_price,
                                  'sp500_p_change':sp500_p_change,
                                  'stock_p_change':stock_p_change,'difference':stock_p_change - sp500_p_change},ignore_index=True)
                except Exception as e :
                  print ("exception >  ",e)
                  pass


    for each_ticker in ticker_list[1:]:
        try:
            plot_df = df[(df['Ticker'] == each_ticker)]
            if not plot_df.empty and plot_df is not None:
                plot_df = plot_df.set_index(['Date'])
                plot_df['difference'].plot(label=each_ticker)
                plt.legend()
        except Exception as e:
            print("Exception in ploting",e)

    save = gather.replace(' ', '').replace(')', '').replace('(', '').replace('/', '') + ('.csv')
    print(save)
    df.to_csv("/Users/PHODU/Desktop/PYTHON/ParsedCSV/"+save)




keyStats()