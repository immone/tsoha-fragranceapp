from entities.db import db
from sqlalchemy.sql import text

class FragranceRepository:
    def __init__(self, db):
        self.db = db

    def get_all_designers(self):
        query = "SELECT id, designer FROM designers WHERE visible=1 ORDER BY name"
        return self.db.session.execute(text(query)).fetchall()

    def get_all_fragrances(self):
        query = "SELECT id, name FROM fragrances WHERE visible=1 ORDER BY name"
        return self.db.session.execute(text(query)).fetchall()

    def get_all_groups(self):
        query = "SELECT id, name FROM groups WHERE visible=1 ORDER BY name"
        return self.db.session.execute(text(query)).fetchall()

    def get_all_perfumers(self):
        query = "SELECT id, name FROM perfumers WHERE visible=1 ORDER BY name"
        return self.db.session.execute(text(query)).fetchall()

    def add_fragrance(self, creator, name, designer, nose, description, notes, year):
        query = """INSERT INTO fragrances (creator_id, designer, name, nose, description, notes, created_in, visible)
                   VALUES (:creator, :designer, :name, :nose, :description, :notes, :year, 1) RETURNING id"""

        db.session.execute(text(query), {"creator": creator, "name": name, "designer": designer,
                                   "nose": nose, "description": description,
                                   "notes": notes, "year": year})
        db.session.commit()
        return query

    def add_designer(self, name):
        query = """INSERT INTO designers (name, visible) VALUES (:name, 1)"""
        db.session.execute(text(query), {"name": name})

    def add_perfumer(self, name):
        query = """INSERT INTO perfumers (name, visible) VALUES (:name, 1)"""
        db.session.execute(text(query), {"name": name})

frag_repository = FragranceRepository(db)