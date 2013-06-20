from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView
from django.shortcuts import get_object_or_404

from .models import Company, Cuisine, Checkin


class CompanyList(ListView):
    template_name = 'trucks/company_list.jinja'

    model = Company

    context_object_name = 'companies'


class CompanyDetail(DetailView):
    template_name = 'trucks/company_detail.jinja'

    slug_field = 'slug'

    model = Company

    context_object_name = 'company'


class CompanyCuisineList(CompanyList):
    template_name = 'trucks/company_cuisine_list.jinja'

    def get_queryset(self):
        slug = self.kwargs['slug']
        self.cuisine = get_object_or_404(Cuisine, slug=slug)
        return self.model.objects.filter(cuisine=self.cuisine)

    def get_context_data(self, **kwargs):
        context = super(CompanyCuisineList, self).get_context_data(**kwargs)
        context['cuisine'] = self.cuisine
        return context


class HomeCompanyList(CompanyList):
    template_name = 'home.jinja'

    def get_queryset(self):
        return self.model.objects.open_trucks()


class CheckinView(CreateView):
    template_name = 'trucks/checkin_form.jinja'
    model = Checkin
    fields = ['location', 'start_time', 'end_time']

# class EditCeckin(UpdateView):
    