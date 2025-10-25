from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Run deployment tasks: migrations, collectstatic, and ensure models exist'

    def handle(self, *args, **options):
        self.stdout.write('Starting deployment tasks...')
        
        # Run migrations
        self.stdout.write('Running migrations...')
        call_command('migrate', verbosity=2)
        
        # Ensure ML models exist
        self.stdout.write('Checking ML models...')
        self.ensure_models_exist()
        
        # Collect static files
        self.stdout.write('Collecting static files...')
        call_command('collectstatic', '--noinput', verbosity=2)
        
        self.stdout.write(
            self.style.SUCCESS('Deployment tasks completed successfully!')
        )
    
    def ensure_models_exist(self):
        """Ensure ML models exist, create them if they don't"""
        from predict.ml_model import HousePricePredictor
        
        checkpoints_dir = Path(__file__).resolve().parents[3] / 'checkpoints'
        model_path = checkpoints_dir / 'model_latest.joblib'
        scaler_path = checkpoints_dir / 'scaler.joblib'
        
        if not (model_path.exists() and scaler_path.exists()):
            self.stdout.write('ML models not found. Creating models...')
            try:
                predictor = HousePricePredictor()
                predictor.train_and_save_model()
                self.stdout.write(self.style.SUCCESS('ML models created successfully!'))
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Could not create models: {e}. Using fallback.')
                )
        else:
            self.stdout.write('ML models found and ready for production!')
