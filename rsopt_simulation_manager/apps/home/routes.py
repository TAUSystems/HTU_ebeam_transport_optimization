# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from typing import NamedTuple
from datetime import datetime

from apps.home import blueprint
from flask import render_template, request, redirect

from ..logic.experiments import create_new_experiment, get_experiments
from ..logic.runs import run_simulation, get_runs
from .forms import ExperimentForm, SettingsForm, RunForm
from ..logic.settings import save_config, load_config

@blueprint.route('/index')
def index():

    return render_template('home/index.html', segment='index')

@blueprint.route('/')
@blueprint.route('/experiments')
def list_experiments(name=None):

    if name is None:
        """ List all experiments """

        return render_template("home/experiments.html", experiment_table_items=get_experiments())

    else:
        # TODO
        return render_template('home/page-404.html'), 404

@blueprint.route('/experiments/new', methods=['GET', 'POST'])
def new_experiment():
    
    form = ExperimentForm()
    
    if form.validate_on_submit():
        create_new_experiment(request.form)
        return redirect('/experiments')

    else:
        return render_template('home/new.html', new_item_class="experiment", form=form)


@blueprint.route('/runs')
def list_runs(datetime_str = None):
    return render_template("home/runs.html", run_table_items=get_runs(datetime_str))

@blueprint.route('/runs/new', methods=['GET', 'POST'])
def new_run():
    
    form = RunForm()
    form.experiment_name.choices = [experiment.name for experiment in get_experiments()]

    if form.validate_on_submit():
        run_simulation(request.form)
        return redirect('/runs')

    else:
        return render_template('home/new.html', new_item_class="run", form=form)


@blueprint.route('/settings', methods=['GET', 'POST'])
def settings():
    
    form = SettingsForm()

    if form.validate_on_submit():
        save_config(form.data)
        return redirect("/")

    else:
        config = load_config()
        form.results_path.data = config['Directories']['results_path']
        form.rsopt_simulation_files_path.data = config['Directories']['rsopt_simulation_files_path']

        return render_template("home/settings.html", form=form)


@blueprint.app_errorhandler(404) 
def not_found(e): 
  # defining function 
  return render_template("home/page-404.html"), 404

@blueprint.app_errorhandler(500) 
def unspecified_error(e): 
  # defining function 
  return render_template("home/page-500.html"), 500
