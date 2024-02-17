import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from vision_check_list import VisionCheckList

app = FastAPI()

class Item(BaseModel):
    store_id : str
    database_id : str
    device_id : str

@app.get("/")
async def root():
    return "hello"

@app.post('/visionchecklist')
async def run(item : Item):
    ret = True
    try:
        store_id = item.store_id
        database_id = item.database_id.split('/')[-1].split('?')[0]
        device_id = item.device_id
        vc = VisionCheckList()
        rst = vc.write_vision_check_list(database_id, store_id, device_id)
        return rst
    except Exception as e:
        print(e)
        ret = e
    return ret

if __name__ == '__main__':
    host = '0.0.0.0'
    uvicorn.run(app, host=host, port=8000)