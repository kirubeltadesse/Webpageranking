# Webpageranking
This repository include visualization and analysis for ranking website. The visualization tools are aimed to give a ranking based on the user interaction with a given the website.

## Visualization
The visualization is done using Bokeh in the ```bokeh_app``` folder. The folder contents to subfolders and `main.py` file which pass the ```data``` from the data folder to respective tabs by calling different script from the ```scripts``` and present on the dashboard for visualization. Click on the YouTube video below to watch a quick demonestration:  
[![Dashboard using Bokeh](https://img.youtube.com/vi/8QJlC4n9W-Y/0.jpg)](https://www.youtube.com/watch?v=yxDvyyUQoUI&t=100s)

## parameters
Below are the list of parameters chosen to rank the website.

- **Load Time:** The time between the initial request and the browser load event
- **First Byte:** The time it takes for the server to respond with the first byte of the response (in other words, the time it takes for the back-end to load)
- **Start Render:** The time until the browser starts painting content to the screen
- **Speed Index:** A custom metric introduced by WebPageTest to rate pages based on how quickly pages are visually populated (see [here](https://sites.google.com/a/webpagetest.org/docs/using-webpagetest/metrics/speed-index) for full details on the metric)
- **DOM Elements:** Number of DOM elements in the page
- **Document Complete:** Set of metrics relative to the time until the browser load event, with Time, Requests and Bytes In representing the load time, number of requests and number of bytes received, respectively
- **Fully Loaded:** Similar to Document Complete, but the metrics are relative to the time at which WebPageTest determines that the page has fully finished loading content. This is relevant and different from the above, because pages may decide to load additional content after the browser load event

## Required packages

The packages required to run the django server and every application on this project are specified in the `windows-specfile.txt` or `linux-specfile.txt`. If you have conda installed in you machine either windows or linux, after cloning the repo you can run conda with the respective specfile. like this for windows:

```
$ conda create --name <env> --file windows-specfile.txt
```
expect `Naked` use
```
$ pip install Naked
```
those should create an environment with the necessary dependencies to run the application. Then, activate your conda env by
```
activate <env>
```
And cd to `webranking` and there should be a `manage.py` file
```
python manage.py makemigrations
```
and
```
python manage.py migrate
```
and finally just to make sure
```
python manage.py migrate --run-syncdb
```
Now, you can lauch you localhost by running
```
python manage.py runserver
```

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
