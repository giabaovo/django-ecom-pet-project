from category.models import CategoryModel

def categories_links(request):
    links = CategoryModel.objects.all()
    return {"links": links}