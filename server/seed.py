from config import app, db
from faker import Faker
from models import User, Event, Group, GroupInvitation, RSVP, Comment
import random

fake = Faker()

def seed_users(num_users=10):
  users = []
  for _ in range(num_users):
    user = User(
      username=fake.user_name(),
      email = fake.email(),
      password = fake.password(),
    )
    db.session.add(user)
    users.append(user)
  db.session.commit()
  return users

def seed_groups(users, num_groups=5):
  groups = []
  for _ in range(num_groups):
    group = Group(
      name = fake.word(),
      description = fake.text(),
      user_id = random.choice(users).id,
    )
    db.session.add(group)
    groups.append(group)
  db.session.commit()
  return groups

def seed_events(users, num_events=10):
  events = []
  for _ in range(num_events):
    event = Event(
      name = fake.catch_phrase(),
      date = fake.date_this_year(),
      location = fake.city(),
      description = fake.text(),
      user_id = random.choice(users).id,
    )

    db.session.add(event)
    events.append(event)
  db.session.commit()
  return events

def seed_rsvps(users, events, num_rsvps=20):
    for _ in range(num_rsvps):
        rsvp = RSVP(
            user_id=random.choice(users).id,
            event_id=random.choice(events).id,
            status=random.choice(['going', 'not_going', 'maybe']),
        )
        db.session.add(rsvp)
    db.session.commit()

def seed_comments(users, events, num_comments=30):
    for _ in range(num_comments):
        comment = Comment(
            content=fake.sentence(),
            user_id=random.choice(users).id,
            event_id=random.choice(events).id,
        )
        db.session.add(comment)
    db.session.commit()


def seed_group_invitations(users, groups, num_invitations=20):
    for _ in range(num_invitations):
        invited_user = random.choice(users)
        group_invitation = GroupInvitation(
            group_id=random.choice(groups).id,
            user_id=random.choice(users).id,
            invited_user_id=invited_user.id,
            status=random.choice(['pending', 'accepted', 'declined']),
        )
        db.session.add(group_invitation)
    db.session.commit()


def seed_all():
    with app.app_context():  # Ensure the application context is active
        db.drop_all()
        db.create_all()

        users = seed_users()
        groups = seed_groups(users, num_groups=5)  # Explicitly passing `num_groups` as the second argument
        events = seed_events(users, num_events=10)  # Explicitly passing `num_events` as the second argument
        
        seed_rsvps(users, events, num_rsvps=20)  # Explicitly passing `num_rsvps` as the third argument
        seed_comments(users, events, num_comments=30)  # Explicitly passing `num_comments` as the third argument
        seed_group_invitations(users, groups, num_invitations=20)  # Explicitly passing `num_invitations` as the third argument

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_all()



