from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import date, timedelta

from ...models import User, Team, Activity, Leaderboard, Workout


class Command(BaseCommand):
    help = "Populate database with sample Octofit Tracker test data"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Clearing existing records...")
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        self.stdout.write("Creating teams...")
        team_names = ["Team A", "Team B", "Team C", "Team D"]
        teams = {}
        for team_name in team_names:
            team, _ = Team.objects.get_or_create(name=team_name, defaults={'members': []})
            teams[team_name] = team

        self.stdout.write("Creating users and assigning teams...")
        users = [
            ("alice@example.com", "Alice", "Team A"),
            ("bob@example.com", "Bob", "Team A"),
            ("carol@example.com", "Carol", "Team B"),
            ("dave@example.com", "Dave", "Team B"),
            ("elena@example.com", "Elena", "Team C"),
            ("frank@example.com", "Frank", "Team C"),
            ("gina@example.com", "Gina", "Team D"),
            ("henry@example.com", "Henry", "Team D"),
        ]

        for email, name, team_name in users:
            User.objects.create(email=email, name=name, team=team_name)
            team = teams.get(team_name) or Team.objects.filter(name=team_name).first()
            if team is None:
                self.stderr.write(self.style.WARNING(f"Team not found: {team_name}"))
                continue
            if name not in team.members:
                team.members.append(name)
                team.save()

        self.stdout.write("Creating workouts...")
        workouts = [
            ("Morning Run", "30-minute easy run", "All"),
            ("HIIT Blast", "High intensity interval training", "Advanced"),
            ("Core Strength", "Pilates + core stability", "Intermediate"),
            ("Yoga Flow", "Flexibility and mobility", "All"),
            ("Team Relay", "Group team competition", "All"),
        ]

        for name, desc, suggested in workouts:
            Workout.objects.create(name=name, description=desc, suggested_for=suggested)

        self.stdout.write("Creating activities...")
        now = date.today()
        sample_activities = [
            ("Alice", "Running", 30, now - timedelta(days=1)),
            ("Alice", "Cycling", 45, now - timedelta(days=2)),
            ("Bob", "Swimming", 40, now - timedelta(days=1)),
            ("Bob", "Rowing", 25, now - timedelta(days=3)),
            ("Carol", "Yoga", 50, now - timedelta(days=4)),
            ("Dave", "Weightlifting", 60, now - timedelta(days=2)),
            ("Elena", "Hiking", 120, now - timedelta(days=6)),
            ("Frank", "Running", 35, now - timedelta(days=3)),
            ("Gina", "Walk", 20, now - timedelta(days=1)),
            ("Henry", "Cycling", 50, now - timedelta(days=5)),
            ("Alice", "HIIT", 20, now - timedelta(days=5)),
            ("Bob", "Pilates", 30, now - timedelta(days=6)),
            ("Carol", "Running", 30, now - timedelta(days=7)),
            ("Dave", "Swimming", 45, now - timedelta(days=2)),
            ("Elena", "Crossfit", 30, now - timedelta(days=1)),
            ("Frank", "Yoga", 40, now - timedelta(days=4)),
            ("Gina", "Dance", 50, now - timedelta(days=5)),
            ("Henry", "Strength", 55, now - timedelta(days=3)),
            ("Alice", "Cycle Sprint", 25, now - timedelta(days=3)),
            ("Bob", "Trail Run", 60, now - timedelta(days=7)),
        ]

        for username, typ, duration, happened in sample_activities:
            Activity.objects.create(user=username, type=typ, duration=duration, date=happened)

        self.stdout.write("Creating leaderboard entries...")
        leaderboard = {
            "Team A": 240,
            "Team B": 220,
            "Team C": 210,
            "Team D": 205,
        }

        for team_name, points in leaderboard.items():
            Leaderboard.objects.create(team=team_name, points=points)

        self.stdout.write(self.style.SUCCESS("Database seed complete."))
