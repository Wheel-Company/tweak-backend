from rest_framework import serializers

class GrammarCorrectionSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, help_text="Text to correct")