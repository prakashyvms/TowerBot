# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 09:33:30 2023

@author: Prakash
"""
import pandas

def buttons_lines(station_name):
    excel_data_df = pandas.read_excel('D:\\ML Course\\SR1_ML_Project\\Programs_Final\\VMG_TLM.xlsx', sheet_name='Sheet1')
    buttons=[]
    line_list=list(excel_data_df['Name_Of_Line2'].unique())
    for line in line_list:
    #button = "{\"payload\"" + ":" + "'" + line + "'" + "," + "\"title\"" + ":" + "\"" + line + "\"}"
        button = {}
        button["payload"] = line
        button["title"] = line
        #print(button)
        buttons.append(button)
    return(buttons)


def fault_location_number(line,fault_distance):
    excel_data_df = pandas.read_excel('D:\\ML Course\\SR1_ML_Project\\Programs_Final\\VMG_TLM.xlsx', sheet_name='Sheet1')
    df=excel_data_df[excel_data_df['Name_Of_Line2']==line].iloc[(excel_data_df[excel_data_df['Name_Of_Line2']==line]['CUM']-fault_distance).abs().argsort()[:2]]
    df1=df[['Tower','Name_Of_Line2','CUM','PS1','PS2','Type_Of_Tower4','Nearest_Village14']].sort_values(by="Tower")
    line_data_df = pandas.read_excel('D:\\ML Course\\SR1_ML_Project\\Programs_Final\\VMG_TLM.xlsx', sheet_name='Sheet5')
    length=line_data_df[line_data_df['Name_Of_Line']==line]["length"].values.max()
    DOCO=line_data_df[line_data_df['Name_Of_Line']==line]["DOCO"].dt.strftime('%m/%d/%Y').values[0]
    TLM_juris = excel_data_df[excel_data_df['Name_Of_Line2']==line]['CUM'].max()
    if(df1.iloc[0,4] == 0):
        msg = "Fault location: {}({}) - {}({});<br>Village: {};<br>Line: {};<br>Phase sequence:{};left to right<br>TLM jurisdiction: {} Kms;<br>line length: {} Kms<br>DOCO: {}".format(df1.iloc[0,0],df1.iloc[0,5],df1.iloc[1,0],df1.iloc[1,5],df1.iloc[0,6],df1.iloc[0,1],df1.iloc[0,3],round(TLM_juris,2),length, DOCO)
    else:
        msg = "Fault location: {}({}) {}({})<br>Village: {}<br>Line: {}<br>Phase sequence of first circuit:{} & second ciruit:{}, top to bottom<br>TLM jurisdiction: {} Kms<br>line length: {} Kms<br>DOCO: {}".format(df1.iloc[0,0],df1.iloc[0,5],df1.iloc[1,0],df1.iloc[1,5],df1.iloc[0,6],df1.iloc[0,1],df1.iloc[0,3],df1.iloc[0,4],round(TLM_juris,2),length, DOCO) 
    return(msg)


def tower_location_dat(line,tower):
    #print(line,tower)
    try:
        tower=int(tower)
    except:
        tower=str(tower)
    excel_data_df = pandas.read_excel('D:\\ML Course\\SR1_ML_Project\\Programs_Final\\VMG_TLM.xlsx', sheet_name='Sheet1')
    line_data_df = pandas.read_excel('D:\\ML Course\\SR1_ML_Project\\Programs_Final\\VMG_TLM.xlsx', sheet_name='Sheet5')
    DOCO=line_data_df[line_data_df['Name_Of_Line']==line]["DOCO"].dt.strftime('%m/%d/%Y').values[0]
    length=line_data_df[line_data_df['Name_Of_Line']==line]["length"].values.max()
    TLM_juris = excel_data_df[excel_data_df['Name_Of_Line2']==line]['CUM'].max()
    df1=excel_data_df[(excel_data_df['Name_Of_Line2']==line) & (excel_data_df['Tower']==tower)][['Tower','Name_Of_Line2','CUM','PS1','PS2','Type_Of_Tower4','Nearest_Village14']]
    if(df1.iloc[0,4] == 0):
        msg = "Tower location: {}({})<br>Village: {}<br>Line: {} Kms<br>Phase sequence:{}, left to right<br>TLM jurisdiction: {} Kms<br>line length: {} Kms<br>DOCO: {}".format(df1.iloc[0,0],df1.iloc[0,5],df1.iloc[0,6],df1.iloc[0,1],df1.iloc[0,3],round(TLM_juris,2),length, DOCO)
        msg = msg+ "<br>" + farmer_details(tower,line)
    else:
        msg = "Fault location: {}({})<br>Village: {}<br>Line: {}<br>Phase sequence of first circuit:{} & second ciruit:{}, top to bottom<br>TLM jurisdiction: {} Kms<br>line length: {} Kms<br>DOCO: {}".format(df1.iloc[0,0],df1.iloc[0,5],df1.iloc[0,6],df1.iloc[0,1],df1.iloc[0,3],df1.iloc[0,4],round(TLM_juris,2),length, DOCO) 
        msg = msg+ "<br>" + farmer_details(tower,line)
    return(msg)

def farmer_details(tower,line):
    key=str(tower) + ": " + line
    farmer_df=pandas.read_excel('D:\\ML Course\\SR1_ML_Project\\Programs_Final\\VMG_TLM.xlsx', sheet_name='Sheet3')
    tree_cutting=pandas.read_excel('D:\\ML Course\\SR1_ML_Project\\Programs_Final\\VMG_TLM.xlsx', sheet_name='Sheet2')
    msg=""
    for index, row in farmer_df[farmer_df["Tower & Line"]==key].iterrows():
        msg=msg+"Farmer:<br>{}<br>Mobile: {}<br><br>".format(row["Farmer Name & Address"],row["Mobile Number"])
    flag=0
    for date in tree_cutting[tree_cutting["Tower & Line"]==key]["Timestamp"].dt.strftime('%m/%d/%Y'):
        if flag==0:
            msg=msg+"Tree Cutting Dates: "
            flag=1
        msg=msg+date+","
    #print(msg)
    return(msg)

def tower_valid(tower,line):
    try:
        tower=int(tower)
    except:
        tower=str(tower)
    excel_data_df = pandas.read_excel('D:\\ML Course\\SR1_ML_Project\\Programs_Final\\VMG_TLM.xlsx', sheet_name='Sheet1')
    df_line=excel_data_df[excel_data_df['Name_Of_Line2']==line]
    if tower in df_line['Tower'].unique():
        msg = "Value Found"
        return(msg)
    else:
        try:
            end_tower=df_line[df_line['CUM']==df_line['CUM'].max()].Tower.values[0]
            start_tower=df_line[df_line['CUM']==df_line['CUM'].min()].Tower.values[0]
            int_list=[]
            str_list=[]
            for index, row in df_line.iterrows():
                try:
                    int_list.append(int(row.Tower))
                except:
                    str_list.append(str(row.Tower))
            msg = "Please enter valid input. Details are given below:<br>start Location: {}, Last Location: {}<br>List of Towers:{}{}<br>".format(start_tower,end_tower,int_list,str_list)
        except:
            msg = "Data is not available"       
    return(msg)
    
def distance_valid(fault_distance,line_name):
    try:
        fault_distance=int(fault_distance)
    except:
        fault_distance=str(fault_distance)
    excel_data_df = pandas.read_excel('D:\\ML Course\\SR1_ML_Project\\Programs_Final\\VMG_TLM.xlsx', sheet_name='Sheet1')
    TLM_juris = excel_data_df[excel_data_df['Name_Of_Line2']==line_name]['CUM'].max()
    try:
        if  TLM_juris<float(fault_distance) or float(fault_distance) <0 :
            msg = "fault is {} Kms beyond Vemagiri TLM jurisdiction".format(round((fault_distance-TLM_juris),2))
        else:
            msg = "VALID"
    except:
        msg = "Please enter distance in Km. Eg: If fault distance is 20km, enter 20"
    return(msg)