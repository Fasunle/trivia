from flaskr.controllers import categories_controller


@categories_controller.route('/')
def index():
    return "Blueprint is working for categories"
