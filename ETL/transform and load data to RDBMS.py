import csv,os,re,time, pymysql,datetime,ast
from bs4 import BeautifulSoup as bs
from pymysql import MySQLError

def parse_topics(long_text):
    listOfLists = []
    regex = re.compile(r"{'urlkey':\s'(.*?)',\s'name':\s'(.*?)',\s'id':\s(\d+)}")
    match = regex.findall(long_text)
    if match:
        for item in match:
            listOfLists.append(item)
    return listOfLists

def parse_members_topics(long_text):
    listOfLists = []
    regex = re.compile(r"{u'name':\su'(.*?)',\su'urlkey':\su'(.*?)',\su'id':\s(\d+)}")
    match = regex.findall(long_text)
    if match:
        for item in match:
            listOfLists.append(item)
    return listOfLists

def find_number(text):
    if not text:
        return None
    phoneNumRegex1 = re.compile(r'\((\d\d\d)\)( |-|.|)(\d\d\d)( |-|.|)(\d\d\d\d)')
    mo = phoneNumRegex1.search(text)
    if not mo:
        phoneNumRegex2 = re.compile(r'(\d\d\d)(-|.|)(\d\d\d)(-|.|)(\d\d\d\d)')
        mo = phoneNumRegex2.search(text)
        if not mo:
            return None
        else:
            return mo.group(1)+mo.group(3)+mo.group(5)
    return mo.group(1)+mo.group(3)+mo.group(5)

def clean_csv_files():
    connection = pymysql.connect(host=os.environ.get('AWS_HOST'),
                             user='root',
                             password=os.environ.get('AWS_PASSWORD'),
                             db=os.environ.get('AWS_DB'),
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
        if file.endswith(".csv"):
            if file.startswith('group'):
                with open(file,'r',encoding='utf8') as filename:
                    reader = csv.reader(filename)
                    next(reader)
                    for row in reader:
                        if row[4].lower() == 'us':
                            cities = ['chicago','san francisco','new york']
                            if any(city in row[3].lower() for city in cities):
                                if row[6]:
                                    row[6] = row[6].strip().replace("\"","")
                                if row[19]:
                                    row[19] = row[19].strip().replace("\"","")
                                if row[21]:
                                    row[21] = row[21].strip().replace("\"","")
                                if row[25]:
                                    row[25] = row[25].strip().replace("\"","")
                                if row[35]:
                                    row[35] = row[35].strip().replace("\"","") 
                                if row[5]:
                                    row[5] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(row[5])/1000))
                                if row[6]:
                                    row[6] = bs(row[6],"lxml").text
                                if row[33]:
                                    row[33] = int(float(row[33])/1000)
                                try:
                                    with connection.cursor() as cursor:
                                        sql = "SELECT `city_id` from `cities` where `city`= '%s' and state = '%s'" %(row[3],row[29])
                                        cursor.execute(sql)
                                        city_id = cursor.fetchone()['city_id']
                                        connection.commit()
                                except MySQLError as e:
                                    print(sql)
                                    print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                                try:
                                    with connection.cursor() as cursor:
                                        sql = "INSERT INTO `groups` (`group_id`,`category_id`,`category.name`,`category.shortname`,`city_id`,`city`,`country`,`created`,`description`,`group_photo.base_url`,`group_photo.highres_link`,`group_photo.photo_id`,`group_photo.photo_link`,`group_photo.thumb_link`,`group_photo.type`,`join_mode`,`lat`,`link`,`lon`,`members`,`group_name`,`organizer.member_id`,`organizer.name`,`organizer.photo.base_url`,`organizer.photo.highres_link`,`organizer.photo.photo_id`,`organizer.photo.photo_link`,`organizer.photo.thumb_link`,`organizer.photo.type`,`rating`,`state`,`timezone`,`urlname`,`utc_offset`,`visibility`,`who`) VALUES (%d,%d,\"%s\",\"%s\",%d,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%d,\"%s\",\"%s\",\"%s\",\"%s\",%f,\"%s\",%f,%d,\"%s\",%d,\"%s\",\"%s\",\"%s\",%d,\"%s\",\"%s\",\"%s\",%f,\"%s\",\"%s\",\"%s\",%d,\"%s\",\"%s\")" % (int(row[13]), int(row[0]) if row[0] else -1, row[1] if row[1] else 'not_found', row[2] if row[2] else 'not_found', int(city_id) if city_id else "",row[3] if row[3] else 'not_found', row[4] if row[4] else 'not_found', row[5] if row[5] else datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), row[6].encode('ascii','ignore').decode("utf-8").replace("\"","").strip() if row[6] else 'not_found', row[7] if row[7] else 'not_found', row[8] if row[8] else 'not_found', float(row[9]) if row[9] else -1, row[10] if row[10] else 'not_found', row[11] if row[11] else 'not_found', row[12] if row[12] else 'others', row[14] if row[14] else 'others', float(row[15]) if row[15] else 0.0, row[16] if row[16] else 'not_found', float(row[17]) if row[17] else 0.0, int(row[18]) if row[18] else -1, row[19].encode('ascii','ignore').decode("utf-8").replace("\"","") if row[19] else 'not_found', float(row[20]) if row[20] else -1, row[21].encode('ascii','ignore').decode("utf-8").replace("\"","") if row[21] else 'not_found', row[22] if row[22] else 'not_found', row[23] if row[23] else 'not_found', float(row[24]) if row[24] else -1, row[25] if row[25] else 'not_found', row[26] if row[26] else 'not_found', row[27] if row[27] else 'others', float(row[28]) if row[28] else 0.0, row[29] if row[29] else 'not_found', row[30] if row[30] else 'not_found', row[32].encode('ascii','ignore').decode("utf-8").strip() if row[32] else 'not_found', int(row[33]) if row[33] else -1, row[34] if row[34] else 'others', row[35].encode('ascii','ignore').decode("utf-8").replace("\"","") if row[35] else 'not_found')
                                        cursor.execute(sql)
                                        connection.commit()
                                except MySQLError as e:
                                    print(sql)
                                    print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                print("Success! file: "+file+" written to groups table in database.")
                with open(file,'r',encoding='utf8') as filename:
                    reader = csv.reader(filename)
                    next(reader)
                    for row in reader:
                        if row[4].lower() == 'us':
                            cities = ['chicago','san francisco','new york']
                            if any(city in row[3].lower() for city in cities):
                                if row[31] and len(row[31])>1:
                                    retList = parse_topics(row[31][1:-1].replace("\"","\'"))
                                    if retList:
                                        ## write each list in this lol to new table
                                        for temp_row in retList:
                                            try:
                                                with connection.cursor() as cursor:
                                                    sql = "INSERT INTO `groups_topics` (`topic_id`, `topic_key`, `topic_name`, `group_id`) VALUES (%d,\"%s\",\"%s\",%d)" % (int(temp_row[2]), temp_row[0], temp_row[1], int(row[13]))
                                                    cursor.execute(sql)
                                                    connection.commit()
                                            except MySQLError as e:
                                                if e.args[0] != 1452: # foreign key constraint error
                                                    print(sql)
                                                    print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                print("Success! file: "+file+" written to groups_topics table in database.")
            elif file.startswith('event'):
                with open(file,'r',encoding='utf8') as filename:
                    reader = csv.reader(filename)
                    next(reader)
                    for row in reader:
                        if row[34].lower() == 'us':
                            cities = ['chicago','san francisco','new york']
                            if any(city in row[33].lower() for city in cities):
                                row = [item.strip().replace("\"","") for item in row]
                                if row[0]:
                                    row[0] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(row[0])/1000))
                                if row[1]:
                                    row[1] = bs(row[1],"lxml").text
                                if row[2]:
                                    row[2] = int(float(row[2])/1000.0)
                                if row[10]:
                                    row[10] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(row[10])/1000))
                                if row[28]:
                                    row[28] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(row[28])/1000))
                                if row[29]:
                                    row[29] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(row[29])/1000))
                                if row[30]:
                                    row[30] = int(float(row[30])/1000.0)
                                if row[40]:
                                    row[40] = find_number(row[40])#row[40].strip().replace(" ","").replace("(","").replace(")","").replace("-","").replace(".","")
                                try:
                                    with connection.cursor() as cursor:
                                        sql = "INSERT INTO `events` (`event_id`,`created`,`description`,`duration`,`event_url`,`fee.accepts`,`fee.amount`,`fee.currency`,`fee.description`,`fee.label`,`fee.required`,`group.created`,`group.group_lat`,`group.group_lon`,`group_id`,`group.join_mode`,`group.name`,`group.urlname`,`group.who`,`headcount`,`how_to_find_us`,`maybe_rsvp_count`,`event_name`,`photo_url`,`rating.average`,`rating.count`,`rsvp_limit`,`event_status`,`event_time`,`updated`,`utc_offset`,`venue.address_1`,`venue.address_2`,`venue.city`,`venue.country`,`venue_id`,`venue.lat`,`venue.localized_country_name`,`venue.lon`,`venue.name`,`venue.phone`,`venue.repinned`,`venue.state`,`venue.zip`,`visibility`,`waitlist_count`,`why`,`yes_rsvp_count`) VALUES (\"%s\",\"%s\",\"%s\",%d,\"%s\",\"%s\",%f,\"%s\",\"%s\",\"%s\",%d,\"%s\",%f,%f,%d,\"%s\",\"%s\",\"%s\",\"%s\",%d,\"%s\",%d,\"%s\",\"%s\",%f,%d,%d,\"%s\",\"%s\",\"%s\",%d,\"%s\",\"%s\",\"%s\",\"%s\",%d,%f,\"%s\",%f,\"%s\",%d,%s,\"%s\",%d,\"%s\",%d,\"%s\",%d	)" % (row[20], row[0] if row[0] else datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), row[1].encode('ascii','ignore').decode("utf-8").strip() if row[1] else 'not_found', int(float(row[2])) if row[2] else 10800, row[3] if row[3] else 'not_found', row[4] if row[4] else 'others', float(row[5]) if row[5] else 0.0, row[6] if row[6] else 'not_found', row[7] if row[7] else 'per person', row[8] if row[8] else 'Price', int(float(row[9])) if row[9] else 0, row[10] if row[10] else datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), float(row[11]) if row[11] else 0.0, float(row[12]) if row[12] else 0.0, int(float(row[13])) if row[13] else -1, row[14] if row[14] else 'others', row[15].encode('ascii','ignore').decode("utf-8").replace("\'","").strip() if row[15] else 'not_found', row[16].encode('ascii','ignore').decode("utf-8").strip() if row[16] else 'not_found', row[17].encode('ascii','ignore').decode("utf-8").strip() if row[17] else 'not_found', int(float(row[18])) if row[18] else -1, row[19].encode('ascii','ignore').decode("utf-8").replace("\\","").strip() if row[19] else 'not_found', int(float(row[21])) if row[21] else -1, row[22].encode('ascii','ignore').decode("utf-8").strip() if row[22] else 'not_found', row[23] if row[23] else 'not_found', float(row[24]) if row[24] else 0.0, int(float(row[25])) if row[25] else -1, float(row[26]) if row[26] else -1, row[27] if row[27] else 'not_found', row[28] if row[28] else 'not_found', row[29] if row[29] else 'not_found', int(float(row[30])) if row[30] else -1, row[31].encode('ascii','ignore').decode("utf-8").strip() if row[31] else 'not_found', row[32].encode('ascii','ignore').decode("utf-8").strip() if row[32] else 'not_found', row[33].encode('ascii','ignore').decode("utf-8").strip() if row[33] else 'not_found', row[34] if row[34] else 'not_found', float(row[35]) if row[35] else -1, float(row[36]) if row[36] else 0.0, row[37] if row[37] else 'not_found', float(row[38]) if row[38] else 0.0, row[39].encode('ascii','ignore').decode("utf-8").strip() if row[39] else 'not_found', int(float(row[40])) if row[40] else -1, row[41] if row[41] else 'FALSE', row[42] if row[42] else 'not_found', int(float(row[43])) if row[43] and type(row[43])==int else -1, row[44] if row[44] else 'others', int(float(row[45])) if row[45] else -1, row[46] if row[46] else 'not_found', int(float(row[47])) if row[47] else -1)
                                        cursor.execute(sql)
                                        connection.commit()
                                except MySQLError as e:
                                    if e.args[0] != 1452: # foreign key constraint error
                                        print(sql)
                                        print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                print("Success! file: "+file+" written to database.")
                        
            elif file.startswith('venue'):
                with open(file,'r',encoding='utf8') as filename:
                    reader = csv.reader(filename)
                    next(reader)
                    for row in reader:
                        if row[3].lower() == 'us':
                            cities = ['chicago','san francisco','new york']
                            if any(city in row[2].lower() for city in cities):
                                if row[1]:
                                    row[1] = row[1].strip().replace("\"","")
                                try:
                                    with connection.cursor() as cursor:
                                        sql = "INSERT INTO `venues` (`venue_id`,`address_1`,`city`,`country`,`distance`,`lat`,`localized_country_name`,`lon`,`venue_name`,`rating`,`rating_count`,`state`,`zip`) VALUES (%d,\"%s\",\"%s\",\"%s\",%f,%f,\"%s\",%f,\"%s\",%f,%d,\"%s\",%d)" % (int(row[5]),row[1].encode('ascii','ignore').decode("utf-8").strip() if row[1] else 'not_found', row[2].encode('ascii','ignore').decode("utf-8").strip() if row[2] else 'not_found',row[3] if row[3] else 'not_found',float(row[4]) if row[4] else 0.0,float(row[6]) if row[6] else 0.0,row[7] if row[7] else 'not_found',float(row[8]) if row[8] else 0.0,row[9].encode('ascii','ignore').decode("utf-8").replace("\"","").strip() if row[9] else 'not_found',float(row[10]) if row[10] else 0.0,int(row[11]) if row[11] else -1, row[12] if row[12] else 'not_found', int(row[13].replace("-","").replace(",","").replace("?","").replace("'","").replace("`","").replace(" ","")) if row[13] else -1)
                                        #print(sql)
                                        cursor.execute(sql)
                                        connection.commit()
                                except MySQLError as e:
                                    if e.args[0]!=1062:
                                        print(sql)
                                        print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                print("Success! file: "+file+" written to database.")

            elif file.startswith('member'):
                with open(file,'r',encoding='utf8') as filename:
                    reader = csv.reader(filename)
                    next(reader)
                    for row in reader:
                        if len(row) < 5:
                            continue
                        row = row[1:11]+row[-5:]
                        if row[2].lower() == 'us':
                            cities = ['chicago','san francisco','new york']
                            if any(city in row[1].lower() for city in cities):
                                if row[0]:
                                    row[0] = row[0].strip().replace("\"","")
                                if row[9]:
                                    row[9] = row[9].strip().replace("\"","")
                                if row[5]:
                                    row[5] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(row[5])/1000))
                                if row[13]:
                                    row[13] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(row[13])/1000))
                                try:
                                    with connection.cursor() as cursor:
                                        sql = "INSERT INTO `members` (`member_id`,`bio`,`city`,`country`,`hometown`,`joined`,`lat`,`link`,`lon`,`member_name`,`state`,`member_status`,`visited`,`group_id`) VALUES (%d,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%f,\"%s\",%f,\"%s\",\"%s\",\"%s\",\"%s\",%d)" % (int(row[4]), row[0].encode('ascii','ignore').decode("utf-8").replace("\"","").strip().replace("\\","") if row[0] else 'not_found', row[1] if row[1] else 'not_found', row[2] if row[2] else 'not_found', row[3].encode('ascii','ignore').decode("utf-8").replace("\"","").strip() if row[3] else 'not_found', row[5] if row[5] else datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), float(row[6]) if row[6] else 0.0, row[7] if row[7] else 'not_found', float(row[8]) if row[8] else 0.0, row[9].encode('ascii','ignore').decode("utf-8").replace("\"","").replace("\\","").strip() if row[9] else 'not_found', row[10] if row[10] else 'not_found', row[11] if row[11] else 'others', row[13] if row[13] else datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), int(row[14]) if row[14] else -1)
                                        #print(sql)
                                        cursor.execute(sql)
                                        connection.commit()
                                except MySQLError as e:
                                    if e.args[0] != 1452 and e.args[0]!=1062: # foreign key constraint error and duplicate primary key
                                        print(sql)
                                        print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                print("Success! file: "+file+" written to members table in database.")
                with open(file,'r',encoding='utf8') as filename:
                    reader = csv.reader(filename)
                    next(reader)
                    for row in reader:
                        if len(row) < 5:
                            continue
                        row = row[1:11]+row[-5:]
                        if row[2].lower() == 'us':
                            cities = ['chicago','san francisco','new york']
                            if any(city in row[1].lower() for city in cities):
                                if row[12] and len(row[12])>2:
                                    retList = parse_members_topics(row[12][1:-1])
                                    if retList:
                                        for temp_row in retList:
                                            try:
                                                with connection.cursor() as cursor:
                                                    sql = "INSERT INTO `members_topics` (`topic_id`, `topic_key`, `topic_name`, `member_id`) VALUES (%d,\"%s\",\"%s\",%d)" % (int(temp_row[2]), temp_row[0].encode('ascii','ignore').decode("utf-8").replace("\"","").strip(), temp_row[1].encode('ascii','ignore').decode("utf-8").replace("\"","").strip(), int(row[4]))
                                                    cursor.execute(sql)
                                                    connection.commit()
                                            except MySQLError as e:
                                                if e.args[0] != 1452 and e.args[0]!=1062:  # foreign key constraint error and duplicate primary key
                                                    print(sql)
                                                    print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                print("Success! file: "+file+" written to members_topics table in database.")
            elif file.startswith('cit'):
                with open(file,'r',encoding='utf8') as filename:
                    reader = csv.reader(filename)
                    next(reader)
                    for row in reader:
                        if row[1] == 'us':
                            cities = ['chicago','san francisco','new york']
                            if any(city in row[0].lower() for city in cities):
                                try:
                                    with connection.cursor() as cursor:
                                        sql = "INSERT INTO `cities` (`city_id`,`city`,`country`,`distance`,`latitude`,`localized_country_name`,`longitude`,`member_count`,`ranking`,`state`,`zip`) VALUES (%d,\"%s\",\"%s\",%f,%f,\"%s\",%f,%d,%d,\"%s\",%d)" % (int(row[3]), row[0].encode('ascii','ignore').decode("utf-8").strip() if row[0] else 'not_found', row[1] if row[1] else 'not_found', float(row[2]) if row[2] else 0.0, float(row[4]) if row[4] else 0.0, row[5] if row[5] else 'not_found', float(row[6]) if row[6] else 0.0, int(row[7]) if row[7] else -1, int(row[8]) if row[8] else -1, row[9] if row[9] else 'not_found', int(row[10]) if row[10] else -1)
                                        #print(sql)
                                        cursor.execute(sql)
                                        connection.commit()
                                except MySQLError as e:
                                    if e.args[0]!=1062: # duplicate primary key
                                        print(sql)
                                        print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                print("Success! file: "+file+" written to database.")
            elif file.startswith('categor'):
                with open(file,'r',encoding='utf8') as filename:
                    reader = csv.reader(filename)
                    next(reader)
                    for row in reader:
                        try:
                            with connection.cursor() as cursor:
                                sql = "INSERT INTO `categories` (`category_id`,`category_name`,`shortname`,`sort_name`) VALUES (%d,\"%s\",\"%s\",\"%s\")" % (int(row[0]), row[1] if row[1] else 'not_found', row[2] if row[2] else 'not_found', row[3] if row[3] else 'not_found')
                                #print(sql)
                                cursor.execute(sql)
                                connection.commit()
                        except MySQLError as e:
                            print(sql)
                            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                print("Success! file: "+file+" written to database.")
#            elif file.startswith('main_topic'):
#                with open(file,'r',encoding='utf8') as filename:
#                    reader = csv.reader(filename)
#                    next(reader)
#                    for row in reader:
#                        for cat in ast.literal_eval(row[0]):
#                            parsed_list = parse_topics(row[6])
#                            try:
#                                with connection.cursor() as cursor:
#                                    sql = "INSERT INTO `main_topics` (`main_topic_id`,`topic_name`,`topic_key`,`shortname`,`sort_name`,`icon`,`photo`,`category_id`) VALUES (%d,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%d)" % (int(parsed_list[0][2]), parsed_list[0][1] if parsed_list[0][1] else 'not_found', parsed_list[0][0] if parsed_list[0][0] else 'not_found', row[4] if row[4] else 'not_found', row[5] if row[5] else 'not_found', row[1] if row[1] else 'not_found', row[3] if row[3] else 'not_found',cat)
#                                    cursor.execute(sql)
#                                    connection.commit()
#                            except MySQLError as e:
#                                print(sql)
#                                print('Got error {!r}, errno is {}'.format(e, e.args[0]))
#                print("Success! file: "+file+" written to database.")
            elif file.startswith('topic'):
                with open(file,'r',encoding='utf8') as filename:
                    reader = csv.reader(filename)
                    next(reader)
                    for row in reader:
                        try:
                            with connection.cursor() as cursor:
                                sql = "INSERT INTO `topics` (`topic_id`, `description`, `link`, `members`, `topic_name`, `urlkey`, `main_topic_id`) VALUES (%d,\"%s\",\"%s\",%d,\"%s\",\"%s\",%d)" % (int(row[2]), row[1].encode('ascii','ignore').decode("utf-8").replace("\"","").strip() if row[1] else 'not_found', row[3] if row[3] else 'not_found', int(row[4]), row[5].replace("\"","") if row[5] else 'not_found', row[7]  if row[7] else 'not_found', int(row[8]))
                                cursor.execute(sql)
                                connection.commit()
                        except MySQLError as e:
                            if e.args[0] != 1062:
                                print(sql)
                                print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                print("Success! file: "+file+" written to database.")
    connection.close()
                
if __name__ == "__main__":
    clean_csv_files()