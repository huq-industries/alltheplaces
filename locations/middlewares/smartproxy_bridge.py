from scrapy_zyte_smartproxy import ZyteSmartProxyMiddleware


class SmartProxyBridgeMiddleware(ZyteSmartProxyMiddleware):
    def is_enabled(self, spider):
        """
        Allows Zyte Smart Proxy to be tied to AllThePlaces' proxy configuration class member
        """
        requires_proxy = getattr(spider, "requires_proxy", False)
        return requires_proxy or isinstance(requires_proxy, str) or super().is_enabled(spider)
