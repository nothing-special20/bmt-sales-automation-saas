from pathlib import Path
import re
import shutil
import os

def extract_static_path(x):
    if ('% static' in x):
        output = re.findall("'.{1,255}?'", x)[0]
        output = re.sub("'", "", output)
        return output
    else:
        return x

# copy all of the file dependencies for a file from one folder to another
def copy_dependencies(file, src_folder, dest_folder):
    data = open(file, 'r').read()
    file_paths = re.findall('".{1,255}?"', data)
    file_paths = [re.sub('"', '', x) for x in file_paths]
    keep_file_exts = ['.css', '.js', '.svg', '.png']
    keep_file_exts = ['\\' + x for x in keep_file_exts]
    keep_file_exts = '|'.join(keep_file_exts)
    # print(extract_static_path("% static 'js/sb-admin-2.min.js' %}"))
    
    file_exts = []
    for x in file_paths:
        try:
            file_exts.append(re.search('\\..{1,5}',x).group(0))
        except:
            pass

    file_exts = list(set(file_exts))

    file_paths = [x for x in file_paths if bool(re.findall(keep_file_exts, x))]
    file_paths = [x for x in file_paths if x[0]!='.']
    file_paths = [extract_static_path(x) for x in file_paths]
    file_paths = [x for x in file_paths if 'custom' not in x]

    file_paths = [re.sub('vendor/bulkit', '', x) for x in file_paths]

    # for x in file_paths:
    #     print(x)

    for x in file_paths:
        src = src_folder + x
        dst = dest_folder + x
        dst_subfolder = os.path.dirname(dst)
        Path(dst_subfolder).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        # try:
        #     shutil.copyfile(src, dst)
        # except:
        #     print('Err! File not found!\t' + src)

# swaps out things like href="lol.png" for href="{ % static 'lol.png' %}"
def django_static_file_ref_update(file):
    data = open(file, 'r').read()
    file_paths = re.findall('".{1,255}?"', data)
    file_paths = [re.sub('"', '', x) for x in file_paths]
    keep_file_exts = ['.css', '.js', '.svg', '.png']
    keep_file_exts = ['\\' + x for x in keep_file_exts]
    keep_file_exts = '|'.join(keep_file_exts)

    file_exts = []
    for x in file_paths:
        try:
            file_exts.append(re.search('\\..{1,5}',x).group(0))
        except:
            pass

    file_exts = list(set(file_exts))

    file_paths = [x for x in file_paths if bool(re.findall(keep_file_exts, x))]
    file_paths = [x for x in file_paths if x[0]!='.']
    file_paths = list(set(file_paths))

    for x in file_paths:
        print('~~~~~~')
        print(x)
        new_path = "{% static '" + x + "' %}"
        data = re.sub(x, new_path, data)
        print(new_path)
    
    new_file = file.split('.')
    new_file = new_file[0] + '_2.' + new_file[1]

    f = open(new_file, "w")
    f.write(data)
    f.close()

    "vendor/jquery/jquery.min.js"
    "{% static 'vendor/jquery/jquery.min.js' %}"


if __name__ == '__main__':
    # file = '/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/bmt-sales-automation-saas/templates/web/components/bulkit_body_old.html'
    file = '/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/bmt-sales-automation-saas/templates/vendor/bootstrap/surveys_body.html'
    src_folder = '/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/tools/themeforest-Y3pCVj8L-bulkit-agency-startup-and-saas-template/precompiled/assets/'
    dest_folder = '/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/bmt-sales-automation-saas/static/vendor/bulkit/'
    copy_dependencies(file, src_folder, dest_folder)
    # django_static_file_ref_update(file)