from django import forms
from inventory.models import Sales

class SalesForm(forms.ModelForm):
    """✅ Custom form to enforce numeric input & auto-calculate Cash Sales"""
    class Meta:
        model = Sales
        fields = "__all__"
        widgets = {
            "date_recorded": forms.DateInput(attrs={"type": "date"}),
            "z_reading": forms.NumberInput(attrs={"step": "0.01"}),
            "eftpos_sales": forms.NumberInput(attrs={"step": "0.01"}),
            "overing": forms.NumberInput(attrs={"step": "0.01"}),
            "down": forms.NumberInput(attrs={"step": "0.01"}),
            "memo": forms.Textarea(attrs={"rows": 2}),
        }

    def clean_numeric_field(self, field_name):
        value = self.cleaned_data.get(field_name)
        if value is None:
            return 0.00  # ✅ Default to 0 if empty
        try:
            return float(value)
        except ValueError:
            raise forms.ValidationError(f"{field_name.replace('_', ' ').title()} must be a numeric value.")

    def clean_z_reading(self):
        return self.clean_numeric_field("z_reading")

    def clean_eftpos_sales(self):
        return self.clean_numeric_field("eftpos_sales")

    def clean_overing(self):
        return self.clean_numeric_field("overing")

    def clean_down(self):
        return self.clean_numeric_field("down")

    def clean(self):
        """✅ Auto-calculate cash sales before saving"""
        cleaned_data = super().clean()
        z_reading = cleaned_data.get("z_reading", 0.00)
        eftpos_sales = cleaned_data.get("eftpos_sales", 0.00)
        overing = cleaned_data.get("overing", 0.00)
        down = cleaned_data.get("down", 0.00)

        cleaned_data["cash_sales"] = z_reading - eftpos_sales + overing - down
        return cleaned_data
