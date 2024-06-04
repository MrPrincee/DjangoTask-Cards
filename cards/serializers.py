from .models import Card
from rest_framework import serializers


class CardSerializer(serializers.ModelSerializer):
    ccv = serializers.IntegerField(write_only=True)
    card_number = serializers.CharField(write_only=True)

    class Meta:
        model = Card
        fields = ['ccv', 'card_number', 'user', 'title']

    def validate_ccv(self, value):
        if value < 100 or value > 999:
            raise serializers.ValidationError("CCV should be between 100-999!")
        return value

    def validate_card_number(self, value):
        if len(value) != 16:
            raise serializers.ValidationError("Card Number must be a 16 digit")
        elif not value.isdigit():
            raise serializers.ValidationError("You can use [0-9] only!")
        return value

    def create(self, validated_data):
        card_number = validated_data.pop('card_number')
        ccv = validated_data.pop('ccv')

        if card_number is None or ccv is None:
            raise serializers.ValidationError("Card number and CCV are required!!")

        if not isinstance(card_number, str) or len(card_number) != 16:
            raise serializers.ValidationError("Card number must be a 16-digit string!!")

        censored_number = card_number[:4] + '********' + card_number[-4:]
        validated_data['censored_number'] = censored_number

        for i in range(0, 16, 4):
            first_number = int(card_number[i:i + 2])
            second_number = int(card_number[i + 2:i + 4])

            validation = pow(first_number, pow(second_number, 3))

            if ccv == 0 or validation % ccv == 1:
                raise serializers.ValidationError("Card is not Valid!!")

        validated_data['is_valid'] = True

        card = super().create(validated_data)
        print(card)
        card.save()

        return card
