all:
	cd src ; \
	zip ../VM-Control-for-Alfred.alfredworkflow . -r --exclude=*.DS_Store*

clean:
	rm -f *.alfredworkflow