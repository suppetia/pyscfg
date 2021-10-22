# pyscfg - _Python Simple Configuration_

A simple solution to store/load/modify configurations for your Python project. 

version: _0.2.0_  
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

## Getting started
This library allows to work with configurations which are supposed to endure a restart of a program (nearly) as simple as working with dictionaries.
Access/update/remove configurations stored in a file using the "bracket-syntax" like using a dictionary 
and the library will handle all the I/O and keep the configs-file up to date.  
At this state of development YAML and JSON files are supported to store the configurations.  
! _All configuration keys must be strings 
and if they contain a dot (".") they are interpreted as multilevel keys._

To get started initialize a SimpleConfigs instance:
```python
from pyscfg import SimpleConfigs

# uses file 'configs.yml' (default) to store the configurations
cfg = SimpleConfigs()
# To store the configs in a specific file, pass the path to configuration file.
cfg = SimpleConfigs("data/configs.yml")
```

If `data/configs.yml` looks like
```yaml
a:
    b: value
    c: value2
d: value3
```
'value' can be accessed using any of the following ways
```python
cfg["a.b"]
cfg["a"]["b"]
cfg.get("a.b")
cfg["a"].get("b")
cfg.get("a").get("b")
cfg.get("a")["b"]
```
Calling 
```python
cfg["a.d"]
```
will raise a `KeyError` while
```python
cfg["a"].get("d")                # returns None
cfg["a"].get("d", default=None)  # returns None
cfg["a"].get("d", default="foo") # returns "foo"
```
returns the default value if the key is not stored in the configs.

To extract a group of configs (a layer in the configs file) as a dictionary use
```python
cfg["a"].as_dict()  # or
dict(cfg["a"])
```

In the same way updating or adding new configuration keys works:
```python
cfg["a.b"] = "new_value"
cfg["a"]["b"] = "new_value"
...
cfg["e"] = "another new value"
...

# to add a group of parameters use a dict:
cfg["f"] = {"g": 1, "h": 1e10}
```

After these changes the `data/configs.yml` file will look like this:
```yaml
a:
    b: new value
    c: value2
d: value3
e: another new value
```

To remove a key use one of the following ways:
```python
cfg.remove("e")
del cfg["e"]

# to retrieve the item to be removed or to safely remove a key use dict-like pop-method
cfg.pop("e")                             # returns "another new value"
cfg.pop("non existing key")              # returns None
cfg.pop("non existing key", default=42)  # returns 42
```

Default values stored in a dictionary can be passed to the constructor. These values will be assigned if the keys aren't in the configurations already.
The configurations file is updated.  
This might be useful to create a configurations file for an app for the first time and these configs might be changed by the user later.

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

if user_chooses_this_option:
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

