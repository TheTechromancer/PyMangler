#!/usr/bin/python3
'''
Version 0.1

TODO:

Forget *pend functions and work on capswap, leet functions
*pending should be done in hashcat.  Don't reinvent the wheel

'''

simple_mangling = False
try:
    from liststat import ListStat
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

# top 2000 numbers from linkedin
simple_nums = ['1','2','3','4','0','123','7','5','12','8','11','01','9','10','6','13','22','2011','23','00','21','99','2010','77','09','69','1234','88','19','33','08','14','24','07','17','25','20','15','18','02','55','16','05','27','06','03','04','28','2009','26','66','44','007','78','30','29','2008','31','87','89','79','76','34','82','75','100','86','45','84','83','85','50','81','98','56','67','32','72','74','2000','73','80','68','57','42','001','65','2007','54','64','71','90','111','777','52','40','63','58','35','12345','47','2006','70','59','53','62','51','97','2012','60','2005','143','101','61','48','321','92','95','96','49','43','91','1980','666','1984','37','36','46','1982','2004','38','1985','41','93','1983','1987','1981','2001','1986','94','2003','2002','1978','1979','786','@123','999','123456','39','1976','1975','333','1977','1974','1988','1969','1973','1970','1972','1989','1971','1968','456','888','1990','1967','1964','1965','1966','555','1963','1960','000','222','@1','1962','1991','1961','1957','1959','1999','789','911','1958','1956','420','1212','1998','1992','1955','1954','1111','1000','200','1010','1997','234','1995','1953','1996','121','1952','1950','1993','1994','112','1313','1951','2020','500','125','1947','1948','1949','1@','444','4321','108','300','987','110','135','7777','345','124','009','247','711','311','1122','212','1945','6969','120','102','1946','002','369','0000','9999','147','159','1001','4444','128','2112','113','213','8888','003','211','103','008','316','127','011','1011','117','1012','1$','122','105','2222','123456789','1210','210','246','201','411','1944','1020','313','109','010','1221','104','314','214','567','126','012','357','400','2323','312','520','@1234','2121','150','812','115','123$','098','1024','1942','131','129','107','1213','1943','118','250','1004','2468','1123','114','168','119','678','187','005','0101','1225','1211','@12','3000','900','2013','310','600','323','106','1205','223','1023','2525','1209','1208','182','512','215','1008','132','@2','360','5555','303','1007','1204','116','0001','1013','1919','@2011','202','$1','1224','1214','1231','1206','1215','225','1025','890','1207','320','315','1941','1940','800','521','130','221','1102','747','1108','220','1104','325','1022','3333','137','1029','1230','1414','317','1201','1107','1223','412','1203','1021','006','217','0123','1105','2424','1031','1202','421','808','1112','1015','133','1103','1218','216','1109','1121','145','510','5150','1314','1220','1002','700','511','1005','004','1028','0909','144','318','1911','1106','1017','1217','1228','1939','365','301','501','714','1234567','350','227','1014','1216','1018','0808','231','1003','1812','218','1101','1120','1027','54321','224','1515','1026','1016','151','2211','410','1006','1227','619','415','612','1124','1125','1030','525','219','134','327','1127','2@','1717','1357','1818','206','1219','1009','613','1019','712','256','1701','235','180','1226','611','713','2345','138','141','203','0102','1128','205','909','626','228','324','1910','912','@2010','155','1912','123@','1938','1229','721','199','258','5678','013','2014','413','811','0711','209','727','226','330','610','322','328','505','2310','0911','515','157','423','1066','232','242','156','2311','1200','305','1310','654','0505','5000','0707','198','717','@11','707','1937','1130','5050','1126','513','2210','1129','1905','1908','0202','710','1920','12345678','153','0809','1410','171','2212','6666','1936','818','1402','425','1412','523','2015','1906','723','207','1312','963','326','910','1903','0303','1411','427','2512','831','1907','142','169','2510','2312','331','319','1311','208','136','2410','245','414','0311','2412','139','204','401','2727','424','422','3030','140','450','1110','1616','623','0404','9876','416','1810','1928','813','0812','1512','177','0506','240','197','1900','621','916','302','@01','417','419','514','810','531','0007','718','190','1510','925','0110','2511','230','426','0912','233','308','0204','329','1492','237','1305','2411','625','1100','0411','1904','1935','0405','0811','750','828','175','616','181','516','1222','0708','0606','517','1308','0512','0305','152','4$','913','518','923','0910','522','2110','1307','2711','1914','2810','430','0511','248','1610','1925','1711','0407','0408','0412','1930','2610','0508','720','404','1113','1909','0104','921','0210','1117','@10','0507','021','1712','0815','1511','0709','0987','0108','929','1710','722','0608','0304','1309','123123','0612','0609','2309','1929','432','0406','823','2911','731','615','725','4711','189','753','2580','160','0810','149','2626','0203','1923','0205','0611','0509','528','1408','815','624','0510','617','1901','901','@3','255','428','1302','0105','1508','1612','0308','654321','154','618','0312','229','1927','0211','1611','1811','146','0212','2105','821','0208','2828','2103','715','2104','236','527','1405','1505','1902','1933','2710','158','1304','0103','195','307','243','429','0310','0306','2109','4545','0607','530','918','1404','524','309','1921','257','1303','0207','418','1409','1407','167','724','922','919','1306','0309','2305','304','2106','1932','914','620','915','2812','3010','238','161','2611','0206','2304','2107','650','2205','0307','165','2308','148','622','241','0109','1934','1406','306','927','2811','2108','519','2204','1115','188','614','3003','0410','55555','3110','0409','2208','0209','1503','0214','@143','163','0106','1114','252','2910','2612','741','928','1301','3112','917','0610','543','0712','2301','239','355','1922','1804','1118','0107','1509','1504','529','2712','2202','716','2501','817','628','816','728','166','2307','2209','1805','173','185','822','729','172','0710','3232','178','454','2505','196','3011','3@','3006','1808','1502','1403','1604','1331','0805','814','1500','951','2303','@7','1704','1705','4567','1369','191','526','251','023','627','1401','920','269','550','2306','1809','170','$123','852','13579','1116','2206','1506','825','924','1926','183','2207','820','0401','1501','630','1803','2509','2244','1924','1432','0905','1800','1602','2101','2408','1609','1776','0704','455','1802','7890','3012','192','926','1703','0804','254','504','2508','824','2504','1608','601','2233','1605','1245','0803','801','787','726','1707','244','6789','262','2912','164','2407','343','629','0901','0904','1801','409','1119','2405','2201','347','1702','1709','2406','405','0908','2404','2203','1917','0112','0801','0402','253','1324','0907','1507','765','440','1337','0501','819','0903','1931','2409','1603','719','2507','989','356','1918','0902','2506','2401','@12345','0502','337','1806','2102','0802','3001','2805','737','162','502','2111','0906','1708','4040','179','2601','0503','280','503','2123','1606','701','730','2709','826','0806','408','2030','351','174','186','9000','0504','4242','2808','@5','0301','1601','2503','2302','9090','3105','827','930','1235','3434','176','2804','11111','275','451','876','$4','3131','3108','402','0302','2801','288','2604','407','0604','0201','2606','1807','1607','249','0705','606','2904','193','0701','2021','0601','1415','0703','3004','2403','1706','2905','702','0602','0603','289','5683','974','2901','990','@22','442','299','0605','2909','1300','2701','281','2929','2502','015','2402','0403','279','972','265','757','829','3456','5656','340','335','277','268','@9','@2009','022','2705','2324','270','509','0807','2704','2803','0420','194','2809','014','267','2608','3008','1913','2707','0702','0321','2609','334','3009','259','0706','830','4000','3636','271','2806','@13','2802','184','2605','3107','3005','069','260','380','017','278','2100','0011','273','2703','486','263','459','696','406','1040','358','272','0923','403','266','282','3103','7878','2122','020','667','2708','805','2603','3101','342','123321','2500','261','1789','1881','264','458','998','2906','024','2907','1321','1379','2908','508','1233','2903','2016','2607','3007','@786','112233','@4','545','1916','767','1236','602','@007','375','@21','3$','5252','540','341','1323','2602','8989','770','2807','549','285','381','8080','445','703','1425','286','099','5454','1600','336','1326','1320','0111','8899','287','019','971','332','0921','3535','0421','018','0913','579','1133','283','0925','016','905','0317','0823','290','0213','507','0220','0315','1325','1177','604','12@','1423','025','111111','1199','0313','1290','1453','699','@23','354','1821','377','359','469','0714','1516','1234567890','457','603','2706','535','0523','2526','0825','0915','2425','0813','1289','903','2025','4747','0521','969','0525','556','565','379','850','7788','908','353','2255','1188','298','468','1080','1256','0413','975','0415','1250','1618','0623','506','0824','0423','0822','1718','0513','291','0522','0125','383','0425','609','0515','2050','373','2702','1315','973','0922','802','1248','1400','0424','0821','0314','0927','0613','363','0818','348','902','344','1688','978','284','0713','704','276','274','0721','352','295','1819','077','778','399','0816','431','027','1050','2022','1138','575','102030','997','546','0330','0215','898','338','0428','0416','0422','0723','0621','0924','339','5151','0918','1421','0323','0625','435','0324','0926','803','0316','0814','0325','1416','904','0622','2$','0916','297','1420','0318','2288','@321','0217','981','9898','669','0124','0218','0524','0914','0219','1322','0624','0417','1232','453','0828','1428','346','050','0831','033','1525','3737','030','642','386','541','1617','390','1915','907','0121','0426','0128','0427','433','0216','889','1520','4141','2277','1317','452','0917','0717','690','809','090','90210','2200','0722','605','0414','0519','645','0626','1155','0919','0528','4455','9900','0322','349','367','980','0514','388','1430','0520','1269','636','465','0326','0928','0331','7272','0618','0516','705','0518','1422','0077','0929','0517','1820','986','7575','551','532','0419','0429','0327','3344','366','0126','0129','378','4848','0826','0526','292','991','585','0614','434','0615','@09','293','0531','0920','0430','0527','954','0418','031','988','1280','560','294','561','@2008','5757','0122','393','2332','5566','899','1144','0628','709','1327','0820','396','569','2017','2325','389','1254','2125','608','1478','296','480','0127','3113','0819','656','1288','976','0329','@99','0817','@8','633','0529','804','0715','996','0727','0930','708','607','7000','478','775','361','055','0725','0320','1723','0731','0829','121212','0120','689','1316','1437','0221','12$','0616','1418','745','1318','2469','883','0630','0319','0328','7007','0724','0228','0728','0627','441','773','159753','4343','732','1328','8181','533','489','437','0620','1258','1255','1523','@6','1278','1424','5858','@25','0224','484','0223','0827','368','4200','985','467','6000','101010','944','371','00000','3210','370','878','477','979','1530','2223','1824','6868','2300','2327','686','1099','945','3838','0629','6464','2326','1620','1822','1521','562','788','0716','443','385','0619','77777','0786','1243','977','0225','0830','3141','706','2040','733','1330','571','2124','1098','0113','3579','464','7474','@24','666666','983','475','2728','0530','0729','387','0719','0115','028','447','026','771','499','0131','578','781','364','0617','474','1721','8787','@77','756','631','460','0726','1417','@14','982','6060','586','2019','2018','599','6565','687','691','1275','845','2213','1055','0718','488','955','131313','564','1239','470','2113','595','1899','760','735','448','1257','799','@1984','589','740','0117','1298','646','8484','534','1625','1350','949','2627','806','8000','2024','580','6996','2023','1441','1825','1299','1623','362','566','0720','632','1340','5353','2552','1319','950','1150','6363','7777777','537','040','538','0130','547','563','588','6767','984','668','751','1166','0227','785','080','2400','2426','7979','554','675','1431','1069','051','372','490','1358','542','1823','029','734','640','1888','1237','@55','557','755','462','1621','0226','1771','762','2131','897','671','780','676','651','1722','880','485','382','906','965','807','637','660','@2012','797','1260','568','2356','590','993','959','3377','577','398','544','657','9988','4488','070','1134','3939','479','0114','742','7070','1517','1700','881','987654321','376','1727','1725','2369','7676','466','2314','1088','665','1729','6262','395','032','0116','536','956','091','436','552','798','2120','1522','957','635','384','7171','776','7373','995','4949','877','0$','1622','1427','696969','8585','1524','0118','1187','858','743','495','768','99999','482','848','@27','449','1624','655','832','661','1345','1720','570','@18','933','875','1169','961','842','1359','@1983','8008','2829','1244','3123','966','3366','1180','@19','088','573','@1986','887','1518','471','4646','559','8282','487','2442','@15','0730','931','1724','891','1488','6699','688','374','1828','@1985','7410','1265','473','1551','833','391','856','@20','010203','1238','576','967','970','1247','1277','1628','1356','1728','476','20000','864','@07','071','1285','840','1329','045','647','@1982','553','783','643','1090','463','2266','1060','964']

# top 19 specials from linkedin
common_specials =   ['@','!','.','_','*','#','$','-',' ','&','+','/','%','?','!!',',','**','=','$$']

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
    'w',
    'd',
    's',
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


# drop the bottom 10% of entries from liststat file
liststat_coverage = 90

# max mutations for each word
# reduces mutation keyspace to linear rather than exponential
max_leet    = 256
max_cap     = 512

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
        self.max_leet       = max(1, min(int(max_leet * multiplier), max_leet))
        self.max_cap        = max(1, min(int(max_cap * multiplier), max_cap))
        self.cur_leet       = 0
        self.cur_cap        = 0

        # TODO - truncate wordlist if mask includes more than one word
        self.inlist         = inlist

        self.perm_depth     = perm
        self.do_leet        = leet
        self.do_capswap     = capswap
        self.do_cap         = cap or capswap


    def gen(self):
        '''
        run mangling functions on wordlist
        '''

        for word in self.cap(self.leet(self.perm(self.inlist))):
            yield word


    def perm(self, inlist, repeat=True):
        '''
        takes:      iterable containing words
        yields:     word permutations ('pass', 'word' --> 'password', 'wordpass', etc.)
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
        index   cap_count
        0:      554766
        -1:     49776
        2:      45958
        1:      42566
        3:      39477
        -2:     36318
        -3:     30583
        4:      29684
        -4:     18056
        5:      14206
        -5:     8622
        6:      6474
        -6:     3605
        7:      2266
        -7:     1374
        8:      720
        -8:     286
        9:      186
        -9:     122
        10:     94
        -10:    59
        11:     36
        -11:    29
        12:     22
        13:     16
        -12:    16

        # TODO: flip common cap indexes first?  meh

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
        takes:      iterable containing words
                    passthrough: whether or not to yield unmodified word
        yields:     case variations (common only, unless 'all' is specified)
        '''

        # set type used to prevent duplicates
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
        takes:      iterable containing words
                    swap_values: dictionary containing leet swaps
                    passthrough: whether or not to yield unmodified word
        yields:     leet mutations, not exceeding max_results per word
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

        self.inlist         = inlist
        self.num_results    = max(1, int(len(inlist) * multiplier))

    def gen(self):

        for i in self.inlist:
            self.num_results -= 1
            if self.num_results >= 0:
                yield i





class Concatenator():

    #def __init__(self, w_list, m_list=None, d_list=None, s_list=None, multiplier=1):
    def __init__(self, lists, perm, leet, cap, capswap):

        # TODO: add hashcat rule functionality
        self.lists          = lists

        self.perm           = perm
        self.leet           = leet
        self.cap            = cap
        self.capswap        = capswap

        self.gen_functions  = {
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

        self.total_possible     = total_possible
        self.total_actual       = total_actual
        self.multiplier         = multiplier
        self.word_multiplier    = word_multiplier

        self.coverage           = total_actual / total_possible * 100

        # tuple in form ( chartype, max_len, gen_func )
        self.chunk_info         = chunk_info



class Overseer():
    # Overseer(options.words, options.masks, options.numbers, options.specials, options.per_second,\
    #       options.time, options.permutations, options.leet, options.capital, options.capswap)
    def __init__(self, words, masks=common_masks, numbers=simple_nums, specials=common_specials, pps=hashrate, \
        target_time=finish_time, perm=0, leet=False, cap=False, capswap=False):

        self.masks          = masks
        self.words          = words
        self.numbers        = numbers
        self.specials       = specials
        self.pps            = pps
        self.target_time    = target_time
        self.perm           = perm
        self.leet           = leet
        self.cap            = cap
        self.capswap        = capswap

        if self.leet:
            self.leet_size  = max_leet
        else:
            self.leet_size  = 1
        if self.capswap:
            self.cap_size   = max_cap
        elif cap:
            self.cap_size   = 5
        else:
            self.cap_size   = 1

        self.lists          = {
            'w': words,
            'd': numbers,
            's': specials
        }



        self.masks.sort(key=lambda x: self._mask_complexity(x))

        self.num_masks      = len(masks)
        self.total_desired  = int(pps * target_time * 60 * 60)
        self.per_mask_limit = int(self.total_desired / self.num_masks)

        self.mask_info      = []

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
            script is created that uses a separate hashcat command to crack each mask (TODO)
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
    takes:      filename
    check:      function (returning true or false) which checks validity of each line
    purpose:    simple generator function
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

    parser.add_argument('-l', '--loadfile',         type=obj_from_file,                                 help="Savefile from liststat.py", metavar='FILE')
    parser.add_argument('-p', '--percent',          type=int,           default=liststat_coverage,      help="Percent coverage from liststat file: default {}".format(liststat_coverage), metavar='INT')
    parser.add_argument('-pps', '--per-second',     type=int,           default=hashrate,               help="Expected hashrate - used for limiting time spent on complex masks: default {}".format(hashrate), metavar='INT')
    parser.add_argument('-t', '--time',             type=int,           default=finish_time,            help="Target time to finish in hours: default {}".format(finish_time), metavar='INT')
    parser.add_argument('-hc', '--hashcat',                                                             help="Use hashcat rules to maximize efficiency", metavar='DIR')

    parser.add_argument('-w', '--words',            type=list_from_file,    default=None,               help="File containing words", metavar='FILE')
    parser.add_argument('-n', '--numbers',          type=list_from_file,    default=simple_nums,        help="File containing numbers: e.g. '7', '123', '1986', etc.", metavar='FILE')
    parser.add_argument('-s', '--specials',         type=list_from_file,    default=common_specials,    help="File containing special characters: e.g. '#', '!!!', '??', etc.", metavar='FILE')
    parser.add_argument('-m', '--masks',            type=list_from_file,    default=common_masks,       help="File containing simple masks: e.g. 'wds' (word-digit-special)", metavar='FILE')

    parser.add_argument('-L',   '--leet',           action='store_true',                                help="All possible 1337 combinations: w0rd")
    parser.add_argument('-c',   '--capital',        action='store_true',                                help="Common caps variations: Word, word, WORD")
    parser.add_argument('-C',   '--capswap',        action='store_true',                                help="All possible case combinations: wOrD")
    parser.add_argument('-P',   '--permutations',   type=int,               default=1,                  help="Max times to combine words (careful! exponential)", metavar='INT')

    parser.add_argument('-mm', '--mask-max',        type=int,                                           help="Maximum masks to take as iput", metavar='INT')
    parser.add_argument('-wm', '--word-max',        type=int,                                           help="Maximum words to take as input", metavar='INT')
    parser.add_argument('-nm', '--number-max',      type=int,                                           help="Maximum numbers to take as input", metavar='INT')
    parser.add_argument('-sm', '--special-max',     type=int,                                           help="Maximum specials to take as input", metavar='INT')
    parser.add_argument('-y', '--no-confirm',       action='store_true',                                help="Don't prompt for confirmation")

    try:

        options = parser.parse_args()

        if options.words is None:
            options.words = [l.decode().strip('\r\n') for l in stdin.buffer.readlines()]

        # parse file from liststat.py
        if options.loadfile and not simple_mangling:

            l = options.loadfile
            p = options.percent

            # override lists loaded from liststat by manually specified ones, if they exist

            if not options.masks:
                options.masks   = list(l.trim(l.simple_masks, p, l.total, max_results=options.mask_max))

            for pos in l.chunks:
                for char in l.chunks[pos]:

                    # check character set
                    if not options.words and char & 6 > 0:
                        options.words       = list(l.trim(l.chunks[pos][char], p, l.chunk_total[pos][char], max_results=options.word_max))

                    elif not options.numbers and char == 1:
                        options.numbers     = list(l.trim(l.chunks[pos][char], p, l.chunk_total[pos][char], max_results=options.number_max))

                    elif not options.specials and char == 8:
                        options.specials    = list(l.trim(l.chunks[pos][char], p, l.chunk_total[pos][char], max_results=options.special_max))

                    # clear dictionary to save memory
                    l.chunks[pos][char] = None
            l = None


        assert options.words, "Please specify wordlist (-w)"

        # def _calc_multiplier(masks, words, numbers, specials, pps, target_time, leet=1, capswap=1, confirm=True):
        # _calc_multiplier( options.masks, options.words, options.numbers, options.specials, options.per_second, options.time,\
        #   (max_leet if options.leet else 1), (max_cap if options.capswap else 5), (not options.no_confirm) )

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
