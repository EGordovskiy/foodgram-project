from django.db import models
from django.contrib.auth import get_user_model
from sorl.thumbnail import ImageField

User = get_user_model()


class Ingredients(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    dimension = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=10)
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    color = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe_author')
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='recipes/', 
        blank=True, 
        null=True)
    description = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredients,
        related_name='recipe_ingredient',
        through='IngredientRecipe'
    )
    tag = models.ManyToManyField(Tag)
    cooking_time = models.IntegerField()
    pub_date = models.DateTimeField(
        'date published', 
        auto_now_add=True)

    def __str__(self):
        return self.title


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE,
        related_name='recipe_ingredients')
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='recipes')
    amount = models.IntegerField()


class FollowRecipe(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='follower_recipe')
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE, 
        related_name='following_recipe')

    def __str__(self):
        return f'follower - {self.user} following recipe - {self.recipe}'


class FollowUser(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='follower')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='following')

    def __str__(self):
        return f'follower - {self.user} following - {self.author}'

class ShopingList(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='user_shoping_list')
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE,
        related_name='recipe_shoping_list')
