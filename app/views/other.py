from django.http import HttpResponse


def user_greetings(request):
    name = "Anna"
    return HttpResponse(
        f"<h2>Hello, {name}!</h2>")