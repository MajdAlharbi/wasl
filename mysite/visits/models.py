from django.db import models
from django.conf import settings


class Goal(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Booth(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    goals = models.ManyToManyField(
        Goal,
        related_name="booths",
        blank=True,
    )
    visit_duration = models.PositiveIntegerField(default=15)

    has_sign_language = models.BooleanField(
        default=False,
        verbose_name="يتوفر محتوى بلغة الإشارة",
    )
    has_captions = models.BooleanField(
        default=False,
        verbose_name="يتوفر نص مكتوب للمحتوى",
    )
    content_text = models.TextField(
        blank=True,
        verbose_name="النص المكتوب لمحتوى البوث",
    )

    def __str__(self):
        return self.name


class VisitorGoal(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="visitor_goals",
    )
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name="visitor_goals",
    )
    priority = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["priority", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "goal"],
                name="unique_user_goal",
            ),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.goal.name}"


class VisitPlan(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="visit_plan",
    )

    def __str__(self):
        return f"خطة {self.user.username}"


class PlanItem(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planned", "مخطط"
        VISITED = "visited", "تمت زيارته"
        SKIPPED = "skipped", "تم تخطيه"

    plan = models.ForeignKey(
        VisitPlan,
        on_delete=models.CASCADE,
        related_name="items",
    )
    booth = models.ForeignKey(
        Booth,
        on_delete=models.CASCADE,
        related_name="plan_items",
    )
    order = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PLANNED,
    )

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["plan", "booth"],
                name="unique_booth_per_plan",
            ),
        ]

    def __str__(self):
        return f"{self.plan} - {self.booth.name}"
