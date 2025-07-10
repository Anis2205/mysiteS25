from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Publisher, Book
from .forms import FeedbackForm, SearchForm, OrderForm

# This file contains views for the myapp application in a Django project.

# This is the main view that lists all books and publishers.
def index(request):
    # response = HttpResponse()

    # # List of books ordered by primary key
    # booklist = Book.objects.all().order_by('pk')
    # heading1 = '<h2>List of available books (by ID):</h2>'
    # response.write(heading1)
    # for book in booklist:
    #     para = f'<p>{book.pk}: {book.title}</p>'
    #     response.write(para)
 
    # # List of publishers ordered by city in descending order
    # publisher_list = Publisher.objects.all().order_by('-city')
    # heading2 = '<h2>List of Publishers (sorted by city, descending):</h2>'
    # response.write(heading2)
    # for publisher in publisher_list:
    #     para = f'<p>{publisher.name} – {publisher.city}</p>'
    #     response.write(para)

    # return response
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': booklist})


# This view provides information about the application.
def about(request):
    return HttpResponse("This is an eBook APP.")

# Detail view for a specific book
def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    title_upper = book.title.upper()
    price_display = f"${book.price}"
    publisher_name = book.publisher.name

    html = f"<h2>{title_upper}</h2><p>Price: {price_display}</p><p>Publisher: {publisher_name}</p>"
    return HttpResponse(html)



#    Publisher.objects.get_or_create(
#         name="Springer",
#         defaults={
#             "website": "https://www.springer.com/",
#             "city": "chicago",
#             "country": "Germany"
#         }
#     )

# This view renders an about page with static content.
def about0(request):
    # No extra context variables are needed for this template
    return render(request, 'myapp/about.html')

# Detail view for a specific book using template
def detail0(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    # YES - passing book variable to the template
    return render(request, 'myapp/detail.html', {'book': book})

def getFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            if feedback == 'B':
                choice = ' to borrow books.'
            elif feedback == 'P':
                choice = ' to purchase books.'
            else: choice = ' None.'
            return render(request, 'myapp/fb_results.html', {'choice':choice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form':form})

def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']
            
            if category:
                booklist = Book.objects.filter(category=category, price__lte=max_price)
            else:
                booklist = Book.objects.filter(price__lte=max_price)
            
            return render(request, 'myapp/results.html', {'name': name, 'category': category, 'booklist': booklist})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form': form})

def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save(commit=False)
            member = order.member
            type = order.order_type
            order.save()
            form.save_m2m()
            if type == 1:
                for b in order.books.all():
                    member.borrowed_books.add(b)
            return render(request, 'myapp/order_response.html', {'books': books, 'order':order})
        else:
            return render(request, 'myapp/placeorder.html', {'form':form})
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form':form})