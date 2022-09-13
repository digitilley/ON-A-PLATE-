from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True) 
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='blogpost_like', blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"

"""
class Recipe(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recipe_posts")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="recipe_posts")
    servings = models.IntegerField()
    # ingredients = models.ManyToManyField(Ingredient)
    ingredients = models.TextField(helptext="Enter each ingredient on a new line")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    recipe_image = models.ImageField(upload_to='images/', blank=True)
    public = models.BooleanField(default=False)
    favourites = models.ManyToManyField(Profile, blank=True, related_name="recipe_favourites")
    likes = models.ManyToManyField(Profile, related_name="recipe_likes", blank=True)
    """