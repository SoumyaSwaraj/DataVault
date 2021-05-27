from django import forms

class DBInput(forms.Form):
    title = forms.CharField(max_length=200)
    file = forms.FileField()

class DataForm(forms.Form):
    
    def __init__(self,*args,**kwargs):
        # print(kwargs)
        # print(args)
        self.cols = args[1]['cols']
        super(DataForm,self).__init__(*args,**kwargs)
        self.fields['graph_x1'].choices = self.cols
        # self.fields['graph_x2'].choices = self.cols
        self.fields['graph_y1'].choices = self.cols
        # self.fields['graph_y2'].choices = self.cols
        self.fields['reg_cols'].choices = self.cols
        self.fields['clas_cols'].choices = self.cols


    title = forms.CharField(max_length=200, required=False,label="Title")
    description = forms.CharField(max_length=1000, required=False,label="Description for the Dataset")

    # cols_name = forms.CharField(max_length=2000, required=False)
    # cols_desc = forms.CharField(max_length=2000, required=False)

    graph_x1 = forms.MultipleChoiceField(required=False, label="Graph : x-axis",widget=forms.CheckboxSelectMultiple)
    graph_y1 = forms.MultipleChoiceField(required=False,label="Graph : y-axis")

    # graph_x2 = forms.MultipleChoiceField(required=False,label="Graph 2: x-axis",choices=())
    # graph_y2 = forms.MultipleChoiceField(required=False,label="Graph 2: y-axis",choices=())

    reg_cols = forms.MultipleChoiceField(required=False,label="Select Columns for Applying Regression: ",widget=forms.CheckboxSelectMultiple)
    
    clas_cols = forms.MultipleChoiceField(required=False,label="Select Columns for Applying Classification: ",widget=forms.CheckboxSelectMultiple)

    price = forms.CharField(max_length=2000, required=False, label="Proposed Price")
    tags = forms.CharField(max_length=2000, required=False, label="Search Keywords")
