import pymongo


def _get_db():
    # cli = pymongo.MongoClient("mongodb://172.17.0.2:27017/")
    cli = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cli['market']
    return db


def _list_db():
    cli = pymongo.MongoClient("mongodb://localhost:27017/")
    dblist = cli.list_database_names()
    print(dblist)


def delete_db():
    cli = pymongo.MongoClient("mongodb://localhost:27017/")
    cli.drop_database('market')


def delete_doc(collection='metals', query=None):
    db = _get_db()

    if not db and not collection and not query:
        return None

    try:
        db[collection].delete_one(query)
    except pymongo.errors.ServerSelectionTimeoutError:
        print("ServerSelectionTimeoutError")


def get_doc(collection='metals', query=None):
    db = _get_db()

    if not db and not collection and not query:
        return None

    try:
        doc = db[collection].find_one(query)
    except pymongo.errors.ServerSelectionTimeoutError:
        print("ServerSelectionTimeoutError")
        doc = None

    return doc


def get_content(collection='metals'):
    db = _get_db()

    if not db:
        return None

    try:
        documents = db[collection].find()
    except pymongo.errors.ServerSelectionTimeoutError:
        print("ServerSelectionTimeoutError")
        documents = None

    return documents


def get_metal_price(name, unit, currency):
    db = _get_db()

    if not db:
        return None
    try:
        query = {'name': name, 'unit': unit, 'currency': currency}
        document = db['metals'].find_one(query)
    except pymongo.errors.ServerSelectionTimeoutError:
        print("ServerSelectionTimeoutError")
        document = None

    return document


def set_metal_price(name, unit, currency, value):
    db = _get_db()
    query = {'name': name, 'unit': unit, 'currency': currency}
    new_query = {"$set": {'name': name, 'unit': unit, 'currency': currency, 'value': value}}

    try:
        db['metals'].update_one(query, new_query, upsert=True)
    except pymongo.errors.ServerSelectionTimeoutError:
        print("ServerSelectionTimeoutError")


def get_crypto_price(name, currency):
    db = _get_db()

    if not db:
        return None
    try:
        query = {'name': name, 'currency': currency}
        document = db['cryptos'].find_one(query)
    except pymongo.errors.ServerSelectionTimeoutError:
        print("ServerSelectionTimeoutError")
        document = None

    return document


def set_crypto_price(name, currency, value):
    db = _get_db()
    query = {'name': name, 'currency': currency}
    new_query = {"$set": {'name': name, 'currency': currency, 'value': value}}

    try:
        db['cryptos'].update_one(query, new_query, upsert=True)
    except pymongo.errors.ServerSelectionTimeoutError:
        print("ServerSelectionTimeoutError")
