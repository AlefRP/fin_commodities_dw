from airflow.decorators import TaskDecoratorCollection
from .custom_task import custom_empty_task

class CustomTaskCollection(TaskDecoratorCollection):
    """
    Extensão da TaskDecoratorCollection para incluir decoradores personalizados.
    """
    empty = staticmethod(custom_empty_task)  # Registra o decorador personalizado
