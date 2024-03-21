model_name = ['zst_asahi'
,'zst_belgium_pilsner_500'
,'zst_belgium_weizen_500'
,'zst_budweiser'
,'zst_cass_fresh_355'
,'zst_cass_fresh_500'
,'zst_cass_light_500'
,'zst_cass_zero_355'
,'zst_edelweiss_500'
,'zst_export'
,'zst_filgood'
,'zst_filite_fresh_500'
,'zst_guinness_440'
,'zst_hanmac_500'
,'zst_heineken_500'
,'zst_hoegaarden_500'
,'zst_iseul_tok_tok_355'
,'zst_jipyeong_makgeolli_750'
,'zst_kgb_lemon_355'
,'zst_kloud_500'
,'zst_kloud_draft_500'
,'zst_somersby_500'
,'zst_soonhari_lemon_4_355'
,'zst_soonhari_lemon_7_355'
,'zst_stella_artois_500_can'
,'zst_test_chamisul_fresh_pet_640'
,'zst_tsingtao_500']


import pandas as pd

df = pd.DataFrame(columns = ['start', 'end', 'sec'])
# print(df)
rst = []
for i in model_name[:15]:
    idx=0
    path = f'/data1/log/ai_engine/fr/cls/{i}/qt_mobilenetv3_small_075/2022-10-05.log'
    fileTest = open(path,'rt')
    fileLines = fileTest.readlines()
    model_name = i

    start = fileLines[-3].split(' ')[1]
    end = fileLines[-2].split(' ')[1]
    sec = fileLines[-1].split(' ')[-1].split('s')[0]

    rst.append([model_name, start, end, sec])
    # df.loc[idx] = [start, end, sec]
    # idx+=1
    # rst = rst.append([start, end, sec])
df = pd.DataFrame(rst)
df.to_csv('./rst.csv')
print(df)
    # for line in fileLines[-3:-1][]:
    #     # print(line)
    #     print(line.split(' ')[1])
    # print(fileLines[-1].split(' ')[-1])

