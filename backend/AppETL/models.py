from django.db import models

# Tabla Customer
class Customer(models.Model):
    customer_id = models.SmallIntegerField(primary_key=True)
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='customers')
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=50)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='customers')
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Tabla Rental
class Rental(models.Model):
    rental_id = models.AutoField(primary_key=True)
    rental_date = models.DateTimeField()
    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE, related_name='rentals')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='rentals')
    return_date = models.DateTimeField(null=True, blank=True)
    staff_id = models.SmallIntegerField()
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rental {self.rental_id}"


# Tabla Store
class Store(models.Model):
    store_id = models.SmallIntegerField(primary_key=True)
    manager_staff_id = models.SmallIntegerField()
    address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='stores')
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Store {self.store_id}"


# Tabla Inventory
class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    film = models.ForeignKey('Film', on_delete=models.CASCADE, related_name='inventories')
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='inventories')
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventory {self.inventory_id}"


# Tabla Film
class Film(models.Model):
    film_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_year = models.IntegerField()
    language = models.ForeignKey('Language', on_delete=models.CASCADE, related_name='films')
    original_language = models.ForeignKey('Language', null=True, blank=True, on_delete=models.SET_NULL, related_name='original_films')
    rental_rate = models.DecimalField(max_digits=4, decimal_places=2)
    length_rate = models.DecimalField(max_digits=5, decimal_places=2)
    length = models.SmallIntegerField()
    replacement_cost = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.CharField(max_length=10)
    special_features = models.TextField()
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Tabla Address
class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address


# Tabla Language
class Language(models.Model):
    language_id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
