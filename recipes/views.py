from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import RecipeForm
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Ingredients, Recipe, FollowRecipe, \
    FollowUser, Tag, IngredientRecipe, User, ShopingList

from .utils import get_ingredients


@user_passes_test(lambda u: u.is_superuser)
def add_ingredients(self):
    import json
    from django.http import HttpResponse

    with open('ingredients.json', 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    for i in data:
        print('You added this new ingredient:', i)
        ingredient = Ingredients(title=i['title'], dimension=i['dimension'])
        ingredient.save()
    return HttpResponse('\n'.join(str(data)))


def index(request):
    recipe_list = Recipe.objects.all()
    tags_slug = request.GET.getlist('filters')

    if tags_slug:
        recipe_list = recipe_list.filter(
            tag__slug__in=tags_slug).distinct().all()
    paginator = Paginator(recipe_list, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def profile(request, username):
    recipe_author = get_object_or_404(User, username=username)
    tag = request.GET.getlist('filters')
    recipe_list = Recipe.objects.filter(
        author=recipe_author).order_by('-pub_date').all()
    if tag:
        recipe_list = recipe_list.filter(tags__slug__in=tag)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'authorRecipe.html',
                  {
                      'page': page,
                      'paginator': paginator,
                      'username': recipe_author,
                  }
                  )


def recipe_view(request, recipe_id, username):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    username = get_object_or_404(User, username=username)
    return render(request, 'singlePage.html', {'username': username, 'recipe': recipe})


@login_required
def new_recipe(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        print(request.POST)
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            recipe = Recipe.objects.create(
                author=request.user,
                title=form.cleaned_data['title'],
                image=form.cleaned_data['image'],
                description=form.cleaned_data['description'],
                cooking_time=form.cleaned_data['cooking_time'],
            )
            recipe.ingredients_set.add(recipe)
            recipe.tag_set.add(recipe)
            recipe.save_m2m()
            return redirect('/')
    form = RecipeForm()
    return render(request, 'new_recipe.html', {'form': form})


def recipe_edit(request):
    pass


def purchases_list(request, user):
    pass
