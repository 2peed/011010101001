class Room:
    def __init__(self, id, owner, obj):
        self.owner = owner
        self.id = id
        self.obj= obj
        self.mode = 1
        self.whitelist = []
        self.blacklist = []

    async def delete(self):
        await self.obj.delete()
    
    def count(self):
        return len(self.obj.members)
    
    def addwhitelist(self, id):
        self.whitelist.append(id)
    
    def addblacklist(self, id):
        self.blacklist.append(id)

