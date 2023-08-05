import re

from drf_yasg.generators import OpenAPISchemaGenerator


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_endpoints(self, request):
        endpoints = super().get_endpoints(request)
        regex = re.compile(r"/api/v1/auth/users/.*")
        for path in list(endpoints):
            if regex.match(path):
                endpoints.pop(path)
        return endpoints
