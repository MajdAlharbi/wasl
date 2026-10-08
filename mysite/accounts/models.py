from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class VisitorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="visitor_profile",
    )
    available_minutes = models.PositiveIntegerField(
        default=60,
        validators=[MinValueValidator(1)],
        verbose_name="الوقت المتاح بالدقائق",
    )
    use_sign_language = models.BooleanField(
        default=False,
        verbose_name="عرض المحتوى بلغة الإشارة",
    )
    show_captions = models.BooleanField(
        default=True,
        verbose_name="إظهار النص المكتوب مع المحتوى",
    )
    use_text_to_speech = models.BooleanField(
        default=False,
        verbose_name="تحويل أسئلتي المكتوبة إلى صوت",
    )

    def __str__(self):
        return f"ملف {self.user.username}"
