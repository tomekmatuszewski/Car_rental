class TestDbMethods:

    @staticmethod
    def create_objects(db_obj, levels_data):
        return [db_obj(**level) for level in levels_data]

    def add_obj(self, level, level_data, session):
        session.add_all(self.create_objects(level, level_data))
        session.commit()