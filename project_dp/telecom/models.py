from django.db import models


class Operator(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    inn = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class PhoneNumber(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.IntegerField()
    start_range = models.BigIntegerField()
    end_range = models.BigIntegerField()
    capacity = models.IntegerField()
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    region = models.TextField()

    class Meta:
        unique_together = (('code', 'start_range', 'end_range'),)

    def __str__(self):
        return f"{self.code} {self.start_range}-{self.end_range}"
