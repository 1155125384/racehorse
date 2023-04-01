import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from constant import buffer
import pandas as pd
import numpy as np

def read_html_raw(url):
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    op.add_argument('log-level=3')
    op.add_argument("start-maximized")
    op.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser=webdriver.Chrome(service=Service(ChromeDriverManager(log_level=0).install()), options=op)

    browser.get(url)
    time.sleep(buffer.load_url)
    temp_html = browser.page_source
    html = temp_html

    # if not os.path.exists("./file"):
    #     os.makedirs("./file")
    # if not os.path.exists("./file/website"):
    #     os.makedirs("./file/website")
    # path = "./file/website/" + "_html.txt"
    # if os.path.exists(path):
    #     os.remove(path)
    #     time.sleep(buffer.delete_file)
    # with open(path, 'w', encoding="utf-8") as f:
    #     f.write(html)
    return html

def read_raw_html_table(html_txt,table_index):
    tables = pd.read_html(html_txt)
    raw_df = tables[table_index]

    # if not os.path.exists("./file"):
    #     os.makedirs("./file")
    # if not os.path.exists("./file/table"):
    #     os.makedirs("./file/table")
    # path = "./file/table/" + "raw_table.csv"
    # if os.path.exists(path):
    #     os.remove(path)
    #     time.sleep(buffer.delete_file)
    # raw_df.to_csv(path)
    return raw_df

def get_table(raw_df):
    raw_date = raw_df.iloc[5][0]
    date = raw_date[-10:]
    raw_time = raw_df.iloc[6][0]
    time = raw_time[-5:]
    if time[0].isalnum() == False:
        time = raw_time[-4:]

    slot = raw_df.iloc[9][1]

    temp_q_df = pd.DataFrame(columns=[i+1 for i in range(14)], index=range(14))
    temp_q_df.index = np.arange(1, len(temp_q_df) + 1)

    temp_pq_df = pd.DataFrame(columns=[i+1 for i in range(14)], index=range(14))
    temp_pq_df.index = np.arange(1, len(temp_pq_df) + 1)
  
    raw_list = []
    for i in range(27,36,1):
        temp_list = []
        if i != 28 or i != 29:
            if i == 27:
                for j in range(3,16,1):
                    temp_list.append(raw_df.iloc[i][j])
                raw_list.append(temp_list)
            if i >= 30:
                col_no = i-26
                for j in range(col_no,16,1):
                    temp_list.append(raw_df.iloc[i][j])
                raw_list.append(temp_list)
    for i in range(30,36,1):
        temp_list = []
        row_no = i-29
        for j in range(i,36,1):
            # print(raw_df.iloc[j][row_no])
            temp_list.append(raw_df.iloc[j][row_no])
        raw_list.append(temp_list)

    for i in range(13):
        for j in range(i+1):
            raw_list[i].insert(0, "----")
    dummy_nth = []
    for i in range(14):
        dummy_nth.append("----")
    raw_list.append(dummy_nth)

    for i in range(len(raw_list)):
        for j in range(len(raw_list[i])):
            temp_input = str(raw_list[i][j])
            temp_q, temp_pq = identifier(temp_input)
            temp_q_df.iloc[i][j+1] = temp_q
            temp_pq_df.iloc[i][j+1] = temp_pq
    
    temp_single_df = pd.DataFrame(columns=["#", "odds"], index=range(14))
    temp_single_df.index = np.arange(1, len(temp_single_df) + 1)
    for i in range(12,26,1):
        temp_single_df.loc[i-11]['#'] = raw_df[0][i]
        temp_single_df.loc[i-11]['odds'] = raw_df[2][i]

    info = [date,time,slot]
    q_df = parse_14d_df(temp_q_df)
    pq_df = parse_14d_df(temp_pq_df)
    single_df = parse_1d_df(temp_single_df)

    print("賽事日期: ", end="")
    print(info[0])
    print("開跑時間: ", end="")
    print(info[1])
    print("賠率設定時間: ", end="")
    print(info[2])
    print("\n獨贏/位置: ")
    print(single_df)
    print("\nQ圖表: ")
    print(q_df)
    print("\nPQ圖表: ")
    print(pq_df)
    return single_df,q_df,pq_df,info

def identifier(input):
    q = "none"
    pq = "none"
    if input[-2:] == "--" and input[0:2] != "--":
        q = float(input[:-2])
        pq = input[-2:]
    elif input == "----":
        q = input[:-2]
        pq = input[-2:]
    elif input.count('.') == 2:
        pos_float = [pos for pos, char in enumerate(input) if char == '.']
        q = float(input[:pos_float[0]+2])
        pq = float(input[pos_float[0]+2:])
    elif input.count('.') == 1:
        pos_float = input.find('.')
        if len(input) - pos_float == 2:
            if len(input) == 4:
                q = float(input[0:1])
                pq = float(input[1:])
            elif len(input) == 5 or len(input) == 6:
                q = float(input[0:2])
                pq = float(input[2:])
            elif len(input) == 7:
                q = float(input[0:3])
                pq = float(input[3:])
        else:
            q = float(input[0:pos_float+2])
            pq = float(input[pos_float+2:])

    else:
        temp_input = float(input)
        if temp_input > 10 and temp_input < 100:
            q = float(input[0])
            pq = float(input[1])
        elif temp_input > 100 and temp_input < 1000:
            q = float(input[0:1])
            pq = float(input[1:])
        elif temp_input > 1000 and temp_input < 10000:
            q = float(input[0:2])
            pq = float(input[2:])
        else:
            q = float(input[0:3])
            pq = float(input[3:])

    if q == "none" or pq == "none":
        if float(input)-100000>0: 
            q = float(input[0:3])
            pq = float(input[3:])

    return q, pq

def parse_1d_df(df):
    df = df[df['#']!= '--']
    return df

def parse_14d_df(df):
    temp_df = df.copy()
    del_index = []
    for i in range(14):
        col_back = df.iloc[i, i:]
        temp_df.iloc[i: ,i] = col_back
        flag = 0
        for j in range(14):
            if temp_df.iloc[i, :].values[j] == '--':
                flag += 1
            if flag == 14:
                del_index.append(i+1)
    temp_df = temp_df.drop(index = del_index)
    temp_df = temp_df.drop(columns = del_index)
    return temp_df

def sort_1d_df(df):
    df['odds'] = pd.to_numeric(df['odds'])
    result_df = df.sort_values(by=['odds'])
    return result_df

def sort_14d_df(df):
    all_df = []
    index_list = []
    for i in range(df.shape[0]):
        index_list.append(i+1)
    for i in range(df.shape[0]):
        single_df = pd.DataFrame(columns=["#"], data = index_list)
        single_df.index = np.arange(1, len(single_df) + 1)
        single_df["odds"] = df.iloc[:,i].values
        all_df.append(single_df)
    for i in range(len(all_df)):
        temp_parse_single_df = all_df[i].copy()
        temp_parse_single_df = temp_parse_single_df.drop(index = i+1)
        temp_parse_single_df = pd.to_numeric(temp_parse_single_df['odds'])
        temp_parse_single_df = pd.DataFrame(temp_parse_single_df)
        temp_parse_single_df['#'] = temp_parse_single_df.index
        parse_single_df = sort_1d_df(temp_parse_single_df)
        cols = ['#','odds']
        parse_single_df = parse_single_df[cols]
        all_df[i] = parse_single_df
    return all_df

def sort_14d_n_1d_df(single_df, raw_14d_df):
    sorted_single_df = sort_1d_df(single_df)
    single_order_list = sorted_single_df['#'].values
    temp_14d_df = sort_14d_df(raw_14d_df)
    all_result = []
    for i in range(len(single_order_list)):
        index = int(single_order_list[i]) - 1
        all_result.append(temp_14d_df[index])
    return all_result

def parse_q_n_pq_df(single_df, q_df, pq_df):
    parse_single_df = sort_1d_df(single_df)
    parse_q_df = sort_14d_n_1d_df(single_df, q_df)
    parse_pq_df = sort_14d_n_1d_df(single_df, pq_df)
    return parse_single_df, parse_q_df, parse_pq_df

def generate_report(parse_single_df, parse_q_df, parse_pq_df):
    if not os.path.exists("./result"):
        os.makedirs("./result")
    path_q = "./result/" + "q.csv"
    if os.path.exists(path_q):
        os.remove(path_q)
        time.sleep(buffer.delete_file)
    f_q = open(path_q, 'w')

    path_pq = "./result/" + "pq.csv"
    if os.path.exists(path_pq):
        os.remove(path_pq)
        time.sleep(buffer.delete_file)
    f_pq = open(path_pq, 'w')

    temp_single_list = parse_single_df.values.tolist()
    single_txt = ''
    for i in range(len(temp_single_list)):
        for j in range(len(temp_single_list[i])):
            single_txt += str(temp_single_list[i][j])
            single_txt += ','
        if i != len(temp_single_list)-1:
            single_txt += ','
    single_txt = single_txt[:-1]
    f_q.write(single_txt)
    f_q.write("\n")
    f_pq.write(single_txt)
    f_pq.write("\n")
    
    for j in range(parse_q_df[0].shape[0]):
        temp_q_txt = ""
        for i in range(len(parse_q_df)):
            temp_index = parse_q_df[i].iloc[j][0]
            temp_odds = parse_q_df[i].iloc[j][1]
            temp_q_txt += str(int(temp_index))
            temp_q_txt += "," 
            temp_q_txt += str(temp_odds)
            temp_q_txt += ",,"
        f_q.write(temp_q_txt[:-2])
        f_q.write("\n")

    for j in range(parse_pq_df[0].shape[0]):
        temp_pq_txt = ""
        for i in range(len(parse_pq_df)):
            temp_index = parse_pq_df[i].iloc[j][0]
            temp_odds = parse_pq_df[i].iloc[j][1]
            temp_pq_txt += str(int(temp_index))
            temp_pq_txt += "," 
            temp_pq_txt += str(temp_odds)
            temp_pq_txt += ",,"
        f_pq.write(temp_pq_txt[:-2])
        f_pq.write("\n")

def find_url():
    url = input("請貼上on.cc東網 - 馬經 - 賠率賽果 - 賠率速遞 - 綜合賠率的連結: ")
    print("錯誤連結會導致程式顯示錯誤")
    print("如發生錯誤，請重新載入頁面，和重新啟動程式")
    print("正確連結例子：https://racing.on.cc/racing/rat/current/rjrata0001x1.html\n")
    return url

def generate_freq(df,ceiling,floor):
    df_len = df.shape[0]
    count = 0
    for i in range(df_len):
        for j in range(df_len):
            temp_data = df.iloc[i][j+1]
            if temp_data == "--":
                continue
            else: 
                data = float(temp_data)
                if data <= ceiling and data >= floor:
                    count += 1
    count /= 2
    return (int(count))

def find_freq_range(q_df, pq_df):
    print("\n請根據以下指示，尋找賠率出現頻率結果：")
    while True:
        option_input = ""
        ceiling = ""
        floor = ""
        freq_int = 0
        while True:
            print("\n請選擇分析的資料:")
            print("1. Q / Qinella / 連贏")
            print("2. PQ / Place Qinella / 位置連贏")
            option_input = input("請在此輸入【1】或【2】：")
            if option_input == "1" or option_input == "2":
                break  
            else:
                print("\n輸入錯誤，請再試")
                pass
        while True:
            ceiling_input = input("\n請輸入賠率上限: ")
            floor_input = input("請輸入賠率下限: ")
            try:
                ceiling = float(ceiling_input)
                floor = float(floor_input)
            except:
                print("\n輸入錯誤，請再試 --- 請輸入數字/小數")
                continue
            if floor > ceiling:
                print("\n輸入錯誤，請再試 --- 下限比上限大")
                continue
            else:
                break
        if option_input == "1" :
            freq_int = generate_freq(q_df,ceiling,floor)
        elif option_input == "2":
            freq_int = generate_freq(pq_df,ceiling,floor)
        temp_txt = "\n賠率於 "
        temp_txt += str(floor)
        temp_txt += " 和 "
        temp_txt += str(ceiling)
        temp_txt += " 之間的出現頻率次數為： "
        temp_txt += str(freq_int)
        print(temp_txt)
        print("\n程式會繼續分析連結內場次的數據")
        print("如欲查詢其他場次，請重新載入頁面，和重新啟動程式")
        print("以下將會重複剛才指示，繼續尋找賠率出現頻率結果：")