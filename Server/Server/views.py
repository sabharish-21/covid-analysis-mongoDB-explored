from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from mongoDB import views as mongo
import base64

db = mongo.connectDB()


def errorPage(request, exception):
    print(exception)
    return render(request, '404.html')


def profilePic(request):
    if str(request.user).lower() != 'anonymoususer':
        temp = db.user.find_one({'email': str(request.user.email)}).get('profilePic', None)
        if temp is not None:
            image_data = base64.b64encode(temp).decode('utf-8')
            return {'img': image_data}
        else:
            return {}
    else:
        return {}


@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html', {'data': mongo.getHomeContent()})


def loginShow(request):
    if str(request.user).lower() == 'anonymoususer':
        return render(request, 'signin.html')
    else:
        return redirect('/')


@csrf_exempt
def loginAuth(request):
    if request.method == 'POST':
        userName = request.POST['mailID']
        pwd = request.POST['password']
        nextTo = request.POST['next']

        if nextTo == '' or nextTo is None:
            nextTo = '/'
        user = auth.authenticate(username=userName, password=pwd)
        if user is not None:
            auth.login(request, user)
            return redirect(nextTo)
        else:
            return render(request, 'signin.html', {'data': '* Invalid Credentials'})
    else:
        return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/login')


# ---------------------------------------------  x ANALYZE START x ---------------------------------- #
@login_required(login_url='/login')
def showAnalyze(request):
    return render(request, 'analysis.html')


def getGraphData(request, *args, **kwargs):
    try:
        aOne = mongo.getAnalysisOne()
        aTwo = mongo.getAnalysisTwo()
        aThree = mongo.getAnalysisThree()
        aFour = mongo.getAnalysisFour()
        aFive = mongo.getAnalysisFive()

        data = {
            'one': {
                'label': aOne[0],
                'data': aOne[1],
                'chartLabel': 'Total Vaccinations of each country',
            },
            'two': {
                'label': list(range(0, max(len(aTwo[1][0]), len(aTwo[1][1]), len(aTwo[1][2])))),
                'data': aTwo[1],
                'chartLabel': aTwo[0],
            },
            'three': {
                'label': aThree[0],
                'data': aThree[1],
                'chartLabel': 'Vaccinations by country',
            },
            'four': {
                'label': aFour[0],
                'dataOne': aFour[1][0],
                'dataTwo': aFour[1][1],
                'chartLabel': 'Fully | Partially Vaccinated',
            },
            'five': {
                'label': aFive[0],
                'data': aFive[1],
                'chartLabel': 'Vaccines Wasted',
            }
        }
    except Exception as e:
        data = {'error_data': e}

    return JsonResponse(data)


# ---------------------------------------------  x ANALYZE END x ---------------------------------- #
# ---------------------------------------------  x DASHBOARD  START x ---------------------------------- #

def districtStreamCheck(request):
    try:
        changeStream = db.districtData.watch()
        for _ in changeStream:
            totalConfirmed = [i['total'] for i in db.districtData.aggregate([
                {'$group': {'_id': None, 'total': {'$sum': '$Confirmed'}}}
            ])][0]

            totalActive = [i['total'] for i in db.districtData.aggregate([
                {'$group': {'_id': None, 'total': {'$sum': '$Active'}}}
            ])][0]

            totalRecovered = [i['total'] for i in db.districtData.aggregate([
                {'$group': {'_id': None, 'total': {'$sum': '$Recovered'}}}
            ])][0]

            totalDeceased = [i['total'] for i in db.districtData.aggregate([
                {'$group': {'_id': None, 'total': {'$sum': '$Deceased'}}}
            ])][0]

            temp = [i for i in db.districtData.find({"State": {"$exists": True}})]
            temp.sort(key=lambda x: x['Active'], reverse=True)
            returnData = []
            for i in temp[0:5]:
                returnData.append({
                    'State': i['State'],
                    'District': i['District'],
                    'Active': int(i['Active']),
                    'Confirmed': int(i['Confirmed']),
                    'Recovered': int(i['Recovered']),
                    'Deceased': int(i['Deceased']),
                })

            data = dict({
                'totalConfirmed': int(totalConfirmed),
                'totalActive': int(totalActive),
                'totalRecovered': int(totalRecovered),
                'totalDeceased': int(totalDeceased),
                'table': returnData
            })
            return JsonResponse(data)

    except Exception as e:
        print(e)
        return JsonResponse({'error_data': str(e)})


# ---------------------------------------------  x DASHBOARD  END x ------------------------------------ #
# ---------------------------------------------  x MODIFICATION START x -------------------------------- #
@login_required(login_url='/login')
def showModify(request):
    return render(request, 'modifyData.html')


@login_required(login_url='/login')
def showView(request):
    return render(request, 'viewData.html', {'states': db.districtData.distinct("State")})


def getDistrict(request):
    try:
        state = str(request.GET.get('state', None))
        district = db.districtData.find({'State': state}, {'_id': 0, 'District': 1})
        district = sorted(list(set([i['District'] for i in district])))

        return JsonResponse({'district': district})
    except Exception as e:
        print(e)
        return JsonResponse({'error_data': str(e)})


def getDistrictData(request):
    try:
        state = str(request.GET.get('state', None))
        district = str(request.GET.get('district', None))

        districtData = db.districtData.find_one({'State': state, 'District': district})
        data = {
            'confirmed': int(districtData['Confirmed']),
            'active': int(districtData['Active']),
            'recovered': int(districtData['Recovered']),
            'deceased': int(districtData['Deceased']),
        }
        return JsonResponse(data)
    except Exception as e:
        print(e)
        return JsonResponse({'error_data': str(e)})


def updateDistrictData(request):
    try:
        state = str(request.GET.get('state', None))
        district = str(request.GET.get('district', None))
        Confirmed = int(request.GET.get('Confirmed', None))
        Active = int(request.GET.get('Active', None))
        Recovered = int(request.GET.get('Recovered', None))
        Deceased = int(request.GET.get('Deceased', None))

        data = {
            "Confirmed": Confirmed,
            "Recovered": Recovered,
            "Active": Active,
            "Deceased": Deceased
        }

        db.districtData.update_one({'State': state, 'District': district}, {'$set': data})

        return JsonResponse({'state': 'success'})
    except Exception as e:
        print(e)
        return JsonResponse({'error_data': str(e)})
# ---------------------------------------------  x MODIFICATION END x ---------------------------------- #
