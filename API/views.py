from django.http import JsonResponse
from django.core import serializers
from .models import *
import hashlib as hash
import requests
import json
from datetime import datetime 

ZOMATO_API_KEY = open('key').read()
LOCATION = {}

def user_signup(request):
    if request.method != 'POST':
        return JsonResponse({
            "success" :	False,
            "data"	:	None,
            "msg"	:	"Invalid request!!"
            })
    else:
        try :
            user_obj=User()
            user_obj.username=request.POST.get("username", False) 
            user_obj.password=hash.sha256(request.POST.get('password', False).encode()).hexdigest()
            user_obj.save()
            return JsonResponse({
                "success" : True,
                "data" : None,
                "msg" : "successfully signed up!!"
            })
        except :
            return JsonResponse({
                "success" : False,
                "data" : None,
                "msg" : "internal server error"
            })
    
def user_login(request):
    if request.method != 'POST':
        return JsonResponse({
            'success'	:	False,
            'data'	: None,
            'msg'	: "invalid request"
            })
    else:
        user_check = request.POST.get('username', False)
        found_user = User.objects.filter(username = user_check)
        if len(found_user) == 0:
            return JsonResponse({
                "success" : False,
                "data" : None,
                "msg" : "User not found"
            })
        else :
            found_user = found_user.get(username = user_check)
            pass_check = hash.sha256(request.POST.get('password', False).encode()).hexdigest()
            print(pass_check)
            if pass_check == found_user.password:
                # login 
                request.session["username"] = found_user.username
                
                return JsonResponse({
                    "success" : True,
                    "data" : None,
                    "msg" : "successfully logged in"	
                })
            else:
                return JsonResponse({
                    "success" : False,
                    "data" : None,
                    "msg" : "Wrong password" 
                })

def user_logout(request):
    if request.method != 'POST':
        return JsonResponse({
            "success"	:False,
            "data"	:	False,
            "msg"	:	"invalid request"
    
            })
    try:

        if None == request.session.get('username', False):
            return JsonResponse({
                "success"	:	False,
                "data"	:	False,
                "msg"	:	"something went wrong...try again"
            })
        else:
            del request.session["username"]
            return JsonResponse({
                "success"	:	True,
                "data"	:	False,
                "msg"	:	"successfully logged out!!"
            })
    except KeyError:
        return JsonResponse({
                "success"	:	False,
                "data"	:	False,
                "msg"	:	"No one logged in"
            })





def post_create(request):
    if request.method == 'POST':
        if request.session.get('username', False) == None:
            return JsonResponse({
                "success" :	False,
                "data" 	:	None,
                "msg"	:	"Not logged in"
                })

        try : 
            post_obj=Post()
            post_obj.username = request.POST.get('username', False)
            post_obj.title = request.POST.get('title', False)
            post_obj.content = request.POST.get('content', False)
            post_obj.save()

            return JsonResponse({
                "success" :	True,
                "data" 	:	serializers.serialize('json', [post_obj]),
                "msg"	:	"successfully created post!!"
            })
        except : 
            return JsonResponse({
                "success" :	False,
                "data" 	:	None,
                "msg"	:	"internal server error"
            })		
    else:
        return JsonResponse({
                "success" :	False,
                "data" 	:	None,
                "msg"	:	"Invalid request"
            })		

def post_list_all(request):
    if request.method != 'GET':
        return JsonResponse({
            "success" :	False,
            "data" 	:	None,
            "msg"	:	"invalid request"
        })

    return JsonResponse({
        "success" :	True,
        "data" 	:	serializers.serialize('json', list(Post.objects.all())),
        "msg"	:	"all the blogs"
    })

# task 1
def location(q):
    url = "https://developers.zomato.com/api/v2.1/cities"
    params = {"q": q}
    res = requests.get(url, params=params, headers={"user-key": ZOMATO_API_KEY})
    r = res.json()
    id_ = r["location_suggestions"][0]["id"]
    name = r["location_suggestions"][0]["name"]
    LOCATION[id_] = name
    return (id_, name)

# task 3,4
def fetch_restaurents(request, search, location_name, page_number, count):
    location_id = location(location_name)[0]
    url = "https://developers.zomato.com/api/v2.1/search"
    params = {"entity_id": location_id, "start": page_number, "count": count, "q": search}
    res = requests.get(url, params=params, headers={"user-key": ZOMATO_API_KEY})
    return JsonResponse(res.json())

def favourite_get(request):
    if not request.session.get("username"):
        return JsonResponse({"error": "No user Logged in"})
    else:
        result = Favourite.objects.filter(user__username=request.session.get("username"))
        res = []
        for i in result:
            obj = {"username": i.user.username, "res_id": i.restaurent.res_id}
            res.append(obj)
        return JsonResponse(res, safe=False)

def favourite(request, res_id):
    if not request.session.get("username"):
        return JsonResponse({"error": "No user Logged in"})
    else:
        F = Favourite()
        user = User.objects.get(username=request.session.get("username"))
        F.user = user
        restaurent_obj = None
        try:
            restaurent_obj = Restaurent.objects.get(res_id=res_id)
        except:
            restaurent_obj = Restaurent()
            restaurent_obj.res_id = res_id
            restaurent_obj.details = json.dumps(restaurent(res_id))
            restaurent_obj.save()
        F.restaurent = restaurent_obj
        F.save()
        return JsonResponse({"message": "restaurent was saved to favourites."})

def restaurent(res_id):
    url = "https://developers.zomato.com/api/v2.1/restaurant"
    params = {"res_id": res_id}
    res = requests.get(url, params=params, headers={"user-key": ZOMATO_API_KEY})
    r = res.json()
    return r


def schedule(request, res_id, schedule_time, guests):
    if guests > 6:
        return JsonResponse({"error": "Number of guests should be less than 6."})
    restaurent_obj = None
    try:
        restaurent_obj = Restaurent.objects.get(res_id=res_id)
    except:
        restaurent_obj = Restaurent()
        restaurent_obj.res_id = res_id
        restaurent_obj.details = json.dumps(restaurent(res_id))
        restaurent_obj.save()
    time = datetime.fromtimestamp(schedule_time)
    endtime = datetime.fromtimestamp(schedule_time + (60 * 60))
    booking = Booking()
    booking.restaurent = restaurent_obj
    booking.time = time
    booking.guests = guests
    bookings = Booking.objects.filter(restaurent__res_id=res_id).filter(time__gte = time).filter(time__lte = endtime)
    result = 0
    for i in bookings:
        result += i.guests
    if result > 20:
        return JsonResponse({"error": "No more bookings are possible in this restaurent"})
    booking.save()
    return JsonResponse({"message": "Restaurent_booked"})
    
