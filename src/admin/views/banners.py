from flask_admin.model.template import macro

from .base import BaseModelView


class BannersView(BaseModelView):
    column_details_list = ["name", "characters"]
    column_formatters = {"name": macro("render_banner_name")}
    column_formatters_detail = {"characters": macro("render_banner_characters")}

    list_template = "banners/list.html"
    details_template = "banners/details.html"
