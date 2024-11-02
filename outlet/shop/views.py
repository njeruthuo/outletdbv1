from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import Shop, ShopSerializer


class ShopAPIView(APIView):
    def get(self, request, *args, **kwargs):
        shops = Shop.objects.all()
        shop_serializer = ShopSerializer(shops, many=True).data
        return Response(shop_serializer, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Combine request data and files into a single data dictionary
        data = request.data.copy()
        if 'licenses' in request.FILES:
            data['licenses'] = request.FILES['licenses']

        print(data.get('licenses'), 'data')

        # Initialize the serializer with the combined data
        serializer = ShopSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Successfully created the shop"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


shop_api_view = ShopAPIView.as_view()
