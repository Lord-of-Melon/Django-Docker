from apps.models import Category


def get_category_descendants(category_id: int):
    """
    Mengembalikan seluruh id kategori
    termasuk kategori itu sendiri.
    """

    ids = [category_id]

    children = Category.objects.filter(parent_id=category_id)

    for child in children:
        ids.extend(
            get_category_descendants(child.id)
        )

    return ids