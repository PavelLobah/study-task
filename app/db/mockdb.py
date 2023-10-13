from app.common.singleton import Singleton

# Singleton!!!!
class Db(Singleton):
    _table_pk = {}
    _db = {}
    # def __init__(self):
    #     self._db = {}

    def init_schema(self, tablename, pk):
        self._table_pk[tablename] = pk
        if tablename not in self._db:
            self._db[tablename] = []

    def get_pk(self, tablename):
        return self._table_pk[tablename]

    def find_by(self, tablename: str, field: str, val=None) -> tuple[list, list[int]]:
        results = []
        indices = []
        for i, row in enumerate(self._db.get(tablename, [])):
            cursor = row.dict().get(field, None)
            if val is not None and cursor == val \
                    or val is None and cursor:
                results.append(row)
                indices.append(i)
        return results, indices

    def add(self, tablename, cls, row):
        _id = str(len(self._db[tablename]) + 1)
        pk = self.get_pk(tablename)
        item = cls(**{pk: _id, **row.dict()})
        self._db[tablename].append(item)
        return item

    def get_all(self, tablename):
        return self._db[tablename]

    def get_one(self, tablename, _id):
        pk = self.get_pk(tablename)
        res, _ = self.find_by(tablename, pk, _id)
        if not res:
            return None
        return res[0]

    # (TABLE_NAME, dto.Issue, issue_id, issue)
    def update_one(self, tablename, cls, _id, row):
        pk = self.get_pk(tablename)
        res, idx = self.find_by(tablename, pk, _id)
        if not res:
            return None
        obj = cls(**{pk: res[0].dict()[pk], **row.dict()})
        self._db[tablename][idx[0]] = obj
        return obj

    def delete_one(self, tablename, _id):
        old_len = len(self._db[tablename])
        pk = self.get_pk(tablename)
        self._db[tablename] = [row for row in self._db[tablename] if row.dict()[pk] != _id]
        return old_len > len(self._db[tablename])


db = Db()
