#########################################################
#
#  benchmark-sharedmem makefile
#
#########################################################

all: numpy-sharedmem

venv: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt
	ln -f -s venv/bin/python

numpy-sharedmem: venv
	rm -rf numpy-sharedmem
	hg clone http://bitbucket.org/cleemesser/numpy-sharedmem
	cd numpy-sharedmem && \
	../python setup.py install

clean:
	rm -rf numpy-sharedmem
	rm -rf python
	rm -rf venv

.PHONY: numpy-sharedmem
