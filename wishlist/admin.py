from django.contrib import admin

from wishlist.models import Customer, Product, Review, Wishlist

admin.site.register(Customer)
admin.site.register(Wishlist)
admin.site.register(Product)
admin.site.register(Review)
