from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'New BLOG'
    site_title = 'New Blog 后台管理系统'
    index_title = '首页'

custom_site = CustomSite(name='cus_admin')