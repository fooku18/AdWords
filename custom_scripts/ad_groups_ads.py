#!/usr/bin/env python
#coding:UTF-8

import re
from googleads import adwords

#tracking template
template = "https://t23.intelliad.de/index.php?redirect={lpurl}cid%3D###cid###%26_gsp_%3D{_gsp}%26_gspr_%3D{_gspr}%26keyword%3D{keyword}&cl=6373634303236323131303&bm=1&bmcl=9383935373335393432303&cp={campaignId}&ag={adgroupId}&sbm={ifSearch:1}{ifContent:2}&ad={creative}&pl={placement}&bk={keyword}&admt={matchtype}&crmt={matchtype}&f={_iafi}&fi={feedItemId}&crid={_iacr}&ph=1&nw={network}&d={device}&dm={devicemodel}&tg={target}&ap={adposition}&pt={product_partition_id}&at={adtype}&p1={param1}&p2={param2}&ac={aceid}&tgids={targetid}&geoid={loc_physical_ms}&intid={loc_interest_ms}"

#mappings
cid_mapping = {
	"other":"c_dhlmp_se_dpcom_00029_00026_GS_Rest",
	"-4047358871470385303": "c_dhlmp_ie_dpcom_00029_18828_YF_170",
	"7477391641924216366": "c_dhlmp_ie_dpcom_00029_56804_TM_271",
	"-4844290245982195030": "c_dhlmp_ie_dpcom_00029_40257_ND_000",
	"-3692872870547437690": "c_dhlmp_ie_dpcom_00029_67503_EW_559",
	"1630781044279653237": "c_dhlmp_ie_dpcom_00029_82947_KN_808",
	"-823909673284230433": "c_dhlmp_ie_dpcom_00029_28092_YJ_023",
	"-8901225909846585574": "c_dhlmp_ie_dpcom_00029_55024_AK_948",
	"-136928849880388598": "c_dhlmp_ie_dpcom_00029_94955_EY_319",
	"-5914235892932915235": "c_dhlmp_ie_dpcom_00029_73713_DB_932",
	"5791209622805759532": "c_dhlmp_ie_dpcom_00029_35812_IM_984",
	"6085370270382652056": "c_dhlmp_ie_dpcom_00029_24118_WK_573",
	"-7183678771116356049": "c_dhlmp_ie_dpcom_00029_63566_VE_166",
	"-7701278134223972650": "c_dhlmp_ie_dpcom_00029_98372_BZ_258",
	"-730821788104646261": "c_dhlmp_ie_dpcom_00029_42890_ZB_567",
	"-7974890371279108093": "c_dhlmp_ie_dpcom_00029_18904_YX_200",
	"1689639310991627077": "c_dhlmp_ie_dpcom_00029_36599_AW_365",
	"-1319082945867661876": "c_dhlmp_ie_dpcom_00029_29165_CD_712",
	"-135859741832737125": "c_dhlmp_ie_dpcom_00029_66743_MB_225",
	"225849170806580462": "c_dhlmp_ie_dpcom_00029_43334_DA_172",
	"-8991081036712453473": "c_dhlmp_ie_dpcom_00029_16364_MZ_475"
}

provision_mapping = {
	"other":0000000,
	"0.0":995492,
	"0.1":540679,
	"0.2":357563,
	"0.3":28909,
	"0.4":765179,
	"0.5":103130,
	"0.6":828824,
	"0.7":844450,
	"0.8":490459,
	"0.9":559066,
	"1.0":488863,
	"1.1":739929,
	"1.2":914574,
	"1.3":285833,
	"1.4":614155,
	"1.5":283242,
	"1.6":677025,
	"1.7":532670,
	"1.8":757468,
	"1.9":140265,
	"2.0":922150,
	"2.1":518000,
	"2.2":416210,
	"2.3":970142,
	"2.4":266614,
	"2.5":497168,
	"2.6":783593,
	"2.7":988033,
	"2.8":318871,
	"2.9":500697,
	"3.0":802808,
	"3.1":284694,
	"3.2":823597,
	"3.3":313040,
	"3.4":315295,
	"3.5":878244,
	"3.6":42125,
	"3.7":192816,
	"3.8":734610,
	"3.9":601284,
	"4.0":265370,
	"4.1":395024,
	"4.2":309555,
	"4.3":109428,
	"4.4":957075,
	"4.5":23595,
	"4.6":828772,
	"4.7":379166,
	"4.8":86339,
	"4.9":12109,
	"5.0":811785,
	"5.1":29728,
	"5.2":689175,
	"5.3":797839,
	"5.4":220146,
	"5.5":157102,
	"5.6":280356,
	"5.7":910326,
	"5.8":793709,
	"5.9":652389,
	"6.0":659562,
	"6.1":521093,
	"6.2":490269,
	"6.3":667375,
	"6.4":322118,
	"6.5":175113,
	"6.6":210618,
	"6.7":36967,
	"6.8":270369,
	"6.9":833073,
	"7.0":988092,
	"7.1":975734,
	"7.2":976837,
	"7.3":452027,
	"7.4":475651,
	"7.5":199022,
	"7.6":365022,
	"7.7":990858,
	"7.8":611205,
	"7.9":951187,
	"8.0":598406,
	"8.1":667382,
	"8.2":794577,
	"8.3":429139,
	"8.4":883694,
	"8.5":116969,
	"8.6":766534,
	"8.7":520653,
	"8.8":450452,
	"8.9":221832,
	"9.0":674696,
	"9.1":711268,
	"9.2":191433,
	"9.3":563076,
	"9.4":983786,
	"9.5":21330,
	"9.6":553734,
	"9.7":535025,
	"9.8":957893,
	"9.9":95756,
	"10.0":538417,
	"10.1":844515,
	"10.2":41217,
	"10.3":140073,
	"10.4":16692,
	"10.5":887058,
	"10.6":645810,
	"10.7":121535,
	"10.8":110217,
	"10.9":742907,
	"11.0":550003,
	"11.1":673419,
	"11.2":497610,
	"11.3":168747,
	"11.4":916349,
	"11.5":409672,
	"11.6":175232,
	"11.7":826663,
	"11.8":651910,
	"11.9":50552,
	"12.0":494620,
	"12.1":124910,
	"12.2":451378,
	"12.3":487169,
	"12.4":433623,
	"12.5":69572,
	"12.6":623943,
	"12.7":789489,
	"12.8":359522,
	"12.9":798034,
	"13.0":559921,
	"13.1":805227,
	"13.2":470485,
	"13.3":661019,
	"13.4":301375,
	"13.5":961103,
	"13.6":667491,
	"13.7":769363,
	"13.8":773308,
	"13.9":671619,
	"14.0":145994,
	"14.1":75608,
	"14.2":138019,
	"14.3":165760,
	"14.4":198824,
	"14.5":695216,
	"14.6":654260,
	"14.7":923381,
	"14.8":561420,
	"14.9":911184,
	"15.0":29646,
	"15.1":320341,
	"15.2":153501,
	"15.3":505798,
	"15.4":697712,
	"15.5":445688,
	"15.6":978718,
	"15.7":536718,
	"15.8":331068,
	"15.9":718456,
	"16.0":306868,
	"16.1":578661,
	"16.2":640442,
	"16.3":383685,
	"16.4":542978,
	"16.5":664959,
	"16.6":843361,
	"16.7":458823,
	"16.8":908900,
	"16.9":937182,
	"17.0":310241,
	"17.1":629623,
	"17.2":492984,
	"17.3":892609,
	"17.4":384671,
	"17.5":347599,
	"17.6":721655,
	"17.7":359845,
	"17.8":185791,
	"17.9":181078,
	"18.0":717554,
	"18.1":410117,
	"18.2":640571,
	"18.3":96484,
	"18.4":60569,
	"18.5":808313,
	"18.6":843732,
	"18.7":667277,
	"18.8":980445,
	"18.9":961363,
	"19.0":653035,
	"19.1":523289,
	"19.2":673314,
	"19.3":663493,
	"19.4":698124,
	"19.5":440735,
	"19.6":168143,
	"19.7":376552,
	"19.8":185783,
	"19.9":148524,
	"20.0":837335,
	"20.1":188211,
	"20.2":100974,
	"20.3":880250,
	"20.4":83835,
	"20.5":583881,
	"20.6":581,
	"20.7":564835,
	"20.8":239929,
	"20.9":791321,
	"21.0":831744,
	"21.1":135048,
	"21.2":692605,
	"21.3":658528,
	"21.4":643037,
	"21.5":970406,
	"21.6":674915,
	"21.7":850982,
	"21.8":265040,
	"21.9":269048,
	"22.0":793262,
	"22.1":18669,
	"22.2":865005,
	"22.3":322460,
	"22.4":581083,
	"22.5":453431,
	"22.6":339239,
	"22.7":587345,
	"22.8":899379,
	"22.9":326946,
	"23.0":605436,
	"23.1":20742,
	"23.2":266052,
	"23.3":822801,
	"23.4":535600,
	"23.5":799716,
	"23.6":582965,
	"23.7":21847,
	"23.8":716016,
	"23.9":882731,
	"24.0":492560,
	"24.1":24527,
	"24.2":867235,
	"24.3":818175,
	"24.4":621168,
	"24.5":466443,
	"24.6":174504,
	"24.7":930330,
	"24.8":58948,
	"24.9":710296,
	"25.0":146111,
	"25.1":734498,
	"25.2":71300,
	"25.3":865838,
	"25.4":522906,
	"25.5":440359,
	"25.6":916283,
	"25.7":847153,
	"25.8":284711,
	"25.9":977367,
	"26.0":756543,
	"26.1":573088,
	"26.2":780066,
	"26.3":464630,
	"26.4":755991,
	"26.5":731076,
	"26.6":54655,
	"26.7":409910,
	"26.8":633807,
	"26.9":601700,
	"27.0":385756,
	"27.1":575403,
	"27.2":796859,
	"27.3":715260,
	"27.4":950593,
	"27.5":646049,
	"27.6":947629,
	"27.7":128538,
	"27.8":530505,
	"27.9":375225,
	"28.0":622363,
	"28.1":775346,
	"28.2":415153,
	"28.3":321173,
	"28.4":376218,
	"28.5":229172,
	"28.6":366674,
	"28.7":371132,
	"28.8":463970,
	"28.9":232409,
	"29.0":709349,
	"29.1":422226,
	"29.2":93092,
	"29.3":784718,
	"29.4":346667,
	"29.5":979180,
	"29.6":571499,
	"29.7":140169,
	"29.8":132902,
	"29.9":873163,
	"30.0":326575
}

price_mapping = {
	"other":0,
	"niedrig":1,
	"mittel":2,
	"hoch":3
}

PAGE_SIZE = 500

ADGROUP_ID = '46365036856'

class tracking_value_item(object):
	def __init__(self,id):
		self.id = id
	def addAttribute(self,attribute_type,attribute_value):
		if attribute_type == "CUSTOM_ATTRIBUTE_0":
			try:
				t_v = str(float(attribute_value))
			except ValueError:
				t_v = attribute_value
			self.provision = provision_mapping[t_v]
		elif attribute_type == "CUSTOM_ATTRIBUTE_4":
			self.price = price_mapping[attribute_value]
		else:
			self.cid = cid_mapping[attribute_value]
	def getTemplate(self):
		return template.replace("###cid###",self.cid)
	def setParams(self,params):
		self.params = params
	def __str__(self):
		return "{}---{}---{}".format(
				template.replace("###cid###",self.cid),
				str(self.provision) if hasattr(self,"provision") else ":",
				str(self.price) if hasattr(self,"price") else ":"
			)

def getCriterions(client,adgroup_id):
	adgroup_criterion_service = client.GetService(
		'AdGroupCriterionService',version='v201708')
	selector = {
		'fields':[
			'Id','PartitionType','CaseValue','ParentCriterionId','UrlCustomParameters'
		],
		'predicates':[
			{
				'field':'AdGroupId',
				'operator':'EQUALS',
				'values':[
					adgroup_id
				]
			},{
				'field':'CriteriaType',
				'operator':'EQUALS',
				'values':[
					'PRODUCT_PARTITION'
				]
			}
		],
		'paging':{
			'startIndex':0,
			'numberResults':PAGE_SIZE
		}

	}
	result = adgroup_criterion_service.get(selector)
	items = {}
	for biddable_criterion in result["entries"]:
		if hasattr(biddable_criterion,"urlCustomParameters"):
			custom_params = biddable_criterion["urlCustomParameters"]["parameters"]
		else:
			custom_params = None
		criterion = biddable_criterion["criterion"]
		child = str(criterion["id"])
		parent = str(criterion["parentCriterionId"]) if "parentCriterionId" in criterion else None
		cVtype = str(criterion["caseValue"]["type"]) if "caseValue" in criterion else None
		cPtype = str(criterion["partitionType"])
		cVvalue = None
		cVParams = custom_params
		if "caseValue" in criterion:
			if "value" in criterion["caseValue"]:
				cVvalue = str(criterion["caseValue"]["value"])
			else:
				cVvalue = "other"
		items[child] = {
			"parent":parent,
			"ctype":cVtype,
			"ptype":cPtype,
			"value":cVvalue,
			"params":cVParams
		}
	new_tracking_templates = []
	for item in items:
		if items[item]["ptype"] == "UNIT":
			ov = tracking_value_item(item)
			if items[item]["params"]:
				ov.setParams(items[item]["params"])
			ov.addAttribute(items[item]["ctype"],items[item]["value"])
			v = items[item]["value"]
			while items[item]["parent"]:
				pv = items[items[item]["parent"]]["value"]
				if pv:
					ov.addAttribute(items[items[item]["parent"]]["ctype"],items[items[item]["parent"]]["value"])
					v += pv
				item = items[item]["parent"]
			new_tracking_templates.append(ov)
	return new_tracking_templates

def set_criterion_values(client,criterions,adgroup_id):
	adgroup_criterion_service = client.GetService(
		'AdGroupCriterionService',version='v201708')
	
	def build_setter(id,params,trk_tpl):
		return {
			"operator":"SET",
			"operand":{
				"xsi_type":"BiddableAdGroupCriterion",
				"adGroupId":adgroup_id,
				"criterionUse":"BIDDABLE",
				"criterion":{
					"id":id
				},
				"urlCustomParameters":{
					"parameters":params,
					"doReplace":"true"
				},
				"trackingUrlTemplate":trk_tpl
			}
		}

	def build_param(key,val):
		return {
			"key":str(key),
			"value":str(val)
		}

	change_ids = [x.id for x in criterions]
	operations = []
	for criterion in criterions:
		params = []
		if hasattr(criterion,"params"):
			for param in criterion.params:
				#keep intelliad parameters
				if re.search("^ia",param["key"]):
					params.append(build_param(param["key"],param["value"]))
		if hasattr(criterion,"provision"):
			params.append(build_param("gsp",criterion.provision))
		if hasattr(criterion,"price"):
			params.append(build_param("gspr",criterion.price))
		operations.append(build_setter(criterion.id,params,criterion.getTemplate()))
	result = adgroup_criterion_service.mutate(operations)
	print result

def get_categorie_mapping(client):
	constant_data_service = client.GetService(
		"ConstantDataService",version="v201708")

	selector = {
		"predicates":[
			{
				"field":"Country",
				"operator":"EQUALS",
				"values":[
					"DE"
				]
			},
			{
				"field":"BiddingCategoryStatus",
				"operator":"EQUALS",
				"values":[
					"ACTIVE"
				]
			}
		]
	}

	cats = constant_data_service.getProductBiddingCategoryData(selector)
	cat_map = {}
	for cat in cats:
		cat_code = str(cat["dimensionValue"]["value"])
		cat_name = cat["displayValue"][0]["value"]
		if str(cat["dimensionValue"]["type"]) != "BIDDING_CATEGORY_L1":continue
		if not cat_code in cat_map.keys():
			cat_map[cat_code] = cat_name
	return cat_map

def main(client, adgroup_id):
	criterions_list = getCriterions(client,adgroup_id)
	set_criterion_values(client,criterions_list,adgroup_id)

if __name__ == '__main__':
	adwords_client = adwords.AdWordsClient.LoadFromStorage()
	main(adwords_client, ADGROUP_ID)