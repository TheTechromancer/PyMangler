#!/usr/bin/python3
'''
Version 0.1

TODO:

analyze lists, update common numbers

Forget *pend functions and work on capswap, leet functions
*pending should be done in hashcat.  Don't reinvent the wheel

IDEA:
1. compile lists
	a. mangle templates ('lws', 'wd', etc...)
	b. input words
	c. if mangle templates include more than 1 word, sort input list by (frequency chunk appears in multi-word passwords)
2. take mangle templates and create generator function for each one
3. add generators to list
4. loop:
	while 1:
		try:
			for g in list_of_generators:
				print(next(g))
		except StopIteration:
			list_of_generators.remove(g)
			if not list_of_generators:
				break
5. REMEMBER: when making mangle function, iterate through charsets with broader curves first
   (e.g. for the simple mask 'wd', iterate like 'w1-d1', 'w2-d1', 'w3-d1', etc...)

When it comes to cracking passwords with 2 or more words:
	it is necessary to discard ones with lower occurrences
	formula would look like:
		discard all <2 occurrences, shortened_length = (.05 / (number_of_words_in_pass - 1)) * wordlist_length
		shortened_list = wordlist[:shortened_length]

IDEA2:
when parsing:
	1. load wordstat object if specified
	2. assign each significant part of object to variables
	3. overwrite each variable with other argument lists, if they exist
	4. end result: analyzed wordlist + custom overrides

'''

simple_mangling = False
try:
	from wordstat import ListStat
except ImportError:
	simple_mangling = True

import pickle
import string
import itertools
from time import sleep
#from signal import signal, SIGPIPE, SIG_DFL
from sys import argv, exit, stdin, stderr
from argparse import ArgumentParser, FileType, ArgumentError

# signal(SIGPIPE,SIG_DFL) # don't ignore SIGPIPE (prevents broken pipe error)



### DEFAULTS - FEEL FREE TO MODIFY, CAREFULLY ###

#simple_nums = []
#for i in range(1,5):
#	simple_nums.extend([''.join(n) for n in itertools.product(string.digits, repeat=i)])
#simple_nums = simple_nums[:3200]
# top 2000 numbers from linkedin
simple_nums = ['1','2','3','4','123','0','7','5','12','8','11','01','9','10','6','13','22','23','00','21','99','77','09','1234','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','69','88','19','33','08','14','24','07','17','25','20','15','18','55','02','16','27','05','06','03','2009','28','04','26','66','007','44','78','30','29','2008','31','87','89','79','76','34','100','82','75','86','45','84','83','85','50','81','56','98','67','32','72','74','2000','73','80','68','57','42','001','2007','65','54','64','71','90','111','777','12345','52','40','63','58','35','2006','47','70','59','143','53','62','51','97','60','2005','321','101','61','48','92','95','96','49','43','1980','91','1984','666','37','36','1982','1985','46','2004','38','1983','1987','1981','41','1986','93','786','2001','2003','94','2002','1978','1979','123456','999','39','1976','1975','1977','333','1974','1988','1973','1969','1972','1970','1989','1971','456','1968','888','1990','1967','1964','1965','1966','555','1963','1960','000','222','1962','1991','789','1961','1957','1959','1999','911','1958','420','1956','1212','1998','1992','1955','1954','1111','1000','200','1010','1997','234','1995','1953','121','1996','1952','1950','1993','1994','112','1313','1951','500','1947','125','1948','1949','4321','444','108','987','300','110','345','135','009','124','7777','247','711','1122','311','212','1945','6969','120','102','002','369','1946','0000','9999','147','159','1001','128','4444','2112','113','213','003','8888','008','211','103','011','316','127','1011','1012','117','122','2222','105','123456789','246','1210','201','210','411','1944','010','1020','313','567','126','104','109','1221','314','214','012','357','400','312','2323','520','150','2121','098','812','115','1942','1024','131','129','107','1213','1943','118','250','1004','2468','1123','168','114','678','119','005','187','0101','1225','1211','900','3000','310','600','106','1205','323','1209','223','2525','1023','1208','182','512','1008','360','132','215','303','5555','1007','0001','116','1204','1919','1013','202','1231','1206','890','1224','1214','1215','225','1207','320','1025','315','800','1940','1941','521','130','221','1102','747','1108','220','1104','325','3333','1230','137','1022','1029','1414','317','1201','1107','412','1203','1223','0123','006','1021','217','1105','2424','1202','421','1031','808','1109','133','1112','1103','1015','1218','216','145','1121','510','5150','1314','1002','700','004','1220','511','1005','0909','1028','144','1911','318','1234567','1106','1217','1017','1228','365','301','501','1939','54321','350','227','714','1014','231','1216','1003','0808','1812','1018','1101','218','224','1120','1027','1026','1515','2211','1016','151','410','619','1006','612','415','1227','1124','1030','1125','134','219','525','1127','1357','327','1818','206','1717','1009','1219','613','712','2345','1019','235','256','1701','180','141','611','203','1226','713','138','0102','205','909','1128','228','1910','324','626','912','5678','1912','155','199','258','721','1229','1938','013','209','413','0711','811','2310','505','0911','226','727','322','515','330','610','157','328','2311','156','198','1310','232','423','242','654','1200','0505','1066','305','5000','0707','707','717','1937','5050','12345678','1130','2210','1126','1905','1129','513','1908','1410','0202','153','1920','0809','2212','171','710','1402','1412','6666','1936','818','1906','425','523','1312','207','723','963','2512','1411','910','326','0303','1903','427','1907','142','2312','831','2510','169','2410','136','1311','208','331','319','245','0311','139','2412','204','414','401','2727','424','422','3030','1110','140','9876','450','1810','197','1616','0404','1512','416','623','1928','177','0812','813','0506','1900','240','621','302','916','1510','810','514','0007','419','2511','0110','417','531','925','190','718','0912','426','2411','230','233','308','237','1305','0204','329','1492','0411','625','1100','0811','1904','750','175','0405','1308','0708','1935','516','0512','0606','828','181','0305','616','152','1222','517','1307','2810','518','0910','913','2110','923','0511','1610','2711','522','1711','248','1914','2610','430','0407','0987','0408','0412','0508','1925','404','1930','720','1909','1712','1113','0210','021','1511','0104','0507','1710','921','123123','432','2309','929','1309','0108','0709','1117','0815','2911','0608','0304','0612','0609','722','0406','189','1929','823','753','149','160','731','725','0810','615','4711','2580','2626','0611','1923','0203','1408','0205','1612','0509','654321','0510','901','528','1508','1901','815','624','617','163','255','0105','1302','1611','0211','154','0308','1811','1927','229','428','2105','146','0208','618','1405','0312','2104','0212','236','2103','0310','1505','2710','715','2828','821','527','158','1304','1902','195','0103','2109','1933','1404','4545','243','0306','429','307','530','309','1407','918','1921','0607','1409','0207','524','257','1303','418','167','1306','2611','919','3010','2812','304','2305','724','0309','922','2106','238','2304','1932','2107','914','161','0307','915','2205','2308','620','0206','2811','165','148','650','0109','1406','241','306','927','2204','622','2208','2108','519','1934','3110','3003','614','0410','55555','1115','0409','188','0209','2612','1503','741','2910','0214','0106','543','3112','252','1114','1301','0712','1509','2301','1804','1504','239','2712','928','0107','0610','1118','1922','917','716','2202','355','2501','529','2307','1805','2209','817','196','166','728','628','172','3011','0710','173','816','729','178','185','2505','822','3232','1502','1808','1403','3006','454','4567','1604','0805','1331','2303','951','814','1500','1704','1705','191','1401','1809','251','023','627','1369','920','526','852','269','550','2306','13579','170','1506','2206','1432','183','2207','1116','1926','825','2509','924','1501','1602','0401','820','1609','7890','1803','0905','2408','2244','630','2101','1800','1776','1924','0704','1802','6789','455','2508','3012','1703','192','254','504','0804','926','1608','2504','824','787','2233','601','801','1245','1707','1605','2912','0803','244','726','262','1801','2407','2201','1702','164','0901','0904','2405','343','409','629','1709','347','1119','0908','2406','2203','0112','405','2404','1917','253','0801','0402','1324','1507','765','0907','2409','0501','440','1603','989','2507','819','2506','2401','0903','0902','356','1337','719','1806','1931','1918','0802','2102','337','179','2805','1708','3001','0502','2601','2111','0906','162','502','737','701','0503','503','1606','2709','4040','2123','280','2030','826','186','408','0806','174','730','9000','1235','3105','4242','2808','351','9090','1601','0504','2503','2302','0301','11111','176','827','930','3434','451','275','876','2804','3108','0302','402','3131','2801','288','2604','2904','2606','1807','407','1607','0604','0201','0705','249','2021','193','0601','0701','606','3004','1415','2905','0703','2403','1706','0602','289','3456','702','974','0603','2909','2901','1300','990','299','442','279','2502','0605','5683','2701','2929','281','015','2402','0403','757','972','265','2705','5656','829','268','340','277','022','335','509','0807','014','2803','194','2809','2704','2324','270','2608','267','2609','2707','0420','3008','0702','0321','3009','259','1913','2806','334','0706','830','4000','3636','3107','271','2802','2605','184','3005','278','017','069','380','2703','260','2100','0011','273','486','459','263','403','406','696','1040','358','272','0923','020','282','266','7878','3103','2122','3101','2708','2603','342','123321','667','261','805','458','264','2500','1881','2906','2907','1789','1233','024','1321','998','2908','2903','1379','508','3007','112233','2607','545','1236','1916','602','767','2602','341','540','8989','285','2807','5252','770','375','1323','445','549','381','099','8080','1425','286','703','5454','0111','1320','1600','019','336','1326','971','8899','332','287','579','018','0421','0921','0913','1133','3535','016','507','283','905','290','0925','0823','0317','1325','0213','025','1423','111111','0315','0220','1177','1199','604','1234567890','0313','1290','469','354','359','457','377','535','2706','2526','699','1453','1516','603','1821','2025','0714','1289','0523','0825','0915','0813','903','2425','379','556','1188','565','4747','298','0521','353','969','7788','468','2255','850','0525','908','1256','1080','975','0413','1618','506','0415','0623','1718','1250','0423','0822','0513','2702','609','0522','291','0824','2050','383','0125','973','0425','1315','802','1248','1400','0922','373','0515','1688','0613','0821','0927','284','0424','344','0818','363','348','902','0314','0713','704','274','978','027','276','2022','1138','077','295','352','1819','102030','0721','431','399','546','778','1050','0816','575','0215','338','339','997','0723','0428','0330','898','0416','0924','0918','0422','0621','1421','0625','435','297','5151','0323','0324','803','1416','0316','1232','1420','0926','0622','904','0814','0325','2288','9898','0916','981','0318','0217','0124','669','0624','0218','0524','541','0914','050','0219','1322','1525','033','1428','0417','0831','1617','0828','453','346','642','030','0121','907','3737','390','889','1915','0426','386','0128','1317','0427','090','0216','433','1520','90210','2277','4141','0717','1155','452','2200','349','690','809','605','645','0414','0917','4455','9900','0626','0919','388','0722','980','0528','0519','1430','0322','367','636','0514','0520','7272','0326','0516','465','1269','551','705','0331','0928','1820','0077','532','0518','986','0929','7575','0517','0618','1422','3344','292','991','585','0429','0419','0327','434','0526','366','293','0826','031','0129','378','954','0920','0614','4848','0430','0126','0615','0418','294','0527','0531','988','560','1280','0122','393','561','569','5566','2332','899','709','5757','1144','396','0820','1254','1327','2125','296','2325','0628','1478','480','389','608','0819','0127','1288','3113','656','976','0817','0329','633','7000','0727','0529','708','804','0930','478','996','607','361','775','0715','055','689','121212','1437','0120','0725','1723','0320','0731','1316','1418','745','0221','0829','0616','883','0630','1318','0228','0319','2469','441','159753','0328','773','0724','7007','4343','0728','437','0627','1424','1328','533','732','0786','489','1258','8181','0620','5858','1523','985','1255','1278','101010','0224','467','4200','00000','484','370','371','0827','6000','368','944','3210','477','1530','0223','979','878','2300','2223','1521','1822','1824','6868','2327','1099','945','0629','1620','443','788','2326','977','1243','686','562','6464','77777','0716','3838','706','385','3141','0619','0225','571','0830','2040','3579','1330','733','666666','2124','1098','983','475','464','2728','447','0113','0530','7474','387','028','781','771','578','0719','0115','026','0729','499','0617','0131','364','1721','8787','1417','460','474','631','756','6060','982','687','586','0726','6565','845','1055','1239','448','1275','564','589','599','2213','0718','488','2627','534','470','691','955','2113','735','595','2023','1899','799','131313','1298','1625','740','1257','949','760','2024','646','580','1350','0117','8000','8484','6996','806','1299','632','1825','1623','362','1319','566','2552','537','1441','5353','1431','0720','538','1340','7777777','751','563','040','950','1150','0130','668','1166','547','984','080','554','785','6363','588','0227','6767','2400','734','051','490','2426','542','7979','675','1237','1358','029','462','372','1771','1069','780','1888','640','1823','2131','906','1621','557','755','762','807','671','0226','485','651','897','676','1722','880','568','590','382','637','959','577','1260','070','965','544','2356','479','797','3377','4488','1729','660','993','657','742','1517','1134','3939','9988','7070','398','987654321','376','1700','2314','1725','0114','881','466','7676','665','2369','1727','1088','6262','536','091','436','1522','552','2120','776','956','384','798','032','1427','395','0116','7373','877','957','7171','1187','8585','1524','99999','743','858','995','1622','696969','635','4949','0118','768','1359','848','495','1345','482','661','1720','832','449','842','1624','875','655','570','933','3123','8008','2829','961','088','1244','1180','573','3366','1169','966','471','887','487','559','8282','891','6699','4646','1518','2442','1724','0730','1828','931','1488','833','7410','010203','374','1238','688','473','071','1247','391','1329','1356','576','967','970','1265','1551','1277','1628','856','20000','864','1728','1285','840','553','783','476','643','1090','647','463','045','000000','964','1056','1060','2266','9696','481','397','10000','4123','992','3211','953','1426','461','6688','748','1469','1434','679','439','8686','1388','1045','2215','2600','1259','749','2628','483','1342','1355','744','2127','438','1827','0119','2313','680','968','446','2315','2321','939','1836','472','0013','1526','752','652','1266','868','1284','937','2930','1077','1830','941','769','766','838','879','572','1287','2530']
# top 19 specials from linkedin
common_specials =	['@','!','.','_','*','#','$','-',' ','&','+','/','%','?','!!',',','**','=','$$']

# most common masks from linkedin
# 'wds' == word + digit + special
'''
             word-number:  41.1%  (24663118)
                    word:  23.4%  (14040483)
                  number:  19.6%  (11723886)
             number-word:  5.0%  (2982894)
        word-number-word:  3.2%  (1940231)
      number-word-number:  1.4%  (868778)
     word-number-special:  1.2%  (717326)
     word-special-number:  1.2%  (700550)
 word-number-word-number:  0.8%  (480862)
       word-special-word:  0.7%  (403672)
            word-special:  0.4%  (266352)
'''
common_masks = [
	's',
	'd',
	'w',
	'wd',
	'dw',
	'ws',
	'dwd',
	'wds',
	'wsd'
	#'dws',
	#'swd',
	#'dsw',
	#'wdw'
	#''
]

# drop the bottom 10% of entries from wordstat file
wordstat_coverage = 90

# max mutations for each word
max_leet	= 256
max_cap		= 512

# expected average hashes per second
hashrate = 1000000

# target time to finish in hours
finish_time = 24 # 168 == 1 week

# don't change unless you get errors
wordlist_encoding = 'utf-8'


### INIT CODE - DO NOT TOUCH ###

simple_chartypes = {
	'd': 1,
	's': 8,
	'w': 6
}


### CLASSES ###


class Mutator():

	def __init__(self, inlist, perm=0, leet=True, cap=True, capswap=True, multiplier=1):

		# "leet" character swaps - modify as needed.
		# Keys are replaceable characters; values are their 1337 replacements.
		self.leet_common = {
			'a': ['@'],
			'A': ['@'],
			'e': ['3'],
			'E': ['3'],
			'i': ['1'],
			'I': ['1'],
			'o': ['0'],
			'O': ['0'],
			's': ['$'],
			'S': ['$'],
		}

		self.leet_all = {
			'a': ['4', '@'],
			'A': ['4', '@'],
			'b': ['8'],
			'B': ['8'],
			'e': ['3'],
			'E': ['3'],
			'i': ['1'],
			'I': ['1'],
			'l': ['1'],
			'L': ['1'],
			'o': ['0'],
			'O': ['0'],
			's': ['5', '$'],
			'S': ['5', '$'],
			't': ['7'],
			'T': ['7']
		}

		# max = maximum mutations per word
		# cur - used for carrying over unused mutations into next iteration
		self.max_leet		= max(1, min(int(max_leet * multiplier), max_leet))
		self.max_cap		= max(1, min(int(max_cap * multiplier), max_cap))
		self.cur_leet		= 0
		self.cur_cap		= 0

		# TODO - truncate wordlist if mask includes more than one word
		self.inlist			= inlist

		self.perm_depth		= perm
		self.do_leet		= leet
		self.do_capswap		= capswap
		self.do_cap			= cap or capswap


	def gen(self):
		'''
		run mangling functions on wordlist
		'''

		for word in self.cap(self.leet(self.perm(self.inlist))):
			yield word


	def perm(self, inlist, repeat=True):
		'''
		takes:		iterable containing words
		yields:		word permutations ('pass', 'word' --> 'password', 'wordpass', etc.)
		'''

		if self.perm_depth > 1:

			words = []

			for word in inlist:
				words.append(word)
			
			for d in range(1, self.perm_depth+1):
				if repeat:
					for p in itertools.product(words, repeat=d):
						yield ''.join(p)

				else:
					for p in itertools.permutations(words, d):
						yield ''.join(p)
		else:
			for word in inlist:
				yield word


	def cap(self, inlist):
		'''
		rockyou.txt
		output from alpha chunks only
		index 	cap_count
		0:		554766
		-1:		49776
		2:		45958
		1:		42566
		3:		39477
		-2:		36318
		-3:		30583
		4:		29684
		-4:		18056
		5:		14206
		-5:		8622
		6:		6474
		-6:		3605
		7:		2266
		-7:		1374
		8:		720
		-8:		286
		9:		186
		-9:		122
		10:		94
		-10:	59
		11:		36
		-11:	29
		12:		22
		13:		16
		-12:	16


		'''
		for word in inlist:

			if self.do_cap:

				self.cur_cap += self.max_cap

				for r in self._cap(word):
					self.cur_cap -= 1
					yield r
					if self.cur_cap <= 0:
						break

			else:
				yield word





	def leet(self, inlist):

		for word in inlist:

			if self.do_leet:

				self.cur_leet += self.max_leet

				results = [] # list is almost 4 times faster than set
				num_results = 0

				gen_common = self._leet(word, swap_values=self.leet_common)
				for r in gen_common:
					if not r in results:
						if self.cur_leet <= 0:
							break
						results.append(r)
						self.cur_leet -= 1
						yield r


				gen_sparse = self._leet(word, swap_values=self.leet_all, passthrough=False)
				for r in gen_sparse:
					if not r in results:
						if self.cur_leet <= 0:
							break
						results.append(r)
						self.cur_leet -= 1
						yield r


				self.cur_leet += (self.max_leet - len(results))

				results = []

			else:
				yield word




	def _cap(self, word, swap=True):
		'''
		takes:		iterable containing words
					passthrough: whether or not to yield unmodified word
		yields:		case variations (common only, unless 'all' is specified)
		'''

		# set used to prevent duplicates
		results = set()
		results.add(word)
		results.add(word.lower())
		results.add(word.upper())
		results.add(word.swapcase())
		results.add(word.capitalize())
		results.add(word.title())

		results = list(results)
		for r in results:
			yield r

		if self.do_capswap:

			# oneliner which basically does it all
			# TODO: change to emulate leet function with common and less common caps
			for r in map(''.join, itertools.product(*zip(word.lower(), word.upper()))):
				if not r in results:
					results.append(r)
					yield r



	def _leet(self, word, swap_values=None, passthrough=True):
		'''
		takes:		iterable containing words
					swap_values: dictionary containing leet swaps
					passthrough: whether or not to yield unmodified word
		yields:		leet mutations, not exceeding max_results per word
		'''

		if not swap_values:
			swap_values = self.leet_all

		if passthrough:
			yield word

		swaps = []
		word_length = len(word)

		for i in range(word_length):
			try:
				for l in swap_values[word[i]]:
					swaps.append((i, l))

			except KeyError:
				continue

		num_swaps_range = range(len(swaps))
		word_list = list(word)


		for num_swaps in num_swaps_range:

			for c in itertools.combinations(num_swaps_range, num_swaps+1):

				try:

					new_word = word_list.copy()
					already_swapped = []

					for n in c:
						assert not swaps[n][0] in already_swapped
						new_word[swaps[n][0]] = swaps[n][1]
						already_swapped.append(swaps[n][0])

					yield ''.join(new_word)

				except AssertionError:
					continue



class Multiplier():

	def __init__(self, inlist, multiplier=1):

		self.inlist			= inlist
		self.num_results	= max(1, int(len(inlist) * multiplier))

	def gen(self):

		for i in self.inlist:
			self.num_results -= 1
			if self.num_results >= 0:
				yield i





class Concatenator():

	#def __init__(self, w_list, m_list=None, d_list=None, s_list=None, multiplier=1):
	def __init__(self, lists, perm, leet, cap, capswap):

		# TODO: add hashcat rule functionality
		self.lists 			= lists

		self.perm			= perm
		self.leet			= leet
		self.cap			= cap
		self.capswap		= capswap

		self.gen_functions	= {
			'w': Mutator,
			'd': Multiplier,
			's': Multiplier
		}


	def gen(self, chunk=None):
		'''
		(o_o)

		'''

		if chunk is None:
			chunk = self.lists

		if len(chunk) == 1:
			chunk = chunk[0]
			chartype, _list, listsize, multiplier = chunk
			if chunk[0] == 'w':
				for c in self.gen_functions[chartype](_list, perm=self.perm, leet=self.leet, cap=self.cap, capswap=self.capswap, multiplier=multiplier).gen():
					yield c
			else:
				for c in self.gen_functions[chartype](_list, multiplier).gen():
					yield c

		else:
			for c1 in self.gen(chunk[:-1]):
				chartype, _list, listsize, multiplier = chunk[-1]
				if chartype == 'w':
					for c2 in self.gen_functions[chartype](_list, perm=self.perm, leet=self.leet, cap=self.cap, capswap=self.capswap, multiplier=multiplier).gen():
						yield c1 + c2
				else:
					for c2 in self.gen_functions[chartype](_list, multiplier).gen():
						yield c1 + c2



class MaskInfo():

	def __init__(self, total_possible, total_actual, multiplier, word_multiplier, chunk_info):

		self.total_possible		= total_possible
		self.total_actual		= total_actual
		self.multiplier			= multiplier
		self.word_multiplier	= word_multiplier

		self.coverage			= total_actual / total_possible * 100

		# tuple in form ( chartype, max_len, gen_func )
		self.chunk_info			= chunk_info



class Overseer():
	# Overseer(options.words, options.masks, options.numbers, options.specials, options.per_second,\
	#		options.time, options.permutations, options.leet, options.capital, options.capswap)
	def __init__(self, words, masks=common_masks, numbers=simple_nums, specials=common_specials, pps=hashrate, \
		target_time=finish_time, perm=0, leet=False, cap=False, capswap=False):

		self.masks			= masks
		self.words			= words
		self.numbers		= numbers
		self.specials		= specials
		self.pps			= pps
		self.target_time	= target_time
		self.perm			= perm
		self.leet			= leet
		self.cap			= cap
		self.capswap		= capswap

		if self.leet:
			self.leet_size	= max_leet
		else:
			self.leet_size	= 1
		if self.capswap:
			self.cap_size	= max_cap
		elif cap:
			self.cap_size	= 5
		else:
			self.cap_size	= 1

		self.lists			= {
			'w': words,
			'd': numbers,
			's': specials
		}



		self.masks.sort(key=lambda x: self._mask_complexity(x))

		self.num_masks		= len(masks)
		self.total_desired	= int(pps * target_time * 60 * 60)
		self.per_mask_limit	= int(self.total_desired / self.num_masks)

		self.mask_info		= []

		self._calc_multiplier()


	def start(self):

		'''
		for minfo in self.mask_info:
			for chunk in minfo.adjusted_lists:
				for g in chunk[2]:
					print(g)
		'''
		for minfo in self.mask_info:
			c = Concatenator(minfo.chunk_info, self.perm, self.leet, self.cap, self.capswap)
			for p in c.gen():
				print(p)



	def _calc_multiplier(self):
		'''
		step 1:
			total_desired
			find target number of words (pps * target_time_in_seconds)
		step 2:
			list_sizes
			find total entries in each of the following lists: 'w', 's', 'd'
		step 3:
			mask_totals = {
				set(): total
			}
			mask_totals[set(list(mask))] = total ...

			find total number of possibilities for each mask (list_length1 * list_length2 * ...)
		step 4:
			per_mask_limit = (total_desired / num_masks)
		step 5:
			sort masks: shorter first
			limit number of tries to per_mask_limit
			if per_mask_limit > mask_total, split remaining attempts across all other masks
		step 6:
			return dictionary in form:
			multipliers {
				set(list(mask)): max_attempts
			}

		then, for each mask:
			step 1:
				total_methods
				add each unique mutation method (e.g. cap + leet + append_num = 3) (same as mask_len + num_mutations)
			step 2:
				find multiplier for each method (e.g. leet*=256, cap*=512, append_num*=3200)
			step 3:
				multiplier = ( total_desired / (wordlist_length * multiplier1 * multiplier2 ...) ) ** (1 / total_methods)
				overwrite multipliers[mask] with multiplier
			step 4:
				output resulting wordlist and associated hashcat rules
				add hashcat command to script

		in summary:
			each mask must have own source wordlist and hashcat rules
			script is created that uses a separate hashcat command to crack each mask
		'''

		

		# print('\nTOTAL_DESIRED: {:,}'.format(self.total_desired))
		# print('per_mask_limit: {:,}\n'.format(self.per_mask_limit))

		# format is:
		# mask: (total_possible, total_actual, multiplier)
		extra_attempts = 0

		if self.leet:
			leet = max_leet
		else:
			leet = 1
		if self.capswap:
			capswap = max_cap
		elif self.cap:
			capswap = 5
		else:
			capswap = 1

		for mask in self.masks:
			self.num_masks -= 1

			num_words = mask.count('w')
			mlen = len(mask)

			# +1 for each exponential mutation - including wordlist, if mask includes more than one word
			# keep word_mutations (such as leet & capswap) separate, since they're required to compute chartype-specific number of attempts
			num_word_mutations = (1 if self.leet_size > 1 else 0) + (1 if self.cap_size > 1 else 0)
			num_pend_mutations = mlen - num_words

			# print('NUM_WORD_MUTATIONS: {}'.format(num_word_mutations))
			# print('NUM_PEND_MUTATIONS: {}'.format(num_pend_mutations))

			num_mutations = max(1, num_word_mutations + num_pend_mutations)

			total_possible = 1
			for chartype in mask:
				if chartype == 'w':
					total_possible *= len(self.lists[chartype]) * self.leet_size * self.cap_size
				else:
					total_possible *= len(self.lists[chartype])

			# print('NUM_MUTATIONS: {}'.format(num_mutations))
			# print('TOTAL_POSSIBLE: {:,}'.format(total_possible))

			multiplier = (self.per_mask_limit / total_possible) ** (1 / num_mutations)

			# print('multiplier: {}'.format(multiplier))

			try:
				word_multiplier = multiplier ** (num_word_mutations / num_words)
			except ZeroDivisionError:
				word_multiplier = multiplier

			# print('WORD_MULTIPLIER: {}'.format(word_multiplier))

			total_actual = 1

			# holds info for each chunk
			# ( chartype, list, listsize, multiplier )
			chunk_info = []
			
			for chartype in mask:
				if chartype == 'w':
					listsize = max(1, min(int(len(self.lists[chartype]) * word_multiplier * self.leet_size * self.cap_size),\
					(len(self.lists[chartype]) * self.leet_size * self.cap_size)))
				else:
					listsize = max(1, min(int(len(self.lists[chartype]) * multiplier), len(self.lists[chartype])))
				
				chunk_info.append( (chartype, self.lists[chartype], listsize, multiplier) )

				total_actual *= listsize	

			# print('TOTAL_ACTUAL: {:,}\n'.format(total_actual))

			total_actual = min(int(total_actual), total_possible)

			self.mask_info.append( MaskInfo(total_possible, total_actual, multiplier, word_multiplier, chunk_info) )

			extra = self.per_mask_limit - total_possible
			if extra > 0 and self.num_masks > 0:
				# print('EXTRA +{}'.format((extra / self.num_masks)))
				self.per_mask_limit += int(extra / self.num_masks)



	def print_job_stats(self, confirm=True):

		if not self.mask_info:
			self.start()

		stderr.write('\nw = word\nd = digit\ns = special\n')
		stderr.write('\n{:>13}{:>43}{:>25}\n'.format('Mask', 'Attempts (approx.)', 'Time'))
		stderr.write('=================================================================================\n')

		actual_attempts = 0

		#for mask in self.masks:
		for minfo in self.mask_info:
			actual_attempts += minfo.total_actual
			
			hours = '{:.3f} hours'.format((minfo.total_actual / self.pps) / 3600)
			attempts = '{:,}'.format(minfo.total_actual)
			
			print_chartypes = []

			for e in minfo.chunk_info:
				print_chartypes.append('{}: {:,}\n'.format(e[0], e[2]))

			stderr.write('{:>10}{:>35,} ({:7.3f}%){:>25}\n'.format(''.join([i[0] for i in minfo.chunk_info]), minfo.total_actual, minfo.coverage, hours))
			for chartype in print_chartypes:
				stderr.write("{:>13} {}".format('|- ', chartype))
			stderr.write('\n')

		nm = '{} masks'.format(len(self.masks))
		hours = '{:.3f} hours'.format((actual_attempts / self.pps) / 3600)
		attempts = '{:,} attempts'.format(int(actual_attempts))

		stderr.write('\n=================================================================================\n')
		stderr.write('{:>16}{:>40}{:>25}\n'.format(nm, attempts, hours))

		if confirm:
			stderr.write("\n Press CTRL+C to Cancel.  Starting in 5 seconds.\n\n")
			#r = input("\n Is this ok? (Y/n)\n ")
			#assert r.lower().startswith('y') or not r, "Operation cancelled"
			sleep(5)


	def _mask_complexity(self, mask, word_multiplier=1):
		c = 1
		for char in mask:
			c *= len(self.lists[char])
			if char == 'w': c *= self.leet_size * self.cap_size
		return c






### FUNCTIONS ###



def gen_from_file(i, max_lines=None):
	'''
	takes:		filename
	check:		function (returning true or false) which checks validity of each line
	purpose:	simple generator function
	'''

	try:

		if type(i) != str:
			for e in i:
				line = e.strip('\r\n')
				if line: yield line

		else:
			f = open(i, mode='rb')
			n = 0

			while 1:

				line = f.readline()

				try:

					if type(line) == bytes:
						line = line.decode(encoding=wordlist_encoding)

					if (max_lines and n > max_lines) or not line:
						break

					line = line.strip('\r\n')
					if line: yield line

				except (UnicodeDecodeError, AssertionError):
					continue
				finally:
					n += 1

	except FileNotFoundError:
		raise AssertionError("File '{}' not found.".format(i))
	except TypeError:
		raise AssertionError("Variable in gen_from_file not iterable")




def list_from_file(f, max_lines=None):

	return [line for line in gen_from_file(f, max_lines)]


def obj_from_file(f):

	with open(f, 'rb') as p:
		return pickle.load(p)





if __name__ == '__main__':

	### ARGUMENTS ###

	parser = ArgumentParser(description="Mangle wordlist using traditional methods, or syllable-like mutations")

	parser.add_argument('-l', '--loadfile',			type=obj_from_file,									help="Savefile from wordstat.py", metavar='FILE')
	parser.add_argument('-p', '--percent',			type=int,			default=wordstat_coverage,		help="Percent coverage from wordstat file: default {}".format(wordstat_coverage), metavar='INT')
	parser.add_argument('-pps', '--per-second',		type=int,			default=hashrate,				help="Expected hashrate - used for limiting time spent on complex masks: default {}".format(hashrate), metavar='INT')
	parser.add_argument('-t', '--time',				type=int,			default=finish_time,			help="Target time to finish in hours: default {}".format(finish_time), metavar='INT')
	parser.add_argument('-hc', '--hashcat',																help="Use hashcat rules to maximize efficiency", metavar='DIR')

	parser.add_argument('-w', '--words',			type=list_from_file,	default=None,				help="File containing words", metavar='FILE')
	parser.add_argument('-n', '--numbers',			type=list_from_file,	default=simple_nums,		help="File containing numbers: e.g. '7', '123', '1986', etc.", metavar='FILE')
	parser.add_argument('-s', '--specials',			type=list_from_file,	default=common_specials,	help="File containing special characters: e.g. '#', '!!!', '??', etc.", metavar='FILE')
	parser.add_argument('-m', '--masks',			type=list_from_file,	default=common_masks,		help="File containing simple masks: e.g. 'wds' (word-digit-special)", metavar='FILE')

	parser.add_argument('-L',	'--leet',			action='store_true',								help="All possible 1337 combinations: w0rd")
	parser.add_argument('-c',	'--capital',		action='store_true',								help="Common caps variations: Word, word, WORD")
	parser.add_argument('-C',	'--capswap',		action='store_true',								help="All possible case combinations: wOrD")
	parser.add_argument('-P',	'--permutations',	type=int,				default=1,					help="Max times to combine words (careful! exponential)", metavar='INT')

	parser.add_argument('-mm', '--mask-max',		type=int,											help="Maximum masks to take as iput", metavar='INT')
	parser.add_argument('-wm', '--word-max',		type=int,											help="Maximum words to take as input", metavar='INT')
	parser.add_argument('-nm', '--number-max',		type=int,											help="Maximum numbers to take as input", metavar='INT')
	parser.add_argument('-sm', '--special-max',		type=int,											help="Maximum specials to take as input", metavar='INT')
	parser.add_argument('-y', '--no-confirm',		action='store_true',								help="Don't prompt for confirmation")

	try:

		options = parser.parse_args()

		# print help if no arguments and no pipe to stdin
		if stdin.isatty() and len(argv) < 2:
			parser.print_help()
			exit(2)


		if options.words is None:
			options.words = [l.decode().strip('\r\n') for l in stdin.buffer.readlines()]

		# parse file from wordstat.py
		if options.loadfile and not simple_mangling:

			l = options.loadfile
			p = options.percent

			# override lists loaded from wordstat by manually specified ones, if they exist

			if not options.masks:
				options.masks	= list(l.trim(l.simple_masks, p, l.total, max_results=options.mask_max))

			for pos in l.chunks:
				for char in l.chunks[pos]:

					# check character set
					if not options.words and char & 6 > 0:
						options.words		= list(l.trim(l.chunks[pos][char], p, l.chunk_total[pos][char], max_results=options.word_max))

					elif not options.numbers and char == 1:
						options.numbers		= list(l.trim(l.chunks[pos][char], p, l.chunk_total[pos][char], max_results=options.number_max))

					elif not options.specials and char == 8:
						options.specials	= list(l.trim(l.chunks[pos][char], p, l.chunk_total[pos][char], max_results=options.special_max))

					# clear dictionary to save memory
					l.chunks[pos][char] = None
			l = None


		assert options.words, "Please specify wordlist (-w)"

		# def _calc_multiplier(masks, words, numbers, specials, pps, target_time, leet=1, capswap=1, confirm=True):
		# _calc_multiplier( options.masks, options.words, options.numbers, options.specials, options.per_second, options.time,\
		#	(max_leet if options.leet else 1), (max_cap if options.capswap else 5), (not options.no_confirm) )

		o = Overseer(options.words, options.masks, options.numbers, options.specials, options.per_second,\
			options.time, options.permutations, options.leet, options.capital, options.capswap)
		if not options.no_confirm:
			o.print_job_stats()
		o.start()
		# run permutations before other mangling operations
		# mangling before permutations produces a lot more output, but probably at reduced quality
		# p = perm(options.permutations, options.words)

		# run mangling functions on wordlist
		# w = [ word for word in cap(options.capital, leet(options.leet, p), swap=options.capswap) ]

		# print(options.masks)

		'''
		m = Mutator(options.words, perm=options.permutations, leet=options.leet, cap=options.capital, capswap=options.capswap)
		mgen = m.start()

		if options.hashcat:
			pass
		else:
			for word in mgen:
				print(word)
		'''
		# hand wordlist to Concatenator, which appends numbers, symbols, etc.
		# c = Concatenator(w, options.masks, options.numbers, options.specials)
		# c.start()


	except ArgumentError:
		stderr.write("\n[!] Check your syntax. Use -h for help.\n")
		exit(2)
	except AssertionError as e:
		stderr.write("[!] {}\n".format(str(e)))
		exit(1)
	except KeyboardInterrupt:
		stderr.write("\n[!] Program interrupted.\n")
		exit(2)
