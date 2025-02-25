from rest_framework.response import Response
from rest_framework import status


# Response if the action was successsful
def ResponseSuccessful(content, status=status.HTTP_200_OK):
    content = {'detail': content}
    return Response(content, status=status)


def ResponseObject(obj, status=status.HTTP_200_OK):
    return Response(obj, status=status)
    

# Response if the action incurred error
def ResponseError(error=["Something happened"]):
    content = {'error': error}
    return Response(content, status=status.HTTP_400_BAD_REQUEST)    