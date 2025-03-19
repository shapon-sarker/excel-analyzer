from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import pandas as pd
import openpyxl
from .forms import ExcelUploadForm
from .models import ExcelFile

def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.save(commit=False)
            excel_file.filename = request.FILES['file'].name
            excel_file.save()
            return redirect('view_excel', pk=excel_file.pk)
    else:
        form = ExcelUploadForm()
    
    context = {
        'form': form,
        'recent_files': ExcelFile.objects.all()[:5]
    }
    return render(request, 'excel_app/upload_excel.html', context)

def view_excel(request, pk):
    excel_file = ExcelFile.objects.get(pk=pk)
    formulas = []
    data = None
    
    try:
        # Read Excel file using openpyxl for formulas
        wb = openpyxl.load_workbook(excel_file.file.path, data_only=False)
        sheet = wb.active
        
        # Extract formulas
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value and str(cell.value).startswith('='):
                    formulas.append({
                        'cell': cell.coordinate,
                        'formula': cell.value
                    })
        
        # Read data using pandas
        df = pd.read_excel(excel_file.file.path)
        data = df.to_html(
            classes='table table-striped table-hover',
            index=False,
            border=0,
            table_id='excel-data'
        )
        
        excel_file.processed = True
        excel_file.save()
        
    except Exception as e:
        messages.error(request, f'Error processing file: {str(e)}')
        return redirect('upload_excel')
    
    context = {
        'excel_file': excel_file,
        'formulas': formulas,
        'data': data,
    }
    return render(request, 'excel_app/view_excel.html', context)
