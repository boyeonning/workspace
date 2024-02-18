#!/usr/bin/env python3
import argparse

from get_db import GetDB
from notion_client import Client

class VisionCheckList:
    def __init__(self):
        notion_secret = 'secret_JbyPk8hmupViZqpMtMwiuQGoUisHJqJs6satah7f6Pe' # 예전 vision secret key
        # notion_secret = 'secret_JBdxSewTbeeeC4BA0zTYojhXQC3Nbsap6BJ4atBmT4j' # 중석님 발급
        self.notion = Client(auth=notion_secret)

    def get_id(self): # 가장 최신의 database만 가져옴
        pages = self.notion.search(filter={"property": "object", "value": "page"})
        page = [page for page in pages['results'] if '비전 test' in page['properties'].keys()]
                
        page_id = page[0]['id']
        database_id = page[0]['parent']['database_id']
        # page_id = page['results'][0]['id']
        # database_id = page['results'][0]['parent']['database_id']
        return page_id, database_id
        # return page, page_id, database_id
        
    def get_lc_list(self, store_id, device_id):
        db = GetDB()
        df = db.vision_check_list(store_id, device_id)
        return df

    def write_vision_check_list(self, database_id, store_id, device_id):
        df = self.get_lc_list(store_id, device_id)

        if df.empty:
            return ('DataFrame is empty!')
            
        else:
            for row in range(len(df)):
                floor = df['floor'].iloc[row]
                column = df['column'].iloc[row]
                goods_name = df['goods_name'].iloc[row]
                goods_id = df['goods_id'].iloc[row]

                properties_new = {
                        '비전 test': {
                            'type': 'rich_text',
                            'rich_text': [{
                                'type': 'text',
                                'text': {
                                    'content': '',
                                    'link': None
                                },
                                'annotations': {
                                    'bold': False,
                                    'italic': False,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': 'default'
                                },
                                'plain_text': '',
                                'href': None
                            }]
                        },
                        'POG': {
                            'type': 'rich_text',
                            'rich_text': [{
                                'type': 'text',
                                'text': {
                                    'content': f'{goods_name}',
                                    'link': None
                                },
                                'annotations': {
                                    'bold': False,
                                    'italic': False,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': 'default'
                                },
                                'plain_text': f'{goods_name}',
                                'href': None
                            }]
                        },
                        'mix 전환 여부': {
                            'type': 'checkbox',
                            'checkbox': False
                        },
                        '열': {
                            'type': 'rich_text',
                            'rich_text': [{
                                'type': 'text',
                                'text': {
                                    'content': f'{column}',
                                    'link': None
                                },
                                'annotations': {
                                    'bold': False,
                                    'italic': False,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': 'default'
                                },
                                'plain_text': '',
                                'href': None
                            }]
                        },
                        '바코드': {
                            'type': 'rich_text',
                            'rich_text': [{
                                'type': 'text',
                                'text': {
                                    'content': f'{goods_id}',
                                    'link': None
                                },
                                'annotations': {
                                    'bold': False,
                                    'italic': False,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': 'default'
                                },
                                'plain_text': f'{goods_id}',
                                'href': None
                            }]
                        },
                        'LC 전환 사유': {
                            'type': 'rich_text',
                            'rich_text': [{
                                'type': 'text',
                                'text': {
                                    'content': '',
                                    'link': None
                                },
                                'annotations': {
                                    'bold': False,
                                    'italic': False,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': 'default'
                                },
                                'plain_text': '',
                                'href': None
                            }]
                        },
                        '단': {
                            'id': 'title',
                            'type': 'title',
                            'title': [{
                                'type': 'text',
                                'text': {
                                    'content': f'{floor}',
                                    'link': None
                                },
                                'annotations': {
                                    'bold': False,
                                    'italic': False,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': 'default'
                                },
                                'plain_text': '',
                                'href': None
                            }]
                        }
                    }
                self.notion.pages.create(parent={'database_id': database_id}, properties=properties_new)
                # try:
                #     print(df)
                    
                #     # return f'Completed writing the checklist!'
                # except Exception as e:
                #     print(e)
                #     return e
            



if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-s', '--store_id', type=str)
    # parser.add_argument('-l', '--database_link', type=str)
    # parser.add_argument('-d', '--device_id', type=str)
    # args = parser.parse_args()

    vc = VisionCheckList()
    store_id = '05282'
    device_id = 'w_00001'
    # database_link = 'https://www.notion.so/interminds/e642a61fd7394f9a9646ea58ea0dd8f6?v=785009a1343840769165d4670151d6e3&pvs=4'
    # database_id = (database_link.split('/')[-1].split('?')[0])
    database_id = 'd054f1d782704cc08a9893d24a53e389'

    print(database_id)
    # # database_id = args.database_link.split('/')[-1].split('?')[0] 
    # # store_id= args.store_id
    # # device_id = args.device_id
    vc.write_vision_check_list(database_id, store_id, device_id)
