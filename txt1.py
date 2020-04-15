
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_blog.settings")
import django
django.setup()

def main():
    from userprofile.models import Profile

    f = open('txt1.txt',encoding="UTF-8")
    ProfileList = [Profile(phone=line.split('**')[0],
                           intro=line.split("**")[1],
                           address=line.split("**")[2],
                           birth=line.split('**')[3],
                           career=line.split('**')[4],
                           education=line.split('**')[5],
                           homepage=line.split("**")[6],
                           profession=line.split('**')[7],
                           school=line.split('**')[8],
                           skill=line.split('**')[9],
                           user_id=line.split('**')[10]) for line in f]

    Profile.objects.bulk_create(ProfileList)
    f.close()

if __name__ == '__main__':
    main()
    print('Done')