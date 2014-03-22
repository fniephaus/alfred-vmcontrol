all:
	cd src ; \
	zip ../VMControl-for-Alfred.alfredworkflow . -r --exclude=*.DS_Store*

clean:
	rm -f *.alfredworkflow