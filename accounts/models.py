import hashlib
from django.core import validators
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils import timezone

# Create your models here.
User._meta.get_field('email')._unique = True

def current_year():
        return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year()+10)(value)

def get_unique_string(body, time):
    s = str(body)+str(time)
    result_str = hashlib.sha1(s.encode()).hexdigest()[:10]
    return result_str

    
gender_choices = (('M', 'MALE'),
('F', 'FEMALE'),
('O', 'OTHER'))
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # personal details
    bio = models.CharField(max_length=500, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    full_name               =       models.CharField(max_length=100, blank=True, null=True)
    gender                  =       models.CharField(choices=gender_choices, max_length=2, blank=True, null=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    state                   =       models.CharField(max_length=40, null=True, blank=True)
    city                    =       models.CharField(max_length=40, null=True, blank=True)
    linkedin                =       models.URLField(max_length=200, null=True, blank=True)
    github                  =       models.URLField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    ph_num = models.CharField(max_length=15, null=True, blank=True)
    skills = models.CharField(max_length=400, null=True, blank=True)
    languages = models.CharField(max_length=400, null=True, blank=True)
    default_coding_lang = models.CharField(max_length=100, null=True, blank=True)
    resume = models.FileField(upload_to='profile_resumes', null=True, blank=True)

    # educational info
    institute_name          =       models.CharField(max_length=100, null=True, blank=True)
    institute_location = models.CharField(max_length=100, null=True, blank=True)
    yearOfPassing           =       models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1980), max_value_current_year], null=True, blank=True)
    current_cgpa       =       models.FloatField(null=True, validators=[MaxValueValidator(100), MinValueValidator(0)], blank=True)
    out_of        =       models.FloatField(null=True, validators=[MaxValueValidator(100), MinValueValidator(0)], blank=True)
    # professional info
    workExp                 =       models.FloatField(null=True, validators=[MinValueValidator(0), MaxValueValidator(50)], blank=True)
    current_CTC             =       models.FloatField(null=True, blank=True)
    notice_period = models.IntegerField(null=True, blank=True)
    willing_to_relocate = models.BooleanField(default=True, null=True, blank=True)
    expected_CTC            =       models.FloatField(null=True, blank=True)
    current_company         =       models.CharField(max_length=200, null=True, blank=True)
    dream_company           =       models.CharField(max_length=200, null=True, blank=True)
    designation             =       models.CharField(max_length=100, null=True, blank=True)
    xp = models.IntegerField(null=True, default=100, blank=True)
    techsnap_cash = models.IntegerField(null=True, default=999, blank=True)

    slug = models.SlugField(max_length=200, editable=False, null=True, blank=True)

    is_student = models.BooleanField(default=True)
    is_creator = models.BooleanField(default=False)
    is_hr = models.BooleanField(default=False)
    teammates = models.ManyToManyField(User, related_name='teammates', blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super(Profile, self).save()
        self.slug = slugify(self.user.username)
        super(Profile, self).save()

    def courseprofile(self):
        return self.course_profile.all()

    @property
    def num_ForumPosts(self):
        return ForumPost.objects.filter(user=self).count()

def edu_generate_code():
    length=9
    base = string.ascii_lowercase+string.ascii_uppercase+string.digits
    while True:
        code = ''.join(random.choices(base, k=length))
        break
    return code

def pro_generate_code():
    length=9
    base = string.ascii_lowercase+string.ascii_uppercase+string.digits
    while True:
        code = ''.join(random.choices(base, k=length))
        break
    return code

class Education(models.Model):
    #profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    slug = models.CharField(max_length=20, default=edu_generate_code, editable=False)
    institute_name          =       models.CharField(max_length=100, null=True, blank=True)
    institute_location = models.CharField(max_length=100, null=True, blank=True)
    yearOfPassing           =       models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1980), max_value_current_year], null=True, blank=True)
    current_cgpa       =       models.FloatField(null=True, validators=[MaxValueValidator(100), MinValueValidator(0)], blank=True)
    out_of        =       models.FloatField(null=True, validators=[MaxValueValidator(100), MinValueValidator(0)], blank=True)

class Proffesion(models.Model):
    #profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    slug = models.CharField(max_length=20, default=pro_generate_code, editable=False)
    workExp                 =       models.FloatField(null=True, validators=[MinValueValidator(0), MaxValueValidator(50)], blank=True)
    current_CTC             =       models.FloatField(null=True, blank=True)
    notice_period = models.IntegerField(null=True, blank=True)
    willing_to_relocate = models.BooleanField(default=True, null=True, blank=True)
    expected_CTC            =       models.FloatField(null=True, blank=True)
    current_company         =       models.CharField(max_length=200, null=True, blank=True)
    dream_company           =       models.CharField(max_length=200, null=True, blank=True)
    designation             =       models.CharField(max_length=100, null=True, blank=True)

class Notifications(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_notifications')
    image = models.ImageField(upload_to='notifications')
    mark_as_read = models.BooleanField(default=False)
    body = models.TextField()
    url = models.URLField(null=True, blank=True)
    url_name = models.CharField(max_length=255, default='View', null=True, blank=True)
    notified_time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=16, null=True, unique=True, editable=False)

    def __str__(self):
        return self.profile.user.username + ' ' + self.body[0:15]

    def save(self, *args, **kwargs):
        super(Notifications, self).save()
        self.slug = slugify(get_unique_string(self.body, self.notified_time))
        super(Notifications, self).save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class TransactionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    log = models.CharField(max_length=300)
    amount = models.IntegerField(default=0)
    code = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"USER [{self.user.username}] LOG [{self.log}] DATE [{self.date}] AMOUNT [{self.amount}]"

# Create your views here.
def create_history(user, to_plan, from_plan=None, upgrade=False):
    if upgrade:
        history = TransactionHistory.objects.get(user=user, code=from_plan.slug)
        today = datetime.date.today()
        completed_days = (today - history.date).days
        payment_per_day = from_plan.price / from_plan.duration
        payment_adv = (from_plan.duration - completed_days)*payment_per_day
        price_to_pay = to_plan.price - payment_adv
        
        log = f"User [{user.username}] Upgraded to Plan [{to_plan}] from Plan [{from_plan}]"
        TransactionHistory.objects.create(user=user, log=log, amount=price_to_pay, code=to_plan.slug)
    else :
        log = f"User [{user.username}] Subscribed to Plan [{to_plan}]"
        TransactionHistory.objects.create(user=user, log=log, amount=to_plan.price, code=to_plan.slug)

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    logged_in = models.BooleanField(default=True)

    def __str__(self):
        status = 'LOGGED OUT'
        if self.logged_in:
            status = 'LOGGED IN'
        return f"USER [{self.user.username}] {status} at [{self.date}]"

class PaytmHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='rel_payment_paytm')
    ORDERID = models.CharField('ORDER ID', max_length=30)
    TXNDATE = models.DateTimeField('TXN DATE', default=timezone.now)
    CURRENCY = models.CharField('CURRENCY', max_length=4, null=True, blank=True, default="INR")
    MID = models.CharField(max_length=40)
    TXNAMOUNT = models.FloatField('TXN AMOUNT', default=1)

    class Meta:
        app_label = 'accounts'

    def __unicode__(self):
        return self.STATUS