from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

from operator import attrgetter

from ..logic.experiments import get_experiments

class ExperimentForm(FlaskForm):
    name = StringField("Experiment name", 
        validators=[DataRequired()], 
        description="Short name for the experiment."
    )
    
    description = TextAreaField("Description",
        description="",
    )
    
    submit = SubmitField("Create experiment")

class RunForm(FlaskForm):
    experiment_name = SelectField("Experiment name", 
        choices = map(attrgetter('name'), get_experiments() ),
    )

    description = TextAreaField("Description",
        description="Notes about this specific run"
    )

    submit = SubmitField("Run simulation")

class SettingsForm(FlaskForm):
    results_path = StringField("Results base folder",
        description="Base folder for results of simulation runs", 
    )
    
    rsopt_simulation_files_path = StringField("RSOpt files folder", 
        description="Folder containing ele, lte, and other files used to run the experiment",
    )

    submit = SubmitField("Save settings")