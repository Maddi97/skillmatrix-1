"""Contains model for a Milestone"""
import json
from src.model.model import Model


class MilestoneModel(Model):

    """Converts given milestone to JSON to hand over to the frontend. Can't be used to identify user and skill"""

    def __init__(self, date, comment):
        self.date = date
        self.comment = comment

    def to_json(self):
        iso_date = self.date.isoformat()
        return json.dumps(dict(date=iso_date, comment=self.comment))
