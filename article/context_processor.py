from userprofile.models import Profile


from django import template

register = template.Library()


@register.inclusion_tag('header.html')
def show_avatar(request):
    profile = Profile.objects.all()

    return { 'profile' : profile}