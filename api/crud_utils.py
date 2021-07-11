from api.models import Company, AccessToken, ServiceArea
from api.serializer import GetCompanySerializer, \
    CreateCompanySerializer, LoginCompanySerializer, UpdateCompanySerializer, \
    GetServiceAreaSerializer, CreateServiceAreaSerializer, \
    UpdateServiceAreaSerializer, GeoJsonPointSerializer, \
    shape, json, mapping
from rest_framework import status
import datetime
from api.constants import ACCESS_TOKEN_EXPIRY_TIME


def generate_access_token(data):
    """
    This function is used to generate access token for the API.
    """
    company = Company.objects.get(email=data.get("email"))
    token = AccessToken.objects.create(
        company=company,
        expiry=datetime.datetime.now() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRY_TIME))
    return token.token


def get_companies(query_data=None):
    """
    This function is used to fetch companies
    """
    response = {}
    companies = Company.objects.all()
    response["success"] = True
    status_code = status.HTTP_204_NO_CONTENT
    if companies:
        serializer_obj = GetCompanySerializer(companies, many=True)
        response["data"] = serializer_obj.data
        response["message"] = "Successfully fetched companies"
        status_code = status.HTTP_200_OK
    else:
        response["data"] = None
        response["message"] = "No Companies found"
    return response, status_code


def get_company(company, id):
    """
    This function is used to retrieve a single company
    """
    response = {}
    serializer_obj = GetCompanySerializer(company)
    response["data"] = serializer_obj.data
    response["message"] = "Company fetched"
    response["success"] = True
    status_code = status.HTTP_200_OK
    return response, status_code


def create_company(data):
    """
    This function is used to create a company instance
    """
    response = {}
    status_code = status.HTTP_400_BAD_REQUEST
    serializer_obj = CreateCompanySerializer(data=data)
    if serializer_obj.is_valid():
        serializer_obj.save()
        response["data"] = None
        response["message"] = "Company creation successful"
        response["success"] = True
        status_code = status.HTTP_201_CREATED
    else:
        response["data"] = serializer_obj.errors
        response["message"] = "Company creation failed"
        response["success"] = False
    return response, status_code


def update_company(company, data):
    """
    This function is used to update a company instance
    """
    response = {}
    status_code = status.HTTP_400_BAD_REQUEST
    serializer_obj = UpdateCompanySerializer(company, data=data)
    if serializer_obj.is_valid():
        serializer_obj.save()
        response["data"] = None
        response["message"] = "Company updation successful"
        response["success"] = True
        status_code = status.HTTP_200_OK
    else:
        response["data"] = serializer_obj.errors
        response["message"] = "Company updation failed"
        response["success"] = False
    return response, status_code


def delete_company(company):
    """
    This function is used to delete a company instance
    """
    response = {}
    ServiceArea.objects.filter(company=company).delete()
    company.delete()
    status_code = status.HTTP_200_OK
    response["data"] = None
    response["message"] = "Company deletion successful"
    response["success"] = True
    return response, status_code


def login(data):
    """
    This function is used for company login
    """
    serializer_obj = LoginCompanySerializer(data=data)
    response = {}
    status_code = status.HTTP_401_UNAUTHORIZED
    if serializer_obj.is_valid():
        token = generate_access_token(serializer_obj.validated_data)
        response["data"] = {"access_token": token}
        response["message"] = "Login Successful"
        response["success"] = True
        status_code = status.HTTP_202_ACCEPTED
    else:
        response["data"] = serializer_obj.errors
        response["message"] = "Login Failed"
        response["success"] = False
    return response, status_code


def create_service_area(company, data):
    """
    This function is used for creating service area
    """
    response = {}
    status_code = status.HTTP_400_BAD_REQUEST
    print(data)
    # if data.get('geo_json', None):
    #     data["geo_json"] = json.dumps(data["geo_json"])
    serializer_obj = CreateServiceAreaSerializer(data=data, context={
        "company": company
    })
    if serializer_obj.is_valid():
        serializer_obj.save()
        response["data"] = None
        response["message"] = "Service Area creation successful"
        response["success"] = True
        status_code = status.HTTP_201_CREATED
    else:
        response["data"] = serializer_obj.errors
        response["message"] = "Service Area creation failed"
        response["success"] = False
    return response, status_code


def update_service_area(service_area_id, data, company):
    """
    This function is used to update service area instance
    """
    response = {}
    status_code = status.HTTP_400_BAD_REQUEST
    try:
        service_area = ServiceArea.objects.get(
            id=service_area_id, company=company, is_deleted=False)
        serializer_obj = UpdateServiceAreaSerializer(service_area, data=data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            response["data"] = None
            response["message"] = "Service Area updation successful"
            response["success"] = True
            status_code = status.HTTP_200_OK
        else:
            response["data"] = serializer_obj.errors
            response["message"] = "Service Area updation failed"
            response["success"] = False
    except ServiceArea.DoesNotExist:
        response["data"] = None
        response["message"] = "Service Area updation failed: No such service area"
        response["success"] = False
    except Exception as e:
        print(e)
    return response, status_code


def get_service_area(service_area_id, company):
    """
    This function is used to retrieve a single service area instance
    """
    response = {}
    status_code = status.HTTP_200_OK
    try:
        service_area = ServiceArea.objects.get(
            id=service_area_id, is_deleted=False, company=company)
        serializer_obj = GetServiceAreaSerializer(service_area)
        response["data"] = serializer_obj.data
        response["message"] = "Service Area fetched"
        response["success"] = True
    except ServiceArea.DoesNotExist:
        response["data"] = None
        response["message"] = "Service Area not found"
        response["success"] = False
        status_code = status.HTTP_204_NO_CONTENT
    return response, status_code


def get_service_areas(company):
    """
    This function returns service areas for a company
    """
    response = {}
    service_area = ServiceArea.objects.filter(
        company=company, is_deleted=False)
    if service_area:
        serializer_obj = GetServiceAreaSerializer(service_area, many=True)
        response["data"] = serializer_obj.data
        response["message"] = "Service Area fetched"
        response["success"] = True
        status_code = status.HTTP_200_OK
    else:
        response["data"] = None
        response["message"] = "No Service Areas found"
        response["success"] = False
        status_code = status.HTTP_204_NO_CONTENT
    return response, status_code


def delete_serializer(service_area_id, company):
    """
    This function deletes a service area for a company
    """
    response = {}
    status_code = status.HTTP_200_OK
    try:
        ServiceArea.objects.get(id=service_area_id, company=company).delete()
        response["data"] = None
        response["message"] = "Service Area deletion successful"
        response["success"] = True
    except ServiceArea.DoesNotExist:
        response["data"] = None
        response["message"] = "Service Area not found"
        response["success"] = False
    return response, status_code
