from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)

from tasks.models import TaskType, Position, Worker, Task
from tasks.forms import (
    TaskForm,
    WorkerCreationForm,
    WorkerUpdateForm,
    WorkerUsernameSearchForm,
    TaskTypeNameSearchForm,
    PositionNameSearchForm,
    TaskNameSearchForm,
)


@login_required
def index(request):
    """View function for the home page of the site."""

    num_task_types = TaskType.objects.count()
    num_positions = Position.objects.count()
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_task_types": num_task_types,
        "num_positions": num_positions,
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "tasks/index.html", context=context)


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task_type_list"
    template_name = "tasks/task_type_list.html"
    paginate_by = 5

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return TaskType.objects.filter(name__icontains=name)
        return TaskType.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeNameSearchForm(initial={"name": name})
        return context


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "tasks/task_type_form.html"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "tasks/task_type_form.html"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "tasks/task_type_confirm_delete.html"
    context_object_name = "task_type"
    success_url = reverse_lazy("tasks:task-type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5

    def get_queryset(self):
        name = self.request.GET.get("name")
        if name:
            return Position.objects.filter(name__icontains=name)
        return Position.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionNameSearchForm(initial={"name": name})
        return context


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("tasks:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("tasks:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("tasks:position-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5

    def get_queryset(self):
        username = self.request.GET.get("username")
        queryset = Worker.objects.all().select_related("position")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerUsernameSearchForm(
            initial={"username": username}
        )
        return context


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("assigned_tasks")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("tasks:worker-list")


class WorkerRegisterView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("tasks:index")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("tasks:index"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(
            self.request,
            self.object,
            backend="tasks.backends.EmailOrUsernameModelBackend",
        )
        return response


class WorkerUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView
):
    model = Worker
    form_class = WorkerUpdateForm
    template_name = "tasks/worker_form.html"

    def test_func(self):
        worker = self.get_object()
        return self.request.user.is_staff or self.request.user == worker

    def get_success_url(self):
        return reverse_lazy(
            "tasks:worker-detail", kwargs={"pk": self.object.pk}
        )


WorkerPositionUpdateView = WorkerUpdateView


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("tasks:worker-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_queryset(self):
        name = self.request.GET.get("name")
        queryset = Task.objects.all().select_related("task_type")
        if name:
            return queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskNameSearchForm(initial={"name": name})
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = (
        Task.objects.all()
        .select_related("task_type")
        .prefetch_related("assignees")
    )


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


@login_required
def toggle_assign_to_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        if request.user in task.assignees.all():
            task.assignees.remove(request.user)
        else:
            task.assignees.add(request.user)
    return HttpResponseRedirect(
        reverse_lazy("tasks:task-detail", args=[pk])
    )
