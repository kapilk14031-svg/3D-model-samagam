PLAN_SCALE=1.4
def planpoint(u,v,y=0):return [(v-760)*PLAN_SCALE,y,(1000-u)*PLAN_SCALE]
features=[]
def feature(id,name,kind,bbox=None,path=None,detail='',status='PDF label and relative position traced; dimensions unmeasured',**kw):
    item=dict(id=id,name=name,kind=kind,bbox=bbox,path=path,detail=detail,status=status,source='Adobe Scan 17 Oct 2026.pdf',page=1,**kw);features.append(item);return item
# Normalized pixel coordinates on the complete, preserved 1824 x 1371 scan.
feature('P01','PARKING-P1','parking',[365,864,450,944],detail='LIGHT VEHICLES / CAR PARKING; red P1 box')
feature('P02','PARKING-P1','parking',path=[[305,946],[405,943],[405,1025],[450,1025],[451,1080],[305,1113]],detail='HEAVY VEHICLES; dense vehicle-row symbols')
feature('P03','PARKING-P2','parking',path=[[488,732],[640,731],[640,818],[562,817]],detail='BUSES & CARS DAILY COMMUTERS; blue P2 box')
feature('P04','PARKING P2 2 WHEELERS','parking',[659,836,713,875],detail='Two-wheeler area')
feature('P05','PARKING P2','parking',[657,876,713,932],detail='P2 strip above the separate I-PARKING pocket; shared arrow approach does not make the polygons overlap')
feature('P06','PARKING-P3','parking',path=[[1052,158],[1214,158],[1214,277],[1041,277]],detail='LIGHT VEHICLES / CAR PARKING & HEAVY VEHICLES PARKING; vehicle row symbols')
feature('P07','PARKING-P4','parking',path=[[1086,765],[1211,777],[1251,796],[1245,838],[1091,843]],detail='LIGHT VEHICLES PARKING / SEWADAR ON DUTY IN DAILY COMMUTER & SAINTS FROM ABROAD')
feature('P08','PARKING-P5','point',[738,1092,852,1133],detail='NEAR FOOT OVER BRIDGE / LOCAL BUS STOP / PARKING DAILY COMMUTERS; location is a textual annotation, not a measured polygon')
feature('P09','I-PARKING','parking',[669,933,711,1018],detail='Green arrows; invited guests / V.I.P. parking')
feature('P10','I-PARKING','parking',[847,878,905,936],detail='Second invited-guest parking pocket')
feature('P11','O PARKING','parking',[855,744,902,780],detail='As printed; letter O retained without expansion')
feature('P12','S C PARKING','parking',[856,785,902,823],detail='Upper SC parking pocket; abbreviation retained')
feature('P13','S C PARKING','parking',[855,827,902,865],detail='Lower SC parking pocket; abbreviation retained')
feature('B01','PANDAL','pandal',path=[[720,743],[831,743],[830,977],[743,1004],[721,990]],detail='Footprint traced from PDF; curved canopy/stage styling remains illustrative')
feature('B02','EXHIBITION','building',[720,717,833,741])
feature('B03','S/D OFFICE','building',[657,577,713,714])
feature('B04','OFFICES','building',[842,742,855,866],detail='Narrow vertical office strip')
feature('B05','TOILETS','toilets',[537,721,635,734],detail='Toilets beside west portion of Road R-2')
feature('B06','TOILETS','toilets',[654,722,710,737],detail='Second toilet label above railway/ISBT alighting area')
feature('B07','ALIGHTING POINT FOR RAILWAY STATION & ISBT VEHICLES','alighting',[654,741,715,827],detail='Mixed pink/blue arrows as drawn')
feature('B08','ALIGHTING','alighting',[1051,622,1103,663],detail='Second alighting pocket near diagonal government road')
feature('B09','LANGAR','building',[963,277,1010,424],detail='Northern langar block')
feature('B10','LANGAR','building',[899,433,949,562],detail='Middle langar block')
feature('B11','LANGAR','building',[657,576,711,697],detail='Label above S/D office area; shared/adjacent outline retained',status='Label readable; internal subdivision of shared outline uncertain')
feature('B12','LANGAR','building',[912,786,950,867],detail='Eastern service cluster langar')
feature('B13','SPECIAL RESIDENCE','building',[979,787,1049,864],detail='Small print read visually; check source crop for exact spelling',status='Small label; transcription needs review')
feature('B14','TOILET (READING UNCERTAIN)','toilets',[956,810,976,864],detail='Narrow service block',status='Very small text; transcription needs review')
feature('B15','PETROL PUMP','building',[916,911,941,948])
feature('B16','UNCLEAR PLOT LABEL U03','building',[943,916,968,943],detail='Tiny two-line label beside petrol pump; retained as a review item',status='Unclear label; do not treat transcription as confirmed')
feature('B17','POLICE CHOWKI','building',[968,876,1047,940])
feature('B18','WASTE LAND','plot',path=[[846,939],[894,938],[889,955],[864,964],[849,957]])
feature('B19','KARISHNA POLYMER','building',path=[[1081,845],[1173,846],[1170,898],[1084,921]],detail='Spelling KARISHNA retained as printed')
feature('B20','SNCF NURSARY','point',[1212,636,1324,660],detail='Spelling NURSARY retained from scan; no exact building footprint supplied')
feature('B21','H T LINE','utility',path=[[918,265],[994,249]],detail='Two crossed-square tower symbols near northern government road')
feature('B22','PDF SMALL LABEL U01','building',[883,326,906,397],detail='Tiny two-line label west of northern langar; original pixels preserved',status='Unclear label; retained for review')
feature('B23','PDF SMALL LABEL U02','building',[1020,794,1031,863],detail='Narrow vertical strip inside eastern service block; original pixels preserved',status='Unclear label; retained for review')
feature('G01','DELHI GATE NO 1','gate',[638,1021,665,1054])
feature('G02','GATE NO 2','gate',[892,963,914,989])
feature('G03','GATE NO 3','gate',[1044,918,1064,942])
feature('G04','GATE','gate',[1253,870,1280,891],detail='Unnumbered entrance into P4 road loop')
feature('G05','GATE','gate',[1076,725,1091,751],detail='Unnumbered gate on diagonal approach')
feature('G06','GATE','gate',[1100,652,1120,675],detail='Unnumbered gate near alighting area')
feature('H01','NATIONAL HIGHWAY','road',path=[[82,1196],[335,1139],[650,1058],[905,989],[1100,950],[1320,888],[1610,824]],detail='NH-44 context; Delhi at left/south, Ambala at right/north')
feature('H02','FLY OVER','flyover',path=[[961,983],[1100,950],[1202,925]],detail='LOCAL flyover label by Gate 3; replaces the unrelated 6.9 km northern candidate in the main plan')
feature('H03','UNDER PASS','underpass',[1085,938,1122,978],detail='Underpass by local flyover / Gate 3')
feature('H04','UNDER PASS','underpass',[313,1143,349,1180],detail='Separate southern underpass near P1')
feature('H05','RAILWAY STATION BHODWAL MAJRI','station',[944,93,1108,133])
feature('H06','RAILWAY LINE TO DELHI','rail',path=[[249,198],[642,170],[1049,142],[1430,113],[1670,93]],detail='Delhi arrow to left; Ambala arrow to right')
feature('H07','RAILWAY LINE TO AMBALA','point',[1450,98,1665,140])
feature('H08','TO DELHI','point',[80,1193,194,1230])
feature('H09','TO AMBALA','point',[1550,812,1665,848])
feature('H10','TO GANNOUR','point',[172,395,262,426],detail='Road branch direction as printed')
feature('V01','VILLAGE PANCHI GUJRAN','village',[188,716,234,963])
feature('V02','VILLAGE BHODWAL MAJRI','village',[1510,283,1701,310])
feature('V03','VILLAGE PATTI KALYANA','village',[1315,720,1474,748])
# Roads and printed width labels. Repeated labels remain individually indexed.
roadpaths=[
('R01','ROAD',[[185,419],[278,398],[521,357],[742,317],[899,280],[1049,247],[1052,144],[1424,128]]),
('R02','ROAD',[[278,402],[287,630],[302,670],[303,1126]]),
('R03','ROAD',[[301,670],[385,670],[424,646],[521,565],[743,318]]),
('R04','ROAD',[[420,648],[485,713],[555,803],[640,812]]),
('R05',"ROAD R-2 90'",[[485,719],[648,719]]),
('R06','ROAD',[[650,1036],[647,816],[648,720],[649,574]]),
('R07','ROAD',[[720,1000],[718,720],[720,570],[1015,570],[1018,283]]),
('R08','ROAD',[[846,933],[844,718],[844,424]]),
('R09','GOV. ROAD',[[1045,284],[1217,286],[1360,285],[1394,271],[1412,272]]),
('R10','GOV. ROAD',[[1362,141],[1392,263],[1430,271],[1458,414],[1491,844]]),
('R11','GOV. ROAD',[[1385,289],[1312,357],[1315,401],[1373,440],[1432,416],[1450,399]]),
('R12','ROAD',[[1080,644],[1197,522],[1317,403]]),
('R13','ROAD',[[1057,927],[1075,774],[1075,714],[1114,665],[1141,623]]),
('R14','ROAD',[[1141,623],[1223,661],[1283,690],[1284,845],[1313,878]]),
('R15','ROAD',[[1083,751],[1227,760],[1258,784],[1258,850],[1279,876]]),
('R16',"ROAD 24 WIDE",[[903,871],[973,871]]),
('R17',"ROAD 80' WIDE",[[837,742],[837,866]]),
('R18','ROAD',[[1058,287],[1054,609],[1081,652]]),
('R19','ROAD',[[1283,852],[1484,848],[1608,825]]),
('R20','ROAD',[[302,939],[451,944],[451,1029]]),
('R21','GOV. ROAD',[[743,318],[897,283],[1049,247]])]
for id,n,p in roadpaths:feature(id,n,'internal_road',path=p,detail='Width shown only where explicitly printed; trace is schematic')
# All annotated boundary walls, plus visible unlabeled plot outlines.
wallpaths=[[[742,422],[845,426],[845,507],[741,507]],[[954,277],[953,424],[895,424],[898,571]],[[954,284],[955,563]],[[1046,285],[1217,288],[1241,459],[1198,466]],[[907,675],[1055,675],[1054,737]],[[721,742],[830,742],[830,977],[743,1006],[721,992],[721,742]],[[1082,764],[1213,777],[1250,794],[1244,839],[1085,843]],[[851,177],[963,176],[963,260],[841,278],[841,222],[858,218],[858,177]],[[1047,287],[1090,290],[1090,532],[1137,535],[1146,460],[1200,461]],[[911,788],[947,788],[948,866]],[[978,789],[1021,789],[1021,856],[1046,856]],[[1048,777],[1061,779],[1057,929]]]
for i,path in enumerate(wallpaths):feature(f'W{i+1:02}','BOUNDARY WALL' if i<5 else 'PDF PLOT OUTLINE','wall',path=path,detail='Visible black boundary/outline traced; not a land survey')
legend=[
('L01','OUT STATION VEHICLES FROM DELHI SIDE SHOWN THUS','#b96c98','arrow','PARKING-P1'),
('L02','VEHICLES FROM DELHI SIDE / SEWADARS ON DUTY IN DAILY COMMUTERS (CHARTED BUSES) SHOWN THUS','#b96c98','shield','PARKING-P2'),
('L03','PARKING - P1 SHOWN THUS','#a25e65','box','P1'),
('L04','VEHICLES FROM DELHI SIDE / SEWADARS ON DUTY IN DAILY COMMUTERS PARKING-P2','#4a7ea1','box','P2'),
('L05','OUT STATION VEHICLES FROM AMBALA SIDE SHOWN THUS','#427b9f','arrow','PARKING-P3'),
('L06','VEHICLES FROM AMBALA SIDE / SEWADARS ON DUTY IN DAILY COMMUTERS SHOWN THUS','#427b9f','shield','PARKING-P2'),
('L07','OUT STATION VEHICLES FROM AMBALA SIDE PARKING-P3','#427b9f','box','P3'),
('L08','VEHICLES FROM AMBALA SIDE / SEWADARS ON DUTY IN DAILY UP & DOWN PARKING-P4','#427b9f','shield','P4'),
('L09','VEHICLES FOR SAINTS FROM ABROAD PARKING-P4','#b76d79','arrow','P4'),
('L10','VEHICLES FOR S.C. PARKING','#419b86','shield','SC'),
('L11','FOR INVITED GUESTS / V.I.P. PARKING','#419b86','arrow','I-PARKING')]
for id,n,c,shape,dest in legend:feature(id,n,'legend',detail='Reference table entry '+id[1:]+'; symbol '+shape+'; destination '+dest,color=c,symbol=shape,destination=dest)
feature('M01','79 TH. NIRANKARI SANT SAMAGAM','metadata',detail='Source drawing title')
feature('M02','TRAFFIC ROUTE PLAN / ALL GROUNDS','metadata',detail='Drawing title and extent')
feature('M03','SNM','metadata',detail='Drawing title block organisation')
feature('M04','LAYOUT INSTALLATION & DECORATION','metadata',detail='DEALT BY, as printed')
feature('M05','14-10-2026','metadata',detail='Printed drawing date, distinct from scan filename')
feature('M06','N','metadata',[898,1195,960,1236],detail='North arrow points generally right on the sheet; world display is rotated to north-up')
feature('S01','VEHICLE ROW SYMBOLS P1','symbols',[303,943,452,1108],detail='Dense rows preserved in source underlay; 3D repetitions are representative, not a counted capacity')
feature('S02','VEHICLE ROW SYMBOLS P3','symbols',[1113,160,1213,276],detail='Vehicle row arrangement retained as representative geometry and exact source pixels')
feature('S03','DIRECTIONAL ARROWS','symbols',detail='Pink, blue and green arrows preserved in exact source image; 3D paths follow visible arrow families, not navigation instructions')
plan_routes=[
dict(id='L01',points=[[98,1197],[323,1140],[307,946],[302,670],[389,668],[488,715],[650,720]],color='#b96c98'),
dict(id='L02',points=[[99,1185],[337,1131],[649,1048],[647,816],[570,814],[496,737]],color='#c388a8'),
dict(id='L05',points=[[1592,830],[1310,898],[1060,950],[650,1055],[650,720],[721,720],[721,574],[1018,574],[1018,286],[1055,254],[1120,249]],color='#427b9f'),
dict(id='L06',points=[[1592,841],[1310,909],[1060,961],[650,1066],[650,816],[696,785]],color='#588eac'),
dict(id='L08',points=[[1590,821],[1485,852],[1317,891],[1284,845],[1284,694],[1222,658],[1140,625],[1082,712],[1208,745]],color='#427b9f'),
dict(id='L09',points=[[99,1207],[650,1070],[1060,970],[1280,891],[1259,848],[1259,788],[1224,762],[1110,753]],color='#b76d79'),
dict(id='L10',points=[[1592,850],[1057,974],[903,982],[902,872],[878,849]],color='#419b86'),
dict(id='L11',points=[[100,1177],[650,1037],[670,1003],[683,959]],color='#3b9178'),
dict(id='L11',points=[[1590,808],[903,967],[902,891],[862,896]],color='#3b9178')]

# Additional visible irregular parcel edges, retained without invented land-use names.
additional_outlines=[[[692,364],[743,364],[743,317]],[[691,366],[689,392],[713,394],[713,451],[742,453]],[[552,510],[616,510],[617,561],[551,561],[552,510]],[[618,477],[667,477],[667,506],[687,507],[687,535],[710,535],[711,563]],[[551,574],[614,574],[614,713]],[[619,574],[655,574]],[[480,621],[480,713],[544,713],[544,574]],[[1032,292],[1193,293],[1193,315],[1226,317],[1225,344],[1246,354],[1246,385],[1267,399],[1268,453],[1196,455],[1195,506],[1169,507],[1168,468],[1125,469],[1125,392],[1100,392],[1098,503],[1070,505],[1070,471],[1044,471],[1044,374],[1032,373],[1032,292]],[[1030,511],[1099,511],[1101,534],[1147,534],[1147,560],[1090,562],[1090,576],[1060,575]],[[1230,508],[1252,507],[1252,534],[1286,531],[1287,555],[1265,563],[1269,584],[1251,589],[1240,573],[1212,578]],[[1206,159],[1234,160],[1234,174],[1264,176],[1264,199],[1241,202],[1239,230],[1224,232],[1222,258]],[[1065,685],[1244,690],[1244,740],[1082,736]],[[1080,844],[1082,920],[1170,898],[1172,845]],[[848,780],[900,780]],[[846,826],[901,826]],[[847,868],[903,868]]]
for i,path in enumerate(additional_outlines):feature(f'W{i+13:02}','PDF UNLABELLED PARCEL OUTLINE','wall',path=path,detail='Irregular black parcel outline traced without assigning a land use; source image retains all minor linework')
feature('S04','NEAR FOOT OVER BRIDGE / LOCAL BUS STOP','point',[718,1077,856,1106],detail='Source annotation near P5; bridge footprint and stairs are not dimensioned in the source')

# Second visual audit: repeated labels and previously omitted minor geometry.
feature('R22','ROAD 24 WIDE','internal_road',path=[[973,871],[1046,871]],detail='Second printed ROAD 24 WIDE annotation; source punctuation/units should be reviewed')
feature('R23',"ROAD R-2 90'",'internal_road',path=[[650,719],[839,719]],detail='Second printed R-2 90 width annotation beside exhibition')
feature('P14','PARKING','point',[838,875,848,936],detail='Vertical generic PARKING label beside I-PARKING; retained without assigning a new numbered parking')
feature('W29','PANDAL INTERNAL DIVIDER','wall',path=[[721,910],[830,910]],detail='Internal horizontal line in pandal footprint; drawn as a low divider because actual height/function is unspecified')
for n,bbox in enumerate([[1048,801,1064,811],[1048,817,1064,829],[1048,834,1064,846],[1048,851,1064,862],[1054,882,1064,899]]):
    feature(f'B{24+n:02}','UNLABELLED GATE 3 BLOCK '+str(n+1),'building',bbox,detail='Small outlined cell beside Special Residence / Gate 3. No use or capacity printed; no facility name invented')
feature('W30','PDF PARCEL OUTLINE','wall',path=[[719,573],[719,714],[835,714],[835,573]],detail='Central rectangular parcel boundary above exhibition')
feature('W31','PDF PARCEL OUTLINE','wall',path=[[850,575],[899,575],[899,675],[850,675],[850,575]],detail='Narrow parcel west of the alighting boundary')
for f in features:
    if f['id']=='R17':f['detail']='Printed vertical width annotation beside offices east of pandal; position corrected after second visual audit';f['status']='Width appears 80; small print needs review, dimensions unmeasured'

# User-requested deeper route palette; original PDF colour values remain recorded.
route_palette={'#b96c98':'#8c285c','#c388a8':'#963564','#a25e65':'#862f43','#4a7ea1':'#175b88','#427b9f':'#175b88','#588eac':'#1f628a','#b76d79':'#912f4d','#419b86':'#176644','#3b9178':'#135b3d'}
for f in features:
    if 'color' in f:f['source_color']=f['color'];f['color']=route_palette.get(f['color'],f['color'])
for r in plan_routes:
    r['source_color']=r['color'];r['color']=route_palette.get(r['color'],r['color'])
