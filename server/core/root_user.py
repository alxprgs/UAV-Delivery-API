from server.core.api.schemes import UserRootCreate
from server.core.database.mongodb import connect_mongo
from server.core.logging import logger
from pymongo.errors import PyMongoError
from sqlalchemy.exc import SQLAlchemyError
from server.core.functions.sqldb import log_system

async def root_user():
    db, client = await connect_mongo(show_log=False)
    data = UserRootCreate.create()
    action = None

    try:
        result = await db["users"].find_one_and_update(
            {"login": data.login},
            {"$set": {"password": data.password, "mail": data.mail, "phone": data.phone, "permissions": {"dev": True}}},
            upsert=True,
            return_document=True
        )
        action = "updated" if result else "created"
        client.close()
    except PyMongoError as e:
        logger.error("MongoDB error on upsert ROOT user: %s", e, exc_info=True)
        await log_system(f"Error {e} during ROOT user upsert (MongoDB).")
        client.close()
        return

    try:
        await log_system(f"Successfully {action} ROOT user '{data.login}'.")
        client.close()
    except SQLAlchemyError as e:
        logger.error("SQLAlchemy error logging system_logs: %s", e, exc_info=True)
        client.close()