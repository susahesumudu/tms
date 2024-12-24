from .models import TeacherProfile, StudentProfile, ParentProfile, StaffProfile

def navbar_profile(request):
    if request.user.is_authenticated:
        try:
            # Fetch the correct profile based on the user group
            if request.user.groups.filter(name='Teacher').exists():
                return {'profile': TeacherProfile.objects.get(user=request.user)}
            elif request.user.groups.filter(name='Student').exists():
                return {'profile': StudentProfile.objects.get(user=request.user)}
            elif request.user.groups.filter(name='Parent').exists():
                return {'profile': ParentProfile.objects.get(user=request.user)}
            elif request.user.groups.filter(name='Staff').exists():
                return {'profile': StaffProfile.objects.get(user=request.user)}
        except Exception:
            return {'profile': None}
    return {'profile': None}
