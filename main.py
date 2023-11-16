import json
import pprint
import sys
import re

def get_country():
    with open('dvhcvn.json') as f:
        data = json.load(f)
    # print(json.dumps(data_by_level1, indent=4))

    data_by_level1 = {}
    for level1 in data['data']:
        level1_name = level1['name']
        data_by_level1[level1_name] = {'level2s': {}, 'count': 0}

        for level2 in level1['level2s']:
            level2_name = level2['name']
            data_by_level1[level1_name]['level2s'][level2_name] = {'level3s': [], 'count': 0}

            for level3 in level2['level3s']:
                level3_name = level3['name']
                data_by_level1[level1_name]['level2s'][level2_name]['level3s'].append(level3_name)
                data_by_level1[level1_name]['count'] += 1
                data_by_level1[level1_name]['level2s'][level2_name]['count'] += 1
    return data_by_level1

def remove_diacritics(name):
    vietnamese_diacritics_a = r"[à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ]"
    name = re.sub(vietnamese_diacritics_a, "a", name,flags=re.IGNORECASE)
    vietnamese_diacritics_u = r"[ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ]"
    name = re.sub(vietnamese_diacritics_u, "u", name,flags=re.IGNORECASE)
    vietnamese_diacritics_i = r"[ì|í|ị|ỉ|ĩ]"
    name = re.sub(vietnamese_diacritics_i, "i", name,flags=re.IGNORECASE)
    vietnamese_diacritics_o = r"[ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ]"
    name = re.sub(vietnamese_diacritics_o, "o", name,flags=re.IGNORECASE)
    vietnamese_diacritics_e = r"[è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ]"
    name = re.sub(vietnamese_diacritics_e, "e", name,flags=re.IGNORECASE)
    vietnamese_diacritics_y = r"[ỳ|ý|ỵ|ỷ|ỹ]"
    name = re.sub(vietnamese_diacritics_y, "y", name,flags=re.IGNORECASE)
    vietnamese_diacritics_d = r"[đ]"
    name = re.sub(vietnamese_diacritics_d, "d", name,flags=re.IGNORECASE)
    vietnamese_diacritics_special = r"[!|@|%|\^|\*|\(|\)|\+|\=|\<|\>|\?|\/|,|\.|\:|\;|\'|\"|\&|\#|\[|\]|~|\$|_|`|-|{|}|\||\\]"
    name = re.sub(vietnamese_diacritics_special, "", name,flags=re.IGNORECASE)
    name = re.sub(r"\s+", " ", name)
    name = name.strip()
    return name

def get_city(country):
    while True:
        for i, level1 in enumerate(country):
            print(i+1, level1)
        select = input('Select city: ')

        #by number
        try: 
            select = int(select)
        except ValueError:
            pass
        else: 
            for i, city in enumerate(country):
                if i+1 == int(select):
                    print(city)
                    return city
                else: 
                    i+=1

        #by name        
        select = remove_diacritics(select).lower()

        #exit
        if select == 'q':
            sys.exit()

        select = re.sub(r"(thanh pho|tinh)",'',select,re.IGNORECASE).strip()

        for level1 in country:
            match = re.search(r"(?:Thành phố|Tỉnh) (?:\s+)?(.*)", level1,re.IGNORECASE)
            if remove_diacritics(match.group(1).lower()) == select.lower():
                return level1
        
        #no match:
        print('Invalid city')

def get_district(country, city):
    while True:
        for i, level2 in enumerate(country[city]['level2s']):
            print(i+1, level2)            
        select = input('Select district: ')
            
        #by number
        try: 
            select = int(select)
        except ValueError:
            pass
        else: 
            for i, district in enumerate(country[city]['level2s']):
                if i+1 == int(select):
                    print(district)
                    return district
                else: 
                    i+=1

        #by name        
        select = remove_diacritics(select).lower()
        # print(select)
        #exit
        if select == 'q':
            sys.exit()
        select = re.sub(r"(quan|huyen|thi xa|thanh pho)",'',select,re.IGNORECASE).strip()
        # print(select)


        for level2 in country[city]['level2s']:
            match = re.search(r"(?:Quận|Huyện|Thị xã|Thành phố) (?:\s+)?(.*)", level2,re.IGNORECASE)
            if remove_diacritics(match.group(1).lower()) == select.lower():
                return level2
        
        #no match:
        print('Invalid district')

def get_commune(country, city, district):
    while True:
        for i, level2 in enumerate(country[city]['level2s'][district]['level3s']):
            print(i+1, level2)            
        select = input('Select commune: ')
            
        #by number
        try: 
            select = int(select)
        except ValueError:
            pass
        else: 
            for i, commune in enumerate(country[city]['level2s'][district]['level3s']):
                if i+1 == int(select):
                    print(commune)
                    return commune
                else: 
                    i+=1

        #by name        
        select = remove_diacritics(select).lower()

        #exit
        if select == 'q':
            sys.exit()
        select = re.sub(r"(xa|phuong|thi tran)",'',select,re.IGNORECASE).strip()


        for level3 in country[city]['level2s'][district]['level3s']:
            match = re.search(r"(?:Xã|Phường|Thị trấn) (?:\s+)?(.*)", level3,re.IGNORECASE)
            if remove_diacritics(match.group(1).lower()) == select.lower():
                return level3
        
        #no match:
        print('Invalid commune')

def explore(country):
    city = get_city(country)
    # print(city)
    district = get_district(country, city)
    # print(district)
    commune = get_commune(country, city, district)
    # print(commune)
    return f"{city} > {district} > {commune}"

def total(country):
    level1_count = len(country)
    level2_count = 0
    level3_count = 0
    for level1 in country:
        level2_count += len(country[level1]['level2s'])
        level2s = country[level1]['level2s']
        for level2 in level2s:
            level3_count += level2s[level2]['count']

    return level1_count, level2_count, level3_count

def stat_city(country, city):
  level2_count = len(country[city]['level2s'])
  level3_count = country[city]['count']
  return level2_count, level3_count

def data_explore(country):
    level1_count, level2_count, level3_count = total(country)

    print(f"Number of level 1: {level1_count}")
    print(f"Number of level 2: {level2_count}")
    print(f"Number of level 3: {level3_count}")
    level1_name = "Thành phố Cần Thơ"
    number_of_level2s, number_of_level3s = stat_city(country, level1_name)
    print(f"Number of level 2s for level 1 '{level1_name}': {number_of_level2s}, {number_of_level3s}")

def main():
    country = get_country()
    # pprint.pprint(country)
    data_explore(country)
    # print(explore(country))


if __name__ == "__main__":
    main()
