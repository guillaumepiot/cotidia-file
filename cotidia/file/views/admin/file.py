# from django.views.generic import ListView
# from django.views.generic.edit import DeleteView
# from django.core.urlresolvers import reverse
# from django.contrib import messages

# from cotidia.account.utils import StaffPermissionRequiredMixin
# from cotidia.file.models import File


# class FileList(StaffPermissionRequiredMixin, ListView):
#     model = File
#     template_name = 'admin/file/file/file_list.html'
#     permission_required = 'file.change_file'

#     def get_queryset(self):
#         queryset = File.objects.filter()
#         return queryset


# class FileDelete(StaffPermissionRequiredMixin, DeleteView):
#     model = File
#     permission_required = 'file.delete_file'
#     template_name = 'admin/file/file/file_confirm_delete.html'

#     def get_next_url(self):
#         self.next_url = None
#         if self.request.GET.get("next"):
#             self.next_url = self.request.GET.get("next")
#         return self.next_url

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context["next_url"] = self.get_next_url()
#         return context

#     def get_success_url(self):
#         messages.success(self.request, 'File has been deleted.')
#         return self.get_next_url() or reverse('file-admin:file-list')


from cotidia.admin.views import AdminListView, AdminDeleteView

from cotidia.file.models import File


class FileList(AdminListView):
    columns = (
        ('Name', 'name'),
        ('Date Created', 'created_at'),
    )
    model = File


class FileDelete(AdminDeleteView):
    model = File
