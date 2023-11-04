from rest_framework import serializers
from api.models import Note
class GrammarCorrectionSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, help_text="Text to correct")

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'  # Include all fields from the Note model