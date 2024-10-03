# dir_scan_vis/views.py

import logging
import pandas as pd
from django.shortcuts import render
from django.views import View
from dir_scan.models import ProjectEntity
import plotly.io as pio
from dir_scan_vis.dash_app.plotly_helpers import create_django_project_analysis_plot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DashAppView(View):
    """
    Class-based view to render the Dash app inside an iframe.
    """

    def get(self, request):
        logger.info('Rendering directory scan visualization page')

        # Pass context to the template
        context = {}
        return render(request, 'dir_scan_vis/vis.html', context)


class GraphView(View):
    """
    View to render the full-screen Dash graph.
    """

    def get(self, request):
        logger.info('Rendering full-screen graph')

        # Load the data from ProjectEntity
        meta_df = pd.DataFrame(list(ProjectEntity.objects.all().values()))

        # Generate the plotly figure
        figure = create_django_project_analysis_plot(meta_df)

        # Convert the figure to JSON
        figure_json = pio.to_json(figure)

        # Pass the figure JSON to the template
        return render(request, 'dir_scan_vis/graph.html', {'figure_json': figure_json})
