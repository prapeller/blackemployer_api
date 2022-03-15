from background_task.models import Task as BgTask


# drops pending tasks before creating new ones
def drop_pending_bg_tasks(app, name, id):
    bg_tasks = BgTask.objects.filter(
        task_params__iregex=r"^\[\[{0}".format(id),
        task_name="app.{0}.tasks.{1}".format(app, name),
    )
    bg_tasks.delete()
