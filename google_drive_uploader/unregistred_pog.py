import time
import gspread
import numpy as np
import pandas as pd
from color_cell import request_update

from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from oauth2client.service_account import ServiceAccountCredentials


def open_worksheet(key, sheet_name=None):
    '''
    ★신규 설치 관련 정보★ 
    sheet_name 입력 안하면 맨 앞 시트 
    '''
    scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    ]
    json_file_name = 'key_1.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)

    if key is not None:
        doc = gc.open_by_key(key)

    if sheet_name is None:
        worksheet = doc.get_worksheet(0)
    else:
        worksheet = doc.worksheet(sheet_name)
    return worksheet 

def get_barcode_from_sheet(worksheet, sheet_range=None, mode=False):
    '''
    1. range가 None 일 경우에는 전체 셀에서 8자리 이상 숫자 가져오기 (바코드는 13자리이지만 db 등록된 바코드가 8자리도 있어서..)
    2. range 지정될 경우는 범위 내에서만 8자리 이상 숫자 가져오기
    '''
    
    if sheet_range is None: # 모든 셀일경우
        values_list = worksheet.get_all_values()
        values_list = np.array(values_list).reshape(-1)
        # raw_barcode_list = [barcode for barcode in values_list if barcode.strip().isdigit() and len(barcode)>=8]#strip안된거
        # barcode_list = [barcode.strip() for barcode in values_list if barcode.strip().isdigit() and len(barcode)>=8]

    else: # 범위 지정일 경우
        values_list = worksheet.batch_get([sheet_range])
        values_list = np.array(values_list).reshape(-1)

    if mode == True:
        temp = ([value.split('/') for value in values_list if '/' in value])
        temp = sum(temp, [])
        barcode_list = [i for i in temp if i.isdigit() and len(i) >= 8]  
        raw_barcode_list = barcode_list
        return barcode_list, raw_barcode_list
    else:
        raw_barcode_list = [barcode for barcode in values_list if barcode.strip().isdigit() and len(barcode)>=8]#strip안된거
        barcode_list = [barcode.strip() for barcode in values_list if barcode.strip().isdigit() and len(barcode)>=8]
            # barcode_list = [barcode.strip() for value in values_list for barcode in value if barcode!= [] and barcode.strip().isdigit() and len(barcode)>=8]
        return barcode_list, raw_barcode_list

def get_db_info(product_101=False):
    engine = create_engine(
        f"postgresql://vision:DlsXjAkDlsWm@smart-retail-db.ctnphj2dxhnf.ap-northeast-2.rds.amazonaws.com:5432/emart24",
        poolclass=NullPool)
    session = scoped_session(sessionmaker(bind=engine))
    if product_101:
        sql = """
            select
            d.goods_id,
            d.design_infer_label,
            g.goods_name,
            d.product_101
            from
            designs d,
            goods g
            where d.goods_id = g.goods_id
            and d.product_101 = 'true'
        """
    else:
        sql = """
            select
            d.goods_id,
            d.design_infer_label,
            g.goods_name
            from
            designs d,
            goods g
            where
            d.goods_id = g.goods_id """
    
    try:
        # result = session.execute(sql).all()
        result = session.execute(sql)
        result = result.fetchall()
        session.close()
        return result
        
    except Exception as e:
        print(e)
        session.close()
        return []

def trans_coord(row, col):
    col_list = [chr(i) for i in range(65,91)]
    col_name = f'{col_list[col-1]}{row}'
  
    return col_name

def fill_bgr_color(worksheet, barcode, r, g, b, alpha):
    '''
    지정한 셀에 색 넣어주기
    '''
    for cell in worksheet.findall(barcode):
        print(cell)
        row, cols = cell.row, cell.col
        cell_address = trans_coord(row,cols)
        worksheet.format(cell_address,  {
            "backgroundColor": {
            "red": r,
            "green": g,
            "blue": b,
            "alpha" : alpha
            },
            "horizontalAlignment": "CENTER",
            "textFormat": {
            "foregroundColor": {
                "red": 0.0,
                "green": 0.0,
                "blue": 0.0
            },
            "bold": False
            }
})



def run(key,  sheet_name=None, sheet_range=None, mode=False, product_101=False, cell_color=None):
    worksheet = open_worksheet(key, sheet_name) # 파일 열기
    barcode, raw_barcode  = get_barcode_from_sheet(worksheet, sheet_range, mode) # 시트 이름, 범위 지정
    

    df = pd.DataFrame(get_db_info(product_101))
    print(df)
    db_barcode = df.iloc[:,0].to_list() 

    
    # for b in barcode: -> requesting higher quota 
    #     if b in db_barcode:
    #         fill_bgr_color(worksheet, b, '1.', '1.', '1.', '1.0')
    #     else:
    #         fill_bgr_color(worksheet, b, '0.6', '0.9', '0.98', '0.7')

   
    # 등록된건 하얀색으로 바꾸쟈 -> 이부분은... 음 쓸지 말지??? 
    # registered_barcode = list(set(barcode) & set(db_barcode))
    # raw_sheet_barcode = ([raw_barcode[barcode.index(bb)] for bb in registered_barcode])
    # for r in raw_sheet_barcode:
    #     fill_bgr_color(worksheet, r, '1.', '1.', '1.', '1.0')
 

    # 미등록은 색표시
    unregistered_barcode = list(set(barcode) - set(db_barcode))
    print(unregistered_barcode)
    raw_sheet_barcode = ([raw_barcode[barcode.index(bb)] for bb in unregistered_barcode])
    red,green,blue = (183/255), (240/255), (177/255)

    for b in raw_sheet_barcode:
        if mode == False:
            try : 
                if cell_color is not None:
                    rgb = tuple(map(lambda x:round(x/255,2), cell_color))
                    red,green,blue = rgb[0], rgb[1], rgb[2]
                    fill_bgr_color(worksheet, b, red, green, blue, '0.7')
                else:
                    fill_bgr_color(worksheet, b, '1.0', '0.6', '0.8', '0.7')

            except Exception as e:
                unregistered_barcode.append(b)
                print("backoff")
                time.sleep(60) # temp
        else:
            request_update(key, worksheet.id, b)

    content = f'시트 이름 : {worksheet} 🤬미등록 바코드 개수 : {len(unregistered_barcode)}'
    
    return content
    
if __name__ == "__main__":
    # run(sheet_name=None, sheet_range='D17:D21') 
    key = '1sPpd-ANd2qqx02SFSH3NusQsuzvEMdyWjIpsrUPDKM0'
    cell_color = (204, 212, 181)
    print(run(key, mode=False, product_101=False))
 

