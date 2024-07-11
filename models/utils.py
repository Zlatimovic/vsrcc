import httpx

async def fetch(url: str, headers: dict = {}, method: str = "GET", data=None, redirects: bool = True):
    # Correct the proxy settings by using full URL schemas for keys
    proxies = {
        "http://": "http://136.226.65.114:10160",
        "https://": "http://136.226.65.114:10160"
    }
    async with httpx.AsyncClient(follow_redirects=redirects, proxies=proxies, verify=False) as client:
        if method == "GET":
            response = await client.get(url, headers=headers)
            return response
        elif method == "POST":
            response = await client.post(url, headers=headers, data=data)
            return response
        else:
            return "ERROR"
