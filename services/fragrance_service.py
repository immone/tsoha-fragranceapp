from repositories.fragrance_repository import frag_repository


class FragranceService():
    """ Responsible for communication between the database and the templates. """

    def __init__(self, fragrance_repository):
        self.fragrance_repository = fragrance_repository

    def post_new_fragrance(self, creator, name, designer, nose, description, notes, year):
        fragrance_id = self.fragrance_repository.add_fragrance(
            creator, name, designer, nose, description, notes, year)

        designers = self.get_all("designers")
        perfumers = self.get_all("perfumers")

        if designers:
            designers = [designer[1] for designer in designers]
        if not designers or designer not in designers:
            self.fragrance_repository.add_designer(designer)

        if perfumers:
            perfumers = [perfumer[1] for perfumer in perfumers]
        if not perfumers or nose not in perfumers:
            self.fragrance_repository.add_perfumer(nose)
        return fragrance_id

    def post_new_review(self, text, rating, fragrance_id, user_id):
        return self.fragrance_repository.add_review(text, rating, fragrance_id, user_id)

    def get_all_by_name(self, table, name):
        return self.fragrance_repository.get_all_by_name(table, name)

    def get_name(self, to_get_id):
        return self.fragrance_repository.fragrance_name(to_get_id)

    def get_all(self, table_name, param=None):
        return self.fragrance_repository.get_all(table_name, param)

    def get_one(self, to_get_id, table_name):
        return self.fragrance_repository.get_one_by_id(to_get_id, table_name)

    def add_to_collection(self, fragrance_id, u_id):
        return self.fragrance_repository.add_to_collection(fragrance_id, u_id)

    def return_statistics(self):
        return self.fragrance_repository.compute_stats()

    def return_average(self):
        return self.fragrance_repository.compute_average()

    def return_average_by_id(self, f_id):
        return self.fragrance_repository.compute_average_by_id(f_id)

    def set_visibility(self, table, item_id, visibility=False):
        self.fragrance_repository.set_visibility(table, item_id, visibility)


fragrance_service = FragranceService(frag_repository)
