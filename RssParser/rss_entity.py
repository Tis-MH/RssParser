import abc
from datetime import datetime
from RssParser.schema import Entity

class RSSEntity:
    def __init__(self, entity: dict) -> None:
        self.entity = entity
    
    @abc.abstractmethod
    def title(self) -> str:
        pass
    
    @abc.abstractmethod
    def magnet(self) -> str:
        pass
    
    @abc.abstractmethod
    def upload_time(self) -> str | None:
        pass
    
    @abc.abstractmethod
    def category(self) -> str | None:
        pass
    
    @abc.abstractmethod
    def size(self) -> str | None:
        pass
    
    def get_entity(self) -> Entity:
        return Entity(
            title=self.title(),
            magnet=self.magnet(),
            upload_time=self.upload_time(),
            category=self.category(),
            size=self.size(),
        )
    
class nyaa(RSSEntity):
    def __init__(self, entity: dict) -> None:
        super().__init__(entity)
    
    def title(self) -> str:
        return self.entity.get('title')
    
    def magnet(self) -> str:
        return "magnet:?xt=urn:btih:" + self.entity.get('nyaa_infohash')

    def upload_time(self) -> datetime | None:
        published = self.entity.get('published_parsed')
        return datetime(*published[:6]) if published else None
        # return time.strftime("%Y-%m-%d %H:%M:%S", published) if published else None
    
    def category(self) -> str | None:
        return self.entity.get('nyaa_category')
    
    def size(self) -> str | None:
        return self.entity.get('nyaa_size')
    
class acgnx(RSSEntity):
    def __init__(self, entity: dict) -> None:
        super().__init__(entity)
    
    def title(self) -> str:
        return self.entity.get('title')
    
    def magnet(self) -> str:
        return self.entity['links'][1]['href']

    def upload_time(self) -> datetime | None:
        published = self.entity.get('published_parsed')
        return datetime(*published[:6]) if published else None
        # return time.strftime("%Y-%m-%d %H:%M:%S", published) if published else None
    
    def category(self) -> str | None:
        return super().category()
    
    def size(self) -> str | None:
        return super().size()
    
class dmhy(RSSEntity):
    def __init__(self, entity: dict) -> None:
        super().__init__(entity)
        
    def title(self) -> str:
        return self.entity.get('title')
    
    def magnet(self) -> str:
        return self.entity.get('links')[1]['href']
    
    def upload_time(self) -> str | None:
        published = self.entity.get('published_parsed')
        return datetime(*published[:6]) if published else None
    
    def category(self) -> str | None:
        return super().category()
    
    def size(self) -> str | None:
        return super().size()
    
def destruction_entity(obj: object, url: str):  # 将实体和url传到这里进行 debug 和 开发
    import feedparser
    entity = feedparser.parse(url)
    obj = obj(entity['entries'][0])
    res = obj.get_entity()

    
# for test
if __name__ == "__main__":
    destruction_entity(dmhy, 'https://dmhy.org/topics/rss/rss.xml')