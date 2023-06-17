from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest

from base.batch.forms import *
from base.verifier import user_owns_resource


@login_required(login_url='login-url')
def batches(request):
    """Reads all user related batches"""

    if request.method == 'GET':
        search = request.GET.get('search', '')
        batches_q = Batch.objects.filter(created_by=request.user, name__icontains=search).order_by('-created_at')
        count = batches_q.count()

        context = {"batches": batches_q, "count": count}
        return render(request, 'batches.html', context)
    return HttpResponseBadRequest('This endpoint allows only get requests!')

@login_required(login_url='login-url')
def batch(request, pk=None):
    """Reads a specific batch and its related details"""

    if request.method == "GET":
        batch = Batch.objects.select_related('livestock').get(id=pk)

        # Check that user is resource owner
        if not user_owns_resource(request, batch):
            return HttpResponseNotAllowed('You are not permitted to access this resource!')

        # Filter batch related items based on search parameter
        search = request.GET.get('search', '')
        batch_items_q = batch.batch_items.filter(name__icontains=search)

        # Perform batch related computations
        items_count = batch_items_q.count()
        cost_per_bird = batch.cost/batch.size
        sale_details = batch.sale_details()
        mortality_details = batch.mortality_details()

        context = { 'batch': batch,
                    'items': batch_items_q,
                    'items_count': items_count,
                    'sale_details': sale_details,
                    'mortality_details': mortality_details,
                    'cost_per_bird': cost_per_bird}
        return render(request, 'batch.html', context)  
    return HttpResponseBadRequest('This endpoint allows only get requests!')

@login_required(login_url='login-url')
def create_batch(request):
    """Controls batch creation logic"""

    if request.method == 'POST':
        b_form = BatchForm(request.POST)
        l_form = LiveStockForm(request.POST)
        if b_form.is_valid() and l_form.is_valid():
            nw_batch = b_form.save(commit=False)
            nw_livestock = l_form.save(commit=False)

            # Update dependant batch attributes
            nw_batch.size = int(request.POST.get('qty'))
            nw_batch.cost = int(request.POST.get('price'))
            nw_batch.livestock = nw_livestock
            nw_batch.created_by = request.user

            # Persist changes to database
            nw_livestock.save()
            nw_batch.save()

            return redirect('batches-url')

    b_form = BatchForm()
    l_form = LiveStockForm()
    
    context = {'b_form': b_form, 'l_form': l_form}
    return render(request, 'create_batch.html', context)

@login_required(login_url='login-url')
def update_batch(request, pk=None):
    """Controls batch update logic"""

    if pk is None:
        return HttpResponseBadRequest("Resource pk is missing. Resource cannot be identified!")

    batch = Batch.objects.get(id=pk)
        
    # Check that user is resource owner
    if not user_owns_resource(request, batch):
        return HttpResponseNotAllowed('You are not permitted to access this resource!')

    if request.method == 'POST':
        b_form = BatchForm(request.POST, instance=batch)
        if b_form.is_valid():
            b_form.save()
            return redirect('batches-url')
        
    b_form = BatchForm(instance=batch)

    context = {'b_form': b_form}
    return render(request, 'update_batch.html', context)

@permission_required('base.delete_batch', raise_exception=True)
@login_required(login_url='login-url')
def delete_batch(request, pk=None):
    """Controls batch delete logic"""
    if request.method == "POST":
        batch = Batch.objects.get(id=pk)      
        if batch:
            # Check that user is resource owner
            if not user_owns_resource(request, batch):
                return HttpResponseNotAllowed('You are not permitted to access this resource!')
            batch.delete()
        messages.error(request, "Sorry, batch does not exist!")
        return redirect('batches-url')
    return HttpResponseBadRequest('This endpoint allows only post requests!')

@login_required(login_url='login-url')
def mortality(request):
    """Retrieve mortality record"""
    search = request.GET.get('search', '')
    mort_q = Mortality.objects.select_related('batch').filter(created_at__icontains=search)
    count = mort_q.count()
    worth = 0

    for mort in mort_q:
        worth += mort.cost

    context = {'mortalities': mort_q, 'worth': worth, 'count': count}
    return render(request, 'mortality.html', context)

@login_required(login_url='login-url')
def create_mortality(request):
    """Create a mortality record"""

    if request.method == 'POST':
        mort_q = MortalityForm(request.POST)
        if mort_q.is_valid:
            mort_q.save()
            return redirect('mortalities-url')

    form = MortalityForm()
    context = {'form': form}
    return render(request, 'create_mortality.html', context)

@login_required(login_url='login-url')
def update_mortality(request, pk):
    """Update a sale record"""

    if pk is None:
        return HttpResponseBadRequest("Resource pk is missing. Resource cannot be identified!")
    
    mort = Mortality.objects.select_related('batch').get(id=pk)

    # Check that user is resource owner
    if not user_owns_resource(request, mort.batch):
        return HttpResponseNotAllowed('You are not permitted to access this resource!')
    
    if request.method == 'POST':
        form = MortalityForm(request.POST, instance=mort)
        if form.is_valid():
            form.save()
            return redirect('mortalities-url')

    form = MortalityForm(instance=mort)
    context = {'form': form}
    return render(request, 'update_mortality.html', context)

@permission_required('base.delete_mortality', raise_exception=True)
@login_required(login_url='login-url')
def delete_mortality(request, pk):
    """Deletes a given mortality record"""
    try:
        mort = Mortality.objects.select_related('batch').get(id=pk)
    except Exception:
        messages.error(request, 'Could not delete Mortality record!')
        return redirect('mortalities-url')
    else:
         # Check that user is resource owner
        if not user_owns_resource(request, mort.batch):
            return HttpResponseNotAllowed('You are not permitted to access this resource!')      
        mort.delete()
        return redirect('mortalities-url')
