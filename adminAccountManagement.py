import re

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from scheduler.models import UserTable, LabTable, CourseTable


def editAccount(email, newEmail, phone, address, role):
    try:
        user = UserTable.objects.get(email=email)

        user.email = newEmail
        user.phone = phone
        user.address = address
        user.userType = role
        user.save()

        account = User.objects.get(email=email)
        account.email = newEmail
        account.save()

        return user
    except UserTable.DoesNotExist:
        raise ValueError("User account does not exist.")
    except Exception as e:
        raise ValueError(str(e))


class AdminAccountManagementPage:
    def __init__(self):
        pass

    @staticmethod
    def createAccount(username, email, password):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if username == '' or email == '' or password == '':
            raise ValueError("All fields need to be filled out")

        if not re.match(pattern, email):
            raise ValueError("Invalid email format")

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        try:
            existing_email = User.objects.get(email=email)
            raise ValueError("User already exists")
        except User.DoesNotExist:
            pass

        newAccount = User.objects.create_user(username=username, email=email, password=password)
        newUser = UserTable(email=email)
        newAccount.save()
        newUser.save()
        return True

    @staticmethod
    def deleteAccount(usernameID, emailID):
        try:
            # Get the user account based on username and email
            account = User.objects.get(id=usernameID)
            user = UserTable.objects.filter(email=account.email).first()
            if (account.email != user.email) | (usernameID != emailID):
                return "username/email match error"

            # Finally delete user...
            user.delete()
            # Delete the account
            account.delete()
            return "Account deleted successfully"
        except ObjectDoesNotExist:
            return "Failed to delete account"
