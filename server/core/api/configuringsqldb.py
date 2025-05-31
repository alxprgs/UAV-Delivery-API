from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, text


metadata = MetaData()

RegistrationLogs = Table(
    "RegistrationLogs", metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String(32), nullable=False),
    Column("ip_address", String(45), nullable=False),
    Column("user_agent", String(500)),
    Column("created_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    extend_existing=True,
)

LoginLogs = Table(
    "LoginLogs", metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String(32), nullable=False),
    Column("ip_address", String(45), nullable=False),
    Column("user_agent", String(500)),
    Column("logined_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    extend_existing=True
)

SystemLogs = Table(
    "SystemLogs", metadata,
    Column("id", Integer, primary_key=True),
    Column("message", String(128), nullable=False),
    Column("timestamp", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    extend_existing=True
)

logs = Table(
    "logs", metadata,
    Column("id", Integer, primary_key=True),
    Column("action", String(128), nullable=False),
    Column("user_login", String(32), nullable=False),
    Column("details", String(256), nullable=True),
    Column("timestamp", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    extend_existing=True
)

Permissionlogs = Table(
    "Permissionlogs", metadata,
    Column("id", Integer, primary_key=True),
    Column("message", String(128), nullable=False),
    Column("timestamp", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    extend_existing=True
)