from .models import Cuisine

def categoryContext(request=None):
    """
    add the category to the request context, but only categories that have
    companies.
    """
    return {
        'cuisines': Cuisine.objects.have_companies()
    }