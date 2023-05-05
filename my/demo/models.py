from django.db import models
class Customer(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    photo = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'


class Cabinet(models.Model):
    id = models.BigAutoField(primary_key=True)
    avail = models.BooleanField(default=True)
    coord = models.CharField(max_length=100,default='Test coord')
    start = models.DateTimeField(blank=True, null=True)
    userid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='userid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cabinet'


class CabinetLockerRentals(models.Model):
    id = models.BigAutoField(primary_key=True)
    cabinetid = models.ForeignKey(Cabinet, models.DO_NOTHING, db_column='cabinetid')
    customerid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='customerid')
    rentdate = models.DateTimeField()
    duration = models.DurationField()
    paymentmethod = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'cabinet_locker_rentals'


