import os

from django.core.files.storage import FileSystemStorage
from PIL import Image
from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from product.models import Product
from product.serializers.product import ProductSerializer


class ProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class ProductDetails(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class ProductDefaultImage(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.FILES.get("image"):
            upload = request.FILES["image"]
            try:
                im = Image.open(upload)
                im.verify()
            except Exception as e:
                raise serializers.ValidationError({"ERROR": "Upload data is not image"})
            fss = FileSystemStorage()
            folder_path = "/product/defaults/"
            # check if the folder path exists, and create it if it doesn't
            if not os.path.exists(fss.base_location + folder_path):
                os.makedirs(fss.base_location + folder_path)
            # delete all files in the folder
            folder_path = "product/defaults/"
            for file_name in fss.listdir(folder_path)[1]:
                fss.delete(f"{folder_path}{file_name}")
            # save the new uploaded file
            file = fss.save(f"{folder_path}{upload.name}", upload)
            return Response({"status": "success"}, status.HTTP_201_CREATED)
        return Response({"status": "failure"}, status.HTTP_400_BAD_REQUEST)
