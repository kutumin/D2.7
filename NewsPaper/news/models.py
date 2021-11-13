from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    full_name = models.CharField(max_length = 255)
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    raiting = models.IntegerField(default = 1)

    def update_rating(self):
        authors_post_raiting = self.post_raiting_set.all().aggregate()
        authors_comment_raiting = self.comment_raiting_set.all().aggregate()
        users_comment_rairing = self.user.comment_raiting_set.all().aggregate()
        self.raiting = 3 * authors_post_raiting + authors_comment_raiting + users_comment_rairing
        self.save()

class Category(models.Model):
	category_name = models.CharField(max_length = 255, unique = True)	

class Post(models.Model):
    post = 'PO'
    news = 'NW'
    POSITIONS=[
    (post,'post'), 
    (news,'news'),
        ]
    post_author = models.ForeignKey(Author, on_delete = models.CASCADE)
    post_type = models.CharField(max_length=2, choices= POSITIONS, unique=True)
    post_date_created = models.DateField(auto_now_add = True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    head_of_post = models.CharField(max_length = 255)
    article_text = models.TextField()
    post_raiting = models.IntegerField(default = 1)

    def like(self):
        self.post_raiting += 1
        self.save()

    def dislike(self):
        self.post_raiting -= 1
        self.save()

    def preview(self):
        review = self.article_text[:124]+'...'
        return review

class PostCategory(models.Model):
	post = models.ForeignKey(Post, on_delete = models.CASCADE)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment_user = models.ForeignKey(User,on_delete = models.CASCADE)
    comment_text = models.TextField()
    comment_date_created = models.DateField(auto_now_add = True)
    comment_raiting = models.IntegerField(default = 1) 
    
    def like(self):
        self.comment_raiting +=1
        self.save()
    
    def dislike(self):
        self.comment_raiting -=1
        self.save()