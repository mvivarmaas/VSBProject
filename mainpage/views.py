from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .forms import IndexForm
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .VSBLogic import get_class, get_date, Scanner
import re
from django.shortcuts import redirect
from .models import Users, CRN
from django.core.exceptions import ValidationError
from .VSBLogic import send_email, FoundCRN
from .forms import ContactForm
import django_heroku
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from VSBProject import settings
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


# Create your views here.
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = IndexForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            class_name = form.cleaned_data.get("class_name")
            term = form.cleaned_data.get("term")

            class_name = class_name.upper()

            class_name = re.sub('[\W_]+', '', class_name)

            class_name = re.split('(\d+)', class_name)

            try:
                class_name = class_name[0] + "-" + class_name[1]
            except:
                HttpResponse(class_name)

            # get_class(class_name, "202109").to_dict().get("timeblocks")
            # return render(request, "results.html", get_class(class_name, "202109").to_dict())
            return redirect('class/' + term + "/" + class_name)


    # if a GET (or any other method) we'll create a blank form
    else:
        form = IndexForm()

    return render(request, 'index.html', {'form': form})




def classfinder(request, class_name, term):
    try:
        if request.method == "POST":
            CRN_Array = []
            email = request.POST.get("email", "")
            tel = request.POST.get("phone", "")

            if not Users.objects.filter(email=email).exists():
                if tel != "":
                    tel = tel.replace(" ", "")
                    tel = tel.replace("-", "")
                    tel = "+1" + tel

                    current_user = Users(email=email, phone_number=tel)

                else:
                    current_user = Users(email=email)

                try:
                    current_user.full_clean()
                    current_user.save()
                except ValidationError as e:
                    print(e)
                    return redirect("404")

            current_user = Users.objects.get(email=email)
            CRNs = ""
            for key in request.POST:

                if key == "email":
                    continue
                if key == "phone":
                    continue
                if key == "csrfmiddlewaretoken":
                    continue
                if key == "None":
                    continue

                key = re.sub("[^0-9]", "", key)
                CRNs = CRNs + " " + key
                if CRN.objects.filter(CRN=key, term=term, class_name=class_name).exists():

                    current_user.crn.add(CRN.objects.get(CRN=key, term=term, class_name=class_name))
                    current_user.full_clean()
                    current_user.save()
                else:
                    new_CRN = CRN(CRN=key, class_name=class_name, term=term)
                    new_CRN.full_clean()
                    new_CRN.save()
                    current_user.crn.add(new_CRN)
                    current_user.full_clean()
                    current_user.save()

            context = {"email": email, "class": class_name, "term": term, "CRNs": CRNs}

            if CRNs == "":
                return render(request, 'no_crn.html', context)

            return render(request, 'success.html', context)

        else:
            try:
                class_value = get_class(class_name, term).to_dict()
            except ArithmeticError as e:
                return render(request, 'fail.html', {"class": class_name, "term": term})

            return render(request, "results.html", class_value)

    except ValidationError as e:
        print(e)
        return redirect("failed")


def blue(request):
    # print(" -/- Users to follow -/- \n\n")
    # for x in Users.objects.all():
    #    print(str(x.email))
    #    print(str(x.phone_number))
    #    print(list(x.crn.all()))
    #    print("-/- CRN to follow -/-")

    # for x in CRN.objects.all():
    #    print(str(x) + "\n")

    # return HttpResponse("Hello, world, text 0v0 if you can see this blue. Hope you had a productive day")

    return HttpResponse("secert feature for Christina 0v0")


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            message = Mail(
                from_email='support@freeseatfinder.com',
                to_emails="abubakar.daud@mail.mcgill.ca",
                subject='CONTACT' + request.POST.get('subject'),
                html_content=request.POST.get('message') + "\n\n" + "email:" + request.POST.get('email'))
            try:
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                response = sg.send(message)
                print(Fore.CYAN + "Contact Email: ", request.POST.get('email')," | ", request.POST.get('subject') )

            except Exception as e:
                print(e)




            return render(request, 'contactsuccess.html')



    form = ContactForm()
    context = {'form': form}
    return render(request, 'contact.html', context)




def API(request):
    return render(request, "API.html")



def API_GET(request, slug, term):

    if getattr(request, 'limited', False):
        return JsonResponse(
            {"error": 'too many requests, you are being rate limited'}, status=429)


    try:
        slug = slug.split("-")
        subjectcode = slug[0]
        subjectnumber = slug[1]

        if not subjectnumber.isdecimal():
            raise ArithmeticError

        if not subjectcode.isalpha():
            raise ArithmeticError
    except:
        return JsonResponse({ "error" : 'Bad request try entering correct subject code and title example "/API/2019/COMP-206"' }, status=400)

    try:
        class_value = get_class(slug, term).to_dict()
    except:
        return JsonResponse({"error": 'not found"'},status=404)

    return JsonResponse(class_value,status=200)


def account(request):
    return HttpResponse("secert feature for Christina 0v0")
