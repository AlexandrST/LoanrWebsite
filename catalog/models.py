from django.db import models
from django.urls import reverse
import uuid
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


class ItemType(models.Model):
    """Model representing a item item_type (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(
        max_length=200,
        help_text="Enter a item item_type (e.g. Science Fiction, French Poetry etc.)"
        )

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

class Item(models.Model):
    """Model representing a item (but not a specific copy of a item)."""
    title = models.CharField(max_length=200)
    rentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000)
    item_type = models.ManyToManyField(ItemType)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_posted = models.DateTimeField(auto_now_add=True,blank=True)
    active = models.BooleanField(default=True)

    def display_item_type(self):
        """Creates a string for the ItemType. This is required to display item_type in Admin."""
        return ', '.join([item_type.name for item_type in self.item_type.all()[:3]])

    display_item_type.short_description = 'ItemType'

    def get_absolute_url(self):
        """Returns the url to access a particular item instance."""
        return reverse('item-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class Rentor(models.Model):
    """Model representing an rentor."""
    user = models.OneToOneField(User, related_name='userprofile',on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True,blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular rentor instance."""
        return reverse('rentor-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.user.last_name,self.user.first_name)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Rentor.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

class CreditCard(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    cc_number = CardNumberField('card number')
    cc_expiry = CardExpiryField('expiration date')
    cc_code = SecurityCodeField('security code')

    def get_absolute_url(self):
        """Returns the url to access a particular item instance."""
        return reverse('card-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.cc_number
