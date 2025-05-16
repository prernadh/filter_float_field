# Float filtering plugin
FiftyOne Plugin to filter dynamic float fields

![](https://github.com/prernadh/filter_float_field/blob/main/filter_by_float.gif)

## Installation

```shell
fiftyone plugins download https://github.com/prernadh/filter_float_field
```

Refer to the [main README](https://github.com/voxel51/fiftyone-plugins) for
more information about managing downloaded plugins and developing plugins
locally.

## Run Example

After installing this plugin, you can try the example yourself on the `quickstart` dataset.
```python
import fiftyone as fo
import fiftyone.zoo as foz

dataset = foz.load_zoo_dataset("quickstart")
session = fo.launch_app(dataset)
```

Click on the `Filter by float field` button in the sample grid -> select the dynamic field you want to filter by and enter the max float value -> click execute and the view will automatically get set in the grid.
