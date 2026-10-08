from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Booth
from django.db import transaction
from .forms import GoalSelectionForm
from .models import Booth, VisitorGoal, VisitPlan, PlanItem
from django.db.models import Max
from django.views.decorators.http import require_POST
from accounts.models import VisitorProfile


@login_required
def index(request):
    selected_goal_ids = VisitorGoal.objects.filter(user=request.user).values_list(
        "goal_id", flat=True
    )

    booths = Booth.objects.prefetch_related("goals").all()

    if selected_goal_ids.exists():
        booths = booths.filter(goals__id__in=selected_goal_ids).distinct()

    return render(
        request,
        "visits/index.html",
        {"booths": booths},
    )


@login_required
def select_goals(request):
    saved_goals = VisitorGoal.objects.filter(user=request.user)

    if request.method == "POST":
        form = GoalSelectionForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                saved_goals.delete()

                for goal in form.cleaned_data["goals"]:
                    VisitorGoal.objects.create(
                        user=request.user,
                        goal=goal,
                        priority=1,
                    )

            return redirect("visits:index")
    else:
        form = GoalSelectionForm(
            initial={
                "goals": list(saved_goals.values_list("goal_id", flat=True)),
            }
        )

    return render(
        request,
        "visits/select_goals.html",
        {"form": form},
    )


@login_required
@require_POST
def add_to_plan(request, booth_id):
    booth = get_object_or_404(Booth, pk=booth_id)

    with transaction.atomic():
        plan, _ = VisitPlan.objects.get_or_create(user=request.user)

        plan = VisitPlan.objects.select_for_update().get(pk=plan.pk)

        last_order = plan.items.aggregate(last=Max("order"))["last"] or 0

        PlanItem.objects.get_or_create(
            plan=plan,
            booth=booth,
            defaults={"order": last_order + 1},
        )

    return redirect("visits:index")


@login_required
def plan(request):
    visit_plan = VisitPlan.objects.filter(user=request.user).first()

    items = []

    if visit_plan:
        items = list(visit_plan.items.select_related("booth").all())

    profile, _ = VisitorProfile.objects.get_or_create(user=request.user)

    total_minutes = sum(item.booth.visit_duration for item in items)
    available_minutes = profile.available_minutes
    over_limit = total_minutes > available_minutes

    return render(
        request,
        "visits/plan.html",
        {
            "items": items,
            "total_minutes": total_minutes,
            "available_minutes": available_minutes,
            "over_limit": over_limit,
        },
    )


@login_required
@require_POST
def remove_from_plan(request, item_id):
    item = get_object_or_404(
        PlanItem,
        pk=item_id,
        plan__user=request.user,
    )
    item.delete()

    return redirect("visits:plan")


@login_required
@require_POST
def update_status(request, item_id):
    item = get_object_or_404(
        PlanItem,
        pk=item_id,
        plan__user=request.user,
    )

    status = request.POST.get("status")

    if status in PlanItem.Status.values:
        item.status = status
        item.save(update_fields=["status"])

    return redirect("visits:plan")


@login_required
@require_POST
def move_plan_item(request, item_id):
    direction = request.POST.get("direction")

    if direction not in ("up", "down"):
        return redirect("visits:plan")

    with transaction.atomic():
        plan = get_object_or_404(
            VisitPlan.objects.select_for_update(),
            user=request.user,
        )

        items = list(plan.items.order_by("order", "id"))

        index = next(
            (i for i, item in enumerate(items) if item.pk == item_id),
            None,
        )

        if index is None:
            return redirect("visits:plan")

        target = index - 1 if direction == "up" else index + 1

        if 0 <= target < len(items):
            items[index], items[target] = items[target], items[index]

            for position, item in enumerate(items, start=1):
                item.order = position

            PlanItem.objects.bulk_update(items, ["order"])

    return redirect("visits:plan")


@login_required
def booth_detail(request, booth_id):
    booth = get_object_or_404(Booth, pk=booth_id)

    profile, _ = VisitorProfile.objects.get_or_create(user=request.user)

    return render(
        request,
        "visits/booth_detail.html",
        {
            "booth": booth,
            "show_captions": profile.show_captions,
        },
    )
