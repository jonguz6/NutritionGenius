from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TransactionTestCase

from food_storage.models import FoodCategory, FoodIngredient


class FoodCategoryModelTest(TransactionTestCase):

    def setUp(self) -> None:
        self.grains = FoodCategory.objects.create(name='Grains')
        self.fruits = FoodCategory.objects.create(name='Fruits')

    def test_category_is_created(self):
        id_1 = FoodCategory.objects.get(id=1)
        grains = FoodCategory.objects.get(name='Grains')

        self.assertEqual(id_1, self.grains)
        self.assertEqual(grains, self.grains)

    def test_second_category_is_created(self):
        grains = FoodCategory.objects.get(name='Grains')
        fruits = FoodCategory.objects.get(name='Fruits')

        self.assertNotEqual(grains, fruits)
        self.assertNotEqual(grains, self.fruits)
        self.assertEqual(grains, self.grains)

    def test_category_name_is_unique(self):
        self.assertRaises(IntegrityError, FoodCategory.objects.create, name='Grains')
        self.assertRaises(IntegrityError, FoodCategory.objects.create, name='Fruits')

    def test_str_method(self):
        self.assertEqual(self.grains.__str__(), 'Grains')
        self.assertEqual(self.fruits.__str__(), 'Fruits')


class FoodIngredientModelTestCase(TransactionTestCase):

    def setUp(self) -> None:
        self.vegetables = FoodCategory.objects.create(name='Vegetables')
        self.potato = FoodIngredient.objects.create(name='Potato',
                                                    food_group='v',
                                                    carbohydrates=1.1,
                                                    fats=2.2,
                                                    protein=3.3,
                                                    calories=4)

    def test_ingredient_is_not_created_with_only_name(self):
        self.assertRaises(IntegrityError, FoodIngredient.objects.create, name='Carrot')

    def test_ingredient_is_created_with_required_fields(self):
        self.carrot = FoodIngredient.objects.create(name='Carrot',
                                                    food_group='v',
                                                    carbohydrates=1.1,
                                                    fats=2.2,
                                                    protein=3.3,
                                                    calories=4)
        self.assertEqual(self.carrot.name, 'Carrot')
        self.assertEqual(self.carrot.food_group, 'v')
        self.assertEqual(self.carrot.carbohydrates, 1.1)
        self.assertEqual(self.carrot.fats, 2.2)
        self.assertEqual(self.carrot.protein, 3.3)
        self.assertEqual(self.carrot.calories, 4)

    def test_food_group_not_in_choices(self):
        self.potato.food_group = 'a'
        self.assertRaises(ValidationError, self.potato.full_clean)

    def test_food_ingredient_name_unique(self):
        self.assertRaises(IntegrityError, FoodIngredient.objects.create,
                          name='Potato',
                          food_group='v',
                          carbohydrates=1.1,
                          fats=2.2,
                          protein=3.3,
                          calories=4)

    def test_category_is_correctly_assigned(self):
        self.potato.category = self.vegetables
        self.assertEqual(self.potato.category, self.vegetables)

    def test_str_method(self):
        self.assertEqual(self.potato.__str__(), "Potato")

