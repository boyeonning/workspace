import json
from sqlite3 import DatabaseError

from time import sleep
from get_db import GetDB
from datetime import datetime
from notion_client import Client
from pprint import pprint


class VisionCheckList:
    def __init__(self):
        notion_secret = 'secret_JbyPk8hmupViZqpMtMwiuQGoUisHJqJs6satah7f6Pe'
        self.notion = Client(auth=notion_secret)

    def get_database_id(self):
        pages = self.notion.search(filter={"property": "object", "value": "page"}, page_size=10)

        for page in pages['results']:
            date = page['last_edited_time'].split('T')[0]
            pprint(page)
        
            # if '비전 test' in page['properties'].keys():
                # print(page)
                # print(page['id'])
                # print(page['parent']['database_id'])

    def run(self, store_id):
        db = GetDB()
        df = db.vision_check_list(store_id=store_id)
        
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
        # create page(row)
            self.notion.pages.create(parent={'database_id': 'a909dd1ada364a38abf766cf3574ff2d'},
                                properties=properties_new)
            print(df.iloc[row])


    def run2(self):
        today = datetime.today().strftime('%Y-%m-%d')
        properties_new = {
        '지점 회사': {
            'type': 'select',
            'select': {
                'name': '양식',
                'color': 'green'
            }
        },
        '작성자': {
            'type': 'select',
            'select': {
                'name': '호호호 연구원',
                'color': 'gray'
            }
        },
        '설치 날짜': {
            'type': 'date',
            'date': {
                'start': f'{today}',
                'end': None,
                'time_zone': None
            }
        },
        '승인': {
            'type': 'select',
            'select': {
                'name': '123 책임',
                'color': 'orange'
            }
        },
        '지점명': {
            'type': 'multi_select',
            'multi_select': [{
                'name': 'test',
                'color': 'orange'
            }]
        },
        '비고': {
            'type': 'title',
            'title': [{
                'type': 'text',
                'text': {
                    'content': 'Vision 체크리스트',
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
                'plain_text': 'Vision 체크리스트',
                'href': None
            }]
        }}

        self.notion.pages.create(parent={'database_id': '97fc2bd26c864ca5bc1d75357f0cb835'},
                                properties=properties_new)

if __name__ == "__main__":
    visioncheck = VisionCheckList()
    page_id = '28d5db55ffd84bedb7bfb8e11115c36e'
    blocks = visioncheck.notion.blocks.children.list(block_id=page_id)

    for i in ['a', 'b' , 'c']:
        children_block_a = {'heading_3': {'color': 'default',
                        'is_toggleable': False,
                        'rich_text': [{'annotations': {'bold': False,
                                                    'code': False,
                                                    'color': 'default',
                                                    'italic': False,
                                                    'strikethrough': False,
                                                    'underline': False},
                                    'href': None,
                                    'plain_text': i,
                                    'text': {'content': i,
                                                'link': None},
                                    'type': 'text'}]}}
        
        children_blocks = []
        children_blocks.append(children_block_a)
  

        visioncheck.notion.blocks.children.append(block_id=page_id, children=children_blocks)
