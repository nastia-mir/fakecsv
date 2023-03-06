from __future__ import absolute_import, unicode_literals

from celery.utils.log import get_task_logger

from fakecsvproject.celery import app
from fakecsvapp.services import File
from fakecsvapp.models import DataSets

logger = get_task_logger(__name__)


@app.task(name='generate_cvs')
def generate_cvs(dataset_id):
    dataset = DataSets.objects.get(id=dataset_id)
    File.generate_csv(dataset)
    logger.info("CSV ready to download")
