from django.db import models
from django.urls import reverse

class Category(models.Model):   
    name = models.CharField(max_length=100, db_index=True)      
    
    #  slug  - конвертация name в url путь для фильтрации
    slug = models.CharField(max_length=100, unique=True)   
    
    
    # внутренний класс в модели, для метаданных и настройки поведения модели
    class Meta:    
        # сортировка - упорядочивание записей ( по умолчанию - по дате создания )
        ordering = ('name',) 
                
        # человекочитаемые имена для админки Django
        verbose_name = 'Категория' 
        verbose_name_plural = "Категории"

    # метод отображения объекта в админке (в данном случае по имени name)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("main:product_list_by_category", args=[self.slug])
    
    
    
class Product(models.Model):
    # наследуем класс Category, чтобы добавленные продукты 
    # были сгруппированы в соответствующуюся категорию
    # ForeignKey = наследование от класса Category
    # related_name = явное имя для обращения к полю
    # CASCADE = позволяет удалить все записи относящиеся к родительскому классу
    category = models.ForeignKey(Category, related_name="products", 
                                 on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100, db_index=True)
    slug = models.CharField(max_length=100, unique=100)
    
    # upload_to - путь хранения фотографии вместе с указанием даты
    # blank  = True - позволяет полю быть пустым ( null = true ) 
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    
    # decimal_places = количество чисел после запятой
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  
    
    class Meta:
        ordering = ('name', )
        
        verbose_name = 'Продукт' 
        verbose_name_plural = "Продукты"
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.id, self.slug])
    