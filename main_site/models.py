# Create your models here.

from django.contrib.auth.models import User
from django.db.models import (Model, 
CharField,
DateTimeField, 
ForeignKey, 
ImageField, 
TextField,
CASCADE)

class ImgPost(Model):
    title = CharField(max_length=64)
    description = TextField()
    img = ImageField(upload_to='post_imgs/')
    publish_date = DateTimeField(auto_now_add=True) 
    owner = ForeignKey(to=User, on_delete=CASCADE)
    
    def __str__(self) -> str:
        return f"{self.title} | {self.owner.username} | {self.publish_date}"

class Comment(Model):
    content = TextField()
    publish_date = DateTimeField(auto_now_add=True)
    owner = ForeignKey(to=User, on_delete=CASCADE)
    post = ForeignKey(to=ImgPost, on_delete=CASCADE)

    def __str__(self) -> str:
        return f"{self.post} | {self.get_content_summary()} | {self.owner.username} | {self.publish_date}"

    def get_content_summary(self):
        """Returns content's first 10 word."""
        
        result_list = self.content.split()[:10]
        result_str = " ".join(result_list)
        
        return result_str 