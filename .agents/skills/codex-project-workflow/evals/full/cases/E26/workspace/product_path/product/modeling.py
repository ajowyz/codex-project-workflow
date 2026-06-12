class ModelProject:
    def __init__(self):
        self.models = []

    def add_model(self, name, shape):
        model = {"name": name, "shape": shape, "version": 1}
        self.models.append(model)
        return model
