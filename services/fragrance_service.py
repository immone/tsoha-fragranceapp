from repositories.fragrance_repository import frag_repository

class FragranceService():
    def __init__(self, fragrance_repository):
        self.fragrance_repository = fragrance_repository

    def post_new_fragrance(self, creator, name, designer, nose, description, notes, year):
        fragrance_id = self.fragrance_repository.add_fragrance(creator, name, designer, nose, description, notes, year)

        all_designers = self.get_all(["designers"])
        all_perfumers = self.get_all(["perfumers"])

        if all_designers:
            designers = [designer[1] for designer in all_designers]
            if designer not in designers:
                self.fragrance_repository.add_designer(designer)

        if all_perfumers:
            perfumers = [perfumer[1] for perfumer in all_perfumers]
            if nose not in perfumers:
                self.fragrance_repository.add_perfumer(designer)

        return fragrance_id


    def get_all(self, to_get):
        if to_get == "groups":
            return self.fragrance_repository.get_all_groups()
        elif to_get == "fragrances":
            return self.fragrance_repository.get_all_fragrances()
        elif to_get == "designers":
            return self.fragrance_repository.get_all_designers()
        elif to_get == "perfumers":
            return self.fragrance_repository.get_all_perfumers()

fragrance_repository = FragranceService(frag_repository)