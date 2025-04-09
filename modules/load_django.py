import os
import sys
import django

# project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("D:\\PyCharm Projects\\parser-project\\wsba_parser")

os.environ['DJANGO_SETTINGS_MODULE'] = 'wsba_parser.settings'
django.setup()
