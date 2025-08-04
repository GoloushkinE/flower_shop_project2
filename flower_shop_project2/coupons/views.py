from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
            messages.success(request, _('Промокод успешно применен.'))
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(request, _('Такого промокода не существует или он недействителен.'))
    
    return redirect('cart:cart_detail')

@require_POST
def coupon_remove(request):
    """
    Удаляет промокод из сессии.
    """
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        request.session['coupon_id'] = None
        messages.success(request, _('Промокод был удален.'))
    return redirect('cart:cart_detail')