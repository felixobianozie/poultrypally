from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from base.sale.forms import *
from base.verifier import user_owns_resource


@login_required(login_url='login-url')
def sale(request):
    """Retrieve sales record"""
    search = request.GET.get('search', '')
    sale_q = Sale.objects.filter(description__icontains=search)
    count = sale_q.count()
    worth = 0

    for sale in sale_q:
        worth += sale.amount

    context = {'sales': sale_q, 'worth': worth, 'count': count}
    return render(request, 'base/sales.html', context)

@login_required(login_url='login-url')
def make_sale(request):
    """Create a sales record"""

    if request.method == 'POST':
        sales_q = SalesForm(request.POST)
        if sales_q.is_valid:
            sales_q.save()
            return redirect('sales-url')

    form = SalesForm()
    context = {'form': form}
    return render(request, 'base/make_sale.html', context)

@login_required(login_url='login-url')
def update_sale(request, pk):
    """Update a sale record"""
    if pk is None:
        return HttpResponseBadRequest("Resource pk is missing. Resource cannot be identified!")
        
    sale = Sale.objects.get(id=pk)

    # Check that user is resource owner
    if not user_owns_resource(request, sale.batch):
        return HttpResponseBadRequest('You are not permitted to access this resource!')
    
    if request.method == 'POST':
        form = SalesForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('sales-url')

    form = SalesForm(instance=sale)
    context = {'form': form, 'sale': sale}
    return render(request, 'base/update_sale.html', context)

@permission_required('base.delete_sale', raise_exception=True)
@login_required(login_url='login-url')
def delete_sale(request, pk):
    """Deletes a given sale object"""

    try:
        sale = Sale.objects.select_related('batch') .get(id=pk)
    except Exception:
        messages.error(request, 'Could not delete Mortality record!')
        return redirect('sales-url')
    else:
        # Check that user is resource owner
        if not user_owns_resource(request, sale.batch):
            return HttpResponseBadRequest('You are not permitted to access this resource!')
        sale.delete()
        return redirect('sales-url')
