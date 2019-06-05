from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from .models import Item, Rentor, ItemType, CreditCard
from .forms import EditProfileForm, RegistrationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.http import HttpResponse
import datetime
import operator

def change_status(request):
    item = Item.objects.filter(pk=self.args['pk'])
    item.active ^= True
    item.save()

def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        items = Item.objects.filter(title__icontains=q)
        return render(request,'catalog/search_results.html', {'items':items,'query':q})
    else:
        return HttpResponse('Please submit a search term')

def index(request):
    """View function for home page of site."""
    num_items = Item.objects.all().count()
    num_rentors = Rentor.objects.count()


    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1


    return render(
        request,
        'index.html',
        context={'num_items': num_items,
                 'num_rentors': num_rentors,
                 'num_visits': num_visits},
    )

class CardListView(generic.ListView):
    """Generic class-based view for a list of credit cards"""
    model = CreditCard
    paginate_by = 10

    template_name = 'catalog/creditcard_list.html'

    def get_queryset(self):
        user = self.request.users
        creditcard_list = CreditCard.objects.filter(created_by=user)

class CardDetailView(generic.DetailView):
    """Generic class-based detail view for a credit card."""
    model = CreditCard

class ItemListView(generic.ListView):
    """Generic class-based view for a list of items."""
    model = Item
    paginate_by = 10

    template_name = 'catalog/item_list.html'


class ItemDetailView(generic.DetailView):
    """Generic class-based detail view for a item."""
    model = Item


class RentorListView(generic.ListView):
    """Generic class-based list view for a list of rentors."""
    model = Rentor
    paginate_by = 10

    template_name = 'catalog/rental_list.html'


class RentorDetailView(generic.DetailView):
    """Generic class-based detail view for an rentor."""
    model = Rentor


from django.contrib.auth.mixins import LoginRequiredMixin

class CardByUserListView(generic.ListView):
    model = CreditCard
    template_name = 'catalog/creditcard_list.html'
    paginate_by = 10



class LoanedItemsByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing items on loan to current user."""
    model = Item
    template_name = 'catalog/iteminstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Item.objects.filter(rentor=self.request.user)


def Register(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # update_session_auth_hash(request, form.user)
            return redirect('/')
    else:
        form = RegistrationForm()

    args = {'form': form}
    return render(request, 'catalog/reg_form.html',args)

def ViewProfile(request):
    args = {'user':request.user}
    return render(request,'catalog/user_profile.html',args)

def EditProfile(request):
    if request.method=='POST':
        form = EditProfileForm(request.POST,instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = EditProfileForm(instance=request.user)

    args={'form':form}
    return render(request, 'catalog/edit_profile.html',args)

def ChangePassword(request):
    if request.method=='POST':
        form = PasswordChangeForm(data=request.POST,user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/')
    else:
        form = PasswordChangeForm(user=request.user)

    args={'form':form}
    return render(request, 'catalog/change_password.html',args)

class RentorCreate(CreateView):
    model = Rentor
    fields = '__all__'



class RentorUpdate(UpdateView):
    model = Rentor
    fields = ['first_name', 'last_name', 'date_of_birth']


class RentorDelete(DeleteView):
    model = Rentor
    success_url = reverse_lazy('rentors')

class ItemCreate(CreateView):
    model = Item

    # fields = '__all__'
    fields = ['title','summary','item_type','price',]

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.rentor = self.request.user
        return super(ItemCreate, self).form_valid(form)


class CardCreate(CreateView):
    model = CreditCard
    fields = ['cc_number','cc_expiry','cc_code']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CardDelete(DeleteView):
    model = CreditCard
    success_url = reverse_lazy('card_list')


class ItemUpdate(UpdateView):
    model = Item
    fields = '__all__'


class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy('items')
