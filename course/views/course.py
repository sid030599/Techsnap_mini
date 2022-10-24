from django.shortcuts import render, redirect
from pygments import highlight
from course.models import *
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.contrib import messages
from course.forms import *

def home(request):
    return render(request, 'index/index.html', {})

def lms(request):
    if request.user.is_authenticated:
        if request.user.profile.is_creator:
            return redirect('admin-panel', request.user.profile.slug)
        elif request.user.profile.is_student:
            announcements = GeneralAnouncement.objects.all()[:5]
            courses = Course.objects.all()
            count = len(courses)
            courses = courses[:6]
            return render(request, 'student/index.html', {'courses': courses, 'announcements': announcements, 'total_courses': count})
    return render(request, 'index/index.html')

def handleteachersignup(request):
    if request.method == 'POST':
        # Get the Post parametres
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['pass2']

        if request.user.profile.status != 'p':
            messages.error(request, "You don't have permission to add a teacher.")
            return redirect('home')

        # check for errorneous input
        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters")
            return redirect('home')

        if " " in username:
            messages.error(request, "Username cannot contain spaces")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Uername already exists. Choose unique username")
            return redirect('home')
        if User.objects.filter(email=email).exists():
            messages.error(request, "email already exists. Please Log in")
            return redirect('home')

        # Create the user
        form1 = userform(request.POST)

        if form1.is_valid():
            form1.save()

            teacher = User.objects.get(username=username)
            teacher.profile.status = 't'
            teacher.profile.college = request.user.profile.college

            teacher.save()

            messages.success(request, "Your have successfully added the teacher " + username)
            return redirect('home')

        else:
            form1 = userform()


    return render(request, "index/signup.html")

def handlesignup(request):
    if request.method == 'POST':
        # Get the Post parametres
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters")
            return redirect('home')

        if " " in username:
            messages.error(request, "Username cannot contain spaces")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Uername already exists. Choose unique username")
            return redirect('home')
        if User.objects.filter(email=email).exists():
            messages.error(request, "email already exists. Please Log in")
            return redirect('home')

        # Create the user
        form1 = userform(request.POST)

        if form1.is_valid():
            form1.save()

            user = User.objects.get(username=username)
            profile = Profile.objects.create(user=user, status="s")
            print(profile)
            user = authenticate(username=username, password=pass1)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in")
                return redirect('home')

            messages.success(request, "Your account has created.")
            return redirect('home')

        else:
            form1 = userform()


    return render(request, "index/signup.html")


def handlelogin(request):
    if request.method == 'POST':
        # Get the Post parametres
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpassword)
        user_verify = User.objects.get(username=loginusername)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('home')
        elif not user_verify.is_active:
            print("fd")
            messages.error(request, "Please verify your email first to login.")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials: Please try again")
            return redirect('home')
    return render(request, "index/login.html")


def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

def logout(request):
    auth.logout(request)
    return redirect('home')

def course_list(request):
    cr_list = Course.objects.all()
    return render(request, 'courses/index.html', {'courses': cr_list})

def course_description(request, slug):
    user = Profile.objects.get(user=request.user)
    enrolled = False
    course = Course.objects.get(slug__iexact=slug)
    job_oppurtunities = JobOpportunities.objects.filter(course = course)
    description = Description.objects.filter(course=course).first()
    what_u_get = WhatYouGet.objects.filter(description=description)
    testimonials = Testimonial.objects.filter(course=course)
    highlight = Highligth.objects.filter(course = course)
    who_should_enroll = WhoShouldEnroll.objects.filter(course=course)
    faqs = FrequentlyAskedQuestion.objects.filter(course=course)
    if len(UserCourseMap.objects.filter(course=course, user=user))>0:
        enrolled = True
        
    units = Unit.objects.filter(course=course)
    contents = []
    for unit in units:
        lessons = Lesson.objects.filter(
            unit=unit
        )
        content = {
            'unit': unit, 
            'lessons': lessons, 
            'length': len(lessons),
        }
        contents.append(content)
    print(job_oppurtunities)
    data = {
        'highlights':highlight,
        'course': course,
        'enrolled': enrolled,
        'job_oppurtunities':job_oppurtunities,
        'description': description,
        'whatuget_points': what_u_get,
        'contents': contents,
        'testimonials': testimonials,
        'who_should_enroll':who_should_enroll,
        'faqs': faqs
    }

    return render(request, 'courses/open.html', data)

def get_total_lessons(course=None, unit=None):
    if unit:
        return len(Lesson.objects.filter(unit=unit))
    num = 0
    for unit in Unit.objects.filter(course=course):
        num += len(Lesson.objects.filter(unit=unit))
    return num

def enroll_in_course(request, slug):
    profile = Profile.objects.get(user=request.user)
    user = profile
    course = Course.objects.get(slug__iexact=slug)
    # Enrollement
    if len(UserCourseMap.objects.filter(user=user, course=course))==0:
        user_course_map = UserCourseMap.objects.create(user=user, course=course)
    #lesson_slug = "no-slug"
    update_userlesson_completion(course, user)
    
    lesson = Lesson.objects.filter(unit__course=course).first()

    if not Rating.objects.filter(course=course):
        Rating.objects.create(course=course)
    if lesson:
        complesson = UserLessonCompletion.objects.get(lesson=lesson, user=user)
        complesson.unlocked = True
        complesson.save(update_fields=['unlocked'])
        lesson_slug = lesson.slug

    # Creating log
    log = f" LOGGED IN to Course [{course.course_title}]"
    EnrollmentHistory.objects.create(user=user, log=log, course=course)

    return render(request, "payment/payment-success.html", {"course":course})

def update_userlesson_completion(course, user):
    id_list = []
    user_course_map = UserCourseMap.objects.get(user=user, course=course)
    for user_lesson in UserLessonCompletion.objects.filter(user=user, lesson__unit__course=course):
        id_list.append(user_lesson.lesson.id)
    for lesson in Lesson.objects.filter(unit__course=course).exclude(id__in=id_list):
        time_left_min = lesson.duration_Minutes
        time_left_sec = lesson.duration_Seconds
        unlocked = False
        if time_left_min<=0 and time_left_sec<=0:
            unlocked=True
        UserLessonCompletion.objects.create(user=user, lesson=lesson,
                                            timer_min_left=time_left_min,
                                            timer_sec_left=time_left_sec, unlocked=unlocked)
    user_course_map.total_lessons = len(UserLessonCompletion.objects.filter(user=user, lesson__unit__course=course))
    user_course_map.total_lessons_completed = len(UserLessonCompletion.objects.filter(user=user, lesson__unit__course=course, completed=True))
    if user_course_map.total_lessons>0:
        user_course_map.percentage_completion = user_course_map.total_lessons_completed / user_course_map.total_lessons * 100
    else :
        user_course_map.percentage_completion = 0
    user_course_map.save(update_fields=['total_lessons', 'total_lessons_completed', 'percentage_completion'])

def lesson_view(request, slug, course_slug):
    profile = Profile.objects.get(user=request.user)
    user = profile
    course = Course.objects.get(slug__iexact=course_slug)
    # Updating user_lesson for any new lesson
    update_userlesson_completion(course, user)
    current_lesson = None
    if slug!='no-slug':
        current_lesson = UserLessonCompletion.objects.get(lesson__slug__iexact=slug, user=user)
    # Fetching data for course page
    user_course_map = UserCourseMap.objects.filter(course=course, user=user).first()
    units = Unit.objects.filter(course=course)
    contents = []
    for unit in units:
        lessons = UserLessonCompletion.objects.filter(user=user, lesson__unit=unit)
        comp = str(len(lessons.filter(completed=True)))+" / "+str(get_total_lessons(unit=unit))
        content = {
            'unit': unit, 
            'lessons': lessons, 
            'completed': comp
        }
        contents.append(content)
    # Announcements
    news = []
    anouncements = Anouncement.objects.filter(course=course)
    for anouncement in anouncements:
        comments = Comment.objects.filter(anouncement=anouncement)
        new = {
            'anouncement': anouncement,
            'comments': comments
        }
        news.append(new)
    # Ratings
    ratings = Rating.objects.filter(course=course)
    rating = ratings.first()
    all_five = []
    for i in ratings.values_list('five', 'four', 'three', 'two', 'one'):
        num = 5
        for any_o in i:
            per = 0
            if rating.get_total()!=0:
                per = any_o/rating.get_total()*100
            any_one = {'per': per, 'votes': any_o, 'for': num}
            all_five.append(any_one)
            num = num - 1
    ratings = {
        'all': all_five,
        'avg': rating.get_average(),
        'avg_per': rating.get_average()*20,
        'total': rating.get_total()
    }
    # Grades 
    grades = []
    for unit in units:
        lessons = Lesson.objects.filter(unit=unit)
        txp = 0
        for lesson in lessons:
            txp = txp + lesson.xp
        grade = {
            'name': unit.title,
            'videos': 0,
            'readings': len(lessons),
            'txp': txp,
            'due': unit.due
        }
        grades.append(grade)
    # Previous and next lesson
    pre_lesson = None
    next_lesson = None
    next_locked = None
    if current_lesson:
        nxt_locked = UserLessonCompletion.objects.filter(lesson__order__gt=current_lesson.lesson.order, unlocked=False)
        back = UserLessonCompletion.objects.filter(lesson__order=current_lesson.lesson.order-1)
        nxt = UserLessonCompletion.objects.filter(lesson__order=current_lesson.lesson.order+1)
        if nxt_locked.exists():
            next_locked = nxt_locked.first()
        if len(back)>0:
            pre_lesson = back.first()
        if len(nxt)>0:
            next_lesson = nxt.first()

    payload = {
        'current_lesson': current_lesson,
        'user_course_map': user_course_map,
        'contents': contents,
        'news': news,
        'ratings': ratings,
        'reviews': Review.objects.filter(course=course),
        'grades': grades,
        'back': pre_lesson,
        'next': next_lesson,
        'next_locked': next_locked,
        'user': user
    }
    return render(request, 'course/course-details.html', payload)

def lesson_completed_or_redo(request, slug):
    profile = Profile.objects.get(user=request.user)
    user = profile
    redo = request.GET.get('redo')
    lesson = Lesson.objects.get(slug__iexact=slug)
    userLesson = UserLessonCompletion.objects.filter(user=user, lesson=lesson).first()
    update_userlesson_completion(lesson.unit.course, user)
    if redo=="false":
        # Creating Log
        log = f" CHECKED lesson [{lesson.title}] as COMPLETED"
        EnrollmentHistory.objects.create(user=user, log=log, course=lesson.unit.course)
        # Updating lesson completed
        userLesson.completed = True
        # Updating UserCourseMap
        user_course_map = UserCourseMap.objects.get(user=user, course=userLesson.lesson.unit.course)
        user_course_map.percentage_completion = (user_course_map.total_lessons_completed+1)/user_course_map.total_lessons*100
        print(user_course_map.percentage_completion)
        user_course_map.total_xp += userLesson.lesson.xp
    else:
        # Creating Log
        log = f" UNCHECKED lesson [{lesson.title}] as NOT-COMPLETED"
        EnrollmentHistory.objects.create(user=user, log=log, course=lesson.unit.course)
        # Updating lesson completed
        userLesson.completed = False
        # Updating UserCourseMap
        user_course_map = UserCourseMap.objects.get(user=user, course=userLesson.lesson.unit.course)
        user_course_map.percentage_completion = (user_course_map.total_lessons_completed-1)/user_course_map.total_lessons*100
        print(user_course_map.percentage_completion)
        user_course_map.total_xp -= userLesson.lesson.xp

    userLesson.save(update_fields=['completed'])
    user_course_map.save(update_fields=['percentage_completion', 'total_xp'])
    data = {
        'percentage': user_course_map.percentage_completion,
    }

    return JsonResponse({'data': data})

class CoursePaymentView(View):
    def get(self, request, slug):
        profile = Profile.objects.get(user=request.user)
        user = profile
        course = Course.objects.filter(slug__iexact=slug).first()
        lessons = Lesson.objects.filter(unit__course=course)
        price = course.course_price

        data = {
            'slug': course.slug,
            'title': course.course_title,
            'img': course.course_img,
            'lessons': len(lessons),
            'price': course.course_price,
        }

        return render(request, 'courses/payment.html', data)
    
    def post(self, request, slug):
        profile = Profile.objects.get(user=request.user)
        user = profile
        course = Course.objects.filter(slug__iexact=slug).first()
        price = course.course_price
        if price != 'FREE':
            price = int(price)
            user.techsnap_cash = user.techsnap_cash - price
            user.save(update_fields=['techsnap_cash'])   
        return redirect('course-enrollment', slug=slug)
        
def log_out_course(request, slug):
    user = Profile.objects.get(user=request.user)
    course = Course.objects.get(slug=slug)

    # Creating log
    log = f" LOGGED OUT of Course [{course.course_title}]"
    EnrollmentHistory.objects.create(user=user, log=log, course=course)

    return redirect('course-description', slug=slug)

def get_history(request, slug, username):
    course = Course.objects.get(slug=slug)
    user = Profile.objects.get(user__username=username)

    logs = EnrollmentHistory.objects.filter(course=course, user=user)
    return render(request, 'course/logs.html', {'logs': logs, 'course': course, 'user': user})

def lesson_timer_update(request, pk):
    lesson = UserLessonCompletion.objects.filter(id=pk).first()
    minutes = request.GET.get('min')
    seconds = request.GET.get('sec')

    if int(lesson.timer_sec_left)>0 or int(lesson.timer_min_left)>0:
        if int(minutes)<=0 and int(seconds)<=0:
            next_lesson_user = UserLessonCompletion.objects.filter(
                lesson__order__gt=lesson.lesson.order, 
                unlocked=False, 
                user=request.user.profile, 
                lesson__unit__course=lesson.lesson.unit.course
                )
            if next_lesson_user.exists():
                next_lesson_user = next_lesson_user.first()
                next_lesson_user.unlocked = True
                next_lesson_user.save(update_fields=['unlocked'])
                
    lesson.timer_min_left = minutes
    lesson.timer_sec_left = seconds
    lesson.save(update_fields=['timer_min_left', 'timer_sec_left'])

    return JsonResponse({})


from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from course import PaytmChecksum
from accounts.models import PaytmHistory
import json
import requests


def payment(request, slug):
    bill_amount = 0
    if slug!="paytm_log":
        course = Course.objects.get(slug=slug)
        bill_amount = course.course_price
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    ENV = "https://securegw-stage.paytm.in"
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    get_lang = "/" + get_language() if get_language() else ''
    CALLBACK_URL = "http://127.0.0.1:8000/response/"+slug
    # Generating unique temporary ids
    
    if bill_amount != "FREE":
        order_id = "order_"+str(datetime.datetime.now().timestamp())
        paytmParams = dict()
        paytmParams["body"] = {
            "requestType"   : "Payment",
            "mid"           : MERCHANT_ID,
            "websiteName"   : "WEBSTAGING",
            "orderId"       : order_id,
            "callbackUrl"   : CALLBACK_URL,
            "txnAmount"     : {
                "value"     : str(float(bill_amount)),
                "currency"  : "INR",
            },
            "userInfo"      : {
                "custId"    : "CUST_001",
            },
        }
        # Generate checksum by parameters we have in body
        # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
        checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), MERCHANT_KEY)
        paytmParams["head"] = {
            "signature"    : checksum
        }
        post_data = json.dumps(paytmParams)
        # for Staging
        url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid="+MERCHANT_ID+"&orderId="+order_id
        # for Production
        # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
        response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
        response_str = json.dumps(response)
        res = json.loads(response_str)
        if res["body"]["resultInfo"]["resultStatus"]=='S':
            token=res["body"]["txnToken"]
        else:
            token=""
        
        profile = Profile.objects.get(user=request.user)
        user = profile
        course = Course.objects.filter(slug__iexact=slug).first()
        lessons = Lesson.objects.filter(unit__course=course)
        price = bill_amount

        data = {
            'slug': course.slug,
            'title': course.course_title,
            'img': course.course_img,
            'lessons': len(lessons),
            'price': course.course_price,
            "txnToken": token,
            "orderId": order_id,
            "amount": 1,
            "env": ENV,
            "mid": MERCHANT_ID
        }

        return render(request, "payment/payment.html", data)
    return redirect('course-enrollment', slug=slug)


@csrf_exempt
def response(request, slug):
    if request.method == "POST":
        data = {k:v[0] for k,v in dict(request.POST).items()}
        print(data)
        if data:
            checksum = data['CHECKSUMHASH']
            data.pop('CHECKSUMHASH', None)

            #verify checksum    
            verifySignature = PaytmChecksum.verifySignature(data, settings.PAYTM_MERCHANT_KEY, checksum)
            text_error = ''
            text_success = ''

            if verifySignature:
                text_success = "Checksum is verified.Transaction details are below"
                PaytmHistory.objects.create(user=request.user)
                return redirect('course-enrollment', slug=slug)
            else:
                text_error = "Checksum is not verified."
                return HttpResponse("checksum verify failed")
        else :
            text_error = "Empty POST Response."
    return HttpResponse(status=200)