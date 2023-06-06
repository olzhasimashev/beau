from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Procedure, ProcedureLimit
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=Procedure)
def create_procedure_limit(sender, instance, **kwargs):
    for user in User.objects.all():
        ProcedureLimit.objects.create(
            procedure=instance,
            user=user,
            limit=instance.limit
        )

@receiver(post_save, sender=User)
def create_user_limit(sender, instance, **kwargs):
    try:
        ProcedureLimit.objects.filter(user=instance)
    except ProcedureLimit.DoesNotExist:
        for procedure in Procedure.objects.all():
            ProcedureLimit.objects.create(
                procedure=procedure,
                user=instance,
                limit=procedure.limit
            )



    