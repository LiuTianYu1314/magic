from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SimpleUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = SimpleUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
    else:
        form = SimpleUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')