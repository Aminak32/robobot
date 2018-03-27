from modelsAlchemy import dbSession, Proxy

class AppProxyHandler:
    def getProxy(self):
        self.dbSession = dbSession()
        proxy = self.dbSession.query(Proxy).filter_by(active=1).first()
        self.dbSession.close()
        return proxy

    def inactiveProxy(self, proxy):
        self.dbSession = dbSession()
        proxy.active = 0
        self.dbSession.add(proxy)
        self.dbSession.commit()
        self.dbSession.close()
