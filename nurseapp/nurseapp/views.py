from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from nurseapp.models import Patient, VitalSign

from nurseapp.settings import BLOOD_PRESSURE_RATES, HEART_RATES


@require_http_methods(['GET'])
def home(request):
    patients = Patient.objects.all().order_by('-id')
    context = {'patients': patients}
    return render(request, 'home.html', context)


@require_http_methods(['POST'])
def patient_delete(request):
    data = request.POST
    patient_id = data.get('patient_id', None)
    if patient_id:
        patient = Patient.objects.get(id=patient_id)
        patient.delete()
    return redirect('home')


@require_http_methods(['GET', 'POST'])
def patient_add(request):
    if request.method == 'POST':
        data = request.POST
        identity_card_number = data.get('identity_card_number', None)
        name = data.get('name', None)
        age = int(data.get('age', None))
        heart_rate = int(data.get('heart_rate', None))
        systolic = int(data.get('systolic', None))
        diastolic = int(data.get('diastolic', None))
        try:
            patient = Patient(name=name, age=age, identity_card_number=identity_card_number)
            patient.save()
            vital_sign = VitalSign(age=age, heart_rate=heart_rate, systolic=systolic, diastolic=diastolic,
                                   patient=patient)
            vital_sign.heart_rate_status = check_heart_rate(age, heart_rate)
            vital_sign.blood_pressure_status = check_blood_pressure(systolic, diastolic)
            vital_sign.save()
            return redirect('patient_edit', patient_id=patient.id)
        except Exception as e:
            print('Error saving patient information: %s', e)
            context = {'name': name, 'age': age, 'identity_card_number': identity_card_number,
                       'heart_rate': heart_rate, 'systolic': systolic, 'diastolic': diastolic}
            return render(request, 'patient_add.html', context)
    else:
        return render(request, 'patient_add.html')


@require_http_methods(['POST'])
def patient_check(request):
    data = request.POST
    patient_id = data.get('patient_id', None)
    age = int(data.get('age', None))
    heart_rate = int(data.get('heart_rate', None))
    systolic = int(data.get('systolic', None))
    diastolic = int(data.get('diastolic', None))
    patient = Patient.objects.get(id=patient_id)
    vital_sign = VitalSign(age=age, heart_rate=heart_rate, systolic=systolic, diastolic=diastolic,
                           patient=patient)
    vital_sign.heart_rate_status = check_heart_rate(age, heart_rate)
    vital_sign.blood_pressure_status = check_blood_pressure(systolic, diastolic)
    vital_sign.save()
    return redirect('patient_edit', patient_id=patient.id)


@require_http_methods(['GET', 'POST'])
def patient_edit(request, patient_id):
    if request.method == 'POST':
        data = request.POST
        patient_id = data.get('patient_id', None)
        name = data.get('name', None)
        age = data.get('age', None)
        identity_card_number = data.get('identity_card_number', None)
        try:
            patient = Patient.objects.get(id=patient_id)
            patient.name = name
            patient.age = age
            patient.identity_card_number = identity_card_number
            patient.save()
        except Exception as e:
            print('Error editing patient: %s', e)
        return redirect('patient_edit', patient_id=patient_id)
    else:
        patient = Patient.objects.get(id=patient_id)
        last_vital_sign = VitalSign.objects.filter(patient_id=patient.id).order_by("-id")[0]
        return render(request, 'patient_edit.html', {'patient': patient, 'last_vital_sign': last_vital_sign})


@require_http_methods(['GET'])
def patient_view(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    vital_sign_list = VitalSign.objects.filter(patient_id=patient.id).order_by("-id")
    context = {'patient': patient, 'vital_sign_list': vital_sign_list}
    return render(request, 'patient_view.html', context)


def check_blood_pressure(systolic, diastolic):
    if systolic <= BLOOD_PRESSURE_RATES['low_systolic'] and diastolic <= BLOOD_PRESSURE_RATES['low_diastolic']:
        return 'low'
    elif systolic <= BLOOD_PRESSURE_RATES['ideal_systolic'] and diastolic <= BLOOD_PRESSURE_RATES['ideal_diastolic']:
        return 'ideal'
    elif systolic <= BLOOD_PRESSURE_RATES['pre_high_systolic'] and \
            diastolic <= BLOOD_PRESSURE_RATES['pre_high_diastolic']:
        return 'pre-high'
    elif systolic > BLOOD_PRESSURE_RATES['pre_high_systolic'] or diastolic > BLOOD_PRESSURE_RATES['pre_high_diastolic']:
        return 'high'
    else:
        return 'undefined'


def check_heart_rate(age, heart_rate):
    if age < 30 and HEART_RATES['age_30_min'] <= heart_rate <= HEART_RATES['age_30_max']:
        return 'normal'
    elif age < 40 and HEART_RATES['age_40_min'] <= heart_rate <= HEART_RATES['age_40_max']:
        return 'normal'
    elif age < 50 and HEART_RATES['age_50_min'] <= heart_rate <= HEART_RATES['age_50_max']:
        return 'normal'
    elif age < 60 and HEART_RATES['age_60_min'] <= heart_rate <= HEART_RATES['age_60_max']:
        return 'normal'
    elif age < 70 and HEART_RATES['age_70_min'] <= heart_rate <= HEART_RATES['age_70_max']:
        return 'normal'
    elif age < 80 and HEART_RATES['age_80_min'] <= heart_rate <= HEART_RATES['age_80_max']:
        return 'normal'
    else:
        return 'abnormal'
