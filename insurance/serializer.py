from rest_framework import serializers
from django.contrib.auth.models import User
from .models import User,Company,Policy,Claim,Payment

# from .models import user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwagrs = {'password':{'write_only':True}}
    #making token
    def create(self, validated_data):
        isinstance = self.Meta.model(**validated_data)
        password = validated_data.pop('password',None)
        if password is not None:
            isinstance.set_password(password)
            isinstance.save()
            return isinstance



class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

