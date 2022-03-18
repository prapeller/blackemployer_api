from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import ContextMixin, RedirectView
from django.conf import settings


class UserIsStuffMixin(View):
    @method_decorator(user_passes_test(lambda u: u is not None and u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserIsSuperuserMixin(View):
    @method_decorator(user_passes_test(lambda u: u is not None and u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserIsNotNoneMixin(View):
    @method_decorator(user_passes_test(lambda u: u is not None))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserIsActiveMixin(View):
    @method_decorator(user_passes_test(lambda u: u is not None and u.is_active))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TitleContextMixin(ContextMixin):
    title = ''

    def get_context_data(self, **kwargs):
        self.extra_context.update({'title': self.title})
        return super().get_context_data(**kwargs)


class PreviousPageMixin(ContextMixin, View):
    extra_context = {}

    def get_context_data(self, **kwargs):
        pre_previous_page_url = self.extra_context.get('previous_page_url')
        previous_page_url = self.request.META.get('HTTP_REFERER')
        current_page_url = settings.DOMAIN_NAME + self.request.META.get('PATH_INFO')
        if current_page_url == previous_page_url:
            self.extra_context.update({'previous_page_url': pre_previous_page_url})
        else:
            self.extra_context.update({'previous_page_url': previous_page_url})
        return super().get_context_data(**kwargs)


class SessionCacheMixin(View):

    def dispatch(self, request, *args, **kwargs):
        # current_page_url = settings.DOMAIN_NAME + self.request.META.get('PATH_INFO')
        # if any(x in current_page_url for x in ['detail/', 'update/']):
        url_name = request.resolver_match.url_name
        obj_id = request.resolver_match.kwargs.get('pk')
        if 'company' in url_name:
            self.request.session['company_id'] = obj_id
        if 'case' in url_name:
            self.request.session['case_id'] = obj_id

        return super().dispatch(request, *args, **kwargs)
