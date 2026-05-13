from rest_framework import serializers
from .models import Item, StockTransaction, Borrowing, Task, TaskItem

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class StockTransactionSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source='item.name')
    
    class Meta:
        model = StockTransaction
        fields = ['id', 'item', 'item_name', 'type', 'quantity', 'remarks', 'timestamp']

class BorrowingSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source='item.name')
    
    class Meta:
        model = Borrowing
        fields = ['id', 'item', 'item_name', 'borrower_name', 'quantity', 'date_borrowed', 'return_date', 'status']

class TaskItemSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source='item.name')
    
    class Meta:
        model = TaskItem
        fields = ['item', 'item_name', 'quantity']

class TaskSerializer(serializers.ModelSerializer):
    items = TaskItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_by', 'created_at', 'items']
