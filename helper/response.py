from rest_framework.response import Response
from rest_framework import status


def response_200(data=None, page_info=None, message=None):
    response = dict(success=True)

    if message is not None:
        response['message'] = message

    if data is not None:
        response['data'] = data

    if page_info is not None:
        response['page_info'] = page_info

    return Response(response, status=status.HTTP_200_OK)


def response_201(data=None, page_info=None, message=None):
    response = dict(success=True)

    if message is not None:
        response['message'] = message

    if data is not None:
        response['data'] = data

    if page_info is not None:
        response['page_info'] = page_info

    return Response(response, status=status.HTTP_201_CREATED)


def response_400(error='Bad request'):
    return Response(
        data=dict(success=False, message=error),
        status=status.HTTP_400_BAD_REQUEST,
    )


def response_401(error='Unauthorized'):
    return Response(
        data=dict(success=False, message=error), 
        status=status.HTTP_401_UNAUTHORIZED,
    )


def response_403(error='Forbidden'):
    return Response(
        data=dict(success=False, message=error), 
        status=status.HTTP_403_FORBIDDEN,
    )


def response_404(error='Not found'):
    return Response(
        data=dict(success=False, message=error), 
        status=status.HTTP_404_NOT_FOUND,
    )


