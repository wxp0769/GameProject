"""
自定义的分页组件，以后如果想要使用这个分页组件，只需要做如下几件事：
def lianghao_list(request):
    #1.根据自己的情况云筛选自己的数据
    queryset = models.Lianghao.objects.filter(**data_dict).order_by('-level')
    #2.实例化分页对象
    page_object=Pagination(request,queryset)
    context={
        'search_data': search_data,
        'queryset':page_object.page_queryset,#分完页的数据
        'page_string':page_object.html()#生成页码
    }
    return  render(request,'lianghao_list.html',context)
在html页面中

    {% for item in queryset %}
                  <tr>
                      <td>{{ item.id }}</td>
                      <td>{{ item.mobile }}</td>
                      <td>{{ item.price }}</td>
                      <td>{{ item.level }}</td>
                      <td>{{ item.status }}</td>
                      <td>
                          <a href="/lianghao/{{ item.id }}/edit/" class="btn btn-primary btn-xs">编辑</a>
                          <a href="/lianghao/del/?uid={{ item.id }}" class="btn btn-danger btn-xs">删除</a>
                      </td>
                  </tr>
    {% endfor %}

        <ul class="pagination" style="float: left;">
            {{ page_string }}
        </ul>
"""
from django.utils.safestring import mark_safe
from django.http.request import QueryDict
import copy


class Pagination(object):
    def __init__(self, request, queryset, page_size, page_param="page", plus=5):
        """
        :param request:请求的对象
        :param queryset:符合条件的数据（根据这个数据进行分页处理）
        :param page_size:每页显示多少条数据
        :param page_param:在URL中传递的获取分页的参数，例如：/user/list/?page=12
        :param plus:显示当前页的 前或后几页（页码）
        """

        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        # print(page,type(page))
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]
        self.plus = plus
        self.page_param = page_param

        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count

    def html(self):
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if self.page + self.plus > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus
        page_list = []
        self.query_dict.setlist(self.page_param, [1])
        page_list.append('<a href="?{}"><span class="next_page">Home</span></a>'.format(self.query_dict.urlencode()))
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<a href="?{}"><span class="next_page"><</span></a>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<a href="?{}"><span class="next_page"><</span></a>'.format(self.query_dict.urlencode())
        page_list.append(prev)

        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<a href="?{}"><span class="next_page active">{}</span></a>'.format(self.query_dict.urlencode(),
                                                                                          i)
            else:
                ele = '<a href="?{}"><span class="next_page">{}</span></a>'.format(self.query_dict.urlencode(), i)
            page_list.append(ele)

        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            nextpage = '<a href="?{}"><span class="next_page">></span></a>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            nextpage = '<a href="?{}"><span class="next_page">></span></a>'.format(self.query_dict.urlencode())
        page_list.append(nextpage)
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_list.append('<a href="?{}"><span class="next_page">Last</span></a>'.format(self.query_dict.urlencode()))
        # search_string = """
        #     <li>
        #         <form method="get" style="float: left;margin-left: -1px">
        #             <div class="input-group" style="width: 200px">
        #                 <input type="text" name="page" class="form-control" style="position: relative;float: left;display: inline-block;width: 100px;border-radius: 0;" placeholder="Page Number">
        #                 <button style="border-radius: 0;" class="btn btn-default" type="submit">Go</button>
        #             </div>
        #         </form>
        #     </li>
        #               """
        # page_list.append(search_string)
        page_string = mark_safe(''.join(page_list))
        return page_string
