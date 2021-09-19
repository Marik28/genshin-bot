from .base import BaseModelView


class BannersView(BaseModelView):
    column_details_list = ["name", "characters"]
