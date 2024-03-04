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
            "designers": "SELECT id, name FROM designers WHERE visible=true ORDER BY name",
            "fragrances": "SELECT id, name, designer, created_in FROM fragrances WHERE visible=true ORDER BY name",
            "fragrances_hidden": "SELECT id, name, designer, created_in FROM fragrances WHERE visible=false ORDER BY name",
            "groups": "SELECT id, name FROM groups WHERE visible=true ORDER BY name",
            "reviews": """SELECT reviews.comment, reviews.rating, users.name, reviews.sent_at, reviews.user_id, reviews.id
                        FROM reviews JOIN users on reviews.user_id=users.id
                         WHERE reviews.fragrance_id=:param and reviews.visible=true
                         ORDER by reviews.sent_at""",
            "all_reviews": "SELECT * from reviews WHERE visible=true ORDER by reviews.sent_at",
            "user_reviews": """SELECT u.name, u.id, r.comment, r.rating, r.sent_at, f.name, f.designer, f.created_in, f.id 
                               FROM reviews r JOIN users u on r.user_id = u.id
                                              JOIN fragrances f on r.fragrance_id = f.id
                               WHERE r.visible=true
                               ORDER by r.sent_at""",
            "perfumers": "SELECT id, name FROM perfumers WHERE visible=true ORDER BY name",
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
                   VALUES (:creator, :designer, :name, :nose, :description, :notes, :year, true) RETURNING id"""

        val = db.session.execute(text(query), {"creator": creator, "designer": designer, "name": name,
                                   "nose": nose, "description": description,
                                   "notes": notes, "year": year})
        db.session.commit()
        return val

    def add_designer(self, name):
        query = """INSERT INTO designers (name, visible) VALUES (:name, true)"""
        db.session.execute(text(query), {"name": name})
        db.session.commit()

    def add_perfumer(self, name):
        query = """INSERT INTO perfumers (name, visible) VALUES (:name, true)"""
        db.session.execute(text(query), {"name": name})
        db.session.commit()

    def add_review(self, comment, rating, fragrance_id, u_id):
        query = """INSERT INTO reviews (comment, rating, sent_at, fragrance_id, user_id, visible) 
                   VALUES (:comment, :rating, NOW(), :fragrance_id, :user_id, true)"""
        db.session.execute(text(query), {"comment": comment, "rating": rating, "fragrance_id": fragrance_id, "user_id": u_id})
        db.session.commit()

    def add_to_collection(self, u_id, f_id):
        query = """INSERT INTO collections (user_id, fragrance_id)
                   SELECT :u_id, :f_id
                   WHERE NOT EXISTS (
                   SELECT fragrance_id FROM collections WHERE fragrance_id=:f_id2)
                   RETURNING id """
        val = db.session.execute(text(query), {"u_id": u_id, "f_id": f_id, "f_id2": f_id})
        db.session.commit()
        return val

    def compute_stats(self):
        users = db.session.execute(text("SELECT COUNT(*) from users")).fetchone()
        fragrances = db.session.execute(text("SELECT COUNT(*) from fragrances WHERE fragrances.visible=true")).fetchone()
        reviews = db.session.execute(text("SELECT COUNT(*) from reviews WHERE reviews.visible=true")).fetchone()
        return users[0], fragrances[0], reviews[0]

    def compute_average(self):
        q = """SELECT fragrances.name, fragrances.id, AVG(reviews.rating)::numeric(10,2) 
            FROM reviews
            JOIN fragrances on reviews.fragrance_id=fragrances.id
            WHERE reviews.visible=true
            GROUP BY fragrances.name, fragrances.id
            ORDER BY AVG(reviews.rating) DESC"""
        avg = db.session.execute(text(q)).fetchall()
        return avg

    def compute_average_by_id(self, f_id):
        q = """SELECT AVG(reviews.rating)::numeric(10,2) 
            FROM reviews
            JOIN fragrances on reviews.fragrance_id=fragrances.id
            WHERE fragrances.id=:f_id and reviews.visible=true
            GROUP BY fragrances.name, fragrances.id
            ORDER BY AVG(reviews.rating) DESC"""
        avg = db.session.execute(text(q), {"f_id": f_id}).fetchall()
        return avg

    def set_visibility(self, table, item_id, visibility=False):
        query_map = {
            "fragrance": "UPDATE fragrances SET visible=:val WHERE id=:f_id",
            "review": "UPDATE reviews SET visible=:val WHERE id=:f_id",
        }
        q = query_map[table]
        db.session.execute(text(q), {"val": visibility, "f_id": item_id})
        db.session.commit()


frag_repository = FragranceRepository(db)