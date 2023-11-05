from rest_framework import serializers
from .models import user_data

class userSeralizer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    Email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, data):
        specialCharectors = ['!','@','#','$','%','^','&','*']
        special_bool = False
        number_bool = False
        isupper_bool = False
        for i in data['password']:
            if i in specialCharectors:
                special_bool = True
            if str(i).isupper():
                isupper_bool = True
            if str(i).isdigit():
                number_bool = True
        if len(data['password']) > 8 and special_bool and isupper_bool and number_bool:
            pass
        else:
            return 'Invalid password'
        
        if len(data['Email'].split('@')) > 1 and len(data['Email'].split('@')[1].split('.')) > 1:
            pass
        else:
            return 'Invalid Email'
        user_data.objects.create(**data)
        return 'Success'

    def update(self, instance, data):
        specialCharectors = ['!','@','#','$','%','^','&','*']
        special_bool = False
        number_bool = False
        isupper_bool = False
        for i in data['password'].value:
            if i in specialCharectors:
                special_bool = True
            if str(i).isupper():
                isupper_bool = True
            if str(i).isdigit():
                number_bool = True
        if len(data['password'].value) > 7 and special_bool and isupper_bool and number_bool:
            pass
        else:
            return 'Invalid password'
        instance.first_name = data['first_name'].value
        if data['last_name'].value:
            instance.last_name = data['last_name'].value
        if len(data['Email'].value.split('@')) > 1 and len(data['Email'].value.split('@')[1].split('.')) > 1:
            instance.Email = data['Email'].value
        else:
            return 'Invalid Email'
        instance.password = data['password'].value
        instance.save()
        return 'Success'
    
    class Meta:
        model = user_data
        fields = [ 'first_name', 'last_name', 'Email', 'password']