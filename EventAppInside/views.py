from django.shortcuts import render, redirect
from django.contrib import messages


def home(requests):
    return render(requests, 'home.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Registration

def signup(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")

        if Registration.objects.filter(user_name=user_id).exists():
            messages.error(request, "Username already exists. Please choose another.")
        else:
            Registration.objects.create(user_name=user_id, password=password)
            messages.success(request, "Account created successfully!")
            return redirect("signup")  # Same page again

    return render(request, "signup.html")



from django.shortcuts import render, redirect
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Registration

def login(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")

        # Check if credentials match a user
        try:
            user = Registration.objects.get(user_name=user_id, password=password)
            request.session["user_name"] = user.user_name
            user_name = request.session.get("user_name", "Guest")
            messages.success(request, f"Welcome, {user.user_name}!")
            return render(request, "front.html", {"user": user_name}) # change to your front page view name
        except Registration.DoesNotExist:
            messages.error(request, "Invalid User ID or Password. Please try again.")
    
    return render(request, "login.html")


def front_page(request):
    print("Session key:", request.session.session_key)
    print("User from session:", request.session.get("user_  id"))
    user = request.session.get("user_id", "Guest")
    print(user)
    return render(request, "front.html", {"user": user})

def location(request):
    # Do something educational
    return render(request, "location.html")

def set_event_type(request):
    if request.method == "POST":
        event_type = request.POST.get("event_type")
        request.session["typeEvent"] = event_type
        return redirect("location")  # or your desired destination
    return redirect("front")

def timeLineEvents(request):
    selected_location = request.POST.get("location")
    event_type = request.session.get("typeEvent")
    request.session["location"] = selected_location
    # You can now use both to filter what gets shown
    return render(request, "timeline.html", {"location": selected_location, "event_type": event_type})


from datetime import date

def upload_post(request):
    today = date.today().isoformat()  # gives 'YYYY-MM-DD'
    return render(request, "upload_post.html", {"today": today})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Photo_store
from datetime import datetime

def save_post(request):
    if request.method == "POST":
        photo_name = request.POST.get("photo_name")
        description = request.POST.get("description")
        location = request.POST.get("location")
        event_type = request.POST.get("event_type")
        date = request.POST.get("timestamp")
        photo_file = request.FILES.get("photo")

        # Check for duplicate photo_name
        if Photo_store.objects.filter(photo_name=photo_name).exists():
            messages.error(request, "Photo name already exists. Please use a unique name.")
            return redirect("upload_post")

        # Convert image to binary
        if photo_file:
            image_binary = photo_file.read()
        else:
            messages.error(request, "Image upload failed.")
            return redirect("upload_post")

        # Save to Photo_store
        Photo_store.objects.create(
            photo= image_binary,
            photo_name=photo_name,
            description=description,
            location=location,
            event_type=int(event_type),
            date=date  # already in YYYY-MM-DD from input[type="date"]
        )

        messages.success(request, "Post uploaded successfully!")
        return redirect("upload_post")

    print("not uploaded")
    return redirect("upload_post")



def admin_dashboard(request):
    # Do something educational
    return render(request, "admin_dashboard.html")

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdminUser

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            admin = AdminUser.objects.get(admin_name=username, password=password)
            request.session["admin_name"] = admin.admin_name
            messages.success(request, f"Welcome, {admin.admin_name}!")
            return redirect("admin_dashboard")
        except AdminUser.DoesNotExist:
            messages.error(request, "Invalid admin credentials. Please try again.")

    return render(request, "admin_login.html")

from django.shortcuts import render
from .models import Photo_store
from datetime import date
import base64

def posts(request):
    if request.method == "POST":
        event_type = request.session.get("typeEvent")
        location = request.session.get("location")
        timeline = request.POST.get("status")
        today = date.today()

        queryset = Photo_store.objects.filter(event_type=event_type, location=location)

        if timeline == "upcoming":
            queryset = queryset.filter(date__gt=today)
        elif timeline == "ongoing":
            queryset = queryset.filter(date=today)
        elif timeline == "closed":
            queryset = queryset.filter(date__lt=today)

        # Convert binary to base64 for HTML rendering
        photos = []
        for item in queryset:
            encoded_photo = base64.b64encode(item.photo).decode('utf-8')
            photos.append({
                "photo_name": item.photo_name,
                "image_base64": encoded_photo
            })

        return render(request, "posts.html", {"photos": photos})

    return render(request, "posts.html", {"photos": []})

def select_photo(request):
    if request.method == "POST":
        photo_name = request.POST.get("photo_name")
        request.session["selected_photo"] = photo_name
        return redirect("post_detail")
    
from .models import Photo_store, Like, Comment
from django.utils import timezone
import base64

def post_detail(request):
    photo_name = request.session.get("selected_photo")
    user = request.session.get("user_name")

    try:
        photo_obj = Photo_store.objects.get(photo_name=photo_name)
    except Photo_store.DoesNotExist:
        return redirect("filtered_photos")

    # Decode image
    image_data = base64.b64encode(photo_obj.photo).decode('utf-8')

    # Handle comment submission
    if request.method == "POST":
        if "comment" in request.POST:
            content = request.POST.get("comment")
            Comment.objects.create(photo=photo_obj, username=user, content=content)

        elif "toggle_like" in request.POST:
            existing = Like.objects.filter(photo=photo_obj, username=user).first()
            if existing:
                existing.liked = not existing.liked
                existing.save()
            else:
                Like.objects.create(photo=photo_obj, username=user, liked=True)

        return redirect("post_detail")

    comments = Comment.objects.filter(photo=photo_obj).order_by("-timestamp")
    like_status = Like.objects.filter(photo=photo_obj, username=user, liked=True).exists()
    like_count = Like.objects.filter(photo=photo_obj, liked=True).count()

    context = {
        "photo_name": photo_obj.photo_name,
        "description": photo_obj.description,
        "image_data": image_data,
        "comments": comments,
        "like_status": like_status,
        "like_count": like_count,
        "user": user
    }
    return render(request, "post_detail.html", context)


