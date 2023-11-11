import data_dicts as dicts

ciclos = list(dicts.dict_ciclos.keys())
cultivos = list(dicts.dict_cultivos.keys())
meses = list(dicts.dict_mes.keys())
modalidad = list(dicts.dict_modalidad.keys())
anios = [2018 + i for i in range(6)]

selector_data = {
    'Anio':['2020'],
    'Ciclos':['Otoño - Invierno'],
    'Cultivos':['Aguacate'],
    'Meses':['Enero'],
    'Modalidad':['Riego']
}

selector_data_gen = {
    'Anio':['2020'],
    'Ciclos':['Otoño - Invierno'],
    'Cultivos':['Aguacate'],
    'Meses':[],
    'Modalidad':[]
}

def check_subset(sub , set):
    s_len = len(sub)
    check = 0
    if s_len > 0:
        check = 1
        s_c = 0
        for e in sub:
            while check > 0:
                try:
                    a = set.index(e)
                    s_c =s_c + 1
                    if s_c == s_len:
                        # print('is a subset of set')
                        check = 0
                except:
                    # print('not subset of the set')
                    check = -1
    else:
        check = check_subset(set,set)
    return check

def verif_selector(selector):
    t_s = 0
    all_data = [anios, ciclos, cultivos, meses, modalidad]
    all_filters = ['Anio','Ciclos','Cultivos','Meses','Modalidad']
    all_size = len(all_data)
    for i in range(all_size):
        t_s = t_s + check_subset(selector[all_filters[i]],all_data[i])
    if t_s == 0:
        print('is a valid selector')
    else: 
        print('check selector')
    return t_s