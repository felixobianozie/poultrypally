from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from base.models import Batch
from base.item.forms import *
from base.verifier import user_owns_resource


@login_required(login_url='login-url')
def store_items(request):
    """Controls item read logic"""
    if request.method == "GET":
        search = request.GET.get('search', '')
        item_q = Item.objects.filter(batch=None, name__icontains=search)
        count = item_q.count()
        worth = 0

        for item in item_q:
            worth += item.price

        # Get batches associated with current user
        # ----- this section is yet to be completed -----
        batch_q = Batch.objects.filter()

        context = {'worth': worth, 'count': count, 'items': item_q, 'batches': batch_q}
        return render(request, 'store.html', context)
    return HttpResponseNotAllowed("This endpoint allows only get requests!")

@login_required(login_url='login-url')
def create_item(request):
    """Create item creation logic"""

    if request.method == 'POST':
        i_form = ItemForm(request.POST)
        batch_id = request.POST.get('batch_id', '')

        if batch_id:
            # Create item to given batch
            try:
                batch = Batch.objects.get(id=batch_id)
            except:
                messages.error("Could not create item. Batch does not exist!")
                return redirect(resolve_url('batches-url'))
            if i_form.is_valid():
                nw_item = i_form.save(commit=False)
                nw_item.batch = batch
                nw_item.save()
                nw_item.batch.update_cost()
                # Notify success
                tmp = f"Item: {nw_item.name}, successfuly created."
                messages.success(request, tmp)
            return redirect(resolve_url('batch-url', pk=batch_id))
        else:
            # Create item to no batch i.e to store
            if i_form.is_valid():
                nw_item = i_form.save()
            # Notify success
            tmp = f"Item: {nw_item.name}, successfuly created."
            messages.success(request, tmp)
            return redirect('store-url')

    i_form = ItemForm()
    batch_id = request.GET.get('batch_id', '')

    context = {'batch_id': batch_id, 'i_form': i_form}
    return render(request, 'create_item.html', context)

@login_required(login_url='login-url')
def update_item(request, pk=None):
    """Controls item update logic"""
    if pk:
        item = Item.objects.select_related('batch').get(id=pk)

    # Check that user is resource owner
    if not user_owns_resource(request, item.batch):
        return HttpResponseBadRequest('You are not permitted to access this resource!')

    if request.method == 'POST':
        i_form = ItemForm(request.POST, instance=item)
        if i_form.is_valid():
            i_form.save()

            # Update batch cost for item associated with a batch
            if item.batch:
                item.batch.update_cost()
                return redirect(resolve_url('batch-url', pk=item.batch.id))
            return redirect('store-url')
    i_form = ItemForm(instance=item)

    context = {'i_form': i_form}
    return render(request, 'base/update_item.html', context)

@permission_required('base.delete_item')
@login_required(login_url='login-url')
def delete_item(request, pk=None):
    """Controls item delete logic"""
    if request.method == "POST":
        # Check item exists
        if pk:
            item = Item.objects.get(id=pk)
        if item:
            # Check that user is resource owner
            # if not user_owns_resource(request, item):
            #     messages.error(request, "You are not permitted to access this resource!")
            #     return redirect("home-url")
            batch = item.batch
            item.delete()
            messages.info(request, "Item has been successfully deleted.")
            if batch:
                batch.update_cost()
                return redirect(resolve_url('batch-url', pk=batch.id))
            return redirect('store-url')
        messages.error(request, "Sorry, item does not exist!")
        return redirect("home-url")
    
    return HttpResponseNotAllowed('This endpoint allows only post requests!')

@login_required(login_url='login-url')
def forward_item(request, pk=None):
    """Forwards item from store to a given batch"""
    if request.method == "POST":
        if pk:
            item = Item.objects.get(id=pk)
        
        batch_id = request.POST.get('batch', "")
        batch = Batch.objects.get(id=batch_id)
        if not batch:
            messages.error(request, "Selected batch was not found!")
            return redirect("store-url")
        
        select = request.POST.get('select', "")

        # Reassigns item when select == "all"
        def select_is_all():
            item.batch = batch
            item.save()
            tmp = "Successfully assigned " + item.name + " to " + batch.name
            messages.success(request, tmp)
            del tmp
            
        if select == "all":
            select_is_all()
            return redirect("store-url")
        
        if select == "some":
            # Check that quatity available in store is sufficient
            tmp = request.POST.get('qty','')
            if not tmp:
                messages.error(request, 'Quantity field is required!')
                return  redirect('store-url')
            qty = int(tmp)
            del tmp
            if item.qty < qty:
                messages.error(request, 'Store has insufficient quantity of your choice item!')
                return  redirect('store-url')
            if item.qty == qty:
                select_is_all()
                return redirect("store-url")
            
            nw_item = Item(name=item.name, description=item.description, measure=item.measure, packaging=item.packaging)
            # Price reconciliation 
            tmp = round((item.price / item.qty)) * qty
            item.price -= tmp
            nw_item.price = tmp
            del tmp

            # Quantity reconciliation
            item.qty -= qty
            nw_item.qty = qty

            # Other reconciliations
            nw_item.batch = batch
            nw_item.created_from = item
            item.save()
            nw_item.save()

            tmp = "Successfully assigned " + item.name + " to " + batch.name
            messages.success(request, tmp)
            del tmp
            return redirect("store-url")


@login_required(login_url="login-url")
def return_item(request, pk=None):
    """Returns item from a given batch to the store"""

    if request.method == "POST":
        if pk:
            item = Item.objects.get(id=pk)

        select = request.POST.get('select', "")        
        
        # Find item parent in store
        try:
            store_item = Item.objects.get(created_from=item)
        except ObjectDoesNotExist:
            store_item = None

        # Check quantity
        def check_quantity():
            tmp = request.POST.get('qty', '')
            if not tmp:
                messages.error(request, 'Quantity field is required!')
                return  redirect(resolve_url('batch-url', item.batch.id))
            qty = int(tmp)
            del tmp
            if item.qty < qty:
                messages.error(request, 'Choice quantity is beyond what is available in item!')
                return  redirect(resolve_url('batch-url', item.batch.id))
            if item.qty == qty:
                batch_id = select_is_all()
                return  redirect(resolve_url('batch-url', batch_id))
            return qty

        # Item parent is in store
        if store_item:
            # Returns item when select == "all"
            def select_is_all():
                # Price & quantity reconciliation
                store_item.price += item.price
                store_item.qty += item.qty
                tmp = item.batch
                item_batch_id = item.batch.id
                item.delete()
                # Save store item
                store_item.save()
                # Update cost of batch associated with item
                tmp.update_cost()
                tmp = f'Item:{item.name} has been returned to store.'
                messages.success(request, tmp)
                del tmp
                return item_batch_id

            if select == "all":
                batch_id = select_is_all()
                return  redirect(resolve_url('batch-url', batch_id))
            
            if select == "some":
                # Check that quatity selected is not more than item.qty
                qty = check_quantity()
                
                # Price reconciliation
                tmp = round((item.price / item.qty)) * qty
                item.price -= tmp
                store_item.price += tmp
                del tmp

                # Quantity reconciliation
                item.qty -= qty
                store_item.qty += qty

                # Other reconciliations
                item.batch.update_cost()
                item.save()
                store_item.save()

                tmp = "Successfully returned Item: " + item.name + " to store"
                messages.success(request, tmp)
                del tmp
                return redirect(resolve_url("batch-url", item.batch.id))

        # Item parent is not in store      
        # Returns item to store when select == "all"
        def select_is_all():
            # Remove batch_item relationship
            tmp = item.batch
            item_batch_id = tmp.id
            item.batch = None
            # Save as store item
            item.save()
            # Update cost of batch associated with item
            tmp.update_cost()
            tmp = f'Item:{item.name} has been returned to store.'
            messages.success(request, tmp)
            del tmp
            return item_batch_id

        if select == "all":
            batch_id = select_is_all()
            return redirect(resolve_url('batch-url', batch_id))

        if select == "some":
            # Create a new item in store
            nw_item = Item(name=item.name, description=item.description, measure=item.measure, packaging=item.packaging)
            
            # Check that quatity selected is not more than item.qty
            qty = check_quantity()

            # Price reconciliation
            tmp = round((item.price / item.qty)) * qty
            item.price -= tmp
            nw_item.price = tmp
            del tmp

            # Quantity reconciliation
            item.qty -= qty
            nw_item.qty = qty

            # Other reconciliations
            nw_item.created_from = item
            item.batch.update_cost()
            item.save()
            nw_item.save()

            tmp = "Successfully returned Item: " + item.name + " to store"
            messages.success(request, tmp)
            del tmp
            return redirect(resolve_url('batch-url', item.batch.id))