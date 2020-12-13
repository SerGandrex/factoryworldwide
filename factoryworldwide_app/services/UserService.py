import clearbit
from factoryworldwide_app.models.UserModel import User

CLEARBIT_API_KEY = 'sk_ea6cb664dc2a1736cfca41a99ba7c60a'
clearbit.key = CLEARBIT_API_KEY


class UserService:
    model = User

    @classmethod
    def create_user(cls, data):
        user = cls.model()
        user.email = data['email']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.password = data['password']
        additional_info = cls._get_additional_info(data['email'])
        if additional_info:
            user.location = additional_info['location']
            user.bio = additional_info['bio']
            user.site = additional_info['site']
            user.facebook_handle = additional_info['facebook']['handle']
            user.twitter_handle = additional_info['twitter']['handle']
            user.github_handle = additional_info['github']['handle']
        user.save()
        return user

    @classmethod
    def login(cls, data):
        user = cls.model.filter(email=data['email'])
        if user is not None and user.verify_password(
                data['password']):
            return user
        return None

    @classmethod
    def get_user_by_email(cls, email):
        user = cls.model.filter(email=email)
        return user

    @classmethod
    def get_user_with_additional_info(cls, email):
        user = cls.get_user_by_email(email)
        user_data = vars(user)
        user_data.pop('password_hash')

        return user_data

    @classmethod
    def _get_additional_info(cls, email):
        additional_info = clearbit.Enrichment.find(email=email, stream=True)

        if additional_info and additional_info['person']:
            return additional_info['person']
        return {}
