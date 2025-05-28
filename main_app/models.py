from django.db import models

class DirectionMod(models.Model):
    name = models.CharField(max_length=100, verbose_name="Yo'nalishlar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Yo'nalish"
        verbose_name_plural = "Yo'nalishlar"

class TeachersMod(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="Ismi")
    direction = models.ForeignKey(to=DirectionMod, on_delete=models.SET_NULL, null=True, verbose_name="Yo'nalishi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    
    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "O'qituvchi"
        verbose_name_plural = "O'qituvchilar"

class GroupsMod(models.Model) :
    name = models.CharField(max_length=50, verbose_name="Guruh nomi")
    teacher = models.ForeignKey(to=TeachersMod, on_delete=models.SET_NULL, null=True, verbose_name="Guruh o'qituvchisi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    def __str__(self):
        return self.name

    class Meta : 
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"

class QuestionMod(models.Model) :
    question = models.TextField(verbose_name="Savollar")
    answer_A = models.CharField(max_length=255, verbose_name="A Javob")
    answer_B = models.CharField(max_length=255, verbose_name="B Javob")
    answer_C = models.CharField(max_length=255, verbose_name="c Javob")
    answer_D = models.CharField(max_length=255, verbose_name="D Javob")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    def __str__(self):
        return self.question

    class Meta :
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"

class UsersMod(models.Model) :
    user_id = models.IntegerField(verbose_name="Foydlanuvchi ID")
    full_name = models.CharField(max_length=100, verbose_name="Ismi")
    direction = models.ForeignKey(to=DirectionMod, on_delete=models.SET_NULL, null=True, verbose_name="Yo'nalishi")
    teacher = models.ForeignKey(to=TeachersMod, on_delete=models.CASCADE, verbose_name="O'qituvchi", null=True)
    group_name = models.CharField(max_length=50, verbose_name="Guruh nomi", blank=True)
    day_type = models.CharField(max_length=30, verbose_name="Dars kunlari", blank=True)
    start_class_time = models.TimeField(verbose_name="Dasr boshlanish vaqti")
    balance = models.IntegerField(default=0, verbose_name="Hisob")
    quiz_sent_today = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    def __str__(self):
        return self.full_name
    
    class Meta :
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

class UserAnswersMod(models.Model) :
    CHOICES = [
        ('--', '--'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    ]
    user = models.ForeignKey(to=UsersMod, on_delete=models.SET_NULL, verbose_name="Foydalanuvchi", null=True)
    question = models.ForeignKey(to=QuestionMod, on_delete=models.SET_NULL, null=True, verbose_name="Savol")
    answer_A = models.CharField(max_length=255, verbose_name="A Javob")
    answer_B = models.CharField(max_length=255, verbose_name="B Javob")
    answer_C = models.CharField(max_length=255, verbose_name="C Javob")
    answer_D = models.CharField(max_length=255, verbose_name="D Javob")
    answer = models.CharField(max_length=255, choices=CHOICES, default="--", verbose_name="Tanlagan javobi")
    comment = models.TextField(verbose_name="O'quvchi taklifi", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = "Yaratilgan vaqt")

    def __str__(self):
        return f"{self.comment}"
    
    class Meta :
        verbose_name = "Foydalanuvchi javobi"
        verbose_name_plural = "Foydalanuvchi javoblari"

class RewardsMod(models.Model) :
    amount = models.IntegerField(verbose_name="Mukofot summasi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    def __str__(self):
        return f"{self.amount}"
    
    class Meta :
        verbose_name = "Mukofot"
        verbose_name_plural = "Mukofot summasi"

