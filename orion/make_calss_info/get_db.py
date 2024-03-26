import pymssql

class GetDB:
    def __init__(self):
        self.server = '192.168.0.85:11433'
        self.user = 'interminds'
        self.password = 'ntflow'
        self.database = 'cspace_test'
        self.port = 11433
        self.conn = pymssql.connect(self.server, self.user, self.password, self.database, charset='CP949')

    def sku_train(self):
        sql = """
            SELECT * from sku_train st ;
             """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()

        self.conn.close()
        return records
    