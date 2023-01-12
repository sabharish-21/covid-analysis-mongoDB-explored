from pymongo import MongoClient

global db, database
databaseName = 'project'


def connectDB():
    global db, database, databaseName
    connString = 'mongodb://192.168.114.124:27017,192.168.114.201:27017,192.168.114.213:27017/?replicaSet=bdms'

    db = MongoClient(connString)
    database = db[databaseName]

    return database


def getAnalysisOne():
    """
    Plotting total vaccination count of each country
    :return:
    """
    inputCountry = ['Austria', 'Hong Kong', 'England', 'Argentina', 'Australia']

    totalVaccinations = [list(i.values()) for i in database.vaccinations.aggregate([
        {'$match': {'country': {'$in': inputCountry}}},
        {'$group': {'_id': "$country", 'Total': {'$max': '$total_vaccinations'}}}
    ])]

    countryList = list(map(lambda x: x[0], totalVaccinations))

    total_vaccinations_count = list(map(lambda x: x[1], totalVaccinations))
    return countryList, total_vaccinations_count


def getAnalysisTwo():
    """
    Plotting daily vaccination details for each country
    :return:
    """
    inputCountry = ["England", 'Australia', 'Argentina']
    data = []

    for j in inputCountry:
        country_daily = [list(i.values()) for i in database.vaccinations.find(
            {'country': j, 'daily_vaccinations': {'$exists': 'true', '$ne': 'null'}},
            {'_id': 0, 'daily_vaccinations': 1, 'date': 1})]

        data.append(list(map(lambda x: x[1], country_daily)))

    return inputCountry, data


def getAnalysisThree():
    """
    Plotting total number of countries used a particular kind of vaccine
    :return:
    """
    # Fetching all vaccine names
    temp_v1 = list(database.vaccinations.find({}, {'vaccines': 1, '_id': 0}))
    temp_v2 = [str(i['vaccines']).split(',') for i in temp_v1]
    vaccines = []
    for i in temp_v2:
        vaccines.extend(i)

    vaccines = list(set([i.strip() for i in vaccines]))

    # Collecting the count of countires for a particular vaccine
    country_count = []
    for i in vaccines:
        country_count.append(len(database.vaccinations.distinct("country", {'vaccines': {'$regex': i}})))

    return vaccines, country_count


def getAnalysisFour():
    """
    Plotting Fully vs Partially Vaccinated People
    :return:
    """
    input_country = ['Austria', 'Hong Kong', 'England', 'Argentina', 'Australia']

    total_vaccinations = [list(i.values())
                          for i in database.vaccinations.aggregate([
            {'$match': {'country': {'$in': input_country}}},
            {'$group': {'_id': "$country", 'Totalp': {'$max': '$people_vaccinated'},
                        'Totalf': {'$max': '$people_fully_vaccinated'}}}
        ])]

    people_partially_vaccinated = list(map(lambda x: abs(x[2] - x[1]), total_vaccinations))
    people_fully_vaccinated = list(map(lambda x: x[2], total_vaccinations))
    countries = list(map(lambda x: x[0], total_vaccinations))

    return countries, [people_fully_vaccinated, people_partially_vaccinated]


def getAnalysisFive():
    """
    Plotting no.of.vaccines wasted in each country
    :return:
    """
    input_country = ['Canada', 'England', 'Argentina', 'Australia', 'Hong Kong']

    vaccine_wasted_list = [list(i.values()) for i in database.vaccinations.aggregate([
        {'$match': {'country': {'$in': input_country}}},
        {'$group': {'_id': "$country", 'm1': {'$max': '$total_vaccinations'}, 'm2': {'$max': '$people_vaccinated'}}}])]

    vaccine_wasted = list(map(lambda x: abs(x[2] - x[1]), vaccine_wasted_list))
    countries = list(map(lambda x: x[0], vaccine_wasted_list))

    return countries, vaccine_wasted


def getHomeContent():
    totalDistrict = len(database.districtData.distinct('District'))

    tempA = database.districtData.find({"State": {'$ne': None}}, {"State": 1, '_id': 0})
    totalState = len(set([i['State'] for i in tempA]))

    totalConfirmed = database.districtData.aggregate([
        {'$group': {'_id': None, 'total': {'$sum': '$Confirmed'}}}
    ])
    totalConfirmed = [i['total'] for i in totalConfirmed][0]

    totalActive = database.districtData.aggregate([
        {'$group': {'_id': None, 'total': {'$sum': '$Active'}}}
    ])
    totalActive = [i['total'] for i in totalActive][0]

    totalRecovered = database.districtData.aggregate([
        {'$group': {'_id': None, 'total': {'$sum': '$Recovered'}}}
    ])
    totalRecovered = [i['total'] for i in totalRecovered][0]

    totalDeceased = database.districtData.aggregate([
        {'$group': {'_id': None, 'total': {'$sum': '$Deceased'}}}
    ])
    totalDeceased = [i['total'] for i in totalDeceased][0]

    temp = []
    for i in database.districtData.find({"State": {"$exists": True}}):
        temp.append(i)
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
    return {
        'totalState': int(totalState),
        'totalDistrict': int(totalDistrict),
        'totalConfirmed': int(totalConfirmed),
        'totalActive': int(totalActive),
        'totalRecovered': int(totalRecovered),
        'totalDeceased': int(totalDeceased),
        'table': returnData
    }
