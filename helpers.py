from faker import Faker


class Helpers:
    def generate_register_data(self):
        faker = Faker()
        return faker.free_email(), faker.password(), faker.first_name()
