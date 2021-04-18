from datetime import date

from django.contrib.auth.models import User
from django.test import TransactionTestCase

from food_storage.models import FoodIngredient
from profiles.models import FoodItem, Profile, UserFoodStorage


def create_vegetable(name):
    return FoodIngredient.objects.get_or_create(name=name,
                                                food_group='v',
                                                carbohydrates=1.1,
                                                fats=2.2,
                                                protein=3.3,
                                                calories=4)[0]


def create_food_item(name, quantity=1):
    ingredient = create_vegetable(name)
    return FoodItem.objects.create(ingredient=ingredient, quantity=quantity)


class FoodItemModelTest(TransactionTestCase):

    def setUp(self) -> None:
        self.carrot = create_vegetable('carrot')

    def test_food_item_is_created(self):
        carrot_1 = FoodItem.objects.create(ingredient=self.carrot, quantity=1)
        self.assertEqual(carrot_1.ingredient, self.carrot)
        self.assertEqual(carrot_1.quantity, 1)

    def test_food_item_methods(self):
        carrot_1 = FoodItem.objects.create(ingredient=self.carrot, quantity=2)
        self.assertEqual(carrot_1.calories, self.carrot.calories * 2)
        self.assertEqual(carrot_1.carbs, self.carrot.carbohydrates * 2)
        self.assertEqual(carrot_1.fats, self.carrot.fats * 2)
        self.assertEqual(carrot_1.protein, self.carrot.protein * 2)
        self.assertEqual(carrot_1.__str__(),
                         f"{self.carrot.__str__()} q:{carrot_1.quantity}")


class ProfileModelTest(TransactionTestCase):

    def setUp(self) -> None:
        self.user_def = User.objects.create_user(username='setup',
                                                 password='password')

    def test_profile_is_created_on_user_creation(self):
        user = User.objects.create_user(username='test', password='password', )
        self.assertTrue(user.profile)

    def test_profile_fields(self):
        Profile.objects.filter(user=self.user_def).update(weight=50,
                                                          height=180,
                                                          calorie_goal=2000)
        profile = self.user_def.profile
        profile.refresh_from_db()
        self.assertEqual(profile.weight, 50)
        self.assertEqual(profile.height, 180)
        self.assertEqual(profile.calorie_goal, 2000)

    def test_profile_properties(self):
        Profile.objects.filter(user=self.user_def).update(weight=50,
                                                          height=180,
                                                          calorie_goal=2000)
        profile = self.user_def.profile
        profile.refresh_from_db()
        for _ in range(3):
            profile.daily_food.add(create_food_item('carrot'))
        carrot = FoodIngredient.objects.get(name='carrot')
        for item in profile.daily_food_items:
            self.assertEqual(item.food.ingredient, carrot)
        self.assertEqual(profile.calories_today, carrot.calories * 3)
        self.assertEqual(profile.carbs_today, carrot.carbohydrates * 3)
        self.assertEqual(profile.fats_today, carrot.fats * 3)
        self.assertEqual(profile.protein_today, carrot.protein * 3)
        self.assertEqual(profile.calories_left_in_goal,
                         profile.calorie_goal - (carrot.calories * 3))
        self.assertEqual(profile.__str__(),
                         f'username: {self.user_def.username}')


class UserFoodStorageModelTest(TransactionTestCase):
    def setUp(self) -> None:
        self.user_def = User.objects.create_user(username='setup',
                                                 password='password')
        self.item = lambda name: create_food_item(name)

    def test_storage_create(self):
        storage = UserFoodStorage.objects.create(user=self.user_def.profile,
                                                 food=self.item('carrot'))
        self.assertEqual(storage.user, self.user_def.profile)
        self.assertEqual(storage.food.ingredient.name, 'carrot')
        self.assertEqual(storage.food.quantity, 1)
        self.assertEqual(storage.date, date.today())

    def test_str_method(self):
        storage = UserFoodStorage.objects.create(user=self.user_def.profile,
                                                 food=self.item('carrot'))
        self.assertEqual(storage.__str__(),
                         f'Storage of user {self.user_def.profile.__str__()} for {date.today()}')
