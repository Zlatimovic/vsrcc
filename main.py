from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import gzip
from models import vidsrctoget, vidsrcmeget, info, fetch
from io import BytesIO
from fastapi.responses import StreamingResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get('/')
async def index(response: Response):
    response.headers['Cache-Control'] = 'no-store'
    return await info()

@app.get('/vidsrc/{dbid}')
async def vidsrc(dbid: str, response: Response, s: int = None, e: int = None):
    response.headers['Cache-Control'] = 'no-store'
    if dbid:
        return {
            "status": 200,
            "info": "success",
            "sources": await vidsrctoget(dbid, s, e)
        }
    else:
        raise HTTPException(status_code=404, detail=f"Invalid id: {dbid}")

@app.get('/vsrcme/{dbid}')
async def vsrcme(response: Response, dbid: str = '', s: int = None, e: int = None, l: str = 'eng'):
    response.headers['Cache-Control'] = 'no-store'
    if dbid:
        return {
            "status": 200,
            "info": "success",
            "sources": await vidsrcmeget(dbid, s, e)
        }
    else:
        raise HTTPException(status_code=404, detail=f"Invalid id: {dbid}")

@app.get('/streams/{dbid}')
async def streams(response: Response, dbid: str = '', s: int = None, e: int = None, l: str = 'eng'):
    response.headers['Cache-Control'] = 'no-store'
    if dbid:
        return {
            "status": 200,
            "info": "success",
            "sources": await vidsrcmeget(dbid, s, e) + await vidsrctoget(dbid, s, e)
        }
    else:
        raise HTTPException(status_code=404, detail=f"Invalid id: {dbid}")

@app.get("/subs")
async def subs(url: str, response: Response):
    response.headers['Cache-Control'] = 'no-store'
    try:
        response_content = await fetch(url)
        with gzip.open(BytesIO(response_content), 'rt', encoding='utf-8') as f:
            subtitle_content = f.read()
        async def generate():
            yield subtitle_content.encode("utf-8")
        return StreamingResponse(generate(), media_type="application/octet-stream", headers={"Content-Disposition": "attachment; filename=subtitle.srt"})
    except:
        raise HTTPException(status_code=500, detail=f"Error fetching subtitle")
