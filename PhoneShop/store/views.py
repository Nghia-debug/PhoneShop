from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse   # thêm dòng này cho about
from .models import Product

def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:8]
    return render(request, 'store/home.html', {'featured_products': featured_products})

def product_list(request):
    products = Product.objects.all().order_by('created_at')
    return render(request, 'store/product_list.html', {'products': products})   # sửa ngoặc

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})

def cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
        total += subtotal   # dòng này rất quan trọng
    return render(request, 'store/cart.html', {
        'products': products,
        'total': total
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

# Thêm hàm about
def about(request):
    return HttpResponse("Trang giới thiệu - PhoneShop")