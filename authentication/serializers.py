from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)

    def create(self, validated_data):

        password = validated_data.get("password")
        confirm_password = validated_data.get("confirm_password")

        user = get_user_model()(
            username = validated_data.get("username"),
            email = validated_data.get("email"),
        )

        if password and password == confirm_password:

            user.set_password(password)

        else:

            raise serializers.ValidationError(
                {
                    "password":"Passwords must match.",
                    "confirm_password":"Passwords must match."
                }
            )
        
        request = self.context["request"]

        if request.user.is_staff or request.user.is_superuser:

            user.is_staff = validated_data.get("is_staff", False)

        if request.user.is_superuser:

            user.is_superuser = validated_data.get("is_superuser", False)
        
        user.save()

        return user
    
    def update(self, instance, validated_data):

        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("username", instance.email)

        password = validated_data.get("password")
        confirm_password = validated_data.get("confirm_password")

        if password and password == confirm_password:

            instance.set_password(password)

        elif password and password != confirm_password:

            raise serializers.ValidationError(
                {
                    "password":"Passwords must match.",
                    "confirm_password":"Passwords must match."
                }
            )        

        instance.save()

        return instance

    class Meta:

        model = get_user_model()
        fields = ["username", "email", "password", "confirm_password", "is_staff", "is_superuser"]
        extra_kwargs = {
            "is_superuser":{
                "write_only": True
            }
        }