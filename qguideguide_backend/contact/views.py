from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', block=True)
def contact_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})
