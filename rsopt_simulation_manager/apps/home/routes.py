# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from typing import NamedTuple
from datetime import datetime

from apps.home import blueprint
from flask import render_template, request, redirect

from ..logic.experiments import create_new_experiment
from ..logic.runs import run_simulation, get_runs

@blueprint.route('/index')
def index():

    return render_template('home/index.html', segment='index')

@blueprint.route('/')
@blueprint.route('/experiments')
def list_experiments(name=None):

    if name is None:
        """ List all experiments """

        return render_template("home/experiments.html", experiment_table_items=experiment_table_items)

    else:
        # TODO
        return render_template('home/page-404.html'), 404

@blueprint.route('/experiments/new', methods=['GET', 'POST'])
def new_experiment():
    if request.method == 'POST':
        create_new_experiment(request.form)
        return redirect('/experiments')

    else:
        return render_template('home/new_experiment.html')



@blueprint.route('/runs')
def list_runs(datetime_str = None):
    return render_template("home/runs.html", run_table_items=get_runs(datetime_str))


@blueprint.app_errorhandler(404) 
def not_found(e): 
  # defining function 
  return render_template("home/page-404.html"), 404

@blueprint.app_errorhandler(500) 
def unspecified_error(e): 
  # defining function 
  return render_template("home/page-500.html"), 500
