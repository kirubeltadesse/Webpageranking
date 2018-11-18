# Webpageranking
This repository include visualization and analysis for ranking website.

## Visualization
The visualization is done using Bokeh in the ```bokeh_app``` folder. The folder contents to subfolders and `main.py` file which pass the ```data``` from the data folder to respective tabs by calling different script from the ```scripts``` and present on the dashboard for visualization. Click on the YouTube video below to watch a quick demonestration:  
[![Dashboard using Bokeh](https://img.youtube.com/vi/qSHbC7QEQdI/0.jpg)](https://www.youtube.com/watch?time_continue=1&v=qSHbC7QEQdI)

## Required package
The packages required to run the django server are:
#### Visualization packages
All the package used in this project are specified in the `spec-file.txt`. If you are using `conda` on windows machine you can directory
```
$ conda create --name <env> --file spec-file.txt
```
expect `Naked` use
```
$ pip install Naked
```
those should create an environment with the necessary dependencies to run the application.

<!-- to table creating  -->
<!-- python manage.py migrate --run-syncdb -->

<!-- the normalized data is missing web name column -->

<!-- ### Comments on Beta release
- Allow the sure to have a side by side view. (https://hub.mybinder.org/user/bokeh-bokeh-notebooks-1zde6jyk/notebooks/tutorial/11%20-%20Running%20Bokeh%20Applictions.ipynb#Directory-Format-Apps-and-Templates)
(https://github.com/bokeh/bokeh/blob/master/examples/app/dash/main.py)
- Give meaningful naming conventions
- Keep consistence across different views  
- While selecting and de-selecting the parameters the x-axis must adjust
- Table view (should be called Detail) has to include all the parameters and their actual values

https://groups.google.com/a/continuum.io/d/msg/bokeh/7T61s6gQyW4/SzHXHSKmAQAJ
 -->
