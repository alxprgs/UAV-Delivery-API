from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, text


metadata = MetaData()

registration_logs = Table(
    "registration_logs", metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String(32), nullable=False),
    Column("ip_address", String(45), nullable=False),
    Column("user_agent", String(500)),
    Column("created_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    extend_existing=True,
)

login_logs = Table(
    "login_logs", metadata,
    Column("id", Integer, primary_key=True),
    Column("login", String(32), nullable=False),
    Column("ip_address", String(45), nullable=False),
    Column("user_agent", String(500)),
    Column("logined_at", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    extend_existing=True
)

system_logs = Table(
    "system_logs", metadata,
    Column("id", Integer, primary_key=True),
    Column("message", String(128), nullable=False),
    Column("timestamp", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    extend_existing=True
)

permission_logs = Table(
    "permission_logs", metadata,
    Column("id", Integer, primary_key=True),
    Column("message", String(128), nullable=False),
    Column("timestamp", DateTime, server_default=text("CURRENT_TIMESTAMP")),
    extend_existing=True
)