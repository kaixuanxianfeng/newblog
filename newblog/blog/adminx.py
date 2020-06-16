from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html
import xadmin
from xadmin.layout import Row, Fieldset
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter
from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from newblog.custom_site import custom_site
from newblog.base_admin import BaseOwnerAdmin


class PostInline(admin.TabularInline):
    fields = ('title', 'desc',)
    extra = 1
    model = Post


# Register your models here.
@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name','status','is_nav','owner','created_time','post_count')
    fields = ('name', 'status', 'is_nav')
    inlines = [PostInline,]

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status','owner', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(RelatedFieldListFilter):

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __int__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_choices = Category.objects.filter(owner=request.user).value_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)

@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    '''
    @property
    def media(self):
        media = super().media()
        media.add_js([("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js",)])
        media.add_css({
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
             })
    
        return media
    '''
    '''
    class Media:
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
             }
        js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js",)
    
    class CategoryOwnerFilter(admin.SimpleListFilter):
        title = '分类过滤器'
        parameter_name = 'owner_category'

        def lookups(self, request, model_admin):
            return Category.objects.filter(owner=request.user).values_list('id', 'name')

        def queryset(self, request, queryset):
            category_id = self.value()
            if category_id:
                return queryset.filter(category_id=self.value())
            return queryset
    '''

    list_display = ('title', 'category','status',
                    'created_time','operator')
    list_display_links = []
    # filter_horizontal = ('tag',)
    filter_vertical = ('tag',)
    # list_filter = [CategoryOwnerFilter]
    list_filter = ['category']
    search_fields = ['title','category__name']
    exclude = ('owner',)
    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', 'category'),
            'status',
            'tag',
            ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        ),
    )

    '''fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title','category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'fields': ('tag',),
        })
    )'''
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            # reverse('cus_admin:blog_post_change', args =(obj.id,))
            reverse('xadmin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

'''
@xadmin.sites.register(LogEntry)
class LogEntryAdmin(BaseOwnerAdmin):
    list_display = ['object_repr','object_id','action_flag','user','change_message']
'''
