from .models import User, Ad, OneTimeCode
import random
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AdForm, ReplyForm, RegistrationForm, VerifyForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from BulletinBoard import DEFAULT_FROM_EMAIL
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView


class IndexView(TemplateView):
    template_name = 'index.html'


class Register(View):
    template_name = 'account/register.html'

    def get(self, request):
        context = {
            'form': RegistrationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            numbers = list('0123456789')
            verify_code = ''
            for x in range(6):
                verify_code += random.choice(numbers)
            OneTimeCode.objects.create(user=user, code=verify_code)
            html_content = render_to_string('registration/verify_email.html', {'code': verify_code})
            msg = EmailMultiAlternatives(
                subject='Подтверждение регистрации',
                from_email=DEFAULT_FROM_EMAIL,
                to=[email]
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            return redirect('confirm_email')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class EmailVerify(View):
    template_name = 'registration/confirm.html'

    def get(self, request):
        context = {
            'form': VerifyForm
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = VerifyForm(request.POST)
        email = request.POST['user']
        code = request.POST['code']
        if OneTimeCode.objects.filter(user__email=email, code=code).exists():
            user = User.objects.get(email=email)
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('index')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class AdCreate(LoginRequiredMixin, CreateView):
    form_class = AdForm
    model = Ad
    template_name = 'ad/create.html'

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.author = User.objects.get(id=self.request.user.id)
        return super().form_valid(form)


class AdView(ListView):
    model = Ad
    template_name = 'ad/list.html'
    ordering = '-datetime_creation'
    context_object_name = 'ad_list'


def AdDetail(request, post_id):
    ad = get_object_or_404(Ad, pk=post_id)
    replies = ad.replies.count
    new_reply = None
    if request.method == 'POST':
        reply_form = ReplyForm(data=request.POST)
        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)
            new_reply.ad = ad
            new_reply.user = User.objects.get(id=request.user.id)
            new_reply.save()
    else:
        reply_form = ReplyForm()
    return render(request, 'ad/ad.html', {'ad': ad, 'replies': replies, 'new_reply': new_reply, 'reply_form': reply_form})
