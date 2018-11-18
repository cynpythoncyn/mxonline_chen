from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from django.views.generic.base import View


class LoginRequiredMixin(View):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request,*args,**kwargs)