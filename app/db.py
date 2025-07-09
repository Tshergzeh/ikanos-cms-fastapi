from sqlalchemy import create_engine, text

dbname = "ikanos_cms"
db_user = "tshergzeh"
db_pass = "chelseafc2013"

engine = create_engine(f"postgresql+postgresql://{db_user}:{db_pass}@localhost:5432/{dbname}", echo=True)

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())