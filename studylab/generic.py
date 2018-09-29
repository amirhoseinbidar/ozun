
class Cache():
    pass
    
class cacheList():
    _list = []
    
    class _meta():
        def __init__(self , flag , id ,cache):
            self.flag = flag
            self.id = id 
            self.cache = cache

    def add_record(self,flag , id , cache):
        self._list.append(self._meta(flag,id,cache))
    
    def find(self,flag = None , id = None):
        cache2 = cacheList()
        for item in self._list:
            if item.flag== flag and item.id == id: 
                return item.cache
            if ((item.flag== None and item.id == id) or 
                (item.flag== flag and item.id == None)):
                
                cache2.add_record(item.flag,item.id,item.cache)
        if cache2.isEmpty():
            return None
        return cache2

    def isEmpty(self):
        return len(self._list) == 0
    
    def delete(self , id= None , flag = None):
        i = 0
        for item in self._list:
            if item.flag == flag or item.id == id:
                del self._list[i]
            i += 1
cache_list = cacheList()        