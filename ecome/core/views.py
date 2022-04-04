from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView,View

from .forms import CouponForm, CheckoutForm
from .models import Address, Coupon, Item, ItemVariation,OrderItem,Order, Variation
from django.utils import timezone
class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"




class ItemDetailsView(DetailView):
    model = Item
    template_name = "product.html"
    slug_url_kwarg = "slug"

    def get_context_data(self,*args, **kwargs):
        context = super(ItemDetailsView,self).get_context_data(*args,**kwargs)
        context['items'] = Item.objects.exclude(slug=self.kwargs['slug'])
        return context

class RemoveFromCart(LoginRequiredMixin,View):
    def get(self,request,slug,*args, **kwargs):
        item = get_object_or_404(Item,slug=slug)

        order_qs = Order.objects.filter(user=request.user,ordered=False)
        
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
                order.items.remove(order_item)
                order_item.delete()
            
            return redirect("core:order-summary")
            
class AddToCart(LoginRequiredMixin,View):
    def get(self,request,slug,*args, **kwargs):
        item = get_object_or_404(Item,slug=slug)

        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )
        # for varient
        var = []

        varient = Variation.objects.filter(item=item)

        for v in varient:
            var.append(request.GET.get(v.name, None))

        order_qs = Order.objects.filter(user=request.user,ordered=False)
        
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item.qty += 1
                order_item.save()
                return redirect("core:order-summary")
            else:
                order.items.add(order_item)
                for v in var:
                    a = ItemVariation.objects.get(value=v, variation__item__slug=item.slug)
                    order_item.item_variations.add(a)
                return redirect("core:order-summary")

        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user,start_date=ordered_date)
            order.items.add(order_item)
            return redirect("core:order-summary")


            
class MinusItemCart(LoginRequiredMixin,View):
    def get(self,request,slug,*args, **kwargs):
        item = get_object_or_404(Item,slug=slug)

        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )
        # for varient
        var = []

        varient = Variation.objects.filter(item=item)

        for v in varient:
            var.append(request.GET.get(v.name, None))

        order_qs = Order.objects.filter(user=request.user,ordered=False)
        
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                if order_item.qty > 1:
                    order_item.qty -= 1
                    order_item.save()
                else: 
                    order.items.remove(order_item)

                return redirect("core:order-summary")

        else:
         
            return redirect("core:order-summary")



class OrderSummaryVIew(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try: 
            order = Order.objects.get(user=self.request.user,ordered=False)
            if order.items.count() < 1:
                return redirect("core:homepage")
            context = {"object":order,"couponform":CouponForm}
        except ObjectDoesNotExist:
            return redirect("core:homepage")

        return render(self.request,"order-summary.html",context)
        
    model = Order 
    template_name = "order_summary.html"

def check_coupon(request,code):
    try:
        coupon = Coupon.objects.get(code=code)
        return True
    except ObjectDoesNotExist:
        return False
    
def getCoupon(request,code):
    try: 
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        return redirect("core:order-summary")
class AddCouponView(View):
    def post(self,*args, **kwargs):
        if self.request.method == "POST":
            form = CouponForm(self.request.POST or None)
            if form.is_valid():
                try:
                    code = form.cleaned_data.get("code")
                    if check_coupon(self.request,code):
                        print("check don")
                        order = Order.objects.get(user=self.request.user,ordered=False)
                        order.coupon = getCoupon(self.request,code)
                        order.save()
                        return redirect("core:order-summary")
                    else: 
                        # if invalid code
                        return redirect("core:order-summary")
                except ObjectDoesNotExist:
                    # invalid cart order
                    return redirect("core:order-summary")
class RemoveCouponView(View):
    def get(self,*args, **kwargs):          
        order = Order.objects.get(user=self.request.user,ordered=False)
        order.coupon = None
        order.save()
        return redirect("core:order-summary")

class CheckOutView(View):

    def get(self,*args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            form  = CheckoutForm()
            address = Address.objects.filter(user=self.request.user)
            return render(self.request,"checkout.html",{"order":order,"forms":form,"address":address})
        
        except ObjectDoesNotExist:
            return redirect("core:checkout")
    
    
    def post(self, *args, **kwargs):
        if self.request.method=="POST":
            order = Order.objects.get(user=self.request.user,ordered=False)
            form= CheckoutForm(self.request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = self.request.user
                data.save()
                order.address = data
                order.save()
                return redirect("core:checkout")
            else:
                return redirect("core:checkout")
        else:
            return redirect("core:checkout")

def save_Address_Action(r):
    if r.method == "POST":
        order = Order.objects.get(user=r.user,ordered=False)
        save_address = r.POST.get("save_address",None)
        selected_address = Address.objects.get(id=save_address)
        order.address = selected_address
        order.save()


