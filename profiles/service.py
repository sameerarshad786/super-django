from django.urls import reverse


def generate_profile_link(request, username):
    profile_link = '{}?username={}'.format(reverse("profile-view"), username)
    return request.build_absolute_uri(profile_link)
