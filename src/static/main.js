function toggleMenu() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('active');
  }

// Adjust the size of bokeh plots on window resize
window.addEventListener('resize', function() {
  var bokehPlots = document.querySelectorAll('.widget-content .bokeh-plot iframe');
  bokehPlots.forEach(function(plot) {
    scaleBokehPlot(plot);
  });
});

// Adjust the size of bokeh plots on page load
window.addEventListener('load', function() {
  var bokehPlots = document.querySelectorAll('.widget-content .bokeh-plot iframe');
  bokehPlots.forEach(function(plot) {
    scaleBokehPlot(plot);
  });
});

// Scale the bokeh plot to fit the container
function scaleBokehPlot(plot) {
  var container = plot.parentNode;
  var containerWidth = container.offsetWidth;
  var containerHeight = container.offsetHeight;

  var plotWidth = plot.offsetWidth;
  var plotHeight = plot.offsetHeight;

  var widthRatio = containerWidth / plotWidth;
  var heightRatio = containerHeight / plotHeight;

  var scale = Math.min(widthRatio, heightRatio);

  plot.style.transform = 'scale(' + scale + ')';
}

// Get a reference to the Bokeh plot div
const bokehPlotDiv = document.getElementById('bokeh-plot');

// Create a ResizeObserver instance to track changes in the parent container width
const resizeObserver = new ResizeObserver(entries => {
  for (let entry of entries) {
    // Get the new width of the parent container
    const width = entry.contentRect.width;

    // Calculate the height based on the width
    const height = width / 2;

    // Set the height of the Bokeh plot div
    bokehPlotDiv.style.height = `${height}px`;
  }
});

// Observe the parent container for width changes
resizeObserver.observe(bokehPlotDiv.parentElement);