# Docstrings templates

Built-in docstring templates to use in inferring function/argument information.
## Description

```python
DESCRIPTION_DOCSTRING = """{{description}}"""
```

## Description epilog

```python
DESCRIPTION_EPILOG_DOCSTRING = """
    {{description}}    

    {{epilog}}
"""
```

## Sphinx

```python
SPHINX_DOCSTRING = """
{{description}}

:param {{parameter_name}}: {{parameter_description}}
:type {{parameter_name}}: {{parameter_type}}
"""
```

## Numpy

```python
NUMPY_DOCSTRING = """
    {{description}}

    Parameters
    ----------
    {{parameter_name}} : {{parameter_type}}
        {{parameter_description}}
"""
```

## Google

```python
GOOGLE_DOCSTRING = """
{{description}}

Args:
    {{parameter_name}} ({{parameter_type}}): {{parameter_description}}
"""
```

## Clig

```python
CLIG_DOCSTRING = """
{{description}}

Parameters
----------
- `{{parameter_name}}` {{parameter_type}}
    {{parameter_description}}
"""
```

## Sphinx  with epilog

```python
SPHINX_DOCSTRING_WITH_EPILOG = """
{{description}}

{{epilog}}

:param {{parameter_name}}: {{parameter_description}}
:type {{parameter_name}}: {{parameter_type}}
"""
```

## Numpy  with epilog

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

## Google  with epilog

```python
GOOGLE_DOCSTRING_WITH_EPILOG = """
{{description}}

{{epilog}}

Args:
    {{parameter_name}} ({{parameter_type}}): {{parameter_description}}
"""
```

## Clig  with epilog

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

## Sphinx  with epilog notypes

```python
SPHINX_DOCSTRING_WITH_EPILOG_NOTYPES = """
{{description}}

{{epilog}}

:param {{parameter_name}}: {{parameter_description}}
"""
```

## Numpy  with epilog notypes

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

## Google  with epilog notypes

```python
GOOGLE_DOCSTRING_WITH_EPILOG_NOTYPES = """
{{description}}

{{epilog}}

Args:
    {{parameter_name}}: {{parameter_description}}
"""
```

## Google  notypes

```python
GOOGLE_DOCSTRING_NOTYPES = """
{{description}}

Args:
    {{parameter_name}}: {{parameter_description}}
"""
```

## Clig  short

```python
CLIG_DOCSTRING_SHORT = """
{{description}}

Parameters
----------
- `{{parameter_name}}` {{parameter_type}}: {{parameter_description}}
"""
```

