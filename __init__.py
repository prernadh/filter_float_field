import fiftyone.operators as foo
import fiftyone.operators.types as types
import fiftyone.core.labels as fol
import fiftyone as fo

from fiftyone import ViewField as F

class FilterDynamicFloatField(foo.Operator):
    @property
    def config(self):
        return foo.OperatorConfig(
            name="filter_float_field",
            label="Filter float field",
            dynamic=False,
        )

    def resolve_placement(self, ctx):
        return types.Placement(
            types.Places.SAMPLES_GRID_ACTIONS,
            types.Button(
                label="Filter by float field",
                prompt=True,
            ),
        )

    def resolve_input(self, ctx):
        inputs = types.Object()
        schema = ctx.dataset.get_field_schema(flat=True)
        if ctx.dataset._has_frame_fields():
            frame_schema = ctx.dataset.get_frame_field_schema(flat=True)
            schema.update(
                {
                    ctx.dataset._FRAMES_PREFIX + path: field
                    for path, field in frame_schema.items()
                }
            )
        # categorical_field_types = (
        #     fo.StringField,
        #     fo.BooleanField,
        #     fo.ObjectIdField,
        # )
        # numeric_field_types = (
        #     fo.FloatField,
        #     fo.IntField,
        #     fo.DateField,
        #     fo.DateTimeField,
        # )
        # valid_field_types = categorical_field_types + numeric_field_types
        valid_field_types = (fo.FloatField)

        path_keys = [
            p
            for p, f in schema.items()
            if (
                isinstance(f, valid_field_types)
                or (
                    isinstance(f, fo.ListField)
                    and isinstance(f.field, valid_field_types)
                )
            )
        ]

        field_names = _get_label_fields(ctx.view, fo.Label)

        path_selector = types.AutocompleteView()
        for key in path_keys:
            for label_field in field_names:
                if key.startswith(label_field):
                    path_selector.add_choice(key, label=key)
                    break
        

        inputs.enum(
            "field_path",
            path_selector.values(),
            label="Select field",
            description="Select a dynamic field to filter on",
            view=path_selector,
            required=True,
        )

        inputs.float(
            "float_value",
            label="Max value",
            description="Enter the max float value to filter by",
            required=True,
        )
        return types.Property(inputs, view=types.View(label="Filter by float field"))


    def execute(self, ctx):
        float_value = ctx.params.get("float_value", None)
        field_path = ctx.params.get("field_path", None)
        label_name = field_path.split(".")[0]
        float_field = field_path.split(".")[-1]
        view = ctx.dataset.filter_labels(label_name, F(float_field) < float_value)
        ctx.ops.set_view(view)


def _get_label_fields(sample_collection, label_types, frames=False):
    if frames:
        schema = sample_collection.get_frame_field_schema(flat=True)
    else:
        schema = sample_collection.get_field_schema(flat=True)

    bad_roots = tuple(
        k + "." for k, v in schema.items() if isinstance(v, fo.ListField)
    )

    label_fields = [
        path
        for path, field in schema.items()
        if (
            isinstance(field, fo.EmbeddedDocumentField)
            and issubclass(field.document_type, label_types)
            and not path.startswith(bad_roots)
        )
    ]

    if frames:
        label_fields = [
            sample_collection._FRAMES_PREFIX + lf for lf in label_fields
        ]

    return label_fields

def register(p):
    p.register(FilterDynamicFloatField)
