# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import six

from rest_framework.settings import api_settings
from rest_framework import fields

from shop.money import Money


class AmountField(fields.FloatField):
    """
    Serializer field for bidirectional exchange of Money amounts. Internally the serialized
    amount is converted to a float without currency symbol and hence suitable to be used in
    input fields.
    """
    def to_representation(self, obj):
        return float(obj)

    def to_internal_value(self, data):
        if isinstance(data, six.text_type) and len(data) > self.MAX_STRING_LENGTH:
            self.fail('max_string_length')

        try:
            return Money(data)
        except (TypeError, ValueError):
            self.fail('invalid')


class FileField(fields.FileField):
    def to_internal_value(self, data):
        # try:
        #     # `UploadedFile` objects should have name and size attributes.
        #     file_name = data.name
        #     file_size = data.size
        # except AttributeError:
        #     self.fail('invalid')
        #
        # if not file_name:
        #     self.fail('no_name')
        # if not self.allow_empty_file and not file_size:
        #     self.fail('empty')
        # if self.max_length and len(file_name) > self.max_length:
        #     self.fail('max_length', max_length=self.max_length, length=len(file_name))
        return data

    def to_representation(self, value):
        use_url = getattr(self, 'use_url', api_settings.UPLOADED_FILES_USE_URL)

        if not value:
            return None

        if use_url:
            if not getattr(value, 'url', None):
                # If the file has not been saved it may not have a URL.
                return None
            url = value.url
            request = self.context.get('request', None)
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return value.name


class ImageField(fields.ImageField):
    def to_internal_value(self, data):
        return data


class TextField(fields.CharField):
    pass