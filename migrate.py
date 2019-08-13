from models import *
from routes import ts, sha3_256
db.drop_all()
db.create_all()
block = Block(is_verified=True)
user = User(name='admin', password='admin', balance=10000)
db.session.add(block)
db.session.add(user)
db.session.commit()
a = sha3_256()
a.update(block.id.to_bytes(4, 'big'))
a.update(ts(block.timestamp).to_bytes(8, 'big'))
block.hash = a.digest()
db.session.commit()
