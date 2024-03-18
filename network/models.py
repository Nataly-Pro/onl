from django.db import models


class NetworkObject(models.Model):

    NETWORK_OBJECT_TYPES = (
        ('factory', 'завод'),
        ('retail', 'розничная сеть'),
        ('entrepreneur', 'ИП'),
    )

    object_type = models.CharField(max_length=12, choices=NETWORK_OBJECT_TYPES,
                                   verbose_name='тип объекта')
    name = models.CharField(max_length=128, verbose_name='название')
    create_date = models.DateTimeField(auto_now_add=True,
                                       verbose_name='время создания')

    email = models.EmailField(unique=True)
    country = models.CharField(max_length=128, verbose_name='страна')
    city = models.CharField(max_length=128, verbose_name='город')
    street = models.CharField(max_length=128, verbose_name='улица')
    bld = models.CharField(max_length=10, verbose_name='номер дома')

    supplier = models.ForeignKey('self', on_delete=models.CASCADE,
                                 verbose_name='поставщик',
                                 null=True, blank=True)
    debt = models.DecimalField(max_digits=10, decimal_places=2,
                               verbose_name='задолженность перед поставщиком',
                               null=True, blank=True)
    hierarchy = models.IntegerField(default=0, verbose_name='уровень иерархии')

    @property
    def products(self):
        return self.supplier.product_set.all()

    def __str__(self):
        return f'{self.object_type} {self.name}'

    class Meta:
        verbose_name = 'объект сети'
        verbose_name_plural = 'объекты сети'
        ordering = ('id',)


class Product(models.Model):
    product_name = models.CharField(max_length=128,
                                    verbose_name='название продукта')
    model = models.CharField(max_length=128, verbose_name='модель')
    release_date = models.DateField(verbose_name='дата выхода на рынок')
    suppliers = models.ManyToManyField('NetworkObject')

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('id',)
