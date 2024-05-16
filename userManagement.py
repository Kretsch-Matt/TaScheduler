from django.core.exceptions import ObjectDoesNotExist

from scheduler.models import UserTable


class UserManagementPage:
    def __init__(self):
        pass

    @staticmethod
    def getRole(email):
        try:
            return UserTable.objects.get(email=email).userType
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def add_skill_to_ta(ta_id, skill):
        if not skill:
            return False, "Skill cannot be empty."

        try:
            # Retrieve the TA based on ID
            ta = UserTable.objects.get(pk=ta_id, userType='ta')

            # Ensure that skills is not None
            current_skills = ta.skills or ""

            # Check if the skill already exists
            if skill.lower() in (existing_skill.lower() for existing_skill in current_skills.split(',')):
                return False, "This skill is already assigned to the TA."

            # Add the new skill
            if ta.skills:
                ta.skills += f", {skill}"
            else:
                ta.skills = skill
            ta.save()

            return True, "Skill successfully added."

        except UserTable.DoesNotExist:
            return False, "TA not found or not eligible."
        except Exception as e:
            return False, f"An unexpected error occurred: {str(e)}"

