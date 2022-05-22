from django.db import models

# Create your models here.
import uuid

# Create your models here.
class CoreModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    

    def __str__(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return self.__str__()
        
    @classmethod
    def get_hidden_fields(cls):
        return ["created_at", "updated_at", "is_deleted", "deleted_at"]
    class Meta:
        abstract = True

class CoreUserModel(models.Model):
    
    is_verified = models.BooleanField(default=False)
    notification_eamil= models.EmailField(null=True, blank=True)

    class Meta:
        abstract = True


