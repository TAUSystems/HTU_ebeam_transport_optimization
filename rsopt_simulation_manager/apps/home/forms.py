from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Regexp

class ExperimentForm(FlaskForm):
    name = StringField("Experiment name", 
        validators=[InputRequired(), Regexp(r'^[^\\/?%*:|"<>\.\s]+$')], 
        description="Short name for the experiment. May not contain /\?%*:|\"<>. or spaces.",
    )
    
    description = TextAreaField("Description",
        description="",
    )
    
    submit = SubmitField("Create experiment")

class RunForm(FlaskForm):
    experiment_name = SelectField("Experiment name")  # choices added after instantiation in new_run()

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