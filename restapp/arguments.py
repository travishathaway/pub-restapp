from flask_restful import reqparse
import checkers as ch

# Create User Parser
create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument(
    'username', type=ch.username_check,
    required=True
)
create_user_parser.add_argument(
    'email', type=str, required=True
)
create_user_parser.add_argument(
    'favorite_color', type=ch.check_color
)

# Update User Parser
update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument(
    'email', type=str
)
update_user_parser.add_argument(
    'favorite_color', type=ch.check_color
)