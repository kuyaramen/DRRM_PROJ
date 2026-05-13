from django.contrib import admin
from .models import Item, StockTransaction, Borrowing, ActivityLog, Task, TaskItem

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'category', 'quantity', 'status')
    list_filter = ('category', 'status')
    search_fields = ('name', 'barcode')

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ('item', 'type', 'quantity', 'timestamp', 'user')
    list_filter = ('type', 'timestamp')

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('item', 'borrower_name', 'quantity', 'date_borrowed', 'status')
    list_filter = ('status', 'date_borrowed')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('timestamp',)

class TaskItemInline(admin.TabularInline):
    model = TaskItem
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [TaskItemInline]
