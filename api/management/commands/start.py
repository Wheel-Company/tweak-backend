from django.core.management.base import BaseCommand, CommandError
import os
import subprocess

class Command(BaseCommand):

  def add_arguments(self, parser):
      pass

  def handle(self, *args, **options):
      subprocess.Popen(['python', 'manage.py', 'runserver', '0.0.0.0:80'])
