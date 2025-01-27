from user_managment.models import User
user = User.objects.get(email='admin@gmail.com')
print(user.is_staff)  # This must be True
