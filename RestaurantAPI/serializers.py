from django.utils import timezone
from .models import (MenuItem,Category,OrderItem,Order,ReservationItem,Reservation,Rating)
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),write_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id',
            'name',
            'price',
            'description',
            'category',
            'category_id',
        ]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = [
            'id',
            'user',
            'menu_item',
            'created_at',
            'score',
            'comment',
        ]
        read_only_fields = [
            'created_at',
            'user'
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all(),write_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'menu_item',
            'menu_item_id',
            'quantity',
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'total_price',
            'items',
            'created_at',
            'user',
            'status',
            'delivery_address'
        ]
        read_only_fields = [
            'created_at',
            'user',
            'status',
            'total_price',
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        total_order_price = 0
        order = Order.objects.create(user=user,total_price=0,**validated_data)
        for item in items_data:
            menu_item = item['menu_item_id']
            quantity = item['quantity']
            item_price = menu_item.price
            item_total_price = item_price * quantity
            total_order_price += item_total_price
            OrderItem.objects.create(order=order,menu_item=menu_item,quantity=quantity,item_price=item_price,total_price=item_total_price)
        order.total_price = total_order_price
        order.save()
        return order

class ReservationItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all(),write_only=True)

    class Meta:
        model = ReservationItem
        fields = [
            'id',
            'menu_item',
            'menu_item_id',
            'quantity',
        ]

class ReservationSerializer(serializers.ModelSerializer):
    items = ReservationItemSerializer(many=True)
    class Meta:
        model = Reservation
        fields = [
            'id',
            'user',
            'created_at',
            'requested_at',
            'note',
            'items',
            'guests_count'
        ]
        read_only_fields = [
            'created_at',
            'user',
        ]

    def validate_requested_at(self, value):
        request = self.context['request']
        if value < timezone.now():
            raise serializers.ValidationError('you can only reserve for future times!')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        reservation = Reservation.objects.create(user=user,**validated_data)
        for item in items_data:
            menu_item = item['menu_item_id']
            quantity = item['quantity']
            ReservationItem.objects.create(reservation=reservation,menu_item=menu_item,quantity=quantity)

        return reservation