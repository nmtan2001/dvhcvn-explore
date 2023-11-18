import json
import pprint
import sys
import os
from colorama import Fore, Back, Style
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

        select = input('Select city: ')

        #by number
        try: 
            select = int(select)
        except ValueError:
            pass
        else: 
            if select > len(country):
                print('Invalid city')
                continue
            else: 
                for i, city in enumerate(country):
                    if i+1 == int(select):
                        print(city)
                        run(city)
                        sys.exit()
                    else: 
                        i+=1
                        
        if isinstance(select, str): 
            #by name     
            select = remove_diacritics(select).lower()

            select = re.sub(r"(thanh pho|tinh)",'',select,re.IGNORECASE).strip()

            for level1 in country:
                match = re.search(r"(?:Thành phố|Tỉnh) (?:\s+)?(.*)", level1,re.IGNORECASE)
                if remove_diacritics(match.group(1).lower()) == select.lower():
                    print(level1)
                    # return level1
                    run(level1)
                    sys.exit()

            #no match:
            print('Invalid city')

def list_city(country):
    for i, level1 in enumerate(country):
        print(i+1, level1)

def stat_city(country, city):
    level2_count = len(country[city]['level2s'])
    level3_count = country[city]['count']
    return level2_count, level3_count

def get_district(country, city):
    while True:
        select = input('Select district: ')
            
        #by number
        try: 
            select = int(select)
        except ValueError:
            pass
        else: 
            if select > len(country[city]['level2s']):
                print('Invalid district')
                continue
            for i, district in enumerate(country[city]['level2s']):
                if i+1 == int(select):
                    print(district)
                    run(city, district)
                    sys.exit()
                else: 
                    i+=1
        if isinstance(select, str): 
            #by name  
            select = remove_diacritics(select).lower()
            #exit
            if select == 'q':
                sys.exit()
            select = re.sub(r"(quan|huyen|thi xa|thanh pho)",'',select,re.IGNORECASE).strip()

            for level2 in country[city]['level2s']:
                match = re.search(r"(?:Quận|Huyện|Thị xã|Thành phố) (?:\s+)?(.*)", level2,re.IGNORECASE)
                if remove_diacritics(match.group(1).lower()) == select.lower():
                    print(level2)
                    run(city, level2)
                    sys.exit()
                    return level2
            
            #no match:
            print('Invalid district')

def list_district(country, city):
    for i, level2 in enumerate(country[city]['level2s']):
        print(i+1, level2)

def get_commune(country, city, district):
    while True:      
        select = input('Select commune: ')
            
        #by number
        try: 
            select = int(select)
        except ValueError:
            pass
        else:
            if select > len(country[city]['level2s'][district]['level3s']):
                print('Invalid commune')
                continue
            else:  
                for i, commune in enumerate(country[city]['level2s'][district]['level3s']):
                    if i+1 == int(select):
                        print(commune)
                        run(city, district, commune)
                        sys.exit()
                        return commune
                    else: 
                        i+=1

        #by name        
        if isinstance(select, str): 
            select = remove_diacritics(select).lower()

            #exit
            if select == 'q':
                sys.exit()
            select = re.sub(r"(xa|phuong|thi tran)",'',select,re.IGNORECASE).strip()


            for level3 in country[city]['level2s'][district]['level3s']:
                match = re.search(r"(?:Xã|Phường|Thị trấn) (?:\s+)?(.*)", level3,re.IGNORECASE)
                if remove_diacritics(match.group(1).lower()) == select.lower():
                    print(commune)
                    run(city, district, level3)
                    sys.exit()
                    return level3
        
            #no match:
            print('Invalid commune')

def list_communes(country, city, district):
    for i, level2 in enumerate(country[city]['level2s'][district]['level3s']):
        print(i+1, level2)     

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

def data_explore(*args):
    if len(args) == 1:
        level1_count, level2_count, level3_count = total(args[0])
        return f"Number of cities: {level1_count}\nNumber of districts: {level2_count}\nNumber of communes: {level3_count}"

    if len(args) == 2:
        country = args[0]
        city = args[1]
        number_of_level2s, number_of_level3s = stat_city(country, city)
        return (f"Number of districts and communes for {city}: {number_of_level2s} districts, {number_of_level3s} communes")
    
    if len(args) == 3:
        country = args[0]
        city = args[1]
        district = args[2]
        level3_count = country[city]['level2s'][district]['count']
        return (f"Number of communes for {district } of {city} : {level3_count} communes")

def bold(type): sys.stdout.write("\033[1m" + type + "\033[0m")

def intro():
    print('Choose what you want to do: ' + Fore.BLUE + 'e (explore) ' + Fore.GREEN + 's (statistic) '+ Fore.YELLOW + 'l (show list of administrative units) ' + Fore.RED + 'q (quit)')
    return input(Style.RESET_ALL + 'What would you like to do? ')

def run(*args):
    country = get_country()
    if len(args) == 0:
        act = intro()
        while act != 'q':
            match act:
                case 'e': 
                    get_city(country)
                case 's': 
                    print(data_explore(country))
                    act = intro()
                case 'l':
                    list_city(country)
                    act = intro()
                case 'q': sys.exit()
                case _:
                    act = intro()
    if len(args) == 1:
        act = intro()
        if act == 'q': sys.exit()
        while act != 'q':
            match act:
                case 'e': 
                    get_district(country, args[0])
                case 's': 
                    print(data_explore(country, args[0]))
                    act = intro()
                case 'l':
                    list_district(country, args[0])
                    act = intro()
                case 'q': sys.exit()
                case _:
                    act = intro()
    if len(args) == 2:
        act = intro()
        if act == 'q': sys.exit()
        while act != 'q':
            match act:
                case 'e': 
                    get_commune(country, args[0], args[1])
                case 's': 
                    print(data_explore(country, args[0], args[1]))
                    act = intro()
                case 'l':
                    list_communes(country, args[0], args[1])
                    act = intro()
                case 'q': sys.exit()
                case _:
                    act = intro()
    if len(args) == 3:
        bold(f"{Fore.BLUE + args[0]} > { Fore.CYAN + args[1]} > {Fore.GREEN +  args[2]}\n")
        bold(Fore.LIGHTRED_EX + 'Thanks for playing\n')

def main():
    bold("Let's explore Vietnam !\n")
    print('Data provided by: https://github.com/daohoangson/dvhcvn')
    run()

if __name__ == "__main__":
    main()
