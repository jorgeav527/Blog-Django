from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager

# Create your models here.

# We are going to create a custom manager to retrieve all posts with published status.
# -----------------------------------------
class PublishedManager(models.Manager):
    def get_queryset(self): # Is the method that returns the QuerySet to be executed.
        return super(PublishedManager, self).get_queryset().filter(status='published') # We can retrieve all published posts.

# Model Post 
# -----------------------------------------
class Post(models.Model):
    STATUS_CHOICES = (
        ( "draft", "Draft" ),
        ( "published", "Published" ),
    )
    title = models.CharField( max_length=120 )
    slug = models.SlugField( max_length=250, unique_for_date="publish" ) # This way we ensure that there will be only one post with a slug for a given date
    author = models.ForeignKey( User, related_name="blog_posts", on_delete=models.CASCADE )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now) # This is just a timezone-aware datetime.now by default.
    created = models.DateTimeField(auto_now_add=True) # The date will be saved automatically when creating an object.
    updated = models.DateTimeField(auto_now=True) # The date will be updated automatically when saving an object..
    status = models.CharField( max_length=10, choices=STATUS_CHOICES, default="draft" )

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    tags = TaggableManager() # Third-party Django

    class Meta:
        ordering = ( "-publish", )

    def __str__(self):
        return f"{self.id} : {self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                    self.publish.month,
                                                    self.publish.day,
                                                    self.slug])


class Comment(models.Model): 
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80) 
    email = models.EmailField() 
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 
 
    class Meta: 
        ordering = ( 'created', ) 
 
    def __str__(self): 
        return f'Comment by {self.name} on {self.post}'