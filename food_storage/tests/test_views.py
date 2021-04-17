from django.test import TestCase

from django.test import TransactionTestCase
from django.urls import reverse

from food_storage.models import FoodCategory, FoodIngredient
from food_storage.views import FoodCategoryCreateView, FoodCategoryListView, FoodCategoryUpdateView, \
    FoodCategoryDeleteView, FoodIngredientCreateView, FoodIngredientListView, FoodIngredientUpdateView, \
    FoodIngredientDeleteView, index


def create_food_category(name):
    return FoodCategory.objects.create(name=name)


def create_fruit(name):
    fruits = FoodCategory.objects.get_or_create(name='Fruits')
    return FoodIngredient.objects.create(name=name, food_group='f',
                                         category=fruits[0], carbohydrates=1,
                                         fats=2, protein=3,
                                         calories=4, quantity=1)


class IndexViewTest(TestCase):
    def test_index_view(self):
        view = reverse('food_storage:index')
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "food_storage-index.html")
        self.assertEqual(response_get.resolver_match.func, index)
        self.assertContains(response_get, 'Food Categories')
        self.assertContains(response_get, 'Ingredients')


class FoodCategoryViewTest(TestCase):
    def setUp(self) -> None:
        self.fruits = create_food_category('Fruits')

    def test_category_create(self):
        view = reverse('food_storage:category-create')
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "FoodCategory/category-create.html")
        self.assertEqual(response_get.resolver_match.func.__name__,
                         FoodCategoryCreateView.as_view().__name__)

        response_post = self.client.post(view, {'name': 'Vegetables'})
        self.assertEqual(response_post.status_code, 302)

        self.assertTrue(FoodCategory.objects.get(name="Vegetables"))

    def test_category_list(self):
        view = reverse('food_storage:category-list')
        response = self.client.get(view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'FoodCategory/category-list.html')

        self.assertEqual(response.resolver_match.func.__name__,
                         FoodCategoryListView.as_view().__name__)
        self.assertQuerysetEqual(response.context.get('object_list'),
                                 FoodCategory.objects.all(),
                                 transform=lambda x: x)

        self.assertEqual(response.context.get('object_list').first(), self.fruits)

    def test_category_update(self):
        view = reverse('food_storage:category-update', args=[self.fruits.id])
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'FoodCategory/category-update.html')

        self.assertEqual(response_get.resolver_match.func.__name__,
                         FoodCategoryUpdateView.as_view().__name__)

        response_post = self.client.post(view, {'name': 'fruits_changed'})
        self.assertEqual(response_post.status_code, 302)

        self.assertTrue(FoodCategory.objects.get(name='fruits_changed'))
        self.assertRaises(FoodCategory.DoesNotExist, FoodCategory.objects.get, name='fruits')

    def test_category_delete(self):
        view = reverse('food_storage:category-delete', args=[self.fruits.id])
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'FoodCategory/category-delete.html')

        response_post = self.client.delete(view)
        self.assertEqual(response_post.status_code, 302)

        self.assertEqual(response_post.resolver_match.func.__name__,
                         FoodCategoryDeleteView.as_view().__name__)

        self.assertRaises(FoodCategory.DoesNotExist, FoodCategory.objects.get, name='fruits')


class FoodIngredientViewTest(TestCase):

    def setUp(self) -> None:
        self.fruits = FoodCategory.objects.create(name='Fruits')

    def test_ingredient_create(self):
        view = reverse('food_storage:ingredient-create')
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        response_post = self.client.post(view, {'name': 'Pear',
                                                'food_group': 'f',
                                                'category': self.fruits.id,
                                                'carbohydrates': 1,
                                                'fats': 2,
                                                'protein': 3,
                                                'calories': 4,
                                                'quantity': 1})
        self.assertEqual(response_post.status_code, 302)
        self.assertEqual(response_post.resolver_match.func.__name__,
                         FoodIngredientCreateView.as_view().__name__)

        pear = FoodIngredient.objects.get(name="Pear")
        self.assertEquals(pear.name, "Pear")
        self.assertEquals(pear.food_group, "f")
        self.assertEquals(pear.category, self.fruits)
        self.assertEquals(pear.carbohydrates, 1)
        self.assertEquals(pear.fats, 2)
        self.assertEquals(pear.protein, 3)
        self.assertEquals(pear.calories, 4)
        self.assertEquals(pear.quantity, 1)

    def test_ingredient_create_with_category_prefilled(self):
        view = reverse('food_storage:ingredient-create-w-cat', args=[self.fruits.id])
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_get.context['form'].initial['category'], self.fruits)
        response_post = self.client.post(view, {'name': 'Pear',
                                                'food_group': 'f',
                                                'carbohydrates': 1,
                                                'fats': 2,
                                                'protein': 3,
                                                'calories': 4,
                                                'quantity': 1})
        self.assertEqual(response_post.status_code, 302)
        self.assertEqual(response_post.resolver_match.func.__name__,
                         FoodIngredientCreateView.as_view().__name__)
        pear = FoodIngredient.objects.get(name="Pear")
        self.assertEquals(pear.name, "Pear")
        self.assertEquals(pear.category, self.fruits)

    def test_ingredient_list(self):
        view = reverse('food_storage:ingredient-list')
        pear = create_fruit('Pear')
        response = self.client.get(view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'FoodIngredient/ingredient-list.html')

        self.assertEqual(response.resolver_match.func.__name__,
                         FoodIngredientListView.as_view().__name__)
        self.assertQuerysetEqual(response.context.get('object_list'),
                                 FoodIngredient.objects.all(),
                                 transform=lambda x: x)

        self.assertEqual(response.context.get('object_list').first(), pear)

    def test_category_list_with_category_filter(self):
        view = reverse('food_storage:ingredient-list-filter-cat', args=[self.fruits.id])
        pear = create_fruit('Pear')
        response = self.client.get(view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'FoodIngredient/ingredient-list.html')

        self.assertEqual(response.resolver_match.func.__name__,
                         FoodIngredientListView.as_view().__name__)
        self.assertQuerysetEqual(response.context.get('object_list'),
                                 FoodIngredient.objects.all(),
                                 transform=lambda x: x)

        self.assertEqual(response.context.get('object_list').first(), pear)

    def test_ingredient_update(self):
        pear = create_fruit('pear')
        view = reverse('food_storage:ingredient-update', args=[pear.id])
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)

        self.assertEqual(response_get.resolver_match.func.__name__,
                         FoodIngredientUpdateView.as_view().__name__)

        response_post = self.client.post(view, {'name': 'strawberry',
                                                'food_group': 'f',
                                                'category': pear.category.id,
                                                'carbohydrates': 1,
                                                'fats': 2,
                                                'protein': 3,
                                                'calories': 4,
                                                'quantity': 1})
        self.assertEqual(response_post.status_code, 302)

        self.assertTrue(FoodIngredient.objects.get(name='strawberry'))
        self.assertRaises(FoodIngredient.DoesNotExist, FoodIngredient.objects.get, name='pear')

    def test_ingredient_delete(self):
        pear = create_fruit('pear')
        view = reverse('food_storage:ingredient-delete', args=[pear.id])
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'FoodIngredient/ingredient-delete.html')

        self.assertEqual(response_get.resolver_match.func.__name__,
                         FoodIngredientDeleteView.as_view().__name__)

        response_post = self.client.delete(view)
        self.assertEqual(response_post.status_code, 302)

        self.assertRaises(FoodIngredient.DoesNotExist, FoodIngredient.objects.get, name='pear')
