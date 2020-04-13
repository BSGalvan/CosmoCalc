# CosmoCalc
A project page for the Cosmological Calculator (à la Ned Wright), written using NumPy, SciPy, pandas, Flask and a little bit of HTML and CSS. The rendered, working website is [here](http://bsgalvan98.pythonanywhere.com/)

---

# Dependencies
Note : Skip this section if you have the [Anaconda](https://www.anaconda.com/distribution/) distribution installed on your system. That will already have the dependencies listed below.

1. Flask, which requires:
	* Werkzeug
	* Jinja2 - which requires MarkupSafe
	* click
	* itsdangerous
2. NumPy
3. Scipy
4. pandas, which requires:
	* python-dateutil - which requires six
	* pytz

To install the above dependencies:

1. Make sure you have a working Python installation on your machine. To do this, type `python --version` in a terminal. If this step produces no output, you may need to [install python](https://www.python.org/downloads/) on your machine. 
2. Once you have Python installed, get `pip`, the python package manager, and install it. Here are [some instructions.](https://pip.pypa.io/en/stable/installing/). Once `pip` is set up, simply execute `pip install <package-name>` to install the required dependencies.

---

# Running this Website on your Local Machine

- Using `git`- from within a terminal:
	```shell
	git clone https://github.com/BSGalvan/CosmoCalc.git
	cd /path-to/CosmoCalc/
	python flask_app.py
	```
- Not using `git` - simply click on the "Clone or Download" button and then click on "Download ZIP" (if you're on the GitHub repository page), or the "Download .zip/.tar.gz" button (if you're on the GitHub Pages site). Extract the directory where you want it, and from within execute the command `python myFirstWebsite.py` from a terminal.

Once you have done the above, go to the address `127.0.0.1:5000/` or `localhost:5000/` and voila!
 
