from datetime import date

from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase
from django.urls import reverse

from food_storage.models import FoodCategory
from profiles.models import FoodItem, Profile, UserFoodStorage
from profiles.views import index, FoodItemCreateView, FoodItemListView, FoodItemUpdateView, FoodItemDeleteView, \
    ProfileListView, ProfileDetailView, ProfileUpdateView, ProfileDeleteView, UserFoodStorageCreateView, \
    UserFoodStorageListView, UserFoodStorageUpdateView, UserFoodStorageDeleteView, SelfProfileDetailView, \
    user_food_storage_create_view, FoodStorageForCurrentUserListView, TodayFoodStorageForCurrentUserListView

from profiles.tests.test_models import create_vegetable, create_food_item


def create_storage(user, item):
    return UserFoodStorage.objects.create(user=user, food=item)


class IndexViewTest(TestCase):
    def setUp(self) -> None:
        permission = Permission.objects.get(name='Can view profile')
        self.user_def = User.objects.create_user(username='setup')
        self.user_def.set_password('password')
        self.user_def.user_permissions.add(permission)
        self.user_def.save()
        self.client.login(username='setup', password='password')

    def test_index_view(self):
        view = reverse('profiles:index')
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "profile-index.html")
        self.assertEqual(response_get.resolver_match.func, index)
        self.assertContains(response_get, 'Profiles')
        self.assertContains(response_get, 'Food Items')


class FoodItemViewTest(TestCase):
    def setUp(self) -> None:
        permissions = Permission.objects.filter(name__endswith='food item')
        self.user_def = User.objects.create_user(username='setup')
        self.user_def.set_password('password')
        self.user_def.user_permissions.set(list(permissions))
        self.user_def.save()
        self.client.login(username='setup', password='password')
        self.carrot = create_vegetable('carrot')
        self.carrot_it = lambda: create_food_item('carrot')
        self.carrot_item = self.carrot_it()

    def test_food_item_create(self):
        view = reverse('profiles:food_item-create')
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "FoodItem/food_item-create.html")
        self.assertEqual(response_get.resolver_match.func.__name__,
                         FoodItemCreateView.as_view().__name__)
        response_post = self.client.post(view,
                                         {'ingredient': self.carrot_item.ingredient.id,
                                          'quantity': 1})
        self.assertEqual(response_post.status_code, 302)

        self.assertEqual(self.carrot_item.ingredient, self.carrot)

    def test_food_item_list(self):
        view = reverse('profiles:food_item-list')
        response = self.client.get(view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'FoodItem/food_item-list.html')

        self.assertEqual(response.resolver_match.func.__name__,
                         FoodItemListView.as_view().__name__)
        self.assertQuerysetEqual(response.context.get('object_list'),
                                 FoodItem.objects.all(),
                                 transform=lambda x: x)

        self.assertEqual(response.context.get('object_list').first(), self.carrot_item)

    def test_food_item_update(self):
        view = reverse('profiles:food_item-update', args=[self.carrot_item.id])
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'FoodItem/food_item-update.html')

        self.assertEqual(response_get.resolver_match.func.__name__,
                         FoodItemUpdateView.as_view().__name__)

        response_post = self.client.post(view,
                                         {'ingredient': self.carrot_item.ingredient.id,
                                          'quantity': 2})
        self.assertEqual(response_post.status_code, 302)
        self.carrot_item.refresh_from_db()
        self.assertEqual(self.carrot_item.ingredient, self.carrot)
        self.assertEqual(self.carrot_item.quantity, 2)
        self.assertRaises(FoodItem.DoesNotExist,
                          FoodItem.objects.get,
                          ingredient=self.carrot_item.ingredient,
                          quantity=1)

    def test_food_item_delete(self):
        view = reverse('profiles:food_item-delete', args=[self.carrot_item.id])
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'FoodItem/food_item-delete.html')

        response_post = self.client.delete(view)
        self.assertEqual(response_post.status_code, 302)

        self.assertEqual(response_post.resolver_match.func.__name__,
                         FoodItemDeleteView.as_view().__name__)

        self.assertRaises(FoodItem.DoesNotExist,
                          FoodItem.objects.get,
                          id=self.carrot_item.id)


class ProfileViewTest(TestCase):
    def setUp(self) -> None:
        permissions = Permission.objects.filter(name__endswith='profile')
        self.user_def = User.objects.create_user(username='setup')
        self.user_def.set_password('password')
        self.user_def.user_permissions.set(list(permissions))
        self.user_def.save()
        self.client.login(username='setup', password='password')

    def test_profile_list(self):
        view = reverse('profiles:profile-list')
        response = self.client.get(view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Profile/profile-list.html')

        self.assertEqual(response.resolver_match.func.__name__,
                         ProfileListView.as_view().__name__)
        self.assertQuerysetEqual(response.context.get('object_list'),
                                 Profile.objects.all(),
                                 transform=lambda x: x)

        self.assertEqual(response.context.get('object_list').first(), self.user_def.profile)

    def test_profile_detail(self):
        view = reverse('profiles:profile-detail', args=[self.user_def.id])
        response = self.client.get(view)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Profile/profile-detail.html')

        self.assertEqual(response.resolver_match.func.__name__,
                         ProfileDetailView.as_view().__name__)
        self.assertEqual(response.context.get('object'), self.user_def.profile)

    def test_profile_update(self):
        view = reverse('profiles:profile-update', args=[self.user_def.id])
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'Profile/profile-update.html')

        self.assertEqual(response_get.resolver_match.func.__name__,
                         ProfileUpdateView.as_view().__name__)

        response_post = self.client.post(view,
                                         {'user': self.user_def.id,
                                          'weight': 60,
                                          'height': 180,
                                          'calorie_goal': 2000})
        self.assertEqual(response_post.status_code, 302)
        profile = self.user_def.profile
        profile.refresh_from_db()
        self.assertEqual(profile.user, self.user_def)
        self.assertEqual(profile.weight, 60)
        self.assertEqual(profile.height, 180)
        self.assertEqual(profile.calorie_goal, 2000)

    def test_profile_delete(self):
        view = reverse('profiles:profile-delete', args=[self.user_def.id])
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'Profile/profile-delete.html')
        self.assertContains(response_get,
                            "Deleting your profile will also delete your account.")
        self.assertContains(response_get,
                            "Are you sure you want to delete it?")

        self.assertEqual(response_get.resolver_match.func.__name__,
                         ProfileDeleteView.as_view().__name__)

        response_post = self.client.delete(view)
        self.assertEqual(response_post.status_code, 302)

        self.assertRaises(Profile.DoesNotExist,
                          Profile.objects.get, user=self.user_def)


class UserStorageViewTest(TestCase):
    def setUp(self) -> None:
        permissions = Permission.objects.filter(name__endswith='user food storage')
        self.user_def = User.objects.create_user(username='setup')
        self.user_def.set_password('password')
        self.user_def.user_permissions.set(list(permissions))
        self.user_def.save()
        self.client.login(username='setup', password='password')
        self.carrot_it = lambda: create_food_item('carrot')
        self.carrot_item = self.carrot_it()

    def test_food_storage_create(self):
        view = reverse('profiles:food_storage-create')
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "UserFoodStorage/food_storage-create.html")
        self.assertEqual(response_get.resolver_match.func.__name__,
                         UserFoodStorageCreateView.as_view().__name__)
        response_post = self.client.post(view,
                                         {'user': self.user_def.profile.pk,
                                          'food': self.carrot_item.pk})
        self.assertEqual(response_post.status_code, 302)

        storage = UserFoodStorage.objects.get(user=self.user_def.profile,
                                              food=self.carrot_item,
                                              date=date.today())
        self.assertEqual(storage.user, self.user_def.profile)

    def test_food_storage_create_with_profile(self):
        view = reverse('profiles:food_storage-w-prof-create', args=[self.user_def.profile.pk])
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "UserFoodStorage/food_storage-create.html")
        self.assertEqual(response_get.resolver_match.func.__name__,
                         UserFoodStorageCreateView.as_view().__name__)
        response_post = self.client.post(view,
                                         {'food': self.carrot_item.pk})
        self.assertEqual(response_post.status_code, 302)

        storage = UserFoodStorage.objects.get(user=self.user_def.profile,
                                              food=self.carrot_item,
                                              date=date.today())
        self.assertEqual(storage.user, self.user_def.profile)

    def test_food_storage_list(self):
        view = reverse('profiles:food_storage-list')
        response = self.client.get(view)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'UserFoodStorage/food_storage-list.html')

        self.assertEqual(response.resolver_match.func.__name__,
                         UserFoodStorageListView.as_view().__name__)
        self.assertQuerysetEqual(response.context.get('object_list'),
                                 UserFoodStorage.objects.all(),
                                 transform=lambda x: x)

    def test_food_storage_update(self):
        storage = create_storage(self.user_def.profile, self.carrot_item)
        view = reverse('profiles:food_storage-update', args=[storage.pk])
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'UserFoodStorage/food_storage-update.html')

        self.assertEqual(response_get.resolver_match.func.__name__,
                         UserFoodStorageUpdateView.as_view().__name__)
        potato = create_food_item('potato')

        response_post = self.client.post(view,
                                         {'user': self.user_def.profile.pk,
                                          'food': potato.pk})
        self.assertEqual(response_post.status_code, 302)
        storage.refresh_from_db()
        self.assertEqual(storage.user, self.user_def.profile)
        self.assertEqual(storage.food, potato)

    def test_food_storage_delete(self):
        storage = create_storage(self.user_def.profile, self.carrot_item)
        view = reverse('profiles:food_storage-delete', args=[storage.pk])
        response_get = self.client.get(view)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'UserFoodStorage/food_storage-delete.html')

        self.assertEqual(response_get.resolver_match.func.__name__,
                         UserFoodStorageDeleteView.as_view().__name__)

        response_post = self.client.delete(view)
        self.assertEqual(response_post.status_code, 302)

        self.assertRaises(UserFoodStorage.DoesNotExist, UserFoodStorage.objects.get, id=storage.pk)


class SelfProfileViewTest(TestCase):
    def setUp(self) -> None:
        self.user_def = User.objects.create_user(username='setup')
        self.user_def.set_password('password')
        self.user_def.save()

        self.client.login(username='setup', password='password')

        self.profile = self.user_def.profile
        self.profile.weight = 50
        self.profile.height = 100
        self.profile.calorie_goal = 2000
        self.profile.save()

        for _ in range(3):
            self.profile.daily_food.add(create_food_item('carrot'))

    def test_self_profile_detail_view(self):
        view = reverse('profiles:user-profile')
        response_get = self.client.get(view)

        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "Current-User/profile-detail.html")
        self.assertContains(response_get, f'{self.profile.weight} kg')
        self.assertContains(response_get, f'{self.profile.height}')
        self.assertContains(response_get,
                            f'Calories today: <strong><span style="white-space: nowrap;">{self.profile.calories_today} / {self.profile.calorie_goal}</span></strong>')
        self.assertContains(response_get,
                            f'Calories left in goal: <strong>{round(self.profile.calories_left_in_goal)}</strong>')
        self.assertContains(response_get,
                            f'Carbs today: <strong>{round(self.profile.carbs_today, 1)}</strong>')
        self.assertContains(response_get, f'Fats today: <strong>{round(self.profile.fats_today, 1)}</strong>')
        self.assertContains(response_get, f'Protein today: <strong>{round(self.profile.protein_today, 1)}</strong>')

        self.assertEqual(response_get.resolver_match.func.__name__,
                         SelfProfileDetailView.as_view().__name__)

    def test_self_user_form(self):
        view = reverse('profiles:user-form')
        response_get = self.client.get(view)

        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "Current-User/profile-form.html")

        self.assertEqual(response_get.resolver_match.func, user_food_storage_create_view)
        carrot = create_vegetable('carrot')
        potato = create_vegetable('potato')

        post_data = {
            'form-TOTAL_FORMS': 2,
            'form-INITIAL_FORMS': 0,
            'form-0-ingredient': carrot.pk,
            'form-0-quantity': 5,
            'form-1-ingredient': potato.pk,
            'form-1-quantity': 7,
        }
        response_post = self.client.post(view, post_data)
        self.assertEqual(response_post.status_code, 200)

        carrot_it_0 = FoodItem.objects.get(ingredient=carrot, quantity=5)
        potato_it_1 = FoodItem.objects.get(ingredient=potato, quantity=7)
        carrot_ufi = UserFoodStorage.objects.get(food=carrot_it_0)
        potato_ufi = UserFoodStorage.objects.get(food=potato_it_1)

        self.assertEqual(carrot_ufi.user, self.profile)
        self.assertEqual(carrot_ufi.food, carrot_it_0)
        self.assertEqual(carrot_ufi.date, date.today())
        self.assertEqual(potato_ufi.user, self.profile)
        self.assertEqual(potato_ufi.food, potato_it_1)
        self.assertEqual(potato_ufi.date, date.today())

    def test_user_food_storage(self):
        view = reverse('profiles:user-food_storage')
        response_get = self.client.get(view)

        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "Current-User/profile-food-storage.html")

        self.assertEqual(response_get.resolver_match.func.__name__,
                         FoodStorageForCurrentUserListView.as_view().__name__)

        queryset_1 = response_get.context.get('object_list').order_by('date')
        queryset_2 = UserFoodStorage.objects.filter(user=self.profile).order_by('date')

        self.assertEqual(list(queryset_1), list(queryset_2))

    def test_user_food_storage_for_today(self):
        view = reverse('profiles:user-today-food_storage')
        response_get = self.client.get(view)

        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "Current-User/profile-food-storage.html")

        self.assertEqual(response_get.resolver_match.func.__name__,
                         TodayFoodStorageForCurrentUserListView.as_view().__name__)

        queryset_1 = response_get.context.get('object_list').order_by('date')
        queryset_2 = UserFoodStorage.objects.filter(user=self.profile, date=date.today()).order_by('date')

        self.assertEqual(list(queryset_1), list(queryset_2))

