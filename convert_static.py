import re


def convert_static_links(html_file_path, output_file_path):
    with open(html_file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # تبدیل لینک‌های خام
    def replace_href(match):
        path = match.group(1)
        return f"href=\"{{% static '{path}' %}}\""

    def replace_src(match):
        path = match.group(1)
        return f"src=\"{{% static '{path}' %}}\""

    content = re.sub(r'href="([^"]+\.(css|js|html))"', replace_href, content)
    content = re.sub(
        r'src="([^"]+\.(js|css|png|jpg|jpeg|gif|svg|webp))"', replace_src, content
    )

    # تبدیل لینک‌های ناقص {% static ... %} که کوتیشن ندارند
    def fix_static_quotes(match):
        attr = match.group(1)
        path = match.group(2)
        return f"{attr}\"{{% static '{path}' %}}\""

    content = re.sub(
        r'(href=|src=)"\{\% static ([^\'"][^ \}]+) \%\}"', fix_static_quotes, content
    )

    # اضافه کردن load static اگر نبود
    if "{% load static %}" not in content:
        content = "{% load static %}\n" + content

    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print("link has be changed ✅ ")


# استفاده
convert_static_links("templates/", "templates/")


# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−− New Version −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−


# import re, os

# def convert_all_templates(folder):
#     for root, _, files in os.walk(folder):
#         for f in files:
#             if f.endswith(".html"):
#                 path = os.path.join(root, f)
#                 with open(path, "r", encoding="utf-8") as file:
#                     content = file.read()

#                 # تغییر href و src
#                 content = re.sub(r'href="([^"]+\.(css|js|html))"',
#                                  lambda m: f'href="{{% static \'{m.group(1)}\' %}}"', content)
#                 content = re.sub(r'src="([^"]+\.(js|css|png|jpg|jpeg|gif|svg|webp))"',
#                                  lambda m: f'src="{{% static \'{m.group(1)}\' %}}"', content)

#                 # اضافه کردن load static
#                 if "{% load static %}" not in content:
#                     content = "{% load static %}\n" + content

#                 with open(path, "w", encoding="utf-8") as file:
#                     file.write(content)
#                 print(f"✅ fixed: {path}")

# # استفاده
# convert_all_templates("templates")
