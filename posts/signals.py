from django.forms import model_to_dict
from django.db.models.signals import pre_save
from django.dispatch import receiver

from posts.models import Remarks


@receiver(pre_save, sender=Remarks)
def handle_double_actions(sender, instance, **kwargs):
    instance_items = model_to_dict(instance)
    fields = ["like", "heart", "funny", "insightful", "disappoint"]
    field_dict = {field: False for field in fields}
    final_data = {**field_dict, **instance_items}
    double_action_check = {key: value for key, value in final_data.items() if value is True if key in fields} # noqa
    if len(double_action_check) > 1:
        raise Exception("you can give only one reaction")
