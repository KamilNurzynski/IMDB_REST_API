from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewListThrottle, ReviewCreateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.api.pagination import WatchListPagination, WatchListWithLimitOffsetPagination, \
    WatchListCursorPagination
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins, generics
from rest_framework.exceptions import ValidationError
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly


# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         try:
#             movies = Movie.objects.all()
#         except Movie.DoesNotExist:
#             return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     username = self.kwargs['username'] # pobiera z adresu url
    #     return Review.objects.filter(author__username=username)

    """
    przez użycie query_params.get() url będzie wyglądał tak: 
    path('reviews/', views.UserReview.as_view(), name='user_review_details')
    """

    def get_queryset(self):
        # inna metoda pobierania danych z url(jeśli nie ma to None)
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(author__username=username)
        # if username is not None:
        #     queryset = queryset.filter(author__username=username)
        # return queryset


class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    throttle_classes = [ReviewCreateThrottle]

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        author = self.request.user  # pobiera pytającego usera
        author_queryset = Review.objects.filter(watchlist=watchlist, author=author)
        if author_queryset:  # lub if quthor_queryset.exists()
            raise ValidationError("You have already reviewed this watch!")
        if watchlist.number_of_ratings == 0:
            watchlist.avg_rating = serializer.validated_data['rating']  # wprowadzana dana
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2
        watchlist.number_of_ratings += 1
        watchlist.save()
        serializer.save(watchlist=watchlist, author=author)


# poniżej usuniemy klasę Create, bo może rodzić to błędy,
#  gdy będzie dodawany nowy review i moglby zostac wpisace inne id watchlist
class ReviewList(generics.ListAPIView):
    # normalnie by wystarczył ale my chcemy do id fimu wyświetlać wszystkie reviews dla niego
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [ReviewListThrottle]

    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)  # or watchlist_id=pk


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # poniżej działą podobnie jak custom throttle classes ale nie trzeba tworzyć nowego pliku throttling.py
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'  # działą z importowanym ScopedRateThrottle.


# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class ReviewDetail(mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


class WatchListView(generics.ListAPIView):
    # normalnie by wystarczył ale my chcemy do id fimu wyświetlać wszystkie reviews dla niego
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer

    # pagination_class = WatchListPagination
    # pagination_class = WatchListWithLimitOffsetPagination
    pagination_class = WatchListCursorPagination

    # w url:  ?search=
    # filter_backends = [filters.SearchFilter]  ## search nie patrzy na wielkosc liter i na spacje
    # search_fields = ['^title', 'stream_platform__name']  # ^title - title startswith...
    # w url:   ?ordering=
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']  # w URL:

    # w url:   ?title=coś&stream_platform=coś
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'stream_platform__name']  # nie trzeba wszystkich wpisywać w URL


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        try:
            movies = WatchList.objects.all()
        except WatchList.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailsAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
            serializer = WatchListSerializer(movie)
            return Response(serializer.data)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        try:
            stream_platforms = StreamPlatform.objects.all()
        except StreamPlatform.DoesNotExist():
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        # poniżej contex dodany, żeby można było użyć hyperLinkRelatedField w serializers.py
        #
        serializer = StreamPlatformSerializer(stream_platforms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailsAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            stream_platform = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializer(stream_platform)
            return Response(serializer.data)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        stream_platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(stream_platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        stream_platform = StreamPlatform.objects.get(pk=pk)
        stream_platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
