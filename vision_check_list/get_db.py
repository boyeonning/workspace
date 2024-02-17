import pandas as pd 

from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class GetDB:

    def __init__(self):
        engine = create_engine(f"postgresql://vision:DlsXjAkDlsWm@smart-retail-db.ctnphj2dxhnf.ap-northeast-2.rds.amazonaws.com:5432/emart24", poolclass=NullPool)
        self.session = scoped_session(sessionmaker(bind=engine))
    
    def vision_check_list(self, store_id, device_id):
        sql = f""" 
        select sh.shelf_floor+1 as floor, ce.cell_column+1 as column, (select goods_name from goods where goods_id = des.goods_id) as goods_name, des.goods_id
        from stores st, devices dev, shelves sh, cells ce, designs des
        where st.store_pkey = dev.store_pkey
        and dev.device_pkey = sh.device_pkey
        and sh.shelf_pkey = ce.shelf_pkey
        and ce.design_pkey_master = des.design_pkey
        and dev.operation = 'true'
        and st.store_id = '{store_id}'
        and dev.device_id = '{device_id}'
        and ce.inference_mode = 'lc'
        order by floor desc, ce.cell_column desc;
            """
        result = self.session.execute(sql)
        result = result.fetchall()

        self.session.close()
        return pd.DataFrame(result, columns=['floor', 'column', 'goods_name', 'goods_id']) 
    


