import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysiteS25.settings')
django.setup()

from myapp.models import Publisher, Book, Member, Order
from django.contrib.auth.models import User

# --- DELETE EXISTING DATA ---
Order.objects.all().delete()
Member.objects.all().delete()
Book.objects.all().delete()
Publisher.objects.all().delete()
# Delete all users except superuser (id=1 is usually superuser, adjust if needed)
User.objects.exclude(is_superuser=True).delete()

# --- PUBLISHERS ---
publishers = [
    {"name": "Wiley", "website": "https://www.wiley.com/", "city": "Hoboken", "country": "USA"},
    {"name": "Pearson", "website": "https://www.pearson.com/", "city": "London", "country": "England"},
    {"name": "Random House", "website": "http://www.randomhousebooks.com/", "city": "New York", "country": "USA"},
]
publisher_objs = {}
for pub in publishers:
    obj, _ = Publisher.objects.get_or_create(
        name=pub["name"],
        website=pub["website"],
        city=pub["city"],
        country=pub["country"]
    )
    publisher_objs[pub["name"]] = obj

# --- BOOKS ---
books = [
    {"title": "Advanced Optical Networks", "category": "S", "num_pages": 110, "price": 98.99, "publisher": "Wiley"},
    {"title": "Wireless Networks", "category": "S", "num_pages": 300, "price": 187.54, "publisher": "Pearson"},
    {"title": "A New World", "category": "T", "num_pages": 75, "price": 60.00, "publisher": "Random House"},
    {"title": "Python Programming", "category": "S", "num_pages": 275, "price": 125.99, "publisher": "Pearson"},
    {"title": "A Good Story", "category": "F", "num_pages": 155, "price": 15.00, "publisher": "Random House"},
    {"title": "Jane Austen", "category": "B", "num_pages": 360, "price": 45.50, "publisher": "Random House"},
    {"title": "Jane Eyre", "category": "F", "num_pages": 280, "price": 9.99, "publisher": "Random House"},
    {"title": "Art History", "category": "O", "num_pages": 430, "price": 155.75, "publisher": "Wiley"},
]
book_objs = []
for book in books:
    obj, _ = Book.objects.get_or_create(
        title=book["title"],
        category=book["category"],
        num_pages=book["num_pages"],
        price=book["price"],
        publisher=publisher_objs[book["publisher"]]
    )
    book_objs.append(obj)

# --- MEMBERS ---
members = [
    {
        "first_name": "John", "last_name": "Smith", "username": "john", "password": "johnpass",
        "status": 2, "address": "123 University Avenue", "city": "Windsor", "province": "ON",
        "borrowed_books": [1, 2, 4], "last_renewal": "2024-02-28", "auto_renew": True
    },
    {
        "first_name": "Mary", "last_name": "Hall", "username": "mary", "password": "marypass",
        "status": 1, "address": "456 Sunset Avenue", "city": "Windsor", "province": "ON",
        "borrowed_books": [1, 3], "last_renewal": "2024-02-14", "auto_renew": True
    },
    {
        "first_name": "Alan", "last_name": "Jones", "username": "alan", "password": "alanpass",
        "status": 1, "address": "789 King Street", "city": "Calgary", "province": "AB",
        "borrowed_books": [2], "last_renewal": "2024-03-22", "auto_renew": False
    },
    {
        "first_name": "Josh", "last_name": "Jones", "username": "josh", "password": "joshpass",
        "status": 3, "address": "456 Sunset Avenue", "city": "Montreal", "province": "QC",
        "borrowed_books": [], "last_renewal": "2024-02-10", "auto_renew": False
    },
    {
        "first_name": "Bill", "last_name": "Wang", "username": "bill", "password": "billpass",
        "status": 2, "address": "", "city": "Edmononton", "province": "AB",
        "borrowed_books": [3, 7, 8], "last_renewal": "2024-02-28", "auto_renew": True
    },
    {
        "first_name": "Anne", "last_name": "Wang", "username": "anne", "password": "annepass",
        "status": 2, "address": "102 Curry Avenue", "city": "Edmononton", "province": "AB",
        "borrowed_books": [], "last_renewal": "2024-04-02", "auto_renew": True
    },
]
member_objs = {}
for mem in members:
    user = User.objects.create_user(
        username=mem["username"],
        first_name=mem["first_name"],
        last_name=mem["last_name"],
        password=mem["password"]
    )
    member = Member.objects.create(
        user=user,
        status=mem["status"],
        address=mem["address"],
        city=mem["city"],
        province=mem["province"],
        last_renewal=mem["last_renewal"],
        auto_renew=mem["auto_renew"],
    )
    # Assign borrowed books by index (1-based to 0-based)
    if mem["borrowed_books"]:
        books_qs = [book_objs[i-1] for i in mem["borrowed_books"]]
        member.borrowed_books.set(books_qs)
    member.save()
    member_objs[mem["username"]] = member

# --- ORDERS ---
orders = [
    {"member": "john", "books": [1, 2], "order_type": 1, "order_date": "2024-03-02"},
    {"member": "john", "books": [3, 4], "order_type": 1, "order_date": "2024-02-19"},
    {"member": "mary", "books": [1, 3], "order_type": 1, "order_date": "2024-03-02"},
    {"member": "alan", "books": [2], "order_type": 1, "order_date": "2024-03-24"},
    {"member": "bill", "books": [3, 7, 8], "order_type": 1, "order_date": "2024-03-02"},
    {"member": "mary", "books": [5, 6], "order_type": 0, "order_date": "2024-02-25"},
    {"member": "josh", "books": [5, 8], "order_type": 0, "order_date": "2024-03-02"},
]
for ord in orders:
    member = member_objs[ord["member"]]
    order = Order.objects.create(
        member=member,
        order_type=ord["order_type"],
        order_date=ord["order_date"]
    )
    books_qs = [book_objs[i-1] for i in ord["books"]]
    order.books.set(books_qs)
    order.save()

print("Database reset and populated with new data.")