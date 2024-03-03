from entities.db import db
from sqlalchemy.sql import text

class FragranceRepository:
    def __init__(self, db):
        self.db = db

    def fragrance_name(self, fragrance_id):
        query = "SELECT name FROM fragrances WHERE id=:fragrance_id"
        return self.db.session.execute(text(query), {"fragrance_id": fragrance_id}).fetchone()

    def get_one_by_id(self, table, get_id):
        query_map = {
            "designer": "SELECT * FROM designers WHERE id=:get_id",
            "fragrance": "SELECT * FROM fragrances WHERE id=:get_id",
            "perfumer": "SELECT * FROM perfumers WHERE id=:get_id",
        }
        query = query_map[table]
        return self.db.session.execute(text(query), {"get_id": get_id}).fetchone()

    def get_all_by_name(self, table, name):
        query_map = {
            "designer": "SELECT * FROM fragrances WHERE designer=:name",
            "perfumer": "SELECT * FROM fragrances WHERE nose=:name"
        }
        query = query_map[table]
        return self.db.session.execute(text(query), {"name": name}).fetchall()

    def get_all(self, table, param=None):
        query_map = {
            "designers": "SELECT id, name FROM designers WHERE visible=1 ORDER BY name",
            "fragrances": "SELECT id, name, designer, created_in FROM fragrances WHERE visible=1 ORDER BY name",
            "groups": "SELECT id, name FROM groups WHERE visible=1 ORDER BY name",
            "reviews": """SELECT * FROM reviews
                         WHERE reviews.fragrance_id=:param
                         ORDER by reviews.sent_at""",
            "all_reviews": "SELECT * from reviews ORDER by reviews.sent_at",
            "user_reviews": """SELECT u.name, u.id, r.comment, r.rating, r.sent_at, f.name, f.designer, f.created_in, r.id 
                               FROM reviews r JOIN users u on r.user_id = u.id
                                              JOIN fragrances f on r.fragrance_id = f.id
                               ORDER by r.sent_at""",
            "perfumers": "SELECT id, name FROM perfumers WHERE visible=1 ORDER BY name",
            "collection": """SELECT fragrances.name, fragrances.designer, fragrances.id FROM fragrances 
                             JOIN collections ON fragrances.id = collections.fragrance_id
                             WHERE collections.user_id=:param"""
        }
        query = query_map[table]
        if param:
            return self.db.session.execute(text(query), {"param": param }).fetchall()
        else:
            return self.db.session.execute(text(query)).fetchall()


    def add_fragrance(self, creator, name, designer, nose, description, notes, year):
        query = """INSERT INTO fragrances (creator_id, designer, name, nose, description, notes, created_in, visible)
                   VALUES (:creator, :designer, :name, :nose, :description, :notes, :year, 1) RETURNING id"""

        val = db.session.execute(text(query), {"creator": creator, "designer": designer, "name": name,
                                   "nose": nose, "description": description,
                                   "notes": notes, "year": year})
        db.session.commit()
        return val

    def add_designer(self, name):
        query = """INSERT INTO designers (name, visible) VALUES (:name, 1)"""
        db.session.execute(text(query), {"name": name})
        db.session.commit()

    def add_perfumer(self, name):
        query = """INSERT INTO perfumers (name, visible) VALUES (:name, 1)"""
        db.session.execute(text(query), {"name": name})
        db.session.commit()

    def add_review(self, comment, rating, fragrance_id, u_id):
        query = """INSERT INTO reviews (comment, rating, sent_at, fragrance_id, user_id) 
                   VALUES (:comment, :rating, NOW(), :fragrance_id, :user_id)"""
        db.session.execute(text(query), {"comment": comment, "rating": rating, "fragrance_id": fragrance_id, "user_id": u_id})
        db.session.commit()

    def add_to_collection(self, u_id, f_id):
        query = "INSERT INTO collections (user_id, fragrance_id) VALUES (:user_id, :fragrance_id) RETURNING id"
        val = db.session.execute(text(query), {"user_id": u_id, "fragrance_id": f_id})
        db.session.commit()
        return val

    def compute_stats(self):
        users = db.session.execute(text("SELECT COUNT(*) from users")).fetchone()
        fragrances = db.session.execute(text("SELECT COUNT(*) from fragrances")).fetchone()
        reviews = db.session.execute(text("SELECT COUNT(*) from reviews")).fetchone()

        return users[0], fragrances[0], reviews[0]


frag_repository = FragranceRepository(db)