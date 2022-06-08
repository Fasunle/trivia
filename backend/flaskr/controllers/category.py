from flaskr.controllers import categories_controller
from models import Category


@categories_controller.route('/')
def fecth_categories():
    """Fetch all categories

    Returns:
        dict: a key-value {'id':'type'}
    """
    all_categories = Category.query.all()
    return {
        Category.format(category)['id']:  Category.format(category)['type']
        for category in all_categories
    }
