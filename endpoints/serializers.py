from rest_framework import serializers
from .models import RSS_Feed_Keyowrds,RSS_Feed_Database,RSS_Feed_Name_Icon


class RSS_Feed_KeyowrdsSerializer(serializers.ModelSerializer):
	class Meta:
		model = RSS_Feed_Keyowrds
		fields ='__all__'


class RSS_Feed_DatabaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = RSS_Feed_Database
		fields ='__all__'



class RSS_Feed_Name_IconSerializer(serializers.ModelSerializer):
	class Meta:
		model = RSS_Feed_Name_Icon
		fields ='__all__'