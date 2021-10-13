
# Reproduce "azure.core.exceptions.ResourceModifiedError"

Install requirements with 

```
pip install -r requirements.txt
```

This repository reproduces the ResourceModifiedError that you get when modifying a big blob while it's streaming. To reproduce, spin up Azurite with:

```
./run.sh
```

Then, run the python script "try_to_break.py":

```
python try_to_break.py
```

This yields the `ResourceModifiedError`
