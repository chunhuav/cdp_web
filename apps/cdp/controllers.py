
"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from cgitb import text
from email.policy import default
from py4web import action, request, abort, redirect, URL
from py4web import action, Field, redirect, URL
from py4web.utils.form import Form,INPUT
from pydal.validators import IS_NOT_EMPTY
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
import requests
import json
import base64
import json2html
from requests.auth import HTTPBasicAuth

unomi_url = "http://3.113.215.104:8181/"
username = 'karaf'
password = 'karaf'
basic_auth = HTTPBasicAuth(username, password)
print(str(basic_auth))
http_header={
        'Authorization': "Basic "+"a2FyYWY6a2FyYWY=",
        'Content-Type': 'application/json'
        }


@unauthenticated("index", "index.html")
def index():
    profilecount = profilecountnumber()
    profilevisitdate_list = profilevisitdate()
    agent_list = useragentlist()
    path_list = getpathlist()
    return dict(profilecount=profilecount,
                profilevisitdate_list=profilevisitdate_list,
                agent_list=agent_list,
                path_list=path_list)


@action("dashboard")
@action.uses('dashboard.html')
def dashboard():
    profilecount = profilecountnumber()
    profilevisitdate_list = profilevisitdate()
    agent_list = useragentlist()
    path_list = getpathlist()
    return dict(profilecount=profilecount,
                profilevisitdate_list=profilevisitdate_list,
                agent_list=agent_list,
                path_list=path_list)

@action("rulelist")
@action.uses("rulelist.html")
def rulelist():

    url = unomi_url+"cxs/rules"
    payload = ""
    headers = http_header

    response = requests.request("GET", url, auth=basic_auth, data=payload)
    # print(response.text)
    rulelistjson = response.text
    rulelist = json.loads(rulelistjson)
    return dict(rulelist=rulelist)


@action('session', method=['GET', 'POST'])
@action.uses('session.html')
def session():
    print(request.query)
    profileid = request.query.profileid
    if profileid:
        url = unomi_url+"cxs/profiles/"+profileid+"/sessions"
        payload = ""
        headers = http_header
        response = requests.request("GET", url, auth=basic_auth, data=payload)
        session = response.text
        print(response.text)
        sessionlist = json.loads(session)
        print(sessionlist["list"])
        return dict(sessionlist=sessionlist["list"])
    else:
        return dict(sessionlist=list())


@action("profilesearch", method=['GET', 'POST'])
@action.uses("profilesearch.html")
def profilesearch():
    form = Form([
        Field('CDP_Username', "str"),
        Field('CDP_Profile_id', 'str'),
    ])
    if form.accepted:
        username = form.vars['CDP_Username']
        profileid = form.vars['CDP_Profile_id']

        url = unomi_url+"cxs/profiles/search/"
        payload = json.dumps({
            "offset": 0,
            "forceRefresh": True,
            "condition": {
                "type": "booleanCondition",
                "parameterValues": {
                    "operator": "or",
                    "subConditions": [
                        {
                            "type": "profilePropertyCondition",
                            "parameterValues": {
                                "propertyName": "properties.username",
                                "comparisonOperator": "startsWith",
                                "propertyValue": username
                            }
                        },
                        {
                            "type": "profilePropertyCondition",
                            "parameterValues": {
                                "propertyName": "itemId",
                                "comparisonOperator": "equals",
                                "propertyValue": profileid
                            }
                        }
                    ]
                }
            },
            "limit": -1
        })

        headers = headers = http_header
        print(headers)
        response = requests.request("POST", url, headers=headers, data=payload)

        profilelistjson = response.text
        # print(profilelistjson)
        profilelist = json.loads(profilelistjson)
        print(profilelist["list"])
        return dict(form=form, profilelist=profilelist["list"])
        # return dict(form=form,profilelist=list())
    if form.errors:
        return dict(form=form, profilelist=list())
    return dict(form=form, profilelist=list())


# @action("createprofile")
# def createprofile():

    # url = unomi_url+"/cxs/profiles/"

    # payload = json.dumps({
    #     "itemId": "f7d1f1b9-4415-4ff1-8fee-407b109364aa",
    #     "itemType": "profile",
    #     "properties": {
    #         "lastName": "Galileo",
    #         "preferredLanguage": "en",
    #         "nbOfVisits": 2,
    #         "gender": "male",
    #         "jobTitle": "Vice President",
    #         "lastVisit": "2020-01-31T08:41:22Z",
    #         "j:title": "mister",
    #         "j:about": "<p> Lorem Ipsum dolor sit amet,consectetur adipisicing elit, sed doeiusmod tempor incididunt ut laboreet dolore magna aliqua. Ut enim adminim veniam, quis nostrudexercitation ullamco laboris nisi utaliquip ex ea commodo consequat.Duis aute irure dolor inreprehenderit in coluptate velit essecillum dolore eu fugiat nulla pariatur.Excepteur sint occaecat cupidatatnon proident, sunt in culpa quiofficia deserunt mollit anim id estlaborum.</p> ",
    #         "firstName": "Bill",
    #         "pageViewCount": {
    #             "digitall": 19
    #         },
    #         "emailNotificationsDisabled": "true",
    #         "company": "Acme Space",
    #         "j:nodename": "bill",
    #         "j:publicProperties": "j:about,j:firstName,j:function,j:gender,j:lastName,j:organization,j:picture,j:title",
    #         "firstVisit": "2020-01-30T21:18:12Z",
    #         "phoneNumber": "+1-123-555-12345",
    #         "countryName": "US",
    #         "city": "Las Vegas",
    #         "address": "Hotel Flamingo",
    #         "zipCode": "89109",
    #         "email": "bill@acme.com",
    #         "maritalStatus": "Married",
    #         "birthDate": "1959-08-12T23:00:00.000Z",
    #         "kids": 2,
    #         "age": 60,
    #         "income": 1000000,
    #         "facebookId": "billgalileo",
    #         "twitterId": "billgalileo",
    #         "linkedInId": "billgalileo",
    #         "leadAssignedTo": "Important Manager",
    #         "nationality": "American"
    #     },
    #     "systemProperties": {
    #         "mergeIdentifier": "bill",
    #         "lists": [
    #             "userListId"
    #         ],
    #         "goals": {
    #             "viewLanguagePageGoalTargetReached": "2020-02-10T19:30:31Z",
    #             "downloadGoalExampleTargetReached": "2020-02-10T15:22:41Z",
    #             "viewLandingPageGoalStartReached": "2020-02-10T19:30:27Z",
    #             "downloadGoalExampleStartReached": "2020-02-10T19:30:27Z",
    #             "optimizationTestGoalStartReached": "2020-02-10T19:30:27Z"
    #         }
    #     },
    #     "segments": [
    #         "leads",
    #         "age_60_70",
    #         "gender_male",
    #         "contacts"
    #     ],
    #     "scores": {
    #         "scoring_9": 10,
    #         "scoring_8": 0,
    #         "scoring_1": 10,
    #         "scoring_0": 10,
    #         "_s02s6220m": 0,
    #         "scoring_3": 10,
    #         "_27ir92oa2": 0,
    #         "scoring_2": 10,
    #         "scoring_5": 10,
    #         "scoring_4": 10,
    #         "scoring_7": 10,
    #         "scoring_6": 10,
    #         "_86igp9j1f": 1,
    #         "_ps8d573on": 0
    #     },
    #     "mergedWith": None,
    #     "consents": {
    #         "digitall/newsletter1": {
    #             "scope": "digitall",
    #             "typeIdentifier": "newsletter1",
    #             "status": "GRANTED",
    #             "statusDate": "2019-05-15T14:47:28Z",
    #             "revokeDate": "2021-05-14T14:47:28Z"
    #         },
    #         "digitall/newsletter2": {
    #             "scope": "digitall",
    #             "typeIdentifier": "newsletter2",
    #             "status": "GRANTED",
    #             "statusDate": "2019-05-15T14:47:28Z",
    #             "revokeDate": "2021-05-14T14:47:28Z"
    #         }
    #     }
    # })
    # # headers = {
    # # 'Authorization': 'Basic a2FyYWY6a2FyYWY=',
    # # 'Content-Type': 'application/json'
    # # }

    # response = requests.request("POST", url, auth=basic_auth, data=payload)

    # print(response.text)


@action("eventlist")
@action.uses('eventlist.html')
def eventlist():
    print(request.query)
    sessionid = request.query.sessionid
    if sessionid:
        url = unomi_url+"cxs/profiles/sessions/"+sessionid+"/events/"
        payload = ""
        headers = http_header

        response = requests.request("GET", url, auth=basic_auth, data=payload)
        events = response.text

        eventlist = json.loads(events)
        print(eventlist["list"])
        return dict(eventlist=eventlist["list"])

    else:
        return dict(eventlist=list())


@action("ecommerce")
@action.uses('ecommerce.html')
def ecommerce():
    return dict()

# @action("ecommerce_segment")
# @action.uses('ecommerce_segment.html')
# def ecommerce_segment():
#     return dict()


@action("profilelist")
@action.uses('profilelist.html')
def profilelist():
    url = unomi_url+"cxs/profiles/search/"
    payload = json.dumps({
        "offset": 0,
        "forceRefresh": True,
        "condition": {
            "type": "booleanCondition",
            "parameterValues": {
                "operator": "or",
                "subConditions": [
                    {
                        "type": "profilePropertyCondition",
                        "parameterValues": {
                            "propertyName": "properties.username",
                            "comparisonOperator": "startsWith",
                            "propertyValue": username
                        }
                    },
                    {
                        "type": "profilePropertyCondition",
                        "parameterValues": {
                            "propertyName": "itemId",
                            "comparisonOperator": "exists",
                        }
                    }
                ]
            }
        },
        "limit": -1
    })

    headers = http_header
    print(headers)
    response = requests.request("POST", url, headers=headers, data=payload)

    profilelistjson = response.text
    # print(profilelistjson)
    profilelist = json.loads(profilelistjson)
    print(profilelist["list"])
    return dict(profilelist=profilelist["list"])



@action("profileedit", method=['GET', 'POST'])
@action.uses('profileedit.html')
def profileedit():
    profileid=request.query.get('profileid')
    url = unomi_url+"cxs/profiles/"
    headers = http_header

    from py4web.utils.form import Form, FormStyleDefault, TextareaWidget
    FormStyleDefault.widgets['profile']=TextareaWidget()
    form = Form([
        Field('profile',default='''{
            "itemId":"'''+profileid+'''",
            "itemType":"profile",
            "properties": {
                "firstName": "testfirstname",
                "username":"testusername",
                "email":"testemail",
                "address":"testaddress",
                "city":"ShangHai",
                "zipcode":"250014",
                "interesttag":"music",
                "gender":"male"
            }
        }'''),
        ])
    form.structure.find('[name=profile]')[0]['_class'] = 'textarea'
    form.structure.find('[name=profile]')[0]['_rows'] = '20'

    if form.accepted:
        profile_str=form.vars['profile']
        payload = profile_str
        print(payload)
        result=requests.request("POST", url, headers=headers, data=payload)
        print(result)
        redirect(URL('profileview')+"?profileid="+profileid)
   
    if form.errors:
        print('not accepted')
    return dict(form=form)


@action("profileview")
@action.uses('profileview.html')
def profileview():
    profileid=request.query.get('profileid')
    url = unomi_url+"cxs/profiles/search/"
    
    payload = '''{
        "offset": 0,
        "forceRefresh": "true",
        "condition": {
            "type": "booleanCondition",
            "parameterValues": {
                "operator": "and",
                "subConditions": [
                    {
                        "type": "profilePropertyCondition",
                        "parameterValues": {
                            "propertyName": "itemId",
                            "comparisonOperator": "equals",
                            "propertyValue":"'''+profileid+'''"
                        }
                    }
                ]
            }
        }
    }'''

    headers = http_header
    response = requests.request("POST", url, headers=headers, data=payload)
    profilelistjson=response.text  
    profilelist = json.loads(profilelistjson)
    return dict(profilelist=profilelist["list"])



def profilecountnumber():
    url = unomi_url+"cxs/query/profile/count"

    payload = json.dumps({
        "parameterValues": {
            "subConditions": [
                {
                    "type": "profilePropertyCondition",
                    "parameterValues": {
                        "propertyName": "itemId",
                        "comparisonOperator": "exists"
                    }
                },
                {
                    "type": "profilePropertyCondition",
                    "parameterValues": {
                        "propertyName": "properties.nbOfVisits",
                        "comparisonOperator": "equals",
                        "propertyValueInteger": 1
                    }
                }
            ],
            "operator": "or"
        },
        "type": "booleanCondition"
    })

    headers = http_header

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    return response.text


def profilevisitdate():

    url = unomi_url+"cxs/query/session/timeStamp"

    payload = json.dumps({
        "aggregate": {
            "type": "date",
            "parameters": {
                "interval": "1d",
                "format": "yyyy-MM-dd"
            }
        },
        "condition": {
            "type": "booleanCondition",
            "parameterValues": {
                "operator": "and",
                "subConditions": [
                    {
                        "type": "sessionPropertyCondition",
                        "parameterValues": {
                            "propertyName": "scope",
                            "comparisonOperator": "equals",
                            "propertyValue": "example"
                        }
                    },
                    {
                        "type": "sessionPropertyCondition",
                        "parameterValues": {
                            "propertyName": "profile.properties.nbOfVisits",
                            "comparisonOperator": "equals",
                            "propertyValueInteger": 1
                        }
                    }
                ]
            }
        }
    })
    headers = http_header

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.text


def useragentlist():

    url = unomi_url+"cxs/query/session/properties.userAgentName"

    payload = json.dumps({
        "aggregate": {
            "type": "str"
        },
        "condition": {
            "type": "booleanCondition",
            "parameterValues": {
                "operator": "and",
                "subConditions": [
                    {
                        "type": "sessionPropertyCondition",
                        "parameterValues": {
                            "propertyName": "scope",
                            "comparisonOperator": "equals",
                            "propertyValue": "example"
                        }
                    },
                    {
                        "type": "sessionPropertyCondition",
                        "parameterValues": {
                            "propertyName": "profile.properties.nbOfVisits",
                            "comparisonOperator": "equals",
                            "propertyValueInteger": 1
                        }
                    }
                ]
            }
        }
    })
    headers = http_header

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.text


def getpathlist():

    url = unomi_url+"cxs/query/event/target.properties.path"

    payload = json.dumps({
        "aggregate": {
            "type": "str"
        },
        "condition": {
            "type": "booleanCondition",
            "parameterValues": {
                "operator": "and",
                "subConditions": [
                    {
                        "type": "eventPropertyCondition",
                        "parameterValues": {
                            "propertyName": "scope",
                            "comparisonOperator": "equals",
                            "propertyValue": "example"
                        }
                    }
                ]
            }
        }
    })
    headers = http_header

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.text





@action("segmentlist")
@action.uses('segmentlist.html')
def segmentlist():
    url = unomi_url+"cxs/segments/"
    payload = ""
        # headers = {
        # 'Authorization': 'Basic a2FyYWY6a2FyYWY='
        # }
    response = requests.request("GET", url, auth=basic_auth, data=payload)
    session = response.text

    segmentist = json.loads(session)

    return dict(segmentlist=segmentist)



@action("createsegment", method=['GET', 'POST'])
@action.uses('createsegment.html')
def createsegment():
    url = unomi_url+"cxs/segments/"


    headers = http_header

    from py4web.utils.form import Form, FormStyleDefault, TextareaWidget
    FormStyleDefault.widgets['segment']=TextareaWidget()
    form = Form([
        Field('segment',default='''{
                "metadata":
                {
                    "id":"customer_art_segment",
                    "name":"Customer Interest insight",
                    "scope":"systemscope",
                    "description":"Regroups all Customer that has interested tag",
                    "readOnly": true
                },
                "condition":
                {
                    "type":"profilePropertyCondition",
                    "parameterValues":
                    {
                        "propertyName":"properties.interesttag",
                        "comparisonOperator":"in",
                        "propertyValues": ["music","picture"]
                    }
                }

            }'''),
        ])
    form.structure.find('[name=segment]')[0]['_class'] = 'textarea'
    form.structure.find('[name=segment]')[0]['_rows'] = '20'

    if form.accepted:
        # Do something with form.vars['product_name'] and form.vars['product_quantity']
        segment_str=form.vars['segment']
        print(segment_str)
        payload = segment_str
        print(payload)
        result=requests.request("POST", url, headers=headers, data=payload)
        print(result)
        redirect(URL('segmentlist'))
    if form.errors:
        # display message error
        redirect(URL('not_accepted'))
    return dict(form=form)
