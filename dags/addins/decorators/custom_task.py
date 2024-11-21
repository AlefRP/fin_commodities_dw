from airflow.operators.empty import EmptyOperator
from airflow.decorators.base import task_decorator_factory
from typing import Callable, Any


class _CustomEmptyOperator(EmptyOperator):
    """
    Custom operator for tasks that do nothing but can be part of a DAG.
    Useful for placeholders or dividing workflow logic.
    """
    custom_operator_name: str = "@custom_task.empty"

    def __init__(
        self,
        *,
        python_callable: Callable | None = None,
        op_args: list[Any] | None = None,
        op_kwargs: dict[str, Any] | None = None,
        **kwargs,
    ) -> None:
        # Remove arguments that are not valid for EmptyOperator
        kwargs.pop("op_args", None)
        kwargs.pop("op_kwargs", None)

        super().__init__(**kwargs)
        self.python_callable = python_callable

    def execute(self, context: Any) -> None:
        """Executes the Python callable if provided, otherwise does nothing."""
        if self.python_callable:
            self.python_callable()
        self.log.info("Executing a custom empty task.")

def custom_empty_task(
    python_callable: Callable | None = None,
    **kwargs,
) -> Callable:
    """
    Wrap a function into a CustomEmptyOperator.

    :param python_callable: Function to decorate.
    """
    return task_decorator_factory(
        python_callable=python_callable,
        decorated_operator_class=_CustomEmptyOperator,
        **kwargs,
    )
