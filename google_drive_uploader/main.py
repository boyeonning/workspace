import uvicorn
import shutil
import unregistred_pog 

from typing import Optional
from pydantic import BaseModel
from google_drive_upload import upload_files
from fastapi import FastAPI, File, UploadFile, APIRouter


app = FastAPI()

class Item(BaseModel):
    id : str 
    sheet_name : str = None
    sheet_range : str = None
    mode : bool = False
    product_101 : bool = False
    cell_color : tuple = None

@app.get("/")
async def root():
    return "hello"

@app.post('/upload')
def upload(file: UploadFile = File(...)):
    
    path=f"files/{file.filename}"
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # return {
    #     'filename': file.filename,
    #     'path': path,
    #     'type': file.content_type
    # }
    id = upload_files(path)
    return id 

# async def save_file(file: IO):
#     # s3 업로드라고 생각해 봅시다. delete=True(기본값)이면
#     # 현재 함수가 닫히고 파일도 지워집니다.
#     with NamedTemporaryFile("wb", delete=False) as tempfile:
#         tempfile.write(file.read())
#         return tempfile.name


# @app.post("/file/store")
# async def store_file(file: UploadFile = File(...)):
#     path = await save_file(file.file)
#     return {"filepath": path}

# @app.post('/test')
# async def run(file: UploadFile):
#     path = await save_file(file.file)
#     key = google_upload.upload_files(path)
#     # rst = unregistred_pog.run(key, sheet_name, sheet_range)
#     # return rst


@app.post('/unregistered')
async def find_unregistered_pog(item : Item):
    ret = True
    try:
        id = item.id
        sheet_name = item.sheet_name
        sheet_range = item.sheet_range
        mode = item.mode
        product_101 = item.product_101
        cell_color = item.cell_color

        rst = unregistred_pog.run(id, sheet_name, sheet_range, mode, product_101, cell_color)
        return rst
    except Exception as e:
        print(e)
        ret = False
    return ret

if __name__ == '__main__':
    host = '0.0.0.0'
    uvicorn.run(app, host=host, port=8004)
    
