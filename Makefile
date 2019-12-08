
all:
	python build.py build_ext --inplace

clean:
	@rm -rf build
	@echo Removed Build Folder

	@echo Removing cython generated files ...
	@find source/assimp -name "*.c" -print -delete
	@find source/assimp -name "*.so" -print -delete
	@find source/assimp -name "*.cpp" -print -delete

	@echo Removing python cache files ...
	@find source -name "*.pyc" -print -delete
	@find source -name "*__pycache__" -print -delete


