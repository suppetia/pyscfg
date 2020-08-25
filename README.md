# pyscfg - _Python Simple Configuration_

A simple solution to store/load/modify user configurations for your Python project. 

version: _0.1.0_  
contributors: _suppetia_

## Setup

installing via pip
```bash
pip install pyscfg
```

installing from source
```bash
git clone https://github.com/suppetia/pyscfg.git
cd pyscfg
python setup.py install
```

## Simple Usage
```python
from pyscfg import SimpleConfigs

# uses file 'configs.yml' (default) to store the user configurations
cfg = SimpleConfigs()

# set configurations depending on user preferences
if user_chooses_this:
    cfg["num"] = 1
else:
    cfg["num"] = -1
```

Specify a path to configuration file.
```python
# uses file 'configs.yml' in subdirectory 'data' to store the user configurations
cfg = SimpleConfigs("data/configs.yml")
```


Use default values for your configurations stored in a dictionary. These values will be assigned if the keys aren't in the configurations already.
The configurations file is updated.

```python
from pyscfg import SimpleConfigs


defaults = {
    "foo": "John",
    "bar": "Doe",
    "num": 0
}

# uses file 'configs.yml' (default) to store the user configurations
cfg = SimpleConfigs(defaults=defaults)

print(cfg["num"]) # prints 0

if user_chooses_this:
    cfg["num"] = 1
else:
    cfg["num"] = -1

print(cfg["num"]) # prints 1 or -1
```

You can also write your defaults into a configuration file (supported: _YAML_, _JSON_) and pass it to the constructor.
```python
# uses file 'default_cfg.yml' in subdirectory 'data' to load the default configuration values
cfg = SimpleConfigs(defaults="data/default_cfg.yml")

```

