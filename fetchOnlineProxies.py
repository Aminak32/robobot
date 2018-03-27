import asyncio
import threading

from proxybroker import Broker


class FetchOnlineProxies:
    judges = ['http://httpbin.org/get?show_env', 'https://httpbin.org/get?show_env']
    providers = ['http://www.proxylists.net/', 'http://fineproxy.org/eng/fresh-proxies/']
    types = ['SOCKS4', 'SOCKS5']
    countries = ['US']
    proxyCount = 100

    async def fetchProxies(self, guiStatusElem):
        proxyList = []
        proxyType = ''
        fetchedCount = 1
        while self.proxies:
            proxy = await self.proxies.get()
            if proxy is None: break
            if 'SOCKS4' in proxy.types:
                proxyType = 'socks4'
            elif 'SOCKS5' in proxy.types:
                proxyType = 'socks5'
            elif 'HTTP' in proxy.types:
                proxyType = 'http'
            else:
                proxyType = 'https'

            proxyList.append({"host":proxy.host, "port":proxy.port, "type":proxyType})
            guiStatusElem.setText("Fetched proxy (" + str(fetchedCount) + "/" + str(self.proxyCount) + ")")
            fetchedCount += 1

        return proxyList


    def getProxies(self, loop, guiStatusElem):
        asyncio.set_event_loop(loop)
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(asyncio.new_event_loop())
        # loop = asyncio.get_event_loop()

        self.proxies = asyncio.Queue()

        # broker = Broker(
        #     proxies, timeout=8, max_conn=200, max_tries=3, verify_ssl=False,
        #     judges=judges, providers=providers, loop=loop)
        broker = Broker(
            self.proxies,
            timeout=8,
            max_conn=200,
            max_tries=3,
            verify_ssl=True,
            judges=self.judges
        )

        tasks = asyncio.gather(
            broker.find(
                types=self.types,
                countries=self.countries,
                strict=True,
                limit=self.proxyCount
            ),
            self.fetchProxies(guiStatusElem)
        )

        proxyList = loop.run_until_complete(tasks)
        # broker.show_stats(verbose=True)
        return proxyList[1]

