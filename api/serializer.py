from rest_framework import serializers
from api.utilities import encrypt_password, verify_encrypted_password
from api.models import Company, ServiceArea
from api.constants import LANGUAGES, CURRENCIES
import json
from shapely.geometry import mapping, shape, polygon, point


class CreateCompanySerializer(serializers.Serializer):
    """
    This class serializes a Company at Company instance creation
    """
    name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    language = serializers.ChoiceField(choices=LANGUAGES)
    currency = serializers.ChoiceField(choices=CURRENCIES)
    password = serializers.CharField()

    def validate(self, attrs):
        password = attrs.get("password", None)
        if password:
            attrs["password"] = encrypt_password(password)
        return attrs

    def create(self, validated_data):
        return Company.objects.create(**validated_data)


class LoginCompanySerializer(serializers.Serializer):
    """
    This class is used to serialize a Company's details
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        try:
            company = Company.objects.get(
                email=attrs.get("email"))
        except Company.DoesNotExist:
            raise serializers.ValidationError("Company doesn't exists")
        if not verify_encrypted_password(attrs.get("password"), company.password):
            raise serializers.ValidationError(
                "Invalid details")
        return attrs


class GetCompanySerializer(serializers.ModelSerializer):
    """
    This class is used to get a company instance
    """
    class Meta:
        model = Company
        exclude = ('password', 'created_at', 'updated_at',)


class UpdateCompanySerializer(serializers.Serializer):
    """
    This class is used to update a Company instance
    """
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    language = serializers.ChoiceField(required=False, choices=LANGUAGES)
    currency = serializers.ChoiceField(required=False, choices=CURRENCIES)
    password = serializers.CharField(required=False)

    def validate(self, attrs):
        password = attrs.get("password", None)
        if password:
            attrs["password"] = encrypt_password(password)
        return attrs

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)
        instance.password = validated_data.get('password', instance.password)
        instance.language = validated_data.get('language', instance.language)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.save()
        return instance


class CreateServiceAreaSerializer(serializers.Serializer):
    """
    This class is used to serialize a ServiceArea at instance creation
    """
    name = serializers.CharField()
    price = serializers.FloatField()
    geo_json = serializers.JSONField()

    def validate(self, attrs):
        company = self.context.get("company", None)
        if company:
            attrs["company_id"] = company.id
        else:
            raise serializers.ValidationError("Company not provided")
        try:
            s_polygon = shape(json.loads(
                attrs.get("geo_json", None)).get("geometry", None))
            if isinstance(s_polygon, polygon.Polygon):
                attrs["geo_json"] = mapping(s_polygon)
            else:
                raise TypeError()
        except (TypeError, ValueError, json.JSONDecodeError):
            raise serializers.ValidationError("Invalid geo_json polygon")
        return attrs

    def create(self, validated_data):
        return ServiceArea.objects.create(**validated_data)


class GetServiceAreaSerializer(serializers.ModelSerializer):
    """
    This class is used to get an instance of a ServiceArea
    """
    class Meta:
        model = ServiceArea
        exclude = ('created_at', 'updated_at',)


class UpdateServiceAreaSerializer(serializers.Serializer):
    """
    This class is used to update a ServiceArea instance
    """
    name = serializers.CharField(required=False)
    price = serializers.FloatField(required=False)
    geo_json = serializers.JSONField(required=False)

    def validate(self, attrs):
        if attrs.get('geo_json', None):
            try:
                s_polygon = shape(json.loads(
                    attrs.get("geo_json")).get("geometry", None))
                attrs["geo_json"] = mapping(s_polygon)
            except (TypeError, ValueError, json.JSONDecodeError):
                raise serializers.ValidationError("Invalid geo_json polygon")
        return attrs

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.geo_json = validated_data.get('geo_json', instance.geo_json)
        instance.save()
        return instance


class GeoJsonPointSerializer(serializers.Serializer):
    """
    This class is used to serialize geo_json point
    """
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    point = serializers.SerializerMethodField()

    # noinspection PyMethodMayBeStatic
    def get_point(self, attrs):
        try:
            return point.Point(attrs['longitude'], attrs['latitude'])
        except (TypeError, ValueError):
            raise serializers.ValidationError("Invalid geo_json point")
