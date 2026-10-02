from django.shortcuts import render, redirect
from .models import FoodPost, Request, Pickup
from .forms import FoodPostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required 
from .models import Request
from .models import Pickup
from .decorators import donor_required, volunteer_required
from .models import UserProfile
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect


# ✅ HOME VIEW
def home(request):
    foods = FoodPost.objects.all()
    return render(request, 'core/home.html', {'foods': foods})


# ✅ ADD FOOD (PROTECTED)
@login_required
@donor_required
def add_food(request):
    if request.method == 'POST':
        form = FoodPostForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)

            # 🔥 REAL USER (IMPORTANT CHANGE)
            food.donor = request.user

            food.save()
            return redirect('home')
    else:
        form = FoodPostForm()

    return render(request, 'core/add_food.html', {'form': form})


# ✅ REGISTER VIEW
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        role = request.POST.get('role')

        if form.is_valid():
            user = form.save()

            UserProfile.objects.create(
                user=user,
                role=role
            )

            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(
        request,
        'core/register.html',
        {'form': form}
    )

@login_required
@volunteer_required
def request_food(request, food_id):
    food = FoodPost.objects.get(id=food_id)

    # prevent duplicate request
    if not Request.objects.filter(food_post=food, volunteer=request.user).exists():
        Request.objects.create(
            food_post=food,
            volunteer=request.user
        )

        # update food status
        food.status = "Requested"
        food.save()

    return redirect('home')

@login_required
@volunteer_required
def my_requests(request):
    requests = Request.objects.filter(volunteer=request.user)
    return render(request, 'core/my_requests.html', {'requests': requests})

@login_required
@donor_required
def manage_requests(request):
    # get requests for foods posted by this user
    requests = Request.objects.filter(food_post__donor=request.user)
    return render(request, 'core/manage_requests.html', {'requests': requests})

@login_required
@donor_required
def accept_request(request, request_id):
    req = Request.objects.get(id=request_id)

    req.status = "Accepted"
    req.save()

    # update food status
    food = req.food_post
    food.status = "Accepted"
    food.save()

    # create pickup
    Pickup.objects.create(
        request=req,
        pickup_time=timezone.now(),
        delivery_status="Pending"
    )

    return redirect('manage_requests')


@login_required
@donor_required
def reject_request(request, request_id):
    req = Request.objects.get(id=request_id)

    if req.food_post.donor == request.user:
        req.status = 'Rejected'
        req.save()

    return redirect('manage_requests')

@login_required
@volunteer_required
def my_pickups(request):
    pickups = Pickup.objects.filter(
        request__volunteer=request.user
    )

    return render(
        request,
        'core/my_pickups.html',
        {'pickups': pickups}
    )


@login_required
@volunteer_required
def update_pickup_status(request, pickup_id, status):
    pickup = Pickup.objects.get(id=pickup_id)

    if pickup.request.volunteer == request.user:
        pickup.delivery_status = status
        pickup.save()

    return redirect('my_pickups')


@login_required
@volunteer_required
def delivered_pickup(request, pickup_id):
    pickup = Pickup.objects.get(id=pickup_id)

    if pickup.request.volunteer == request.user:
        pickup.delivery_status = "Delivered"
        pickup.save()

    return redirect('my_pickups')
