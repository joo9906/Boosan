from django.db import models
from account.models import User

# Create your models here.

class MealStore(models.Model):
    store_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone = models.CharField(max_length=20)
    merchant_type = models.CharField(max_length=50)
    is_free_meal = models.BooleanField(default=False)

    class Meta:
        db_table = 'meal_store'

class ChildMealCard(models.Model):
    card_id = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_cards')
    child_id = models.CharField(max_length=100)
    issue_date = models.DateField()
    subsidy_limit = models.IntegerField()
    balance = models.IntegerField()
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'child_meal_card'

class MealTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    card = models.ForeignKey(ChildMealCard, on_delete=models.CASCADE, related_name='transactions')
    transaction_date = models.DateField()
    transaction_time = models.TimeField()
    store = models.ForeignKey(MealStore, on_delete=models.CASCADE)
    amount = models.IntegerField()
    item_category = models.CharField(max_length=50)

    class Meta:
        db_table = 'meal_transaction'
