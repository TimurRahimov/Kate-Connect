import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get('/{_:path}')
async def https_redirect(request: Request):
    return RedirectResponse(request.url.replace(scheme='https'))


if __name__ == '__main__':
    uvicorn.run('https_redirect:app', port=80, host='192.168.0.2')
