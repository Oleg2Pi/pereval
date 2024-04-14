from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import PerevalSerializer, PerevalListSerializer


class PerevalCreateViewset(viewsets.ModelViewSet):
    '''Создание перевала'''

    queryset = PerevalModel.objects.filter(id=0)
    serializer_class = PerevalSerializer

    def create(self, request, *args, **kwargs):

        serializer = PerevalSerializer(data=request.data)
        response_data = {}

        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status': 200,
                'message': '',
                'id': serializer.data.get('id')
            }

        elif status.HTTP_500_INTERNAL_SERVER_ERROR:
            response_data = {
                'status': 500,
                'message': 'Ошибка подключения к базе данных',
                'id': serializer.data.get('id')
            }

        elif status.HTTP_400_BAD_REQUEST:
            response_data = {
                'status': 400,
                'message': 'Неверный запрос',
                'id': serializer.data.get('id')
            }

        return Response(response_data)
    

class PerevalUpdateViewset(viewsets.ModelViewSet):
    """Обновление данных перевала"""

    queryset = PerevalModel.objects.all().order_by('id')
    serializer_class = PerevalSerializer

    def partial_update(self, request, *args, **kwargs):

        pereval = self.get_object()
        serializer = PerevalSerializer(pereval, data=request.data, partial=True)

        if request.data['status'] == 'New':
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 1,
                    'message': 'Данные успешно изменены',
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'status': 0,
                    'message': 'Данные о пользователе нельзя изменять',
                }
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        else:
            response_data = {
                'status': 0,
                'message': 'Изменение отклонено. Данные проходят проверку модератором',
            }
            return Response(response_data, status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)


class PerevalUserListViewset(APIView):
    """Вывод списка перевалов, добавленных пользователем"""

    def get(self, request, email):
        perevals = PerevalModel.objects.filter(user__email=email).order_by('id')
        serializer = PerevalListSerializer(perevals, many=True)

        return Response(serializer.data)