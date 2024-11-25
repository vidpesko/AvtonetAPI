import time, asyncio
import nodriver as uc
from pyvirtualdisplay import Display


async def main():
    display = Display(visible=0, size=(1080,720))
    display.start()
    browser = await uc.start()
    page = await browser.get(
        "https://www.avto.net/Ads/details.asp?id=20315130&display=Mercedes-Benz%20C-Razred"
    )
    await asyncio.sleep(10)
    display.stop()


if __name__ == '__main__':
    # since asyncio.run never worked (for me)
    uc.loop().run_until_complete(main())