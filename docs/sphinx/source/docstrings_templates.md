# Docstrings templates

Built-in docstring templates
## Description Docstring

```python
DESCRIPTION_DOCSTRING = """{{description}}"""
```
## Description Epilog Docstring

```python
DESCRIPTION_EPILOG_DOCSTRING = """
    {{description}}    

    {{epilog}}
"""
```
## Sphinx Docstring

```python
SPHINX_DOCSTRING = """
{{description}}

:param {{parameter_name}}: {{parameter_description}}
:type {{parameter_name}}: {{parameter_type}}
"""
```
## Numpy Docstring

```python
NUMPY_DOCSTRING = """
    {{description}}

    Parameters
    ----------
    {{parameter_name}} : {{parameter_type}}
        {{parameter_description}}
"""
```
## Google Docstring

```python
GOOGLE_DOCSTRING = """
{{description}}

Args:
    {{parameter_name}} ({{parameter_type}}): {{parameter_description}}
"""
```
## Clig Docstring

```python
CLIG_DOCSTRING = """
{{description}}

Parameters
----------
- `{{parameter_name}}` {{parameter_type}}
    {{parameter_description}}
"""
```
## Sphinx Docstring With Epilog

```python
SPHINX_DOCSTRING_WITH_EPILOG = """
{{description}}

{{epilog}}

:param {{parameter_name}}: {{parameter_description}}
:type {{parameter_name}}: {{parameter_type}}
"""
```
## Numpy Docstring With Epilog

```python
NUMPY_DOCSTRING_WITH_EPILOG = """
    {{description}}

    {{epilog}}

    Parameters
    ----------
    {{parameter_name}} : {{parameter_type}}
        {{parameter_description}}
"""
```
## Google Docstring With Epilog

```python
GOOGLE_DOCSTRING_WITH_EPILOG = """
{{description}}

{{epilog}}

Args:
    {{parameter_name}} ({{parameter_type}}): {{parameter_description}}
"""
```
## Clig Docstring With Epilog

```python
CLIG_DOCSTRING_WITH_EPILOG = """
{{description}}

{{epilog}}

Parameters
----------
- `{{parameter_name}}` {{parameter_type}}
    {{parameter_description}}
"""
```
## Sphinx Docstring With Epilog Notypes

```python
SPHINX_DOCSTRING_WITH_EPILOG_NOTYPES = """
{{description}}

{{epilog}}

:param {{parameter_name}}: {{parameter_description}}
"""
```
## Numpy Docstring With Epilog Notypes

```python
NUMPY_DOCSTRING_WITH_EPILOG_NOTYPES = """
    {{description}}

    {{epilog}}

    Parameters
    ----------
    {{parameter_name}}
        {{parameter_description}}
"""
```
## Google Docstring With Epilog Notypes

```python
GOOGLE_DOCSTRING_WITH_EPILOG_NOTYPES = """
{{description}}

{{epilog}}

Args:
    {{parameter_name}}: {{parameter_description}}
"""
```
## Google Docstring Notypes

```python
GOOGLE_DOCSTRING_NOTYPES = """
{{description}}

Args:
    {{parameter_name}}: {{parameter_description}}
"""
```
## Clig Docstring Short

```python
CLIG_DOCSTRING_SHORT = """
{{description}}

Parameters
----------
- `{{parameter_name}}` {{parameter_type}}: {{parameter_description}}
"""
```
