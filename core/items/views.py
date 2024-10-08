import logging
from rest_framework import generics, status
from .models import Item
from .serializers import ItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from django.core.cache import cache


logger = logging.getLogger('inventory')


class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logger.info('Fetching all Items')
        items = self.queryset.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        logger.info('Creating a new Item.')
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            item = serializer.save()
            logger.info(f'Item created: {item}')
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            logger.error(f'Error creating item: {serializer.errors}')
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        item_id = self.kwargs['item_id']

        cached_item = cache.get(f'item_{item_id}')
        if cached_item:
            logger.info('Returning cached item')
            return Response(cached_item)

        try:
            item = self.queryset.filter(pk=item_id).first()
            serializer = self.serializer_class(item)
            logger.info(f'Fetched item with id: {item_id}')

            cache.set(f'item_{item_id}', serializer.data, timeout=3600*2)
            logger.info(f'Caching item with id: {item_id}')
            return Response(serializer.data, status.HTTP_200_OK)

        except Item.DoesNotExist:
            logger.error(f'Item with id {item_id} not found.')
            raise NotFound(detail='Item not found', code=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        item_id = self.kwargs['item_id']
        try:
            item = self.queryset.filter(pk=item_id).first()
            serializer = self.serializer_class(item, data=request.data)

            if serializer.is_valid():
                updated_item = serializer.save()
                logger.info(f'Updated Item with id: {item_id}')
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                logger.error(f'Error updating item: {serializer.errors}')
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            logger.error(f'Item with id {item_id} not found.')
            raise NotFound(detail='Item not found', code=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        item_id = self.kwargs['item_id']
        try:
            item = self.queryset.filter(pk=item_id).first()
            item.delete()
            logger.info(f'Deleted Item with id: {item_id}')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            logger.error(f'Item with id {item_id} not found.')
            raise NotFound(deta='Item not found', code=status.HTTP_404_NOT_FOUND)
