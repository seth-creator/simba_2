from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.db.models import Count, Q

# Create your views here.
from simba_app.models import Crud, MonOffre, UserProfile
from simba_app.forms import  MonOffreForm
from django.views.generic.list import ListView, View
from import_export import mixins, resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

ajout = ""
def crud (request, id=None):
    if id :
        bien = det-object_or_404(Crud, pk=id)
    if request.method == 'POST':
        ajout = Crud.objects.create(nom = request.POST['nomo'], prenom = request.POST['prenomo'], age = request.POST['ageo'], pays= request.POST['payso'])
        
    return render (request, 'simba/index_crud.html')


def delete(request, id):
	# return HttpResponse("Effacer")
	immobilier = get_object_or_404(MonOffre, pk=id)
	immobilier.delete()
	return redirect('index')


def formu(request, id = None ) :
        if id :
            bien = get_object_or_404(MonOffre, pk = id)
        else :
            bien = MonOffre()
        if request.method == 'POST':
            form = MonOffreForm(request.POST, request.FILES, instance = bien)
        #form = MonOffreForm(request.POST)
            if form.is_valid():
                bien = form.save(commit = False)
                if request.user.is_authenticated :
                    bien.users = request.user.username
                    bien.fournisseur = UserProfile.objects.get(user_id =request.user.id)
                    bien.save()
            #text = form.cleaned_data['post']
           
                return redirect('index')
        else :
             form = MonOffreForm(instance=bien)
            
        args = {'form': form}   
        return render(request,'simba/form.html', dict(form=form, id=id))
    
def index(request):
    user = request.user
    immobilier = MonOffre.objects.filter(users__contains=user).order_by('id') #Obtenez de la valeur
    return render(request, 'simba/accueil_crud.html', {'members': immobilier,'user':user}) #Passer une valeur au modèle

#Détails
def detail(request, id=id):
    bien = get_object_or_404(MonOffre, pk=id)
    return render(request, 'simba/detail_crud.html', {'member':bien})

from simba_app.models import MonOffre
#from myapp.serializers import PurchaseSerializer
from rest_framework import generics

class PurchaseList(generics.ListAPIView):
    #serializer_class = PurchaseSerializer
    template_name = 'simba/accueil_crud.html'
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        usa = UserProfile.objects.filter(user=user)
        return render(request, self.template_name,{'Usa':usa} )
    
    
class PurchaseListo(generics.ListAPIView):
    #serializer_class = PurchaseSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        username = self.kwargs['username']
        return MonOffre.objects.filter(fournisseur__username=username)
    
    
@login_required(login_url = 'acces')   
def ticket_class_view(request):
    dataset = MonOffre.objects.filter(users__contains=request.user) \
        .values('types') \
        .annotate(survived_count=Count('types', filter=Q(types = 'Villa')),
                  bureau_count=Count('types', filter=Q(types = 'Bureau')),
                  terrain_count=Count('types', filter=Q(types = 'Terrain')),
                  not_survived_count=Count('types', filter=Q(types = 'Appartement' ))) \
        .order_by('types')
    return render(request, 'simba/ticket_class.html', {'dataset': dataset})

class CountryResource(resources.ModelResource):
    class Meta:
        model = MonOffre
        
class CountryExport(View):

    def get(self, *args, **kwargs ):
        dataset = CountryResource().export()
        response = HttpResponse(dataset.csv, content_type="csv")
        response['Content-Disposition'] = 'attachment; filename=filename.csv'
        return response
    
"""class CountryImport(View):
    model = MonOffre
    from_encoding = "utf-8"

    #: import / export formats
    DEFAULT_FORMATS = (
        base_formats.CSV,
        base_formats.XLS,
        base_formats.TSV,
        base_formats.ODS,
        base_formats.JSON,
        base_formats.YAML,
        base_formats.HTML,
    )
    formats = DEFAULT_FORMATS
    #: template for import view
    import_template_name = 'simba/accueil_crud.html'
    resource_class = None

    def get_import_formats(self):
        
        #Returns available import formats.
        
        return [f for f in self.formats if f().can_import()]

    def get_resource_class(self):
        if not self.resource_class:
            return modelresource_factory(self.model)
        else:
            return self.resource_class

    def get_import_resource_class(self):
       
        "Returns ResourceClass to use for import.
        
        return self.get_resource_class()

    def get(self, *args, **kwargs ):
        '''
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        '''
        resource = self.get_import_resource_class()()

        context = {}

        import_formats = self.get_import_formats()
        form = ImportForm(import_formats,
                          self.request.POST or None,
                          self.request.FILES or None)

        if self.request.POST and form.is_valid():
            input_format = import_formats[
                int(form.cleaned_data['input_format'])
            ]()
            import_file = form.cleaned_data['import_file']
            # first always write the uploaded file to disk as it may be a
            # memory file or else based on settings upload handlers
            with tempfile.NamedTemporaryFile(delete=False) as uploaded_file:
                for chunk in import_file.chunks():
                    uploaded_file.write(chunk)

            # then read the file, using the proper format-specific mode
            with open(uploaded_file.name,
                      input_format.get_read_mode()) as uploaded_import_file:
                # warning, big files may exceed memory
                data = uploaded_import_file.read()
                if not input_format.is_binary() and self.from_encoding:
                    data = force_text(data, self.from_encoding)
                dataset = input_format.create_dataset(data)
                result = resource.import_data(dataset, dry_run=True,
                                              raise_errors=False)

            context['result'] = result

            if not result.has_errors():
                context['confirm_form'] = ConfirmImportForm(initial={
                    'import_file_name': os.path.basename(uploaded_file.name),
                    'input_format': form.cleaned_data['input_format'],
                })

        context['form'] = form
        context['opts'] = self.model._meta
        context['fields'] = [f.column_name for f in resource.get_fields()]

        return TemplateResponse(self.request, [self.import_template_name], context)


    def post(self, *args, **kwargs ):
        '''
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        '''
        resource = self.get_import_resource_class()()

        context = {}

        import_formats = self.get_import_formats()
        form = ImportForm(import_formats,
                          self.request.POST or None,
                          self.request.FILES or None)

        if self.request.POST and form.is_valid():
            input_format = import_formats[
                int(form.cleaned_data['input_format'])
            ]()
            import_file = form.cleaned_data['import_file']
            # first always write the uploaded file to disk as it may be a
            # memory file or else based on settings upload handlers
            with tempfile.NamedTemporaryFile(delete=False) as uploaded_file:
                for chunk in import_file.chunks():
                    uploaded_file.write(chunk)

            # then read the file, using the proper format-specific mode
            with open(uploaded_file.name,
                      input_format.get_read_mode()) as uploaded_import_file:
                # warning, big files may exceed memory
                data = uploaded_import_file.read()
                if not input_format.is_binary() and self.from_encoding:
                    data = force_text(data, self.from_encoding)
                dataset = input_format.create_dataset(data)
                result = resource.import_data(dataset, dry_run=True,
                                              raise_errors=False)

            context['result'] = result

            if not result.has_errors():
                context['confirm_form'] = ConfirmImportForm(initial={
                    'import_file_name': os.path.basename(uploaded_file.name),
                    'input_format': form.cleaned_data['input_format'],
                })

        context['form'] = form
        context['opts'] = self.model._meta
        context['fields'] = [f.column_name for f in resource.get_fields()]

        return TemplateResponse(self.request, [self.import_template_name], context)

class CountryProcessImport(View):
    model = MonOffre
    from_encoding = "utf-8"

    #: import / export formats
    DEFAULT_FORMATS = (
        base_formats.CSV,
        base_formats.XLS,
        base_formats.TSV,
        base_formats.ODS,
        base_formats.JSON,
        base_formats.YAML,
        base_formats.HTML,
    )
    formats = DEFAULT_FORMATS
    #: template for import view
    import_template_name = 'simba/accueil_crud.html'
    resource_class = None



    def get_import_formats(self):
       
       # Returns available import formats.
      
        return [f for f in self.formats if f().can_import()]

    def get_resource_class(self):
        if not self.resource_class:
            return modelresource_factory(self.model)
        else:
            return self.resource_class

    def get_import_resource_class(self):
       
        #Returns ResourceClass to use for import.
       
        return self.get_resource_class()

    def post(self, *args, **kwargs ):
        '''
        Perform the actual import action (after the user has confirmed he
    wishes to import)
        '''
        opts = self.model._meta
        resource = self.get_import_resource_class()()

        confirm_form = ConfirmImportForm(self.request.POST)
        if confirm_form.is_valid():
            import_formats = self.get_import_formats()
            input_format = import_formats[
                int(confirm_form.cleaned_data['input_format'])
            ]()
            import_file_name = os.path.join(
                tempfile.gettempdir(),
                confirm_form.cleaned_data['import_file_name']
            )
            import_file = open(import_file_name, input_format.get_read_mode())
            data = import_file.read()
            if not input_format.is_binary() and self.from_encoding:
                data = force_text(data, self.from_encoding)
            dataset = input_format.create_dataset(data)

            result = resource.import_data(dataset, dry_run=False,
                                 raise_errors=True)

            # Add imported objects to LogEntry
            ADDITION = 1
            CHANGE = 2
            DELETION = 3
            logentry_map = {
                RowResult.IMPORT_TYPE_NEW: ADDITION,
                RowResult.IMPORT_TYPE_UPDATE: CHANGE,
                RowResult.IMPORT_TYPE_DELETE: DELETION,
            }
            content_type_id=ContentType.objects.get_for_model(self.model).pk
            '''
            for row in result:
                LogEntry.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=content_type_id,
                    object_id=row.object_id,
                    object_repr=row.object_repr,
                    action_flag=logentry_map[row.import_type],
                    change_message="%s through import_export" % row.import_type,
                )
            '''
            success_message = _('Import finished')
            messages.success(self.request, success_message)
            import_file.close()

            url = reverse('%s_list' % (str(opts.app_label).lower()))
            return HttpResponseRedirect(url)"""