import requests
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


def forward_request(base_url, path, method, headers, data=None, files=None, params=None):
    url = f'{base_url}{path}'
    forward_headers = {}
    if 'Authorization' in headers:
        forward_headers['Authorization'] = headers['Authorization']
    if 'Content-Type' in headers and not files:
        forward_headers['Content-Type'] = headers['Content-Type']

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=forward_headers,
            data=data,
            files=files,
            params=params,
            timeout=30,
        )
        return HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'application/json'),
        )
    except requests.RequestException as exc:
        return HttpResponse(
            content=f'{{"error": "Service unavailable: {str(exc)}"}}',
            status=503,
            content_type='application/json',
        )


@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def auth_proxy(request, path=''):
    base = settings.SERVICE_URLS['auth']
    mapped = settings.AUTH_ROUTE_MAP.get(path, f'/api/{path}')
    return forward_request(base, mapped, request.method, request.headers, request.body)


@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def groups_proxy(request, path=''):
    base = settings.SERVICE_URLS['groups']
    target = f'/api/groups/{path}' if path else '/api/groups'
    return forward_request(base, target, request.method, request.headers, request.body, params=request.GET)


@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def bills_proxy(request, path=''):
    base = settings.SERVICE_URLS['bills']
    target = f'/api/bills/{path}' if path else '/api/bills'
    return forward_request(base, target, request.method, request.headers, request.body, params=request.GET)


@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def settlement_proxy(request, path=''):
    base = settings.SERVICE_URLS['settlement']
    target = f'/api/settlement/{path}'
    return forward_request(base, target, request.method, request.headers, request.body)


@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def receipt_proxy(request, path=''):
    base = settings.SERVICE_URLS['receipt']
    target = f'/api/receipt/{path}'
    if request.method == 'POST' and request.FILES:
        files = {}
        for key in request.FILES:
            f = request.FILES[key]
            files[key] = (f.name, f.read(), f.content_type)
        return forward_request(base, target, request.method, request.headers, files=files)
    return forward_request(base, target, request.method, request.headers, request.body)


@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def notifications_proxy(request, path=''):
    base = settings.SERVICE_URLS['notifications']
    if path == 'notify' or path.startswith('notify'):
        target = '/api/notify'
    else:
        target = f'/api/{path}' if path else '/api/notifications'
    return forward_request(base, target, request.method, request.headers, request.body, params=request.GET)
