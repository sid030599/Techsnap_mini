from decimal import Context
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User, auth
from django.views.generic import UpdateView, DetailView
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from course.models import *
# Create your views here.

from .models import *
from .forms import ProfileForm

# Create your views here.
def update_profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    if request.method == "POST":
        bio = request.POST.get('bio')
        profile_pic = request.FILES.get('profile_pic')
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        linkedin = request.POST.get('linkedin')
        github = request.POST.get('github')
        email = request.POST.get('email')
        ph_num = request.POST.get('ph_no')
        default_coding_lang = request.POST.get('d_c_l')
        resume = request.FILES.get('resume')
        institute_name = request.POST.get('institute_name')
        institute_location = request.POST.get('location')
        out_of = request.POST.get('out_of')
        yearOfPassing = request.POST.get('yearOfPassing')
        btech_percentage = request.POST.get('current_cgpa')
        current_ctc = request.POST.get('current_ctc')
        notice_period = request.POST.get('period')
        willing_to_relocate = request.POST.get('willing')
        if willing_to_relocate=='True':
            profile.willing_to_relocate = True
        elif willing_to_relocate=='False':
            profile.willing_to_relocate = False
        expected_ctc = request.POST.get('expected_ctc')
        current_com = request.POST.get('current_com')
        dream_com = request.POST.get('dream_com')
        designation = request.POST.get('desg')
        workexp = request.POST.get('workexp')


        profile.notice_period = notice_period
        profile.willing_to_relocate = willing_to_relocate
        profile.current_CTC = current_ctc
        profile.expected_CTC = expected_ctc
        profile.current_company = current_com
        profile.dream_company = dream_com
        profile.designation = designation
        profile.workExp = workexp
        profile.institute_name = institute_name
        profile.yearOfPassing = yearOfPassing
        profile.institute_location = institute_location
        profile.out_of = out_of
        profile.current_cgpa = btech_percentage
        profile.bio = bio
        profile.full_name = full_name
        profile.gender = gender
        profile.country = country
        profile.state = state
        profile.city = city
        profile.linkedin = linkedin
        profile.github = github
        profile.email = email
        profile.ph_num = ph_num
        profile.default_coding_lang = default_coding_lang
        if profile.profile_pic and profile_pic:
            profile.profile_pic = profile_pic
        elif profile.profile_pic is not None and profile_pic:
            profile.profile_pic = profile_pic
        if profile.resume and resume:
            profile.resume = resume
        elif profile.resume is not None and resume:
            profile.resume = resume
        profile.save()
        return HttpResponseRedirect(reverse('show_profile', kwargs={'slug':slug}))
    else:
        if request.user == profile.user:
            skills = profile.skills.split(',') if profile.skills else None
            languages = profile.languages.split(',') if profile.languages else None
            print(skills)
            return render(request, 'editprofile.html', {
                'profile': profile,
                'skills': skills,
                'langs': languages,
                })
        else:
            return HttpResponse('siggu undali....')

def update_education(request, slug):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        institute_name = request.POST.get('institute_name')
        institute_location = request.POST.get('location')
        out_of = request.POST.get('out_of')
        yearOfPassing = request.POST.get('yearOfPassing')
        btech_percentage = request.POST.get('current_cgpa')

        if slug=='create':
            Education.objects.create(
                profile=profile,
                institute_name=institute_name,
                institute_location=institute_location,
                out_of=out_of,
                yearOfPassing=yearOfPassing,
                current_cgpa=btech_percentage
            )
            return HttpResponseRedirect(reverse('show_profile', kwargs={'slug':profile.slug}))

        education = Education.objects.get(slug=slug)

        education.institute_name = institute_name
        education.yearOfPassing = yearOfPassing
        education.institute_location = institute_location
        education.out_of = out_of
        education.current_cgpa = btech_percentage
        education.save()
        return HttpResponseRedirect(reverse('show_profile', kwargs={'slug':profile.slug}))
    else:
        if request.user == profile.user:
            if slug=='create':
                return render(request, 'editeducation.html', {
                    'edu': None,
                    'slug': 'create'
                })
            education = Education.objects.get(slug=slug)
            return render(request, 'editeducation.html', {
                'edu': education,
                'slug': slug
                })
        else:
            return HttpResponse('siggu undali....')


def update_proffesion(request, slug):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        current_ctc = request.POST.get('current_ctc')
        notice_period = request.POST.get('period')
        willing_to_relocate = request.POST.get('willing')
        if willing_to_relocate=='True':
            profile.willing_to_relocate = True
        elif willing_to_relocate=='False':
            profile.willing_to_relocate = False
        expected_ctc = request.POST.get('expected_ctc')
        current_com = request.POST.get('current_com')
        dream_com = request.POST.get('dream_com')
        designation = request.POST.get('desg')
        workexp = request.POST.get('workexp')

        if slug=='create':
            Proffesion.objects.create(
                profile=profile,
                current_CTC=current_ctc,
                notice_period=notice_period,
                willing_to_relocate=willing_to_relocate,
                expected_CTC=expected_ctc,
                current_company=current_com,
                dream_company=dream_com,
                designation=designation,
                workExp=workexp
            )
            return HttpResponseRedirect(reverse('show_profile', kwargs={'slug':profile.slug}))

        proffesion = Proffesion.objects.get(slug=slug)

        proffesion.notice_period = notice_period
        proffesion.willing_to_relocate = willing_to_relocate
        proffesion.current_CTC = current_ctc
        proffesion.expected_CTC = expected_ctc
        proffesion.current_company = current_com
        proffesion.dream_company = dream_com
        proffesion.designation = designation
        proffesion.workExp = workexp
            
        proffesion.save()
        return HttpResponseRedirect(reverse('show_profile', kwargs={'slug':profile.slug}))
    else:
        if request.user == profile.user:
            if slug=='create':
                return render(request, 'editproffesion.html', {
                    'pro': None,
                    'slug': 'create'
                })
            proffesion = Proffesion.objects.get(slug=slug)
            return render(request, 'editproffesion.html', {
                'pro': proffesion,
                'slug': slug
                })
        else:
            return HttpResponse('siggu undali....')



class UpdateProfile(UpdateView):
    model = Profile
    template_name = 'editprofile.html'
    form_class = ProfileForm
    success_url = '/'

def update_skill(request, delete):
    profile = Profile.objects.get(user=request.user)
    skill = request.GET.get('tag')
    if delete=='True':
        skills = profile.skills.split(',')
        updated_skills = []
        for i in skills:
            if i != skill:
                updated_skills.append(i)
        profile.skills = ",".join(updated_skills)
        profile.save(update_fields=['skills'])
        return JsonResponse({})
    if profile.skills:
        profile.skills = profile.skills + ',' + skill
    else :
        profile.skills = skill
    profile.save(update_fields=['skills'])
    return JsonResponse({})

def update_language(request, delete):
    profile = Profile.objects.get(user=request.user)
    lang = request.GET.get('tag')
    if delete=='True':
        languages = profile.languages.split(',')
        updated_languages = []
        for i in languages:
            if i != lang:
                updated_languages.append(i)
        profile.languages = ",".join(updated_languages)
        profile.save(update_fields=['languages'])
        return JsonResponse({})
    if profile.languages:
        profile.languages = profile.languages + ',' + lang
    else :
        profile.languages = lang
    profile.save(update_fields=['languages'])
    return JsonResponse({})

class ShowProfile(DetailView):
    model = Profile
    template_name = 'myprofile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfile, self).get_context_data(*args, **kwargs)
        page_profile = get_object_or_404(Profile, slug=self.kwargs['slug'])

        blogs = Blogs.objects.filter(author=page_profile.user)

        posts = Posts.objects.filter(profile=page_profile)
        posts_ = []
        for post in posts:
            img = PostImage.objects.filter(post=post)
            if img.exists():
                img = img.first().img_url
            post_ = {
                'details': post,
                'img': img,
            }
            posts_.append(post_)
        usercoursemaps = UserCourseMap.objects.filter(user=page_profile)

        context['teammates'] = page_profile.teammates.all()

        hrs = Profile.objects.filter(is_hr=True)
        employees = Profile.objects.filter(is_hr=False, is_employee=True)
        context['hrs'] = hrs
        context['employees'] = employees

        educations = Education.objects.filter(profile=page_profile)
        proffesions = Proffesion.objects.filter(profile=page_profile)
        context['educations'] = educations
        context['proffesions'] = proffesions

        context['page_profile'] = page_profile
        context['blogs'] = blogs
        context['usercoursemaps'] = usercoursemaps
        context['posts'] = posts_
        if self.request.user==page_profile.user:
            self.template_name = 'myprofile.html'
        elif self.request.user!=page_profile.user or self.request.user.is_anonymous:
            self.template_name = 'outerprofile.html'
        return context


class ShowDashboard(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'dashboard.html'

    def get_context_data(self, *args, **kwargs):
        profiles = Profile.objects.all()
        context = super(ShowDashboard, self).get_context_data(*args, **kwargs)
        profile_page = get_object_or_404(Profile, slug=self.kwargs['slug'])
        context['profile_page'] = profile_page
        return context


class RegistrationView(View):
    def get(self, request):
        return render(request, "index/signup.html")

    def post(self, request):
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'username': username,
            'email': email
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password is too short')
                    return redirect('handlesignup')

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Successfully logged in")
                    return redirect('home')
                """uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                               'uidb64': uidb64, 'token': token_generator.make_token(user)})
                email_subject="Activate your Account"
                activate_url = 'http://'+domain+link
                email_body = 'Hi, ' + user.username + \
                    ' Please use this link to verify your account\n' + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'from@example.com',
                    [email],
                )
                email.send(fail_silently=False)"""
                messages.success(
                    request, 'Account successfully created!')
                return redirect('home')

            messages.warning(request, "This Email already exists!")
            return redirect('handlesignup')
        else:
            messages.warning(request, "This username already exists!")
            return redirect('handlesignup')


class VerificationView(View):
    def get(self, request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            auth.login(request, user,
                    backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
        else:
            return render(request, 'registration/login.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        if 'login_page' in request.POST:
            next = request.POST.get('next')
            username = request.POST['username']
            password = request.POST['password']
            context = {
                'user_found': True,
                'user_name': username
            }
            if username and password:
                if User.objects.filter(username=username).exists():
                    user = auth.authenticate(
                        username=username, password=password)
                    if user:
                        if user.is_active:
                            auth.login(request, user)
                            LoginHistory.objects.create(user=user)
                            if next:
                                return redirect(next)
                            return redirect("index")

                        messages.error(
                            request, "Account is not active,please check your email"
                        )

                elif User.objects.filter(email=username).exists():
                    user = User.objects.get(email=username)
                    user = auth.authenticate(
                        username=user.username, password=password)
                    if user:
                        if user.is_active:
                            auth.login(request, user)
                            LoginHistory.objects.create(user=user)
                            if next:
                                return redirect(next)
                            return redirect("index")

                        messages.error(
                            request, "Account is not active,please check your email"
                        )
                elif (User.objects.filter(email=username).exists() or User.objects.filter(username=username).exists() == False):
                    messages.error(
                        request, "The username or Email you have entered does not exist.")
                    return render(request, 'registration/login.html', context)

            context = {
                'user_found': True,
                'user_name': username
            }
            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'registration/login.html', context)

        return render(request, "registration/login.html")


def logout(request):
    LoginHistory.objects.create(user=request.user, logged_in=False)
    auth.logout(request)
    return redirect('index')


@login_required
def xp_redeem_cash(request, slug):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        xp = int(request.POST['xp'])
        if profile.xp >= xp:
            if profile.xp >= 1000:
                temp = profile.xp//10
                temp_xp = profile.xp - (temp*10)
                profile.techsnap_cash = profile.techsnap_cash + temp
                profile.xp = temp_xp
                profile.save()
                return HttpResponseRedirect(reverse('dashboard', kwargs={'slug': request.user.profile.slug}))
            else:
                return HttpResponse('Your xp is not enough')
        else:
            return HttpResponse('Enter xp less than or equal to yours')
    else:
        return render(request, 'redeem.html', {'profile': profile})

def account_del(request):
    try:
        user = User.objects.get(username=request.user.username)
        user.delete()
        return render(request, 'account_del.html', {'msg': 'Account deleted Successfully'})
    except User.DoesNotExist:
        return render(request, 'account_del.html', {'msg': 'User doesnot exist'})
    except Exception as e:
        return render(request, 'account_del.html', {'msg': e.message})



def leaderboard(request,slug):
    return render(request, 'leaderboard.html')

def accountsettings(request,slug):
    plan = Profile.objects.get(user=request.user).plan
    upgrade = None
    premium = Plan.objects.filter(title='Premium')
    premium_slug = ''
    if premium.exists():
        premium=premium.first()
        if not plan.slug == premium.slug:
            upgrade = premium.title
            premium_slug = premium.slug
    transaction_logs = TransactionHistory.objects.filter(user=request.user)
    enrollment_logs = EnrollmentHistory.objects.filter(user__user=request.user)
    login_logs = LoginHistory.objects.filter(user=request.user)
    payload = {
        'plan': plan,
        'upgrade': upgrade,
        'slug': premium_slug,
        'transaction_logs': transaction_logs,
        'enrollment_logs': enrollment_logs,
        'login_logs': login_logs
    }
    return render(request, 'accountsettings.html', payload)

class dashcourseListView(ListView):
    model = Course
    template_name = 'dash_courses.html'

def dashprojects(request,slug):
    return render(request, 'dash_projects.html')

def dashassesments(request,slug):
    return render(request, 'dash_assesments.html')

"""def feed(request,slug):
    return render(request, 'dash_feed.html')"""

def notify(request,slug):
    profile = get_object_or_404(Profile, slug=slug)
    context = {}
    context['recent_notifications'] = profile.user_notifications.filter(mark_as_read=False)
    context['seen_notifications'] = profile.user_notifications.filter(mark_as_read=True)
    return render(request, 'dash_notification.html', context)

def mark_read(request, slug):
    ss = request.GET.get('status')
    notifi = get_object_or_404(Notifications, slug=slug)
    if ss=='t':
        notifi.mark_as_read = True
    elif ss=='f':
        notifi.mark_as_read = False
    elif ss=='d':
        notifi.delete()
        return HttpResponseRedirect(reverse('notifications', kwargs={'slug': notifi.profile.slug}))
    notifi.save()
    return HttpResponseRedirect(reverse('notifications', kwargs={'slug': notifi.profile.slug}))

def topics(request,slug):
    return render(request, 'dash_topics.html')

def events(request,slug):
    return render(request, 'dash_events.html')