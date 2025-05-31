from server.core.database.MongoDB import connect_mongo

async def conf_mongodb():
    db, client = await connect_mongo(show_log=False)
    del client
    await db.users.create_index([("login", 1)], unique=True)
    await db.users.create_index([("mail", 1)], unique=True)
    await db.users.create_index([("phone", 1)], unique=True)
