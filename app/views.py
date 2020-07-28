from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, SellerAccount
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import ItemForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def seller_sign_up(request):
    if request.user.is_authenticated:
        return request('dashboard')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_staff = True
                user.save()
                SellerAccount.objects.create(user=user)
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('dashboard')
        return render(request, 'signup.html', {'form': UserCreationForm()})

def seller_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')    
    else:        
        if request.method == 'POST':
            user = authenticate(username= request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        return render(request, 'login.html', {'form': AuthenticationForm()})

    
def seller_dashboard(request):
    if request.user.is_authenticated and request.user.is_staff:
        items = Item.objects.filter(seller__user = request.user)
        return render(request, 'sellerdashboard.html', {'items': items})
    else:
        return redirect('login')

def seller_logout(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_authenticated:
            logout(request)
            return redirect('login')
        return render(request, 'sellerdashboard.html')
    else:
        return redirect('login')

def seller_add_product(request):
    if request.user.is_authenticated and request.user.is_staff:    
        form = ItemForm()
        if request.method == 'POST':
            form = ItemForm(request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                item.seller = SellerAccount.objects.get(user=request.user)
                item.img = request.POST['img']
                item.save()
                return redirect('dashboard')
        else:
            return render(request, 'addproduct.html', {'form': form})
    else:
        return redirect('login')

def seller_edit_product(request, pk):
    if request.user.is_authenticated and request.user.is_staff:
        item = get_object_or_404(Item, pk = pk, seller__user = request.user)
        form = ItemForm(instance=item)
        if request.method == 'POST':
            form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                item = form.save(commit=False)
                item.seller = SellerAccount.objects.get(user=request.user)
                item.save()
                return redirect('dashboard')
        else:
            return render(request, 'editproduct.html', {'form': form})
    else:
        return redirect(login)

def seller_delete_product(request, pk):
    if request.user.is_authenticated and request.user.is_staff:

        item = get_object_or_404(Item, pk = pk, seller__user = request.user)
        item.delete()
        return redirect('dashboard')
    else:
        return redirect('login')

def seller_view_product(request, pk):
    if request.user.is_authenticated and request.user.is_staff:
            
        item = get_object_or_404(Item, pk = pk, seller__user = request.user)
        return render(request, 'viewproduct.html', {'item': item})
    else:
        return redirect('login')

