from sqlalchemy import Select

from fast_zero.models import User


def test_create_user(session):
    # Arrange
    email = 'jocelio@vieira.com'
    password = 'senha'
    username = 'jocelio2020'

    user_to_be_created = User(
        email=email,
        password=password,
        username=username,
    )

    # Act
    session.add(user_to_be_created)
    session.commit()

    result = session.scalar(Select(User).where(User.username == username))

    # Assert
    assert result.email == email
    assert result.username == username
