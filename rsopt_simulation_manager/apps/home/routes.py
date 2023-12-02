# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from typing import NamedTuple
from datetime import datetime

from apps.home import blueprint
from flask import render_template, request
from jinja2 import TemplateNotFound

@blueprint.route('/')
@blueprint.route('/index')
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/experiments')
def list_experiments(name=None):

    if name is None:
        """ List all experiments """

        Experiment = NamedTuple("Experiment", name=str, description=str, num_runs=int)

        experiment_table_items = [
            Experiment(
                name = "quad_scan_with_jitter",
                description = "Quadrupole scan where noise is added to position, angle, and momentum.",
                num_runs = 14,
            )
        ]

        return render_template("home/experiments.html", experiment_table_items=experiment_table_items)

    else:
        # TODO
        return render_template('home/page-404.html'), 404


@blueprint.route('/runs')
def list_runs(datetime_str = None):

    if datetime_str is None:

        Run = NamedTuple("Run", datetime=datetime, description=str, experiment=str, status=str)

        run_table_items = [
            Run(
                datetime = datetime(2023, 12, 1, 18, 33, 12),
                description = "start changed to xx",
                experiment = "quad_scan_with_jitter",
                status = "Success",
            )
        ]

        return render_template("home/runs.html", run_table_items=run_table_items)

    else:
        return render_template('home/page-404.html'), 404

# @blueprint.route('/<template>')
# def route_template(template):

#     try:

#         if not template.endswith('.html'):
#             template += '.html'

#         # Detect the current page
#         segment = get_segment(request)

#         # Serve the file (if exists) from app/templates/home/FILE.html
#         return render_template("home/" + template, segment=segment)

#     except TemplateNotFound:
#         return render_template('home/page-404.html'), 404

#     except:
#         return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
