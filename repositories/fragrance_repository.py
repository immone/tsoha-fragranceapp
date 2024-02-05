from entities.db import db
from sqlalchemy.sql import text

class FragranceRepository:
    def __init__(self, db):
        self.db = db

    def fragrance_name(self, fragrance_id):
        query = "SELECT name FROM fragrances WHERE id=:fragrance_id"
        return self.db.session.execute(text(query), {"fragrance_id": fragrance_id}).fetchone()

    def get_one_fragrance(self, fragrance_id):
        query = "SELECT * FROM fragrances WHERE id=:fragrance_id"
        return self.db.session.execute(text(query), {"fragrance_id": fragrance_id}).fetchone()

    def get_all_designers(self):
        query = "SELECT id, name FROM designers WHERE visible=1 ORDER BY name"
        return self.db.session.execute(text(query)).fetchall()

    def get_all_fragrances(self):
        query = "SELECT id, name, designer, created_in FROM fragrances WHERE visible=1 ORDER BY name"
        return self.db.session.execute(text(query)).fetchall()

    def get_all_groups(self):
        query = "SELECT id, name FROM groups WHERE visible=1 ORDER BY name"
        return self.db.session.execute(text(query)).fetchall()

    def get_all_perfumers(self):
        query = "SELECT id, name FROM perfumers WHERE visible=1 ORDER BY name"
        return self.db.session.execute(text(query)).fetchall()

    def get_all_reviews(self):
        query = """SELECT u.name, r.comment, r.review, r.sent_at, f.name, f.designer,
                          f.created_in, r.id FROM reviews r, users u, fragrances f
                   WHERE r.user_id = u.id AND f.id = r.fragrance_id ORDER by r.sent_at"""
        return self.db.session.execute(text(query)).fetchall()

    def add_fragrance(self, creator, name, designer, nose, description, notes, year):
        query = """INSERT INTO fragrances (creator_id, designer, name, nose, description, notes, created_in, visible)
                   VALUES (:creator, :designer, :name, :nose, :description, :notes, :year, 1) RETURNING id"""

        db.session.execute(text(query), {"creator": creator, "designer": designer, "name": name,
                                   "nose": nose, "description": description,
                                   "notes": notes, "year": year})
        db.session.commit()
        return query

    def add_designer(self, name):
        query = """INSERT INTO designers (name, visible) VALUES (:name, 1)"""
        db.session.execute(text(query), {"name": name})
        db.session.commit()

    def add_perfumer(self, name):
        query = """INSERT INTO perfumers (name, visible) VALUES (:name, 1)"""
        db.session.execute(text(query), {"name": name})
        db.session.commit()

    def add_review(self, text, review, fragrance_id, user_id):
        query = """INSERT INTO reviews (comment, review, sent_at, fragrance_id, user_id) 
                   VALUES (:text, :review, NOW(), :fragrance_id, :user_id)"""
        db.session.execute(text(query), {"text": text, "review": review, "fragrance_id": fragrance_id, "user_id": user_id})
        db.session.commit()

frag_repository = FragranceRepository(db)