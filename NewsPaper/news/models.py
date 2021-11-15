from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    full_name = models.CharField(max_length = 255)
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    rating = models.IntegerField(default = 1)

    def update_rating(self):
        post_rating = self.post_set.all().aggregate(sumrating = Sum('post_rating'))
        authors_post_rating = 0
        authors_post_rating = authors_post_rating + post_rating.get('sumrating')

        comment_rating = self.user.comment_set.all().aggregate(sumrating1 = Sum('comment_rating'))
        authors_comment_rating = 0
        authors_comment_rating = authors_comment_rating + comment_rating.get('sumrating1')

        #comment_rating2 = self.user.comment_rating_set.filter(post=self.post_set.all()).aggregate(sumrating = Sum('author_comment_rating'))
        
        authors_post_comment_rating = 0

        for i in self.post_set.all():
                comment_rating3 = self.user.comment_set.all().aggregate(sumrating1 = Sum('comment_rating'))
                authors_post_comment_rating += comment_rating3.get('sumrating1')
            
        #users_comment_rating = 0
        #users_comment_rating += comment_rating2.get('author_comment_rating')

        #self.rating = 3 * authors_post_rating + authors_post_comment_rating + users_comment_rating
        self.raiting = authors_post_comment_rating
        self.save()

class Category(models.Model):
	category_name = models.CharField(max_length = 255, unique = True)	

class Post(models.Model):
    post = 'PO'
    news = 'NW'
    POSITIONS=[
    (post,'post'), 
    (news,'news'),]
    post_author = models.ForeignKey(Author, on_delete = models.CASCADE)
    post_type = models.CharField(max_length=2, choices= POSITIONS)
    post_date_created = models.DateField(auto_now_add = True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    head_of_post = models.CharField(max_length = 255)
    article_text = models.TextField()
    post_rating = models.IntegerField(default = 1)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
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
    comment_rating = models.IntegerField(default = 1) 
    
    def like(self):
        self.comment_rating +=1
        self.save()
    
    def dislike(self):
        self.comment_rating -=1
        self.save()