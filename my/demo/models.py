from django.db import models
class Customer(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField()
    email = models.CharField(unique=True)
    password = models.CharField()
    photo = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'


class Cabinet(models.Model):
    id = models.BigAutoField(primary_key=True)
    avail = models.BooleanField(default=True)
    open = models.BooleanField(default=False)
    coord = models.CharField(default='Test coord')
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
    paymentmethod = models.CharField()
    fee = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'cabinet_locker_rentals'


