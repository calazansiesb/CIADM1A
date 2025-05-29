NotImplementedError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/home/adminuser/venv/lib/python3.12/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 600, in _run_script
    exec(code, module.__dict__)
File "/mount/src/ciadm1a/pages/teste-diego.py", line 257, in <module>
    melhores_correlacoes_com_desc = melhores_correlacoes_geral.rename(
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/pandas/core/series.py", line 4918, in rename
    return super()._rename(
           ^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/pandas/core/generic.py", line 1086, in _rename
    new_index = ax._transform_index(f, level=level)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/pandas/core/indexes/base.py", line 6463, in _transform_index
    return type(self).from_arrays(values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/pandas/core/indexes/multi.py", line 531, in from_arrays
    codes, levels = factorize_from_iterables(arrays)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/pandas/core/arrays/categorical.py", line 3023, in factorize_from_iterables
    codes, categories = zip(*(factorize_from_iterable(it) for it in iterables))
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/pandas/core/arrays/categorical.py", line 3023, in <genexpr>
    codes, categories = zip(*(factorize_from_iterable(it) for it in iterables))
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/pandas/core/arrays/categorical.py", line 2996, in factorize_from_iterable
    cat = Categorical(values, ordered=False)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/pandas/core/arrays/categorical.py", line 462, in __init__
    dtype = CategoricalDtype(categories, dtype.ordered)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/pandas/core/dtypes/dtypes.py", line 211, in __init__
    self._finalize(categories, ordered, fastpath=False)
File "/home/adminuser/venv/lib/python3.12/site-packages/pandas/core/dtypes/dtypes.py", line 368, in _finalize
    categories = self.validate_categories(categories, fastpath=fastpath)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/pandas/core/dtypes/dtypes.py", line 566, in validate_categories
    if categories.hasnans:
       ^^^^^^^^^^^^^^^^^^
File "properties.pyx", line 36, in pandas._libs.properties.CachedProperty.__get__
File "/home/adminuser/venv/lib/python3.12/site-packages/pandas/core/indexes/base.py", line 2820, in hasnans
    return bool(self._isnan.any())
                ^^^^^^^^^^^
File "properties.pyx", line 36, in pandas._libs.properties.CachedProperty.__get__
File "/home/adminuser/venv/lib/python3.12/site-packages/pandas/core/indexes/base.py", line 2790, in _isnan
    return isna(self)
           ^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/pandas/core/dtypes/missing.py", line 178, in isna
    return _isna(obj)
           ^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/pandas/core/dtypes/missing.py", line 203, in _isna
    raise NotImplementedError("isna is not defined for MultiIndex")
