#-*- coding:utf-8 -*-
import argparse
from datetime import datetime,timedelta
from googleads import adwords
from adobe_api.data_sources import data_source
from adobe_api.reporting import getReport
import hashlib
import re

#AdWords Data
#Testaccount
#CAMPAIGN_ID = "920028644"
#Produktion
SHOPPING_CAMPAIGN_ID = "637256552"
RETARGETING_CART_ID = "775107070"
RETARGETING_CHECKOUT_ID = "793689836"
MONEY_DIVISOR = 1000000

#Adobe API Data
USERNAME = "mp.service:Deutsche Post AG"
SECRET = "893b59a90511bc65db4afb455f8f575a"
PROXY = "http://globalproxy.goc.dhl.com:8080"
REPORTSUITE = "deutschepostwpmdhlmpprod"

category_cid_mapping = {
    "Baby & Kleinkind":"c_dhlmp_ie_dpcom_00029_66743_MB_225",
    "Bekleidung & Accessoires":"c_dhlmp_ie_dpcom_00029_67503_EW_559",
    "Bürobedarf":"c_dhlmp_ie_dpcom_00029_56804_TM_271",
    "Elektronik":"c_dhlmp_ie_dpcom_00029_16364_MZ_475",
    "Fahrzeuge & Teile":"c_dhlmp_ie_dpcom_00029_98372_BZ_258",
    "Gesundheit & Schönheit":"c_dhlmp_ie_dpcom_00029_29165_CD_712",
    "Heim & Garten":"c_dhlmp_ie_dpcom_00029_42890_ZB_567",
    "Heimwerkerbedarf":"c_dhlmp_ie_dpcom_00029_36599_AW_365",
    "Kameras & Optik":"c_dhlmp_ie_dpcom_00029_18828_YF_170",
    "Kunst & Unterhaltung":"c_dhlmp_ie_dpcom_00029_55024_AK_948",
    "Medien":"c_dhlmp_ie_dpcom_00029_28092_YJ_023",
    "Möbel":"c_dhlmp_ie_dpcom_00029_35812_IM_984",
    "Nahrungsmittel, Getränke & Tabak":"c_dhlmp_ie_dpcom_00029_40257_ND_000",
    "Software":"c_dhlmp_ie_dpcom_00029_18904_YX_200",
    "Spielzeuge & Spiele":"c_dhlmp_ie_dpcom_00029_94955_EY_319",
    "Sportartikel":"c_dhlmp_ie_dpcom_00029_24118_WK_573",
    "Taschen & Gepäck":"c_dhlmp_ie_dpcom_00029_73713_DB_932",
    "Tiere & Tierbedarf":"c_dhlmp_ie_dpcom_00029_63566_VE_166",
    "Wirtschaft & Industrie":"c_dhlmp_ie_dpcom_00029_82947_KN_808",
    "Religion & Feierlichkeiten":"c_dhlmp_ie_dpcom_00029_43334_DA_172"
}

retargeting_id_mapping = {
    "775107070":"c_dhlmp_be_dpcom_00108_00001_WA_001",
    "793689836":"c_dhlmp_be_dpcom_00108_00001_CA_001"
}

#parser = argparse.ArgumentParser()
#parser.add_argument("--date",help="Define custom date -> format:\"YYYYMMDD\" (default: yesterday)",default=(datetime.now()-timedelta(1)).strftime("%Y%m%d"))
#parser.add_argument("--proxy",nargs='?',default=0)
#args=parser.parse_args()

def get_retargeting_report(client,date):
    report_downloader = client.GetReportDownloader(version="v201710")

    report = {
        "reportName":"Kostenimport",
        "dateRangeType":"CUSTOM_DATE",
        "reportType":"CAMPAIGN_PERFORMANCE_REPORT",
        "downloadFormat":"CSV",
        "selector":{
            "dateRange":{
                "min":date,
                "max":date
            },
            "fields":["Date","CampaignId","Cost","Impressions","Clicks","Conversions","TrackingUrlTemplate"],
            "predicates":[
                {
                    "field":"AdvertisingChannelType",
                    "operator":"NOT_EQUALS",
                    "values":[
                        "SHOPPING"
                    ]
                },
                {
                    "field":"Cost",
                    "operator":"GREATER_THAN",
                    "values":[
                        "0"
                    ]
                }
            ]
        }
    }

    result = report_downloader.DownloadReportAsString(
        report,skip_report_header=True,skip_column_header=False,
        include_zero_impressions=False,skip_report_summary=True
    )
    
    return result

def get_shopping_report(client,campaign_id,date):
    report_downloader = client.GetReportDownloader(version="v201710")

    report = {
        "reportName":"Kostenimport",
        "dateRangeType":"CUSTOM_DATE",
        "reportType":"SHOPPING_PERFORMANCE_REPORT",
        "downloadFormat":"CSV",
        "selector":{
            "dateRange":{
                "min":date,
                "max":date
            },
            "fields":["Date","CategoryL1","Cost","Impressions","Clicks","Conversions","CustomAttribute3","OfferId"],
            "predicates":[
                {
                    "field":"CampaignId",
                    "operator":"EQUALS",
                    "values":[
                        campaign_id
                    ]
                },
                {
                    "field":"Cost",
                    "operator":"GREATER_THAN",
                    "values":[
                        "0"
                    ]
                }
            ]
        }
    }

    result = report_downloader.DownloadReportAsString(
        report,skip_report_header=True,skip_column_header=False,
        include_zero_impressions=False,skip_report_summary=True
    )
    
    return result

def format(report,typ="s"):
    formatted = []
    lines = report.split("\n")
    regEx = re.compile("(\"([^\"]*)\"|[^,]*)(,|$)")
    for i,line in enumerate(lines):
       if not i:continue
       if not line:continue
       cost_entry = [x[0].replace('"','') for x in re.findall(regEx,line)[:-1]]
       cost_entry[0] = datetime.strptime(cost_entry[0],"%Y-%m-%d").strftime("%m/%d/%Y")
       #modifications
       try:
           if typ == "s":
               #cost_entry[1] = unicode(category_cid_mapping[cost_entry[1]])
               cost_entry[1] = str(category_cid_mapping[cost_entry[1]])
               cost_entry[6] = cost_entry[6].split(":")[0]
           else:
               cid_regEx = re.compile("%3D([\w\d]+?)(?:&|%26)")
               cid = re.findall(cid_regEx,cost_entry[-1])
               if not len(cid):continue
               cost_entry[1] = cid[0] 
       except Exception as e:
           continue
       #cost_entry[2] = unicode(float(cost_entry[2])/MONEY_DIVISOR)
       cost_entry[2] = str(float(cost_entry[2])/MONEY_DIVISOR)
       if typ == "s":
           formatted.append(cost_entry)
       else:
           formatted.append(cost_entry[:-1])
       #formatted = [[y.encode("utf-8") for y in x] for x in formatted]
    return formatted

def get_adobe_report(period):
    report = getReport.Report(
        USERNAME,
        SECRET,
        reportsuite=REPORTSUITE,
        timeout=5
    )
    report.set_date(period[0],period[1],granularity="day")
    report.set_elements({"id":"trackingcode"},{"id":"product"},{"id":"evar37"})
    report.set_metrics({"id":"cm970_5a4f923455bf1517cb9dbaf5"},{"id":"event305"},{"id":"event306"},{"id":"cm970_5a6516b6cf72d8c7379849a9"})
    response = report.get()
    reponse = _format_report(response)
    return response

def _zerofill(number):
    if(type(number).__name__ == "int"):
        return "0{}".format(number) if number < 10 else number
    else:
        return "0{}".format(number) if len(number) > 1 else number

def _format_report(input):
    response = []
    for date in input["data"]:
        try:
            n_date = datetime.strptime(
                "{}{}{}".format(
                    _zerofill(date["day"]),
                    _zerofill(date["month"]),
                    date["year"]
                ),
                "%d%m%Y"
            )
            for category in date["breakdown"]:
                cid = category["name"]
                for product in category["breakdown"]:
                    pid = product["name"]
                    merch = product["breakdown"][0]["name"]
                    events = product["breakdown"][0]["counts"]
                    response.append(
                        [
                            n_date.strftime("%m/%d/%Y"),
                            cid,
                            events[0],
                            events[1],
                            events[2],
                            events[3],
                            merch,
                            pid
                        ]
                    )
        except Exception as e:
            continue
    return response

def compare_arrays(adobe,google):
    print(adobe)
    print(google)
    response = []
    adobe_hashes = [
        hashlib.md5(
            "{}{}{}{}".format(
                x[0],
                x[1],
                x[6],
                x[7],
            ).encode("utf-8")
        ).hexdigest() for x in adobe
    ]
    print(adobe_hashes)
    for google_row in google:
        hash = hashlib.md5(
            "{}{}{}{}".format(
                google_row[0],
                google_row[1],
                google_row[6],
                google_row[7],
            ).encode("utf-8")
        ).hexdigest()
        print(hash)
        try:
            idx = adobe_hashes.index(hash)
            print(idx)
            a_g = [
                float(adobe[idx][2]),
                float(adobe[idx][3]),
                float(adobe[idx][4]),
                float(adobe[idx][5])
            ]
            b_a = [
                float(google_row[2]),
                float(google_row[3]),
                float(google_row[4]),
                float(google_row[5])
            ]
            z = zip(a_g,b_a)
            if any(list(map(lambda a:a[0]-a[1],z))):
                response.append(
                    [
                        adobe[idx][0],
                        adobe[idx][1],
                        str(round(float(google_row[2])-float(adobe[idx][2]),2)),
                        str(int(google_row[3])-int(adobe[idx][3])),
                        str(int(google_row[4])-int(adobe[idx][4])),
                        str(round(float(google_row[5])-float(adobe[idx][5]),2)),
                        adobe[idx][6],
                        adobe[idx][7]
                    ]
                )
        except Exception as e:
            print(e)
            response.append(google_row)
            continue
    return response

def send_to_adobe(rows,typ="s"):
    request = data_source.DataSource(
        USERNAME,SECRET,
        reportsuite=REPORTSUITE,
        debug=1
    )
    request.set_id(19)
    request.set_job_name("AdWords Cost Import")
    if typ == "s":
        request.set_columns("Date","Tracking Code","Event 250","Event 305","Event 306","Event 307","Evar 37","Product")
    else:
        request.set_columns("Date","Tracking Code","Event 250","Event 305","Event 306","Event 307")
    for row in rows:
        request.set_rows(row)
    request.send()

def save_obj(obj,name):
	import pickle
	with open('./'+ name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
	import pickle
	with open('./' + name + '.pkl', 'rb') as f:
		return pickle.load(f)

def main(client,period):
    ##shopping
    #shopping_data = get_shopping_report(client,SHOPPING_CAMPAIGN_ID,date)
    #save_obj(shopping_data,"test")
    shopping_data = load_obj("test")
    google = format(shopping_data)
    #print(shopping_formatted)
    #response = get_adobe_report(period)
    #save_obj(response,"reporting")
    response = load_obj("reporting")
    adobe = _format_report(response)

    #adobe = [['01/20/2018', 'c_dhlmp_ie_dpcom_00029_98372_BZ_258', '1.31', '330', '25', '0.00', '1962', '1047282763'],['01/20/2018', 'c_dhlmp_ie_dpcom_00029_98372_BZ_258', '1.31', '330', '25', '0.00', '1963', '1047282763']]
    #google = [['01/19/2018', 'c_dhlmp_ie_dpcom_00029_98372_BZ_258', '0.01', '1', '1', '0.00', '1962', '1047282763'],['01/20/2018', 'c_dhlmp_ie_dpcom_00029_98372_BZ_258', '1.19', '229', '25', '0.00', '1963', '1047282763']]

    res = compare_arrays(adobe,google)
    print(res)
    #send_to_adobe(shopping_formatted)
    ##sea/retargeting
    #campaign_data = get_retargeting_report(client,date)
    #campaign_formatted = format(campaign_data,typ="r")
    #send_to_adobe(campaign_formatted,typ="r")
    pass

if __name__ == "__main__":
    #try:
    #    chk_time = datetime.strptime(args.date,"%Y%m%d")
    #except ValueError as e:
    #    print(e)
    (start_date,end_date) = (
        (datetime.now() - timedelta(5)).strftime("%Y-%m-%d"),
        (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
    )
    adwords_client = adwords.AdWordsClient.LoadFromStorage("C:/Python Projects/AdWordsAPI_py3/app/googleads.yaml")
    main(adwords_client,(start_date,end_date))