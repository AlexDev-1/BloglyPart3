"""Seed file to make sample data for Posts db."""

from models import User, Post, Tag, PostTag, db, check_table_exists
from app import app

# Wrap operations in application context
with app.app_context():

    # Create all tables
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()
    Post.query.delete()
    Tag.query.delete()

    # Add users
    first_user = User(first_name='John', last_name="Smith", image_url='https://banner2.cleanpng.com/20180714/fok/kisspng-computer-icons-question-mark-clip-art-profile-picture-icon-5b49de29708b76.026875621531567657461.jpg')
    second_user = User(first_name='Adam', last_name="White", image_url='https://cdnb.artstation.com/p/assets/images/images/054/013/735/large/nathan-rosengrun-20-weege.jpg?1663579498')
    third_user = User(first_name='Walter', last_name="Snow",image_url='https://banner2.cleanpng.com/20180714/fok/kisspng-computer-icons-question-mark-clip-art-profile-picture-icon-5b49de29708b76.026875621531567657461.jpg')

    # Add new objects to session, so they'll persist
    db.session.add_all([first_user, second_user, third_user])
    db.session.commit()
    
    # Add Posts
    first_post = Post(title='Hello', content="Hello World", user_id=1)
    second_post = Post(title='Greetings', content="Greetings World", user_id=2)
    third_post = Post(title='Ciao', content="Ciao World",user_id=3)

    # Add new objects to session, so they'll persist
    db.session.add_all([first_post, second_post,third_post])
    db.session.commit()

    # Add Tags
    first_tag = Tag(name='Fun')
    second_tag = Tag(name='Even More')
    third_tag = Tag(name='Bloop')
    forth_tag = Tag(name='Zope')

    # Add new objects to session, so they'll persist
    db.session.add_all([first_tag, second_tag, third_tag, forth_tag])
    db.session.commit()

    # Add PostTags
    first_posttag = PostTag(post_id=first_post.id, tag_id=first_tag.id)
    second_posttag = PostTag(post_id=second_post.id, tag_id=forth_tag.id)
    third_posttag = PostTag(post_id=third_post.id, tag_id=second_tag.id)

    # Add new objects to session, so they'll persist
    db.session.add_all([first_posttag,second_posttag,third_posttag])
    db.session.commit()