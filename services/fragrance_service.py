from repositories.fragrance_repository import frag_repository

class FragranceService():
    def __init__(self, fragrance_repository):
        self.fragrance_repository = fragrance_repository

    def post_new_fragrance(self, creator, name, designer, nose, description, notes, year):
        fragrance_id = self.fragrance_repository.add_fragrance(creator, name, designer, nose, description, notes, year)

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

        print(designers, perfumers)
        return fragrance_id

    def get_name(self, to_get_id):
        return self.fragrance_repository.fragrance_name(to_get_id)

    def get_all(self, to_get):
        if to_get == "groups":
            return self.fragrance_repository.get_all_groups()
        elif to_get == "fragrances":
            return self.fragrance_repository.get_all_fragrances()
        elif to_get == "designers":
            return self.fragrance_repository.get_all_designers()
        elif to_get == "perfumers":
            return self.fragrance_repository.get_all_perfumers()
        elif to_get == "reviews":
            return self.fragrance_repository.get_all_reviews()

    def get_one(self, to_get_id):
        return self.fragrance_repository.get_one_fragrance(to_get_id)

fragrance_repository = FragranceService(frag_repository)