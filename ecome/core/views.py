from ast import arg
from importlib.resources import contents
from re import template
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView,DetailView,View
from .models import Item, ItemVariation,OrderItem,Order, Variation

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


class AddToCart(View):
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
            if order.items.filter(user=request.user,ordered=False):
                order_item.qty += 1
                order_item.save()
            else:
                order.items.add(order_item)
                for v in var:
                    a = ItemVariation.objects.get(value=v, variation__item__slug=item.slug)
                    order_item.item_variations.add(a)



    