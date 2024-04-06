from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from employee.serializer import AddEmployeeSerializer
from employee.models import Employee
from rest_framework.pagination import PageNumberPagination
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.db.models import Sum
from io import BytesIO
from django.http import HttpResponse, JsonResponse
import json



@api_view(['POST'])
def  LoginView(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response(
            {"name": username,
                'refresh': str(refresh),
                'access_token': str(refresh.access_token)
            }, status=status.HTTP_200_OK
        )
    return Response({'error': "Invalid Cred"}, 
                    status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])    
@permission_classes((IsAuthenticated,))
def AddEmployee(request):
    serializer = AddEmployeeSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET']) 
@permission_classes((IsAuthenticated,))
def ViewAllEmployee(request):
    name = request.GET.get('name')
    designation = request.GET.get('designation')
    if name and designation:
        employees = Employee.objects.filter(name__icontains=name,
                                            designation__icontains=designation)
    elif name:
        employees = Employee.objects.filter(name__icontains=name)
    elif designation:
        employees = Employee.objects.filter(designation__icontains=designation)    
    else:
        employees = Employee.objects.all()  
          
    paginator = PageNumberPagination()
    paginator.page_size = 2
    result_page = paginator.paginate_queryset(employees, request)

    serializer = AddEmployeeSerializer(result_page, many=True)
    if employees:
        return Response({"employee details": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# update employee deatails
@api_view(['PATCH'])    
@permission_classes((IsAuthenticated,))
def UpdateEmployee(request, id):
    try:
        employee = Employee.objects.get(id=id)
    except Employee.DoesNotExist:
        return Response({"error": "Invalid employee id"}, status=status.HTTP_400_BAD_REQUEST)    
    serializer = AddEmployeeSerializer(employee, request.data, partial=True)
    if serializer.is_valid():
        serializer.save(user=request.user)
        data = {"message": "update employee deatils successfully", "data": serializer.data}
        return Response(data=data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])    
@permission_classes((IsAuthenticated,))
def DeleteEmployee(request, id):
    try:
        employee = Employee.objects.get(id=id)
    except Employee.DoesNotExist:
        return Response({"error": "Invalid employee id"}, status=status.HTTP_400_BAD_REQUEST)    
    employee.delete()
    return Response({"data": "Employee is deleted successfully"}, status=status.HTTP_200_OK)


# monthly salery report generate in pdf
@api_view(['POST'])    
@permission_classes((IsAuthenticated,))
def GenerateSaleryReport(request):
    name = request.data.get('name')
    month, year = int(request.data.get('month')), int(request.data.get('year'))
    if not name:
        return HttpResponse("Employee name is required.", status=400)
    try:
        employee = Employee.objects.get(name__icontains=name)
    except Employee.DoesNotExist:
        return HttpResponse("Employee not found.", status=404)
    salaries = Employee.objects.filter(name__icontains=employee, issue_date__month=month, issue_date__year=year)
    total_salary = salaries.aggregate(total=Sum('emp_salary'))['total'] or 0
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    data = [['Employee Name', 'Salary Amount']] + [[salary.name, str(salary.emp_salary)] for salary in salaries] + [['Total', str(total_salary)]]
    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)), ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('BOTTOMPADDING', (0, 0), (-1, 0), 12), ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)), ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))])
    table.setStyle(style)
    pdf.build([table])
    pdf_data = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="salary_report.pdf"'
    return response


#fetch data from a JSON file and Display data in proper format.
@api_view(['GET'])
def get_json_data(request):
    try:
        with open('data.json', 'r',  encoding='utf-8' ) as f:
            data = json.loads(f.read())
    except FileNotFoundError:
        return JsonResponse({'error': 'Data file not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format in data file'}, status=500)

    # Format and return the data
    formatted_data = []
    for item in data:
        formatted_data.append({
            'Name': item['name'],
            'Age': item['age'],
            'Email': item['email']
        })

    return JsonResponse(formatted_data, safe=False)
