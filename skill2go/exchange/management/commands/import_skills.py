import csv
import os
from django.core.management.base import BaseCommand
from exchange.models import Skill, SkillCategory, SkillProvider
from django.db import transaction

# Get the root directory of the project by using the settings module path
project_root = '/Users/carlos/Documents/shipd_challenges/CHALLENGE_PROPOSAL/Skill2Go/skill2go'
# Construct the path to the CSV file (relative to project root)
file_path = os.path.join(project_root, 'exchange', 'data', 'skills.csv')

class Command(BaseCommand):
    help = 'Imports skills data from a CSV file'

    def handle(self, *args, **options):
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)

                # Start a transaction for atomicity
                with transaction.atomic():
                    for row in reader:
                        skill_title = row['skill_title'].strip()
                        skill_category_name = row['skill_category'].strip()

                        # Skip if the skill title is empty or malformed
                        if skill_title:
                            # Ensure the category exists, or create a new one
                            category, created = SkillCategory.objects.get_or_create(name=skill_category_name)

                            # Assign the first provider (modify if needed)
                            provider = SkillProvider.objects.first()  # Default provider

                            # Handle images later, using a default image for now
                            image = "default_image.jpg"  # Placeholder image path

                            # Create the skill instance
                            Skill.objects.create(
                                title=skill_title,
                                description="Description here",  # Placeholder description
                                category=category,
                                provider=provider,
                                image=image
                            )

            self.stdout.write(self.style.SUCCESS('Successfully imported skills'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing skills: {e}'))
