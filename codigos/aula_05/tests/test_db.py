from fast_zero.models import User
from sqlalchemy import select

def test_create_user_ok(client, session):
    # Arrange
    new_user = User(
        username='alice',
        email='alice.coltrane@music.com',
        password='jazz'
    )
    
    # Act
    session.add(new_user)
    session.commit()
    
    response = session.scalar(select(User).where(User.username == new_user.username))
    
    # Assert
    assert response.username == new_user.username