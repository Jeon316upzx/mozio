from rest_framework.views import APIView
from rest_framework.response import Response
from api import crud_utils as utils
from api import permissions


class CompanyLogin(APIView):
    def post(self, request):
        """
        This API is used to login a company
        """
        (response, status_code) = utils.login(request.data)
        return Response(response, status=status_code)


class CompanyCreate(APIView):
    def post(self, request):
        """
        This API is used to create a new company instance
        """
        (response, status_code) = utils.create_company(request.data)
        return Response(response, status=status_code)


class CompanyGPDP(APIView):
    """
    This APIVIew has single retrieve, update and delete methods
    """
    permission_classes = (permissions.CompanyPermission,)

    def get(self, request):
        """
        This API is used to retrieve single company instance
        """
        (response, status_code) = utils.get_company(request.user)
        return Response(response, status=status_code)

    def put(self, request):
        """
        This API is used to update a company instance
        """
        (response, status_code) = utils.update_company(request.user, request.data)
        return Response(response, status=status_code)

    def delete(self, request):
        """
        This API is used to delete a company instance
        """
        (response, status_code) = utils.delete_company(request.user)
        return Response(response, status=status_code)


class CompanyGP(APIView):
    """
    This APIView has retrieve multiple company instances and login
    """

    permission_classes = (permissions.CompanyPermission,)

    def get(self, request):
        """
        This API is used to retieve multiple company instances
        """
        (response, status_code) = utils.get_companies()
        return Response(response, status=status_code)


class ServiceAreaPG(APIView):
    """
    This APIView has create and multiple instance retrive methods
    """
    permission_classes = (permissions.CompanyPermission,)

    def post(self, request):
        """
        This API is used to create a new company instance
        """
        (response, status_code) = utils.create_service_area(
            request.user, request.data)
        return Response(response, status=status_code)

    def get(self, request):
        """
        This API is used to retieve multiple service area instances of a company
        """
        (response, status_code) = utils.get_service_areas(request.user)
        return Response(response, status=status_code)


class ServiceAreaGPD(APIView):
    """
    This APIVIew has single retrieve, update and delete methods
    """
    permission_classes = (permissions.CompanyPermission,)

    def get(self, request, service_area_id):
        """
        This API is used to retrieve single service area instance
        """
        (response, status_code) = utils.get_service_area(
            service_area_id, request.user)
        return Response(response, status=status_code)

    def put(self, request, service_area_id):
        """
        This API is used to update a service area instance
        """
        (response, status_code) = utils.update_service_area(
            service_area_id, request.data, request.user)
        return Response(response, status=status_code)

    def delete(self, request, service_area_id):
        """
        This API is used to delete a service instance
        """
        (response, status_code) = utils.delete_serializer(
            service_area_id, request.user)
        return Response(response, status=status_code)
