from django.db import models

class Category(models.Model):   
    name = models.CharField(max_length=100, db_index=True)      
    
    #  slag  - конвертация name в url путь для фильтрации
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