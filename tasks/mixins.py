from django.core.exceptions import PermissionDenied

class UserIsOwnerOrAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # спробуємо отримати owner, якщо немає — author
        owner = getattr(obj, 'owner', None) or getattr(obj, 'author', None)
        if owner != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
