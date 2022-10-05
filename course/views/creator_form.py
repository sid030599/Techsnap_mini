from django.shortcuts import render, redirect
from course.models import *
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import auth, User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from course.forms import *
import json


def course_form(request, code):
    profile = Profile.objects.get(slug=code)
    if request.method == 'GET':
        courses = Course.objects.filter(instructor=profile)
        form = CourseForm()
        return render(request, 'teacher/index.html', {'courses': courses, 'creator': profile, 'form': form})
    else :
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = profile
            course.save()
            return redirect('admin-panel', code=profile.slug)
        print(form.errors)
        return redirect('admin-panel', code=profile.slug)

def update_course_details(request, slug):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        if profile.is_creator:
            course = Course.objects.filter(slug__iexact=slug).first()
            course_form = CourseForm(instance=course)
            return render(request, "course/creator_form/update_course_details.html", {'course': course, 'form': course_form})
        return redirect('')

def update_course_desc(request, slug):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        if profile.is_creator:
            course = Course.objects.filter(slug__iexact=slug).first()
            description = Description.objects.filter(course=course)
            if description.exists():
                desc_form = DescriptionForm(instance=description.first())
            else :
                desc_form = DescriptionForm()
            data = {
                'desc': description.first(),
                'form': desc_form,
                'slug': course.slug
            }
            return render(request, "course/creator_form/update_course_desc.html", data)
        return redirect('')

def update_course_info(request, slug):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        if profile.is_creator:
            course = Course.objects.filter(slug__iexact=slug).first()

            anouncements = Anouncement.objects.filter(course=course)
            anouncement_form = AnouncementForm()

            faq_objs = FrequentlyAskedQuestion.objects.filter(course=course)
            faq_form = FrequentlyAskedQuestionForm()

            data = {
                'slug': course.slug,
                'anouncements': anouncements,
                'form': anouncement_form,
                'faqs': faq_objs,
                'faq_form': faq_form
            }
            return render(request, "course/creator_form/update_course_info.html", data)
        return redirect('')

def course_desc_form(request, slug):
    code = Course.objects.get(slug=slug).instructor.slug
    profile = Profile.objects.get(slug=code)
    if request.method == 'GET':
        if profile.is_creator:
            # course
            course = Course.objects.filter(slug__iexact=slug).first()
            # units
            units = Unit.objects.filter(course=course)
            unit_form = UnitForm()
            # rating 
            rating = Rating.objects.filter(course=course)
            rating_form = RatingForm()
            if rating.exists():
                rating_update_form = RatingForm(instance=rating.first())
            else :
                rating_update_form = None
            # review
            review_objs = Review.objects.filter(course=course)
            review_form = ReviewForm()
            reviews = []
            for review in review_objs:
                data = {
                    'name': review.name,
                    'id': review.id,
                }
                reviews.append(data)
            # testimonial 
            testimonial_objs = Testimonial.objects.filter(course=course)
            testimonial_form = TestimonialForm()
            testimonials = []
            for testimonial in testimonial_objs:
                data = {
                    'name': testimonial.name,
                    'id': testimonial.id,
                }
                testimonials.append(data)

            payload = {
                'course': course,
                'units': units,
                'rating': rating.first(),
                'reviews': reviews,
                'testimonials': testimonials,
                # Forms
                'unit_form': unit_form,
                'rating_form': rating_form,
                'rating_update_form': rating_update_form,
                'review_form': review_form,
                'testimonial_form': testimonial_form,
                'creator': profile
            }

            return render(request, "teacher/course.html", payload)
        return redirect('')


# Delete views 

def delete_course(request, slug):
    code = Course.objects.get(slug=slug).instructor.slug
    Course.objects.get(slug__iexact=slug).delete()
    return redirect('admin-panel', code=code)

def delete_unit(request, pk):
    slug = Unit.objects.get(id=pk).course.slug
    Unit.objects.get(id=pk).delete()
    return redirect('course-desc-form', slug=slug)

def delete_anouncement(request, pk):
    slug = Anouncement.objects.get(id=pk).course.slug
    Anouncement.objects.get(id=pk).delete()
    return redirect('course-desc-form', slug=slug)

def delete_review(request, pk):
    slug = Review.objects.get(id=pk).course.slug
    Review.objects.get(id=pk).delete()
    return redirect('course-desc-form', slug=slug)

def delete_testimonial(request, pk):
    slug = Testimonial.objects.get(id=pk).course.slug
    Testimonial.objects.get(id=pk).delete()
    return redirect('course-desc-form', slug=slug)

def delete_faq(request, pk):
    slug = FrequentlyAskedQuestion.objects.get(id=pk).course.slug
    FrequentlyAskedQuestion.objects.get(id=pk).delete()
    return redirect('course-desc-form', slug=slug)

def delete_lesson(request, slug):
    code = Lesson.objects.get(slug__iexact=slug).unit.course.slug
    Lesson.objects.get(slug__iexact=slug).delete()
    return redirect('course-desc-form', slug=code)


# Create views 

def create_obj(request, slug, obj):
    if request.method == 'POST':
        course = Course.objects.get(slug__iexact=slug)
        profile = Profile.objects.get(user=request.user)
        if obj=='unit':
            form = UnitForm(request.POST, request.FILES)
            if form.is_valid():
                unit = form.save(commit=False)
                unit.course = course
                unit.save()
                return redirect('course-desc-form', slug=slug)
            
        elif obj=='anouncement':
            form = AnouncementForm(request.POST, request.FILES)
            if form.is_valid():
                anouncement = form.save(commit=False)
                anouncement.course = course
                anouncement.instructor = profile
                anouncement.save()
                return redirect('update-course-info', slug=slug)
            
        elif obj=='review':
            form = ReviewForm(request.POST, request.FILES)
            if form.is_valid():
                review = form.save(commit=False)
                review.course = course
                review.save()
                return redirect('course-desc-form', slug=slug)
            
        elif obj=='testimonial':
            form = TestimonialForm(request.POST, request.FILES)
            if form.is_valid():
                testimonial = form.save(commit=False)
                testimonial.course = course
                testimonial.save()
                return redirect('course-desc-form', slug=slug)
            
        elif obj=='faq':
            form = FrequentlyAskedQuestionForm(request.POST, request.FILES)
            if form.is_valid():
                faq = form.save(commit=False)
                faq.course = course
                faq.save()
                return redirect('update-course-info', slug=slug)
            
        elif obj=='description':
            form = DescriptionForm(request.POST, request.FILES)
            if form.is_valid():
                desc = form.save(commit=False)
                desc.course = course
                desc.save()
                return redirect('course-desc-form', slug=slug)
            
        elif obj=='rating':
            form = RatingForm(request.POST, request.FILES)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.course = course
                rating.save()
                return redirect('course-desc-form', slug=slug)
        print(form.errors)
        return redirect('course-desc-form', slug=slug)
    return redirect('course-desc-form', slug=slug)


def update_obj(request, slug, obj, pk):
    if request.method == 'POST':
        if obj=='unit':
            unit = Unit.objects.get(id=pk)
            form = UnitForm(request.POST, request.FILES, instance=unit)
            if form.is_valid():
                form.save()
                return redirect('update-unit', slug=slug, unit_slug=unit.slug)
            print(form.errors)
            return redirect('update-unit', slug=slug, unit_slug=unit.slug)

        elif obj=='course':
            course = Course.objects.get(id=pk)
            form = CourseForm(request.POST, request.FILES, instance=course)
            if form.is_valid():
                form.save()
                return redirect('update-course-details', slug=course.slug)
            print(form.errors)
            return redirect('update-course-details', slug=course.slug)

        elif obj=='anouncement':
            anouncement = Anouncement.objects.get(id=pk)
            form = AnouncementForm(request.POST, request.FILES, instance=anouncement)
            if form.is_valid():
                form.save()
                return redirect('update-course-info', slug=slug)
            print(form.errors)
            return redirect('update-course-info', slug=slug)

        elif obj=='review':
            review = Review.objects.get(id=pk)
            form = ReviewForm(request.POST, request.FILES, instance=review)
        elif obj=='testimonial':
            testimonial = Testimonial.objects.get(id=pk)
            form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        elif obj=='faq':
            faq = FrequentlyAskedQuestion.objects.get(id=pk)
            form = FrequentlyAskedQuestionForm(request.POST, request.FILES, instance=faq)

        elif obj=='description':
            desc = Description.objects.get(id=pk)
            form = DescriptionForm(request.POST, request.FILES, instance=desc)
            if form.is_valid():
                form.save()
                return redirect('update-course-desc', slug=course.slug)
            print(form.errors)
            return redirect('update-course-desc', slug=course.slug)

        elif obj=='rating':
            rating = Rating.objects.get(id=pk)
            form = RatingForm(request.POST, request.FILES, instance=rating)
        elif obj=='lesson':
            lesson = Lesson.objects.get(id=pk)
            form = LessonForm(request.POST, request.FILES, instance=lesson)
            if form.is_valid():
                form.save()
                return redirect('update-unit', slug=slug, unit_slug=lesson.unit.slug)
            print(form.errors)
            return redirect('update-unit', slug=slug, unit_slug=lesson.unit.slug)

        if form.is_valid():
            form.save()
            return redirect('course-desc-form', slug=slug)
        print(form.errors)
        return redirect('course-desc-form', slug=slug)

    if obj=='unit':
        unit = Unit.objects.get(id=pk)
        form = UnitForm(instance=unit)
    elif obj=='anouncement':
        anouncement = Anouncement.objects.get(id=pk)
        form = AnouncementForm(instance=anouncement)
        static = anouncement

    elif obj=='review':
        review = Review.objects.get(id=pk)
        form = ReviewForm(instance=review)
        static = review

    elif obj=='testimonial':
        testimonial = Testimonial.objects.get(id=pk)
        form = TestimonialForm(instance=testimonial)
        static = testimonial

    elif obj=='faq':
        faq = FrequentlyAskedQuestion.objects.get(id=pk)
        form = FrequentlyAskedQuestionForm(instance=faq)
    elif obj=='description':
        desc = Description.objects.get(id=pk)
        form = DescriptionForm(instance=desc)
    elif obj=='rating':
        rating = Rating.objects.get(id=pk)
        form = RatingForm(instance=rating)
    elif obj=='lesson':
        lesson = Lesson.objects.get(id=pk)
        form = LessonForm(instance=lesson)
        static = lesson

    data = {
        'static': static,
        'form': form, 
        'slug': slug, 
        'obj': obj, 
        'pk': pk
    }

    return render(request, 'course/creator_form/obj_update.html', data)
    
def update_unit(request, slug, unit_slug):
    profile = Profile.objects.get(user=request.user)
    if profile.is_creator:
        if request.method=='POST':
            unit = Unit.objects.get(slug__iexact=unit_slug)
            latest_order = Lesson.objects.filter(unit__course=unit.course).order_by('-order')
            if latest_order:
                latest_order = latest_order.first().order
            else :
                latest_order = 0
            form = LessonForm(request.POST, request.FILES)
            if form.is_valid():
                lesson = form.save(commit=False)
                lesson.unit = unit
                lesson.order = latest_order + 1
                lesson.save()
                return redirect('update-unit', slug=slug, unit_slug=unit_slug)
            print(form.errors)
            return redirect('update-unit', slug=slug, unit_slug=unit_slug)
        
        unit = Unit.objects.filter(slug=unit_slug).first()
        lessons = Lesson.objects.filter(unit=unit)
        lesson_form = LessonForm()
        unit_form = UnitForm(instance=unit)
        data = {
            'slug': slug,
            'unit': unit,
            'unit_form': unit_form,
            'lesson_form': lesson_form,
            'lessons': lessons
        }
        return render(request, 'course/creator_form/unit_lesson.html', data)

def hr_panel(request):
    profile = Profile.objects.get(user=request.user)
    if profile.is_hr:
        multiple = []
        creators = Profile.objects.filter(is_creator=True)
        for creator in creators:
            total_courses = len(Course.objects.filter(instructor=creator))
            single = {
                'details': creator,
                'total_courses': total_courses
            }
            multiple.append(single)
        print(multiple)
        return render(request, 'course/hr_panel/panel.html', {'creators': multiple})

def get_creator_panel(request, code):
    print(code)
    profile = Profile.objects.get(user=request.user)
    if profile.is_hr:
        return redirect('admin-panel', code=code)

def stats_page(request, slug):
    user = Profile.objects.get(user=request.user)
    if user.is_creator:
        course = Course.objects.filter(slug=slug).first()
        enrolled_profiles = UserCourseMap.objects.filter(course=course)
        stats = []
        for profile in enrolled_profiles:
            completed = []
            not_completed = []
            for lesson in UserLessonCompletion.objects.filter(lesson__unit__course=course, user=profile.user):
                if lesson.completed:
                    completed.append(lesson.lesson.title)
                else :
                    not_completed.append(lesson.lesson.title)
            detail = json.dumps({
                "completed": completed,
                "not_completed": not_completed,
                "username": profile.user.user.username
            })
            stat = {
                    "map": profile,
                    "detail": detail,
            }
            stats.append(stat)
        payload = {
            'stats': stats, 
            'course': course,
            'user': user,
        }
        print(user.user.username)
        return render(request, 'course/creator_form/stats.html', payload)
    return redirect('course-desc-form', slug=slug)

def lesson_stats_page(request, slug):
    completed = []
    not_completed = []
    for lesson in UserLessonCompletion.objects.filter(lesson__slug=slug):
        if lesson.completed:
            completed.append(lesson.user.user.username)
        else :
            not_completed.append(lesson.user.user.username)
    payload = {
        'lesson': Lesson.objects.get(slug=slug),
        'completed': completed,
        'not_completed': not_completed
    }
    return render(request, 'course/creator_form/lesson_stats.html', payload)